#!/usr/bin/env python3
"""Render connected-by-data-answers.md as a standalone HTML page.

The Markdown is the source; run this after editing it:

    python3 graphwiseAI-summit2026/build-html.py

Handles exactly what the answers use: headings, paragraphs, bullet and
numbered lists, tables, **bold**, *italic*, `code`, links and rules. Evidence
kinds (Live / Published / Repo) become labels, "On stage" lines callouts."""
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / 'connected-by-data-answers.md'
OUT = HERE / 'connected-by-data-answers.html'


LINK = re.compile(r'\[((?:[^\]`]|`[^`]*`)+)\]\(([^)\s]+)\)')


def inline(text):
    """Links first, so a label may hold code or emphasis; then code spans."""
    out, pos = [], 0
    for m in LINK.finditer(text):
        out.append(spans(text[pos:m.start()]))
        out.append('<a href="' + html.escape(m.group(2)) + '">' + spans(m.group(1)) + '</a>')
        pos = m.end()
    out.append(spans(text[pos:]))
    return ''.join(out)


def spans(text):
    out, pos = [], 0
    # code spans first, so nothing inside them is touched
    for m in re.finditer(r'`([^`]+)`', text):
        out.append(fmt(text[pos:m.start()]))
        out.append('<code>' + html.escape(m.group(1)) + '</code>')
        pos = m.end()
    out.append(fmt(text[pos:]))
    return ''.join(out)


def fmt(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'&lt;(https?://[^&]+)&gt;', r'<a href="\1">\1</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    return t


def kind_cell(text):
    """The last table column names the kind of evidence: label it."""
    for kind in ('Live', 'Published', 'Repo', 'Arithmetic'):
        text = re.sub(r'\b' + kind + r'\b', f'<span class="kind k-{kind.lower()}">{kind}</span>', text)
    return text


def render(md):
    lines = md.split('\n')
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('---'):
            out.append('<hr>')
            i += 1
            continue
        m = re.match(r'(#{1,3}) (.*)', line)
        if m:
            level, text = len(m.group(1)), m.group(2)
            ident = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
            out.append(f'<h{level} id="{ident}">{inline(text)}</h{level}>')
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]
            last = len(head) - 1
            t = ['<div class="tableWrap"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>']
            for r in body:
                t.append('<tr>' + ''.join(
                    f'<td>{kind_cell(inline(c)) if k == last and head[last].lower() == "kind" else inline(c)}</td>'
                    for k, c in enumerate(r)) + '</tr>')
            out.append(''.join(t) + '</tbody></table></div>')
            continue
        if re.match(r'(- |\d+\. )', line):
            ordered = bool(re.match(r'\d+\. ', line))
            items = []
            while i < len(lines) and (re.match(r'(- |\d+\. )', lines[i]) or (lines[i].startswith('  ') and items)):
                if re.match(r'(- |\d+\. )', lines[i]):
                    items.append(re.sub(r'^(- |\d+\. )', '', lines[i]))
                else:
                    items[-1] += ' ' + lines[i].strip()
                i += 1
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
            continue
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'(#|\||- |\d+\. |---)', lines[i]):
            para.append(lines[i])
            i += 1
        text = ' '.join(p.strip() for p in para)
        if text.startswith('**On stage:**'):
            out.append('<p class="stage">' + inline(text) + '</p>')
        elif text.startswith('**Key message'):
            out.append('<p class="key">' + inline(text) + '</p>')
        else:
            out.append('<p>' + inline(text) + '</p>')
    return '\n'.join(out)


PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Connected by Data — ERA</title>
<style>
  :root{
    --bg:#f7f8fb; --paper:#ffffff; --ink:#18202f; --muted:#5a6475; --line:#dde2ea;
    --accent:#1f5fae; --key-bg:#eef4fc; --stage-bg:#fdf6e7; --stage-line:#d99a1c;
    --live:#1d7a4f; --published:#1f5fae; --repo:#7a3fb0; --arith:#5a6475;
  }
  @media (prefers-color-scheme: dark){
    :root:not([data-theme="light"]){
      --bg:#0e131c; --paper:#161d29; --ink:#e7ecf4; --muted:#a3adbf; --line:#2a3445;
      --accent:#7fb0ef; --key-bg:#18263a; --stage-bg:#2a2414; --stage-line:#e0a93a;
      --live:#5fcf98; --published:#7fb0ef; --repo:#c79bef; --arith:#a3adbf;
    }
  }
  :root[data-theme="dark"]{
    --bg:#0e131c; --paper:#161d29; --ink:#e7ecf4; --muted:#a3adbf; --line:#2a3445;
    --accent:#7fb0ef; --key-bg:#18263a; --stage-bg:#2a2414; --stage-line:#e0a93a;
    --live:#5fcf98; --published:#7fb0ef; --repo:#c79bef; --arith:#a3adbf;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 "Segoe UI",system-ui,-apple-system,Arial,sans-serif;}
  main{max-width:920px;margin:0 auto;padding:32px 16px 64px;}
  h1{font-size:26px;line-height:1.25;margin:0 0 12px;}
  h2{font-size:20px;margin:36px 0 10px;padding-top:4px;color:var(--accent);}
  h3{font-size:16px;margin:28px 0 8px;}
  p{margin:10px 0;}
  ul,ol{margin:8px 0 12px;padding-left:22px;}
  li{margin:5px 0;}
  hr{border:none;border-top:1px solid var(--line);margin:30px 0;}
  a{color:var(--accent);}
  code{font:13px/1.4 "SF Mono",Consolas,monospace;background:color-mix(in srgb,var(--line) 55%,transparent);padding:1px 5px;border-radius:4px;overflow-wrap:anywhere;}
  .key{background:var(--key-bg);border-left:4px solid var(--accent);padding:12px 14px;border-radius:6px;}
  .stage{background:var(--stage-bg);border-left:4px solid var(--stage-line);padding:12px 14px;border-radius:6px;font-style:italic;}
  .stage strong{font-style:normal;}
  .tableWrap{overflow-x:auto;margin:12px 0;border:1px solid var(--line);border-radius:8px;background:var(--paper);}
  table{border-collapse:collapse;width:100%;font-size:14px;}
  th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line);}
  th{font-size:12px;text-transform:uppercase;letter-spacing:.4px;color:var(--muted);font-weight:600;}
  tr:last-child td{border-bottom:none;}
  td:last-child{white-space:nowrap;}
  td code{white-space:nowrap;overflow-wrap:normal;}
  .kind{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.3px;border:1px solid currentColor;border-radius:4px;padding:0 5px;}
  .k-live{color:var(--live);} .k-published{color:var(--published);} .k-repo{color:var(--repo);} .k-arithmetic{color:var(--arith);}
  @media (max-width:640px){ td:last-child{white-space:normal;} }
  @media print{
    body{background:#fff;color:#000;font-size:12px;} main{max-width:none;padding:0;}
    h2{break-after:avoid;} .tableWrap,.key,.stage{break-inside:avoid;}
  }
</style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
'''

if __name__ == '__main__':
    OUT.write_text(PAGE.replace('{body}', render(SRC.read_text(encoding='utf-8'))), encoding='utf-8')
    print('wrote', OUT.name)
