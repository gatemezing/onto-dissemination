# onto-dissemination

Materials and demo tools for disseminating the ERA ontology (ERA vocabulary) and
demonstrating "follow your nose" Linked Data navigation over live railway
infrastructure data (RINF), published by the European Union Agency for
Railways at `graph.data.era.europa.eu`.

Every tool is a single self-contained HTML file — no build step, no server,
no dependencies — that queries the live SPARQL endpoints directly from the
browser and exports results as CSV or Excel. The one exception is the ERADIS
Explorer, which searches a snapshot because its endpoint does not allow
cross-origin requests yet (see [Data snapshots](#data-snapshots)).

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
| Eurostat Exporter (sections of line / TEN-T flags as CSV or Excel) | https://gatemezing.github.io/onto-dissemination/eurostat.html |
| ERADIS Explorer (EC declarations and NoBo certificates, ERADIS search forms) | https://gatemezing.github.io/onto-dissemination/eradis.html |
| Interoperable Europe reusability answers | https://gatemezing.github.io/onto-dissemination/interopable-eu-portal-answers.html |
| Connected by data — ERA's answers, Graphwise AI Summit 2026 panel | https://gatemezing.github.io/onto-dissemination/connected-by-data.html |

Every tool links to the others in its footer. Deployment is automatic:
[.github/workflows/pages.yml](.github/workflows/pages.yml) rebuilds and
publishes GitHub Pages on every push to `main` that touches one of the tool
files.

## Data snapshots

Three tools ship data extracted ahead of time. The dates below are written by
the scripts that build each extract, so they stay current with the files.

| Extract | Used by | Latest extraction | Built by |
|---|---|---|---|
| RINF parameter catalogue — every ERA property with a RINF index, with per-country coverage | RINF Parameter Values explorer | <!-- extract:rinf-catalog -->2026-10-06 — 294 properties (213 populated), 27 countries, 54 datasets<!-- /extract:rinf-catalog --> | `scripts/build-rinf-parameter-catalog.py`, checked nightly (see [below](#keeping-the-rinf-parameter-snapshot-fresh)) |
| ERADIS EC declarations, organisations, TSIs and directives | ERADIS Explorer | <!-- extract:eradis-declarations -->2026-09-30 — 22,256 declarations<!-- /extract:eradis-declarations --> | `scripts/build-eradis-snapshot.py` |
| ERADIS NoBo certificates | ERADIS Explorer | <!-- extract:eradis-certificates -->2026-09-30 — 43,471 certificates<!-- /extract:eradis-certificates --> | `scripts/build-eradis-snapshot.py` |

Everything else — the Eurostat extracts included — is queried live when you run
it, so it is always as current as the endpoint. The Eurostat query set was last
measured against the live graph on 2026-10-02 (see [eurostat/](eurostat/)).

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
points' real coordinates, over a plain Esri basemap via Leaflet, with an
OpenRailwayMap overlay available but off by default so its own colours never
compete with the map's own. The map's legend/segment colours avoid green and
teal (the overlay's own track rendering uses both), and it can be popped out
into its own browser window with independent zoom.

**[era-rcc-parameters.html](scripts/assets/era-rcc-parameters.html)** — pick
one or more countries and one or more of their national lines (or "Select
all"), and get every RINF parameter flagged `era:usedInRCCCalculations` —
route-compatibility checking, positioned by kilometre post along the line and
at its operational points. Includes a network map, poppable into its own
window the same way the RINF Parameter Values map is. Query set and the
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
network map draws the selection, one colour per line, poppable into its own
window the same way the RINF Parameter Values map is. Query set in
[scripts/assets/routebook/README.md](scripts/assets/routebook/README.md).

**[era-eurostat-exporter.html](scripts/assets/era-eurostat-exporter.html)** —
exports the two optimised Eurostat extracts in [eurostat/](eurostat/) as CSV:
sections of line with their track parameters (30 columns, coded values given
as their `skos:prefLabel`; operational-point positions as a WKT point plus
latitude/longitude, read through `era:netReference/geo:hasGeometry`; optionally
a 31st column with each section's own geometry), and the TEN-T /
corridor classification flags (40 columns, including the post-2024
`era:partOfTENT` network levels, traffic types and European Transport
Corridors). Pick one country or the whole EU, see the exact SPARQL that will be
sent before running it, and get per-column coverage statistics with the result —
so an empty column is visibly a publication gap rather than a silent blank. Only the
description valid today is exported, so sections a manager has already
republished for next year (Germany) are not counted twice. A value the graph
does not carry reads `no data`, never an empty cell. The whole EU is fetched one
country at a time, six in parallel (~50 s). Dates are ISO 8601 (`YYYY-MM-DD`) throughout;
since a spreadsheet opening the CSV reformats them, except the pre-1900
placeholders, the result also downloads as `.xlsx`, where every date stays
`YYYY-MM-DD` text.

**[era-eradis-explorer.html](scripts/assets/era-eradis-explorer.html)** —
searches two ERADIS registers in `ERADIS-KG`, each with the fields of its
ERADIS search form:
- **EC declarations** of verification, conformity and suitability for use:
  Document ID, applicant and authorised representative, type of subsystem,
  constituent, certificate, directives, TSIs, signatories, date of issue;
- **NoBo certificates** (`era:CertificationLevelDocument`): number, type,
  module, object of assessment, validity today, subsystem, TSIs, applicant,
  manufacturer, notified body and NANDO number, dates, and whether a
  declaration cites it.

Every country and organisation field (applicant, authorised representative,
manufacturer, notified body) takes several values or all: a searchable
checkbox list, with the organisations narrowed to the countries picked.
The two registers link to each other in both directions. Every search is shown
as SPARQL, runnable live or in the GraphDB workbench; "Run live" returns every
match (all 43,471 certificates in ~10 s), in two phases. Results come with a
per-year chart, CSV download, and a detail view with each cited TSI linked to
its ELI in `era-lex`.

The dev endpoint sends no CORS headers, so the page searches snapshots built by
the same queries ([eradis/](eradis/), `scripts/build-eradis-snapshot.py`); the
certificate snapshot loads only when its tab is opened. Some values are derived
rather than recorded — "type of subsystem" (from the TSIs, through era-lex) and
a certificate's validity (from its validity window) — see
[eradis/README.md](eradis/README.md).

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
  (a stylised demo scene used for a short explainer video),
  `era-data-stories-member-state-demo.html` (a Data Stories reuse demo for a
  Member State) and `era-rinf-value-explorer-v0.html` (the first version of the
  value explorer, kept for reference). None of the three is deployed.
- `scripts/build-rinf-parameter-catalog.py` — regenerates the parameter and
  country/dataset snapshot embedded in the Value Explorer; see below.
- `scripts/build-eradis-snapshot.py` — rebuilds the two ERADIS snapshots
  from ERADIS-KG and era-lex, with the queries in `eradis/`; it needs access to
  the development endpoint.
- `scripts/build-eurostat-queries.py` — generates the optimised Eurostat
  queries in `eurostat/` and the copies embedded in the Eurostat Exporter, so
  the two never drift apart.
- `scripts/build-era-answers-pptx.py` — regenerates
  `interop-europe/ERA-ontology-reusability.pptx` from the answers (needs
  `python-pptx`).
- `interop-europe/` — the assessment questions, drafted answers, and the
  extracted Data Stories query catalogue.
- `eradis/` — the ERADIS-KG query set behind the ERADIS Explorer: the search
  and detail queries, the snapshot queries (ERADIS-KG and era-lex), and how the
  ERADIS form maps onto the graph.
- `eurostat/` — the Eurostat query set: the original queries, their optimised
  and live-tested rewrites, and data-quality extracts. Each optimised file
  documents what was wrong with the original and the measured runtimes.
- `sample-data/` — example SPARQL query + RDF/XML result pairs, with the
  engineering rationale in `sample-data/README.md`.
- `website/` — draft text and architecture diagram for an ERA Knowledge Graph
  web page.
- `.claude/skills/era-graph/` — what was measured about querying the ERA graph
  (publisher variations, validity rules, query shapes), kept for anyone, human
  or AI assistant, writing queries against it.
- `LICENSE` — the European Union Public Licence v1.2.

## Keeping the RINF parameter snapshot fresh

`python3 scripts/build-rinf-parameter-catalog.py` re-derives the whole
parameter/country catalogue from the live endpoint (~80 s) and rewrites it in
place, reproducibly.
[.github/workflows/refresh-rinf-catalog.yml](.github/workflows/refresh-rinf-catalog.yml)
runs it nightly and only commits when something actually changed — a quiet
night leaves a "checked — no change" note rather than an empty commit. A commit
also updates the extraction date in [Data snapshots](#data-snapshots). The
script refuses to write a snapshot that looks broken (wrong HTTP status,
missing columns, or a >20% drop in properties/countries) rather than
silently publishing bad data.

## Licence

The code and documentation in this repository are licensed under the
[European Union Public Licence v1.2](LICENSE) (EUPL-1.2), the official text
published by the European Commission
([Joinup](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)).
Under its Article 5, a work derived from both this code and code under one of
the compatible licences in its appendix may be distributed under that other
licence: GPL v2 and v3, AGPL v3, OSL v2.1 and v3.0, EPL v1.0, CeCILL v2.0 and
v2.1, MPL v2, LGPL v2.1 and v3, CC BY-SA 3.0 (for works other than software),
EUPL v1.1, and LiLiQ-R / LiLiQ-R+.

The railway data the tools query, and the snapshots derived from it, come from
the European Union Agency for Railways and remain under the Agency's own terms
of use; the licence above does not cover them.
