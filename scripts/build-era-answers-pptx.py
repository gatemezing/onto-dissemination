#!/usr/bin/env python3
"""Build the 5-slide ERA reusability summary as a real .pptx.

Run:  python3 scripts/build-era-answers-pptx.py   (needs python-pptx)
Source text: interop-europe/answers.md  ·  page: scripts/assets/era-interop-answers.html

Styling follows the ERA deck template: navy title/closing panels, white content
slides with a numbered navy chip and the agency mark, a light-weight grey slide
title set right, and navy-headed tables on pale blue rows.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import pathlib

NAVY   = RGBColor(0x2E, 0x43, 0x72)
CHIP   = RGBColor(0x2F, 0x4B, 0x7C)
FILL   = RGBColor(0xDC, 0xE6, 0xF1)
FILL2  = RGBColor(0xED, 0xF2, 0xF9)
HEAD   = RGBColor(0x59, 0x59, 0x59)
INK    = RGBColor(0x26, 0x26, 0x26)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
AMBER  = RGBColor(0x8A, 0x56, 0x10)
AMBBG  = RGBColor(0xFB, 0xF1, 0xE0)
GREEN  = RGBColor(0x25, 0x5C, 0x45)
GRNBG  = RGBColor(0xE8, 0xF1, 0xEC)
MUTED  = RGBColor(0x5B, 0x65, 0x77)
FONT   = "Calibri"
MONO   = "Consolas"

LOGO = pathlib.Path(__file__).resolve().parent / "assets" / "era-logo.png"
W, H = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]


def box(slide, x, y, w, h, fill=None, line=None):
    from pptx.enum.shapes import MSO_SHAPE
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sh.shadow.inherit = False
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line; sh.line.width = Pt(1)
    sh.text_frame.clear()
    return sh


def text(slide, x, y, w, h, runs, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT,
         font=FONT, space=6, line=1.25):
    """runs: str, or list of paragraphs; a paragraph is a str or list of (txt, **fmt)."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space)
        p.line_spacing = line
        parts = para if isinstance(para, list) else [(para, {})]
        for txt, fmt in parts:
            r = p.add_run(); r.text = txt
            f = r.font
            f.name = fmt.get("font", font)
            f.size = Pt(fmt.get("size", size))
            f.bold = fmt.get("bold", bold)
            f.italic = fmt.get("italic", False)
            f.color.rgb = fmt.get("color", color)
    return tb


def header(slide, num, title):
    """Navy numbered chip + agency mark + right-set light title."""
    box(slide, Inches(.62), Inches(.42), Inches(.5), Inches(.5), fill=CHIP)
    text(slide, Inches(.62), Inches(.53), Inches(.5), Inches(.4), str(num),
         size=15, color=WHITE, align=PP_ALIGN.CENTER)
    slide.shapes.add_picture(str(LOGO), Inches(1.30), Inches(.36), height=Inches(.62))
    text(slide, Inches(5.4), Inches(.36), Inches(7.3), Inches(1.0), title,
         size=27, color=HEAD, align=PP_ALIGN.RIGHT, line=1.06)


def footer(slide, left, num):
    text(slide, Inches(.62), Inches(6.98), Inches(9.5), Inches(.3), left,
         size=9.5, color=RGBColor(0x8A, 0x93, 0xA6))
    text(slide, Inches(12.0), Inches(6.98), Inches(.7), Inches(.3), str(num),
         size=9.5, color=RGBColor(0x8A, 0x93, 0xA6), align=PP_ALIGN.RIGHT)


def callout(slide, x, y, w, h, kind, parts):
    bg, bar, hue = {"amber": (AMBBG, AMBER, AMBER),
                    "green": (GRNBG, GREEN, GREEN),
                    "navy":  (FILL, NAVY, NAVY)}[kind]
    box(slide, x, y, w, h, fill=bg)
    box(slide, x, y, Inches(.05), h, fill=bar)
    runs = [(t, dict(f, color=hue) if f.get("bold") else f) for t, f in parts]
    text(slide, x + Inches(.22), y + Inches(.14), w - Inches(.42), h - Inches(.2),
         [runs], size=13.5, line=1.22)


def table(slide, x, y, w, rows, widths, size=12.5, rh=Inches(.32)):
    n, m = len(rows), len(rows[0])
    shp = slide.shapes.add_table(n, m, x, y, w, rh * n)
    tbl = shp.table
    tbl.first_row = True
    for j, fr in enumerate(widths):
        tbl.columns[j].width = Emu(int(w * fr))
    for i, row in enumerate(rows):
        tbl.rows[i].height = rh
        for j, cell in enumerate(row):
            c = tbl.cell(i, j)
            c.text = ""
            c.margin_left = c.margin_right = Inches(.09)
            c.margin_top = c.margin_bottom = Inches(.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.fill.solid()
            c.fill.fore_color.rgb = NAVY if i == 0 else (FILL if i % 2 else FILL2)
            p = c.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT if (j and str(cell).replace(",", "").replace("%", "").isdigit()) else PP_ALIGN.LEFT
            r = p.add_run(); r.text = str(cell)
            r.font.size = Pt(size)
            r.font.name = FONT
            r.font.bold = (i == 0)
            r.font.color.rgb = WHITE if i == 0 else INK
    return shp


# ── 1 ─────────────────────────────────────────────────────── title
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, W, H, fill=NAVY)
text(s, Inches(.95), Inches(2.05), Inches(9.6), Inches(1.05),
     [[("Reusing the ", {"size": 46}), ("ERA Ontology", {"size": 46, "bold": True})]],
     color=WHITE, line=1.02, space=2)
text(s, Inches(.95), Inches(3.15), Inches(9.6), Inches(.6),
     "Seven answers for the Interoperable Europe assessment", size=21, color=WHITE)
box(s, Inches(.95), Inches(4.0), Inches(4.2), Pt(1), fill=RGBColor(0x8E, 0xA2, 0xC6))
text(s, Inches(.95), Inches(4.25), Inches(10.0), Inches(1.0),
     ["Every figure is a legal reference, a measurement of the published artefacts "
      "(ontology v3.3.4, era-shapes, era-skos), or a measurement against the live "
      "knowledge graph on 22 August 2026.",
      "Parameter counts exclude owl:deprecated terms."],
     size=13, color=RGBColor(0xD3, 0xDD, 0xEE), line=1.3)
s.shapes.add_picture(str(LOGO), Inches(.95), Inches(5.75), height=Inches(.78))

# ── 2 ─────────────────────────────────────────── the case for reuse
s = prs.slides.add_slide(BLANK)
header(s, 2, "Not an interpretation of the law —\nthe law in machine-readable form")
text(s, Inches(.62), Inches(1.62), Inches(12.1), Inches(.4),
     "Reg. (EU) 2019/777, as amended by (EU) 2023/1694, defines RINF as a numbered parameter list.",
     size=15.5, color=NAVY, bold=True)
text(s, Inches(.62), Inches(2.08), Inches(12.1), Inches(.75),
     [[("era:rinfIndex", {"font": MONO, "size": 13.5}),
       (" binds each property to its legal index: parameter ", {}),
       ("1.1.1.1.4.1 “Nominal track gauge”", {"bold": True}),
       (" is ", {}), ("era:wheelSetGauge", {"font": MONO, "size": 13.5}),
       (". The trace from legal text to data field is machine-checkable, not a documentation promise.", {})]],
     size=14.5, line=1.3)

stats = [("292", "Live RINF parameters\n(37 more deprecated)"),
         ("4", "Registers on one vocabulary\nRINF · ERATV · EVR · ERADIS"),
         ("420", "Ontology terms citing\n79 legal acts via ELI"),
         ("27", "Countries publishing,\n54 national datasets")]
for k, (big, lab) in enumerate(stats):
    x = Inches(.62 + k * 3.05)
    box(s, x, Inches(3.0), Inches(2.85), Inches(1.16), fill=FILL)
    box(s, x, Inches(3.0), Inches(.05), Inches(1.16), fill=NAVY)
    text(s, x + Inches(.18), Inches(3.06), Inches(2.5), Inches(.44), big,
         size=22, color=NAVY, bold=True, space=0, line=1.1)
    text(s, x + Inches(.18), Inches(3.5), Inches(2.55), Inches(.62), lab,
         size=10, color=MUTED, line=1.15)

callout(s, Inches(.62), Inches(4.45), Inches(12.1), Inches(.95), "green",
        [("The chain runs end to end. ", {"bold": True}),
         ("era:tsiMagneticFields carries RINF index 1.1.1.3.9.1 and points at "
          "eli/reg_impl/2023/1695/oj — the act in the Official Journal. "
          "Data field → legal parameter → provision, with no human in the loop.", {})])
callout(s, Inches(.62), Inches(5.62), Inches(12.1), Inches(.95), "amber",
        [("Stated plainly. ", {"bold": True}),
         ("The vocabulary spans four registers, but only RINF data is openly queryable today; "
          "and the deployed validation carries roughly half the published shapes "
          "(76 node shapes against 147).", {})])
footer(s, "ERA Ontology v3.3.4 · EUPL 1.2 · DOI 10.5281/zenodo.15089005", 2)

# ── 3 ───────────────────────────────── one URI + cross-border value
s = prs.slides.add_slide(BLANK)
header(s, 3, "One URI, reusable everywhere")
text(s, Inches(.62), Inches(1.62), Inches(12.1), Inches(.35),
     "A thing gets one identifier, and everyone points at it instead of describing it again.",
     size=15.5, color=NAVY, bold=True)

text(s, Inches(.62), Inches(2.12), Inches(5.9), Inches(.3), "Reuse what already exists",
     size=13.5, color=NAVY, bold=True)
text(s, Inches(.62), Inches(2.5), Inches(5.9), Inches(1.8),
     ["•  90,235 references to ELI legal acts",
      "•  6,688 to Publications Office corporate bodies",
      "•  1,863 to its language authority",
      "•  1,092 to EuroVoc subjects · 93 to treaties",
      "•  Countries are Publications Office URIs, not ERA codes"],
     size=13, line=1.25, space=4)

text(s, Inches(6.85), Inches(2.12), Inches(5.85), Inches(.3), "Mint once, reuse across registers",
     size=13.5, color=NAVY, bold=True)
text(s, Inches(6.85), Inches(2.5), Inches(5.85), Inches(1.8),
     ["•  body/organisation/0080 is DB InfraGO — holding IM, RU, ECM, Keeper, Owner and ECM-CB roles at once",
      "•  Those roles belong to different registers: IM→RINF, Keeper/Owner/ECM→EVR, certification→ERADIS",
      "•  665,487 infrastructure elements name that one URI as their manager",
      "•  2,909 of 5,528 organisations (53%) hold more than one role"],
     size=13, line=1.25, space=4)

text(s, Inches(.62), Inches(4.42), Inches(5.9), Inches(.3),
     "One question, 27 countries, seconds", size=13.5, color=NAVY, bold=True)
table(s, Inches(.62), Inches(4.78), Inches(5.9).emu,
      [["Gauge", "Network", "Running tracks"],
       ["1435", "Standard", "697,901"],
       ["1668", "Iberian", "13,275"],
       ["1524", "Finnish / Baltic", "2,813"],
       ["1600", "Irish", "274"]],
      [.22, .43, .35], size=11.5, rh=Inches(.29))

callout(s, Inches(6.85), Inches(4.42), Inches(5.85), Inches(1.05), "navy",
        [("Route compatibility spans three registers", {"bold": True}),
         (" — the vehicle in EVR, its type in ERATV, the line in RINF. "
          "One vocabulary makes it a query, not an integration project.", {})])
callout(s, Inches(6.85), Inches(5.58), Inches(5.85), Inches(1.05), "green",
        [("A shared identifier space is durable sovereignty", {"bold": True}),
         (" — custody stays national, open W3C/OGC standards, EUPL 1.2, "
          "archival DOI. It cannot be withdrawn by a supplier.", {})])
footer(s, "era-lex holds 7,317 legal acts and 7,198 addressable subdivisions, in 24 languages", 3)

# ── 4 ──────────────────────────────────────────── lessons / defects
s = prs.slides.add_slide(BLANK)
header(s, 4, "Lessons learnt —\nand what is not yet right")
text(s, Inches(.62), Inches(1.72), Inches(12.1), Inches(.35),
     "A shared vocabulary does not by itself produce comparable data. "
     "Publication and convergence are different problems.",
     size=15.5, color=NAVY, bold=True)
callout(s, Inches(.62), Inches(2.22), Inches(12.1), Inches(.74), "amber",
        [("Four defects, one failure mode: the silent, well-formed zero. ", {"bold": True}),
         ("Nothing errors, nothing warns, and the wrong conclusion looks like a correct one.", {})])
table(s, Inches(.62), Inches(3.05), Inches(12.1).emu,
      [["What we found", "Why it matters"],
       ["8 concepts minted into a scheme the check validates against",
        "Conformance resolved from the working graph is self-certified"],
       ["17 deprecated properties still carrying 237,781 statements",
        "Only 1 declares a successor; deprecation never reached the data"],
       ["87 of 180 organisation URIs do not resolve",
        "Belgium’s IM is 0088 in RINF, 1976 in the register"],
       ["Notebook queries name graphs that are empty in the deployment",
        "Run as published, they return HTTP 200 and no rows"]],
      [.44, .56], size=12, rh=Inches(.42))
text(s, Inches(.62), Inches(5.42), Inches(12.1), Inches(1.0),
     [[("Transferable rules. ", {"bold": True, "color": NAVY}),
       ("Resolve a value set from a trusted, published artefact — never from the same graph the "
        "data under test can write into. Validate the vocabulary, not only the data. Stand up the "
        "identifier register before the datasets that cite it, and treat deprecation as a data "
        "migration rather than an annotation.", {})]],
     size=13.5, color=MUTED, line=1.3)
footer(s, "Stated deliberately: an assessment is worth more when it is honest", 4)

# ── 5 ────────────────────────────────────── how to reuse + sources
s = prs.slides.add_slide(BLANK)
header(s, 5, "How to start reusing —\nand where everything lives")
text(s, Inches(.62), Inches(1.72), Inches(5.9), Inches(.3),
     "Governance", size=13.5, color=NAVY, bold=True)
text(s, Inches(.62), Inches(2.08), Inches(5.9), Inches(2.05),
     ["The vocabulary needs central governance. The deployment does not.",
      "•  Central, non-negotiable: one owner, one version line, one licence — otherwise 27 dialects",
      "•  Decentralised, valuable at once: Bane NOR (Norway) gains value publishing alone, outside the EU mandate",
      "•  Every level: Italy has 9 publishing organisations, Austria 8, Belgium 1"],
     size=12.5, line=1.24, space=4)

text(s, Inches(6.85), Inches(1.72), Inches(5.85), Inches(.3),
     "First steps", size=13.5, color=NAVY, bold=True)
text(s, Inches(6.85), Inches(2.08), Inches(5.85), Inches(2.05),
     ["1.  Run the published queries — 38 in the Data Stories catalogue plus 47 across three notebooks",
      "2.  Adopt the identifiers before modelling anything",
      "3.  Adopt the code lists — where most comparability is won",
      "4.  Validate early with the shipped SHACL shapes; check every external URI resolves",
      "5.  Publish into your own dataset, keeping custody"],
     size=12.5, line=1.24, space=4)

text(s, Inches(.62), Inches(4.32), Inches(12.1), Inches(.3),
     "References", size=13.5, color=NAVY, bold=True)
text(s, Inches(.62), Inches(4.66), Inches(6.0), Inches(2.2),
     ["ERA Ontology v3.3.4 — rinf.data.era.europa.eu/era-vocabulary",
      "Application guides — RINF, ERATV, EVR, ERADIS (same host)",
      "Published artefacts — era-shapes, era-skos, era-telem-skos, ontology.nt",
      "Live knowledge graph — graph.data.era.europa.eu",
      "Data Stories, 38 queries + 3 notebooks — rinf.data.era.europa.eu/data-stories"],
     size=11.5, line=1.3, space=4)
text(s, Inches(6.85), Inches(4.66), Inches(5.85), Inches(2.2),
     ["Reg. (EU) 2019/777, amended by (EU) 2023/1694 — RINF",
      "Decision 2011/665/EU; Reg. (EU) 2019/776 — ERATV",
      "Reg. (EU) 2023/1695; Decision (EU) 2018/1614 — EVR",
      "Dir. (EU) 2016/797 and 2016/798; Reg. (EU) 2016/796 — ERADIS",
      "Interoperable Europe Portal — ERA Vocabulary solution",
      "Repository — gitlab.com/era-europa-eu/public/interoperable-data-programme",
      "Logo: ERA-rgb-300dpi.jpg, Wikimedia Commons, public domain, by ERA"],
     size=11.5, line=1.3, space=4)
footer(s, "Full answers: gatemezing.github.io/onto-dissemination/interopable-eu-portal-answers.html", 5)

out = (pathlib.Path(__file__).resolve().parent.parent /
       "interop-europe" / "ERA-ontology-reusability.pptx")
prs.save(out)
print(f"saved {out.name}: {out.stat().st_size:,} bytes, {len(prs.slides.__iter__.__self__._sldIdLst)} slides")
