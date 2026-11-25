#!/usr/bin/env python3
"""Browser check of the ERATV Explorer's type view (scripts/assets/era-eratv-explorer.html),
against the acceptance checks of the type viewer:

- it works from a static host with only the snapshot (the endpoints are blocked);
- a type with parameter sets shows one column per configuration, a type without
  shows only "All configurations";
- a comparison marks differences with a visible "≠" and hidden text, "Show only
  differences" hides the equal rows, and the URL restores both selections;
- no request carries credentials, and the snapshot holds no holder or note.

Then, with the endpoint reachable, the same type is shown from a live query.
Needs Playwright (pip install playwright && playwright install chromium).

Usage: python3 scripts/tests/eratv_viewer_check.py [--shots DIR]
"""
import functools, gzip, http.server, json, pathlib, socketserver, sys, threading
from playwright.sync_api import sync_playwright

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
SNAP = json.loads(gzip.decompress((ASSETS / "era-eratv-snapshot.json.gz").read_bytes()))
SHOTS = pathlib.Path(sys.argv[sys.argv.index("--shots") + 1]) if "--shots" in sys.argv else None
ENDPOINTS = ("graph.uat.data.test-era.europa.eu", "graph.tst.data.test-era.europa.eu")

# Types picked from the snapshot, so the check follows the data
T = SNAP["T"]
sets = {k: len(v["s"]) for k, v in T.items()}
types_rows = SNAP["index"]["types"]
h = types_rows["h"]
ids = {}
for r in types_rows["r"]:
    key = r[h.index("vt")].rsplit("/", 1)[1]
    ids.setdefault(r[h.index("id")], []).append(key)
MANY = max((k for k in sets if "%" not in k), key=lambda k: (min(sets[k], 12), k))           # several configurations
NONE = sorted(k for k, n in sets.items() if n == 0 and "%" not in k)[0]                      # no parameter set
# one Type ID in two Member States: the same parameter sets, so every column pairs by IRI
SAME = next(sorted(v)[:2] for i, v in sorted(ids.items()) if len(v) > 1 and all(sets.get(k, 0) > 1 for k in sorted(v)[:2]))
# two different types with several configurations each: their values differ
OTHER = next(k for k in sorted(sets) if sets[k] > 1 and "%" not in k and k.split("-")[:3] != MANY.split("-")[:3])
PAIR = [MANY, OTHER]
assert len({c[1] for c in T[MANY]["s"]}) > 1, "the type with many sets should have several configurations"


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


failures = []
def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def main():
    srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ASSETS)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}/era-eratv-explorer.html"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for scheme in ("dark", "light"):
            ctx = browser.new_context(viewport={"width": 1366, "height": 900}, color_scheme=scheme)
            page = ctx.new_page()
            errors, creds = [], []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" and "Failed to load resource" not in m.text and "ERR_FAILED" not in m.text else None)
            page.on("request", lambda r: creds.append(r.url) if {"authorization", "cookie"} & set(k.lower() for k in r.headers) else None)
            # only the snapshot: the endpoints cannot be reached
            for host in ENDPOINTS:
                page.route(f"https://{host}/**", lambda route: route.abort())
            print(f"--- snapshot only ({scheme} scheme)")
            page.goto(f"{base}?type={MANY}")
            page.wait_for_selector("table.vt", timeout=30000)
            heads = page.locator("table.vt thead tr").last.locator("th").all_inner_texts()
            n_cols = len(heads) - 2
            check(n_cols == 1 + sets[MANY], f"{MANY}: {n_cols} value columns for {sets[MANY]} parameter sets plus 'All configurations'")
            check(heads[2].startswith("All configurations"), "the first value column is 'All configurations'")
            check("snapshot of" in page.inner_text("#viewSource"), "the source line names the snapshot")
            check(page.locator("#idxText").inner_text().startswith("snapshot of"), "the index comes from the snapshot")
            check(page.locator("table.vt caption").count() == 1 and page.locator("table.vt th[scope=row]").count() > 10, "a captioned table with row headers")
            check(page.locator("tr.secRow th").first.inner_text().strip() != "", "rows are grouped under section headings")
            if SHOTS and scheme == "dark":
                SHOTS.mkdir(parents=True, exist_ok=True)
                page.locator("#typePanel").screenshot(path=str(SHOTS / "type-dark.png"))

            page.goto(f"{base}?type={NONE}")
            page.wait_for_selector("table.vt", timeout=30000)
            heads = page.locator("table.vt thead tr").last.locator("th").all_inner_texts()
            check(len(heads) == 3 and heads[2].startswith("All configurations"), f"{NONE}: no parameter set, only 'All configurations'")

            # one Type ID in two Member States: every column pairs by configuration IRI, nothing differs
            page.goto(f"{base}?type={SAME[0]}&compare={SAME[1]}")
            page.wait_for_selector("table.vt thead tr.r2", timeout=30000)
            check(page.locator("table.vt thead .only").count() == 0 and page.locator("table.vt td.diff").count() == 0,
                  f"{SAME[0]} and {SAME[1]} share their parameter sets: every column paired, no difference")

            # two different types, through the pickers, then the URL
            page.goto(base)
            page.wait_for_function("!document.getElementById('typeInput').disabled", timeout=30000)
            page.fill("#typeInput", PAIR[0])
            page.fill("#compareInput", PAIR[1])
            page.click("#openBtn")
            page.wait_for_selector("table.vt thead tr.r2", timeout=30000)
            url = page.url
            check(f"type={PAIR[0]}" in url and f"compare={PAIR[1]}" in url, f"the URL keeps both selections: {url.split('?')[1]}")
            groups = page.locator("table.vt thead th.grp").all_inner_texts()
            check(groups == PAIR, f"two header rows, each type's columns under its ID: {groups}")
            check(page.locator("table.vt thead .only").count() > 0, "configurations only one type has are marked 'only in …'")
            diff_cells = page.locator("table.vt td.diff")
            n_diff = diff_cells.count()
            check(n_diff > 0, f"{n_diff} cells differ")
            first = diff_cells.first
            check(first.locator(".neq").inner_text() == "≠" and first.locator(".neq").get_attribute("aria-hidden") == "true", "a difference shows a visible ≠")
            check(first.locator(".vh").inner_text().startswith("differs from "), "and hidden text 'differs from …' for screen readers")
            check(first.evaluate("e => getComputedStyle(e).fontWeight") in ("700", "bold"), "and bold text")
            check(first.evaluate("e => getComputedStyle(e).backgroundColor") not in ("rgba(0, 0, 0, 0)", "transparent"), "and a light background")
            rows_all = page.locator("table.vt tbody tr:not(.secRow)").count()
            differing = page.locator("table.vt tbody tr[data-differs='1']").count()
            page.check("#diffOnly")
            shown = page.locator("table.vt tbody tr:not(.secRow):visible").count()
            check(0 < shown == differing < rows_all, f"'Show only differences' shows {shown} of {rows_all} rows ({differing} differ)")
            page.uncheck("#diffOnly")
            check(page.locator("table.vt tbody tr:not(.secRow):visible").count() == rows_all, "and unticking shows them all again")
            if SHOTS:
                page.locator("#typePanel").screenshot(path=str(SHOTS / f"compare-{scheme}.png"))
            page.goto(url)
            page.wait_for_selector("table.vt thead tr.r2", timeout=30000)
            check([page.input_value("#typeInput"), page.input_value("#compareInput")] == PAIR, "reloading the URL restores both selections")
            check(page.locator("table.vt thead th.grp").all_inner_texts() == PAIR, "and the comparison")

            # a phone: no horizontal scroll of the page itself
            page.set_viewport_size({"width": 390, "height": 860})
            check(page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"), "no page-wide horizontal scroll at phone width")
            if SHOTS and scheme == "light":
                page.screenshot(path=str(SHOTS / "phone-light.png"))
            check(not creds, f"no request carries credentials ({len(creds)})")
            check(not errors, f"no page errors {errors[:3]}")
            ctx.close()

        print("--- live")
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()
        page.goto(f"{base}?type={MANY}")
        page.wait_for_function("document.getElementById('liveText').textContent.startsWith('reachable') || document.getElementById('liveText').textContent.startsWith('not readable')", timeout=30000)
        live = page.inner_text("#liveText").startswith("reachable")
        page.wait_for_selector("table.vt", timeout=60000)
        if live:
            page.wait_for_function("document.getElementById('viewSource').textContent.includes('live')", timeout=60000)
            heads = page.locator("table.vt thead tr").last.locator("th").all_inner_texts()
            check(len(heads) - 2 == 1 + sets[MANY], f"live: the same {sets[MANY] + 1} value columns as the snapshot")
            check("queried live" in page.inner_text("#viewSource"), "live: the source line says so")
        else:
            print("     (ERATV-KG not reachable from here: live part skipped)")
        ctx.close()
        browser.close()

    text = json.dumps(SNAP)
    check(all(w not in text for w in ("rdf-schema#comment", "rdf-schema#seeAlso", "editorialNote", "vehicleTypeAuthorisationHolder", '"holder"')),
          "the snapshot holds no holder, comment or note")
    print(f"{len(failures)} FAILED" if failures else "all checks pass")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
