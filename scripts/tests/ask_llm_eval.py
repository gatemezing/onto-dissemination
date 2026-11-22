#!/usr/bin/env python3
"""Evaluate how the Ask the ERA Graph page (scripts/assets/era-ask.html) reads questions:
the in-browser language model against keyword matching, on the labelled questions in
scripts/tests/ask-questions.json.

The page itself does the reading: it is served locally and driven in Chromium with
WebGPU, so the model, the prompt, the JSON schema and the checks are exactly those a
visitor gets. For legislation questions the resulting topic is also counted in era-lex,
because a topic that is not in English finds nothing in the acts' English titles.

Needs Playwright (pip install playwright && playwright install chromium) and a GPU that
Chromium exposes through WebGPU (any recent Mac; elsewhere add the flags your platform
needs). Models are downloaded once into the browser profile in ERA_ASK_EVAL_PROFILE
(default ~/.cache/era-ask-eval).

Usage: python3 scripts/tests/ask_llm_eval.py [model-key ...] [--failures]
       model keys as in LLM_MODELS in era-ask.html; default qwen2.5-1.5b
"""
import functools, http.server, json, os, pathlib, socketserver, sys, threading, time
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUESTIONS = json.loads((ROOT / "tests" / "ask-questions.json").read_text())
PROFILE = os.environ.get("ERA_ASK_EVAL_PROFILE", str(pathlib.Path.home() / ".cache" / "era-ask-eval"))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
MODELS = args or ["qwen2.5-1.5b"]
SHOW_FAILURES = "--failures" in sys.argv

# In the page: one question, read both ways, and summarised for scoring.
READ_JS = """async ({q, useLlm}) => {
  const A = window.eraAsk;
  const sum = p => !p || p.unsupported ? {entity:'none'} : {entity:p.entity.id, intent:p.intent, cc:p.cc,
    topic:p.topic || null, orgCode:p.orgCode || null, orgName:p.orgName || null, missing:!!(p.noTopic || p.noCode)};
  const out = {kw: sum(A.parseQuestion(q))};
  if(useLlm){
    const r = await A.llmRead(q);
    out.llm = sum(A.intentToParsed(r.form, q)); out.form = r.form; out.seconds = r.seconds; out.usage = r.usage;
  }
  return out;
}"""
LEX_COUNT_JS = """async (topic) => {
  const b = window.eraAsk.buildQuery({id:'legal', kind:'lex'}, null, topic);
  const res = await fetch('https://graph.data.era.europa.eu/repositories/era-lex', {method:'POST',
    headers:{'Content-Type':'application/sparql-query', 'Accept':'application/sparql-results+json'}, body:b.countQuery});
  return +(await res.json()).results.bindings[0].n.value;
}"""


def correct(exp, got):
    """Every field the label gives must match; nothing else is checked. A label may list
    alternative readings ("alt") for a question that honestly asks two things."""
    if any(correct(dict(a, q=exp["q"]), got) for a in exp.get("alt", [])):
        return True
    if got["entity"] != exp["entity"]:
        return False
    if exp["entity"] == "none":
        return True
    if got.get("missing"):
        return False
    if "cc" in exp and got.get("cc") != exp["cc"]:
        return False
    if exp.get("intent") and got.get("intent") != exp["intent"]:
        return False
    if exp.get("topic") and not any(t in (got.get("topic") or "") for t in exp["topic"]):
        return False
    if exp.get("orgCode") and got.get("orgCode") != exp["orgCode"]:
        return False
    if exp.get("orgName") and exp["orgName"] not in (got.get("orgName") or "").lower():
        return False
    return True


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT / "assets")))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}/era-ask.html"
    report = {}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE, channel="chromium", headless=True,
                                                   args=["--enable-unsafe-webgpu"])
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        for key in MODELS:
            page.goto(f"{base}?model={key}")
            page.wait_for_function("window.eraAsk && true")
            t0 = time.time()
            page.evaluate("async (k) => { await window.eraAsk.llmStartup; if(window.eraAsk.llm.state !== 'ready') await window.eraAsk.loadLlm(k, false); }", key)
            state = page.evaluate("window.eraAsk.llm.state")
            if state != "ready":
                print(f"{key}: model not ready ({state}): {page.inner_text('#llmNote')[:300]}")
                continue
            load_s = time.time() - t0
            rows, secs, usage = [], [], []
            for item in QUESTIONS:
                r = page.evaluate(READ_JS, {"q": item["q"], "useLlm": True})
                rows.append((item, r)); secs.append(r["seconds"]); usage.append(r.get("usage") or {})
            ok_llm = [correct(i, r["llm"]) for i, r in rows]
            ok_kw = [correct(i, r["kw"]) for i, r in rows]
            # legislation: does the topic the reading produced find any act in era-lex?
            lex = {"llm": 0, "kw": 0, "n": 0}
            for i, r in rows:
                if i["entity"] != "legal":
                    continue
                lex["n"] += 1
                for side in ("llm", "kw"):
                    t = r[side].get("topic") if r[side]["entity"] == "legal" else None
                    if t and page.evaluate(LEX_COUNT_JS, t) > 0:
                        lex[side] += 1
            refuse = [i for i in QUESTIONS if i["entity"] == "none"]
            report[key] = {
                "model_id": page.evaluate("window.eraAsk.llm.id"), "load_seconds": round(load_s, 1),
                "questions": len(rows), "llm_correct": sum(ok_llm), "keyword_correct": sum(ok_kw),
                "llm_refusals_right": sum(ok for (i, _), ok in zip(rows, ok_llm) if i["entity"] == "none"),
                "keyword_refusals_right": sum(ok for (i, _), ok in zip(rows, ok_kw) if i["entity"] == "none"),
                "refusal_questions": len(refuse),
                "legislation_topics_with_hits": {"llm": lex["llm"], "keywords": lex["kw"], "of": lex["n"]},
                "seconds_per_question": {"median": sorted(secs)[len(secs) // 2], "max": max(secs)},
                "tokens": {k: sorted(u.get(k) or 0 for u in usage)[len(usage) // 2] for k in ("prompt_tokens", "completion_tokens")},
                "tokens_per_second": {k: round(sorted((u.get("extra") or {}).get(k) or 0 for u in usage)[len(usage) // 2], 1)
                                      for k in ("prefill_tokens_per_s", "decode_tokens_per_s")},
                "failures": [{"q": i["q"], "expected": {k: v for k, v in i.items() if k != "q"}, "model": r["llm"], "form": r["form"]}
                             for (i, r), ok in zip(rows, ok_llm) if not ok],
                "keyword_failures": [{"q": i["q"], "keywords": r["kw"]} for (i, r), ok in zip(rows, ok_kw) if not ok],
            }
            m = report[key]
            print(f"{key} ({m['model_id']}): model {m['llm_correct']}/{m['questions']}, keywords {m['keyword_correct']}/{m['questions']}; "
                  f"refusals {m['llm_refusals_right']}/{m['refusal_questions']} vs {m['keyword_refusals_right']}/{m['refusal_questions']}; "
                  f"legislation topics finding acts {lex['llm']}/{lex['n']} vs {lex['kw']}/{lex['n']}; "
                  f"{m['seconds_per_question']['median']:.2f} s median, {m['seconds_per_question']['max']:.2f} s max; loaded in {m['load_seconds']} s; "
                  f"tokens {m['tokens']}, speed {m['tokens_per_second']}")
            if SHOW_FAILURES:
                for f in m["failures"]:
                    print("   model wrong:", f["q"], "| expected", f["expected"], "| got", f["model"])
        ctx.close()
        if errors:
            print("page errors:", errors[:5])
    out = pathlib.Path(os.environ.get("ERA_ASK_EVAL_OUT", "ask-eval-report.json"))
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print("report:", out)


if __name__ == "__main__":
    main()
