# onto-dissemination

Materials and demo tools for disseminating the ERA ontology (ERA vocabulary) and
demonstrating "follow your nose" Linked Data navigation over live railway
infrastructure data (RINF), published by the European Union Agency for
Railways at `graph.data.era.europa.eu`.

Every tool is a single self-contained HTML file — no build step, no server,
no dependencies — that queries the live SPARQL endpoint directly from the
browser and exports results as CSV or Excel.

## Live demos

| Tool | URL |
|---|---|
| ERA Graph Explorer (bubble-graph, offline + live) | https://gatemezing.github.io/onto-dissemination/ |
| Ask the ERA Graph (natural-language / voice query) | https://gatemezing.github.io/onto-dissemination/ask.html |
| Holobox Frame (4-face pyramid hologram display) | https://gatemezing.github.io/onto-dissemination/holobox.html |
| RDF Exporter | https://gatemezing.github.io/onto-dissemination/exporter.html |
| RINF Parameter Values explorer | https://gatemezing.github.io/onto-dissemination/values.html |
| RCC Parameters (route compatibility) | https://gatemezing.github.io/onto-dissemination/rcc.html |
| Route Book (TSI OPE Appendix D2) | https://gatemezing.github.io/onto-dissemination/routebook.html |
| Interoperable Europe reusability answers | https://gatemezing.github.io/onto-dissemination/interopable-eu-portal-answers.html |

Every tool links to the others in its footer. Deployment is automatic:
[.github/workflows/pages.yml](.github/workflows/pages.yml) rebuilds and
publishes GitHub Pages on every push to `main` that touches one of the tool
files.

## Quick start

Open any tool directly in a browser, or serve the repo locally (recommended,
since some browsers restrict `file://` pages):

```bash
python3 -m http.server 8000
# then open http://localhost:8000/scripts/assets/era-graph-explorer-app.html
```

## The tools

**[era-graph-explorer-app.html](scripts/assets/era-graph-explorer-app.html)** —
the flagship "follow your nose" bubble-graph explorer. Ships with a curated,
verified-offline dataset centred on Oslo Central Station (Bane NOR) so a booth
demo works with no network at all, plus a live SPARQL mode for visitors who
want to query the real graph and follow any resource's real outgoing and
incoming links, including ERA's ontology and SKOS (controlled-vocabulary)
graphs.

**[era-ask.html](scripts/assets/era-ask.html)** — ask about railway
infrastructure, organisations and EU rail law in plain language, typed or
spoken (via the browser's built-in speech recognition), in English, French,
German, Spanish or Italian. A small keyword-matched vocabulary — not a
language model — turns a recognised question into a live SPARQL query across
three endpoints (`rinf-plus`, `OCR-KG`, `era-lex`); an unrecognised question
gets pointed at the sample questions rather than a guess, and the generated
query is always one click away.

**[era-holobox-frame.html](scripts/assets/era-holobox-frame.html)** — renders
that same bubble-graph view natively across all four faces of a pyramid
hologram display (white stage; per-face rotation calibrated to your physical
reflector), driven from one shared live query so all four faces and the
navigation trail stay in lock-step. An earlier version tried to embed the
GraphDB Workbench's own visual graph via `<iframe>`; that endpoint sends
`X-Frame-Options: SAMEORIGIN`, which silently blocks framing from any other
origin in every browser, so it's now a first-party renderer instead.

**[era-rdf-exporter.html](scripts/assets/era-rdf-exporter.html)** — paste any
ERA/RINF resource URI, get its full RDF graph as RDF/XML, recursed to real
leaf values with ontology/SHACL noise and retired (`owl:deprecated`)
properties filtered out. Query rationale in
[sample-data/README.md](sample-data/README.md).

**[era-rinf-value-explorer.html](scripts/assets/era-rinf-value-explorer.html)**
— pick RINF parameters and countries (or, with a single country selected,
extract its whole catalogue of populated parameters in one click), get every
distinct value actually reported, with counts. Surfaces national practice
and data-quality drift (e.g. Croatia publishing operational-point types under
a different concept scheme than everyone else, typos included). Exports a
transposed one-row-per-location sheet — country, start/end operational point,
that section's own length (`era:lengthOfSectionOfLine`), and the value — plus
a network map: sections of line drawn as chords between their operational
points' real coordinates, over live OpenStreetMap/OpenRailwayMap tiles via
Leaflet. The map's own background and legend/segment colours are a plain
light theme with no green or teal (OpenStreetMap's land-cover rendering
already uses green, which used to swallow a same-coloured segment), and it
can be popped out into its own browser window with independent zoom.

**[era-rcc-parameters.html](scripts/assets/era-rcc-parameters.html)** — pick
one or more countries and one or more of their national lines (or "Select
all"), and get every RINF parameter flagged `era:usedInRCCCalculations` —
route-compatibility checking, positioned by kilometre post along the line and
at its operational points. Includes a network map. Query set and the
five country-modelling variations it absorbs (line identity, part-whole
direction, validity scoping, etc.) documented in
[scripts/assets/rcc/README.md](scripts/assets/rcc/README.md).

**[era-route-book.html](scripts/assets/era-route-book.html)** — same
multi-country, multi-line, "Select all" selection as the RCC tool, for the
TSI OPE Appendix D2 route book: every property an infrastructure manager owes
a railway undertaking, with a coverage view showing which of the 46 D2
elements a selection carries, which are published elsewhere, and which no
manager populates at all. Sections of line are named by the operational
points they run between rather than shown by kilometre position alone, and a
network map draws the selection, one colour per line. Query set in
[scripts/assets/routebook/README.md](scripts/assets/routebook/README.md).

**[era-interop-answers.html](scripts/assets/era-interop-answers.html)** — the
ERA reusability answers for the Interoperable Europe assessment (source text
in [interop-europe/answers.md](interop-europe/answers.md)).

### Shared behaviour across the live-query tools

- **Retired properties excluded everywhere.** Anything `owl:deprecated` is
  filtered out at query time, consistently, in every tool.
- **Validity handled place by place, never line-wide.** Managers republish
  descriptions differently — some republish a whole stretch yearly, others
  date each section by the day it opened — so the newest-window filter is
  applied per place, not per line, or a line-wide filter would silently
  delete most of a country's real data.
- **Every country is supported, not just the well-behaved ones.** National
  publishers model line identity, point positioning, and part-whole links
  differently; each tool absorbs the variations rather than returning
  nothing for the countries that differ (Croatia and Norway are the usual
  outliers).
- **Fetch failures are diagnosed, not just displayed.** A cross-origin
  request that fails gives the browser no way to tell "the server refused
  cross-origin access" apart from "there's no server to reach" — so each
  tool probes the endpoint separately and reports which one actually
  happened, with a plain-language explanation, a *Try again* action, and the
  raw error tucked behind a details toggle rather than shown as the headline.

## Repository layout

- `scripts/innotrans2026-era-ontology-script.md` — booth/demo script for
  InnoTrans 2026: elevator pitch, demo queries, checklist.
- `scripts/assets/` — the tools above, plus `era-follow-your-nose-scene.html`
  (a stylised demo scene used for a short explainer video).
- `scripts/build-rinf-parameter-catalog.py` — regenerates the parameter and
  country/dataset snapshot embedded in the Value Explorer; see below.
- `scripts/build-era-answers-pptx.py` — regenerates
  `interop-europe/ERA-ontology-reusability.pptx` from the answers (needs
  `python-pptx`).
- `interop-europe/` — the assessment questions, drafted answers, and the
  extracted Data Stories query catalogue.
- `sample-data/` — example SPARQL query + RDF/XML result pairs, with the
  engineering rationale in `sample-data/README.md`.

## Keeping the RINF parameter snapshot fresh

`python3 scripts/build-rinf-parameter-catalog.py` re-derives the whole
parameter/country catalogue from the live endpoint (~80 s) and rewrites it in
place, reproducibly.
[.github/workflows/refresh-rinf-catalog.yml](.github/workflows/refresh-rinf-catalog.yml)
runs it nightly and only commits when something actually changed — a quiet
night leaves a "checked — no change" note rather than an empty commit. The
script refuses to write a snapshot that looks broken (wrong HTTP status,
missing columns, or a >20% drop in properties/countries) rather than
silently publishing bad data.
