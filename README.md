# onto-dissemination

Materials and demo tools for disseminating the ERA ontology (ERA vocabulary) and
demonstrating "follow your nose" Linked Data navigation over live railway
infrastructure data (RINF), published by the European Union Agency for
Railways at `graph.data.era.europa.eu`.

Every tool is a single self-contained HTML file — no build step, no server —
that queries the live SPARQL endpoints directly from the browser and exports
results as CSV or Excel. The external code is Leaflet in the map tools and
N3.js in the SHACL Shape Viewer, both pinned to a version and checked with
SRI. The Synthetic RINF Data page also loads Pyodide 0.28.3 and vis-network 9.1.9
(pinned, SRI-checked) and installs RDFGraphGen 1.2.0, rdflib 7.6.0 and exrex 0.12.0
from PyPI at pinned versions. Ask the ERA Graph can load WebLLM 0.2.87 (pinned, with its
SHA-384 hash in an import map) and an open-weights model from Hugging Face, only when asked. The ERADIS Explorer searches a snapshot and runs
the same search live on request (see [Data snapshots](#data-snapshots)).

## Live demos

| Tool | URL |
|---|---|
| ERA Graph Explorer (bubble-graph, offline + live) | https://gatemezing.github.io/onto-dissemination/ |
| Ask the ERA Graph (natural-language / voice query) | https://gatemezing.github.io/onto-dissemination/ask.html |
| Holobox Frame (the bubble graph on a single stage, natively rendered) | https://gatemezing.github.io/onto-dissemination/holobox.html |
| RDF Exporter | https://gatemezing.github.io/onto-dissemination/exporter.html |
| RINF Parameter Values explorer | https://gatemezing.github.io/onto-dissemination/values.html |
| RCC Parameters (route compatibility) | https://gatemezing.github.io/onto-dissemination/rcc.html |
| Route Book (TSI OPE Appendix D2) | https://gatemezing.github.io/onto-dissemination/routebook.html |
| Eurostat Exporter (sections of line / TEN-T flags as CSV or Excel) | https://gatemezing.github.io/onto-dissemination/eurostat.html |
| ERADIS Explorer (EC declarations and NoBo certificates, ERADIS search forms) | https://gatemezing.github.io/onto-dissemination/eradis.html |
| ERATV Explorer (authorised vehicle types: one column per configuration, two types compared, the ERATV advanced-search fields; UAT ERATV-KG, with a snapshot) | https://gatemezing.github.io/onto-dissemination/eratv.html |
| Primary Locations in RINF (every `era:PrimaryLocation` of a country as CSV, optionally narrowed to national lines) | https://gatemezing.github.io/onto-dissemination/plc-extraction.html |
| Synthetic RINF and EVR Data (realistic synthetic Turtle from the UAT SHACL shapes with RDFGraphGen. RINF: tracks, sidings, platform edges and tunnels linked to their sections and stations with `era:hasPart`/`era:isPartOf`, on a map. EVR + ERATV: vehicles with valid EVNs, vehicle types with ERATV numbers, type authorisations with EINs, invented keepers, owners and ECMs, and the `vpa:` chain from type authorisation to registration; graph, checks and export) | https://gatemezing.github.io/onto-dissemination/synthetic.html |
| SHACL Shape Viewer (ERA's PROD and UAT validation shapes, a PROD → UAT comparison, an OWL gap analysis of the UAT release candidate with the immediate actions to fix, or your own SHACL file, as a navigable diagram) | https://gatemezing.github.io/onto-dissemination/shapes.html |
| Interoperable Europe reusability answers | https://gatemezing.github.io/onto-dissemination/interopable-eu-portal-answers.html |
| Connected by data — ERA's answers, Graphwise AI Summit 2026 panel | https://gatemezing.github.io/onto-dissemination/connected-by-data.html |
| Slides: A Semantic Backbone for European Rail Data Exchange (KGSWC 2026) | https://gatemezing.github.io/onto-dissemination/kgswc-2026/ |
| Slides: Build on the rail graph (FOSDEM 2027, Railways and Open Transport devroom) | https://gatemezing.github.io/onto-dissemination/carto-rinf-open-data/ |

The live-query tools link to each other in their footers. No other page links
yet to the Holobox Frame, the ERATV Explorer, Primary Locations in RINF, the SHACL Shape Viewer or the
two answer pages, and only the ERATV Explorer links to the ERADIS Explorer. Deployment is automatic:
[.github/workflows/pages.yml](.github/workflows/pages.yml) rebuilds and
publishes GitHub Pages on every push to `main` that touches one of the tool
files.

## Data snapshots

Three tools ship data extracted ahead of time. The dates below are written by
the scripts that build each extract, so they stay current with the files.

| Extract | Used by | Latest extraction | Built by |
|---|---|---|---|
| RINF parameter catalogue — every ERA property with a RINF index, with per-country coverage | RINF Parameter Values explorer | <!-- extract:rinf-catalog -->2026-11-25 — 293 properties (221 populated), 27 countries, 71 datasets<!-- /extract:rinf-catalog --> | `scripts/build-rinf-parameter-catalog.py`, checked nightly (see [below](#keeping-the-rinf-parameter-snapshot-fresh)) |
| ERADIS EC declarations, organisations, TSIs and directives | ERADIS Explorer | <!-- extract:eradis-declarations -->2026-11-19 — 22,256 declarations<!-- /extract:eradis-declarations --> | `scripts/build-eradis-snapshot.py` |
| ERADIS NoBo certificates | ERADIS Explorer | <!-- extract:eradis-certificates -->2026-11-19 — 43,615 certificates<!-- /extract:eradis-certificates --> | `scripts/build-eradis-snapshot.py` |
| ERATV vehicle types: the search index and every type's values per configuration, with property names and ERATV numbers from the ERA ontology release | ERATV Explorer, when ERATV-KG cannot be read | <!-- extract:eratv -->2026-11-25, 4,149 vehicle types<!-- /extract:eratv --> | `scripts/build-eratv-snapshot.js` |

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
German, Spanish or Italian. A small open-source language model, Qwen2.5-1.5B-Instruct
(Apache 2.0), runs in the browser through [WebLLM](https://github.com/mlc-ai/web-llm)
on WebGPU and reads the question the way such models are trained to call
functions: it fills in one typed form (question shape, count or list,
country, a legislation topic in English, an organisation code or name), with
decoding constrained to a JSON schema whose enums hold only values the page
knows. The form selects one of the hand-written SPARQL queries across three
endpoints (`rinf-plus`, `OCR-KG`, `era-lex`), so the model never writes a
query; a code or a name it reports must occur in the question. Questions
outside the fixed shapes (conditions, rankings, single named places) are
declined, with keyword matching's reading offered as an alternative. The
model is loaded on request (downloaded once from Hugging Face and cached by
the browser, then reloaded automatically); without WebGPU, or before it is
loaded, keyword matching reads the question as before. The form the model
filled in and the query are always one click away.
The model proposes and rules verify: count or list comes from the trigger
words when the question has them, a five-language list of superlatives and
thresholds declines the question, and the keyword extractors stand in when
the model gives no usable organisation code or name.
[scripts/tests/ask_llm_eval.py](scripts/tests/ask_llm_eval.py) scores both
readings on the 70 labelled questions in
[scripts/tests/ask-questions.json](scripts/tests/ask-questions.json): on
2026-11-22, on an Apple M1, Qwen2.5-1.5B read 68 correctly against 56 for
keyword matching, declined 8 of the 9 out-of-scope questions (6), turned all
7 legislation topics into English words that find acts in era-lex (3), and
took 4.4 s per question; Qwen2.5-0.5B read only 40.

**[era-holobox-frame.html](scripts/assets/era-holobox-frame.html)** — renders
that same bubble-graph view natively on a single desktop stage, driven from one
live query, with a navigation trail and an Expand-to-next-bubble control. It
began as a four-face pyramid hologram layout, simplified to one view in commit
`27ab948`. An earlier version tried to embed the
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
as SPARQL, to run live or in the GraphDB workbench. "Run live" returns every
match in two phases (all 43,615 certificates in ~14 s). Results come with a
per-year chart, CSV download, and a detail view with each cited TSI linked to
its ELI in `era-lex`; the full record of a document is read live.

Searches run on snapshots built by the same queries ([eradis/](eradis/),
`scripts/build-eradis-snapshot.py`), and the certificate snapshot loads only
when its tab is opened. The dev endpoint is open for anonymous reads and
answers browsers on any origin again (it sent no CORS headers until October
2026, and asked for a login from 2026-10-12 until November 2026), so "Run live"
works from GitHub Pages; the snapshot keeps the page working when it doesn't.
On 2026-11-19 snapshot and live answers matched document for document and
field by field. ERA reloaded ERADIS-KG in November 2026 with a new certificate
model (new URIs, recorded subsystem, acts cited four ways, constituents named
in era-lex); both the snapshot and the live queries follow it. Some values are
derived rather than recorded — a declaration's "type of subsystem" (from its
TSIs, through era-lex) and a certificate's validity (from its validity window)
— see [eradis/README.md](eradis/README.md).

**[era-eratv-explorer.html](scripts/assets/era-eratv-explorer.html)** —
opens an authorised vehicle type from `ERATV-KG` on ERA's UAT server
(`graph.uat.data.test-era.europa.eu`, anonymous and open to any origin) and
shows its values in one table: ERATV's numbering (`era:eratvIndex`) down the
side, the technical characteristics (4.x) first, and across, "All
configurations" (the values stated on the type) and then one column per
configuration (one per parameter set, so two sets of one configuration get a
column each), with the conformity with TSI of each. A second type can be put
beside it: columns are paired by configuration IRI, then by configuration
label, and a differing cell is marked with a visible "≠", bold text, a light
background and hidden text for screen readers ("differs from …"); "Show only
differences" hides the equal rows, and the address (`?type=…&compare=…`)
keeps both choices for sharing. The pickers search by Type ID, platform or
alternative name. To find types, the ERATV advanced-search fields are there
too: Type ID or name, EIN, category and subcategory, manufacturer (by
country, name or pick), conformity with TSI, EC certificate or declaration
reference, Member State (including "authorised by ERA"), authorisation
status, area of use, comments, authorisation date and last update, with a
per-year chart by category and CSV download. Every search is shown as SPARQL,
and "Run live" sends it and checks that it returns the same types.

The page opens on a snapshot, `era-eratv-snapshot.json.gz` (1.1 MB), so it
works from any static host even when ERATV-KG cannot be read: the search
index and every type's values per configuration, built by
[scripts/build-eratv-snapshot.js](scripts/build-eratv-snapshot.js) with the
page's own queries (`npm install --no-save n3@2.13.12 && node
scripts/build-eratv-snapshot.js`). Parameter names and ERATV numbers come
from the ERA ontology release (`--tag`, default `v4.0.0`) and its SKOS, then
from ERATV-KG's own ontology and SKOS graphs, so the page needs no ontology at
run time. A type's values are queried live whenever ERATV-KG answers; the
comments field always is, because the snapshot carries no authorisation
holders, comments or notes. The page sends no credentials. The ERATV+ server
(`graph.tst.data.test-era.europa.eu`) answers 401 to anonymous queries
(measured 2026-11-25), so the page does not use it yet; its type query
already reads that layout (graphs under `https://data.europa.eu/949/graph/eratv/`
except `notes/`, `derived/` and `links/`, and `era:hasVehicleTypeConfiguration`).
The data has gaps the page shows rather than fills: no type carries a type
name (`rdfs:label`, ERATV 1.1), no authorisation holder resolves to an
organisation, ERATV-KG mints a configuration IRI per parameter set (so two
different types are compared on configuration labels), and only 71 of the 456
coded values it uses have a label, in ERATV-KG or in the v4.0.0 SKOS. Tested
by [scripts/tests/eratv-explorer.test.js](scripts/tests/eratv-explorer.test.js)
(`npm install --no-save sparqljs@3.7.3 && node --test scripts/tests/eratv-explorer.test.js`),
against the live graph by `node scripts/tests/eratv-live-parity.js` (the 23
searches both ways, and the snapshot against live answers), and in a browser
by `python3 scripts/tests/eratv_viewer_check.py` (the type view's acceptance
checks, from the snapshot alone and live, in both colour schemes).

<a id="plc-extraction"></a>
**[era-plc-extraction.html](scripts/assets/era-plc-extraction.html)** —
Primary Locations in RINF (published as `/plc-extraction.html`; `/op-rcc.html`
redirects to it). Pick a country and get a CSV of every TAF/TAP primary location
(`era:PrimaryLocation`) that RINF publishes for it: code, name, infrastructure
manager, the four TAF/TAP flags, validity, position, NUTS 3, operating language,
the dataset it comes from and the operational points that point to it.
Optionally pick national lines to narrow the extract. No RCC parameters are
exported. The rules, as implemented:

- **What is exported.** Every resource typed `era:PrimaryLocation` in rinf-plus
  (52,331 on 2026-11-20, under 48,824 distinct codes). RINF links operational
  points to a primary location with `era:primaryLocation`, only in that
  direction (`era:isPrimaryLocationOf` is not used). Many managers publish only
  a stub (code, label, position), so the name, flag, manager and validity
  columns are filled for a minority of codes in most countries.
- **Which country.** A resource belongs to the country of its own
  `era:inCountry`. When it names none (4,282 resources, 783 codes: Croatia,
  Lithuania and a few others), the ISO-2 prefix of the code decides. "EU" codes
  without `era:inCountry` go to the country whose sections of line share their
  dataset graph. The `country_rule` column says which rule applied.
  `era:inCountry` and the prefix disagree for one resource: ES04313 carries both
  ESP and FRA, so it appears in the Spanish and the French extract. Danish codes
  are RINF's own, not RNE codes; do not join them to CRD.
- **One row per code.** The key is (country, `era:primaryLocationCode`), not the
  resource: 167 codes are minted as several resources, and Lithuania publishes
  3,700 resources for 201 codes. Resources of one code that pass the validity
  rule are merged; differing values are joined with ` | `, and
  `primary_location_iris` lists them all.
- **Validity: the window in force on the chosen date, per code.** Managers
  republish, and some publish ahead (DB InfraGO's operational points carry a
  2026 window and a from-2027 window), so "the newest window" would pick data
  that is not valid yet. Per code, the resources whose window contains the
  "Valid on" date are kept (the latest beginning wins). With none in force, the
  most recent window that has begun is used and `validity_status` reads
  `ended`. A code whose windows all lie in the future is left out and counted.
  Resources with no dated validity are always kept; most primary locations are
  undated (9,618 of 9,619 German ones). A bound published as
  `time:inXSDDateTimeStamp` (four small Austrian managers) is read like
  `time:inXSDDate`. Some datasets date every location with its publication date
  (all 582 Croatian ones begin 2026-10-16), so an earlier date returns none of
  them, and the page says so. The same rule picks the operational points listed
  in `linked_op_*`.
- **Narrowing by line.** Each line is resolved to its operational points, by a
  kilometric post on the line's own linear positioning system *or* as the start
  or end of one of its sections (Norway's posts sit on one nationwide system,
  and Croatia publishes no kilometric coordinates). The points valid on the date
  are kept once per `era:uopid`, and the primary locations they reference,
  restricted to the country's own, give the codes. The rows are then the same
  as the whole-country extract's for those codes, with `selected_lines` added.
  Lines are resolved one query each, six at a time. Lithuania links its
  locations from tracks and sidings rather than from points, so narrowing finds
  nothing there.
- **Shareable links** list the country, the date and every line as a repeated
  `l=` parameter (`#c=FRA&l=830000-1&d=2026-11-20&run=1`). Nothing picked means
  the whole country; a link whose lines do not resolve does not run.
- **Columns.** `country`, `primary_location_code`, `country_rule`, `in_country`,
  `name` (`era:primaryLocationName`, English first; when none is published, the
  `rdfs:label` with the code stripped out, unless only the code is left),
  `name_source`, `name_language`, `names_all` (every name as `text@lang`),
  `label` (every raw `rdfs:label`), `infrastructure_manager_code` (the
  organisation code of `era:infrastructureManager`),
  `infrastructure_manager_name` (from OCR-KG, joined on that code; RINF holds no
  names), `passenger_flag`, `freight_flag`, `container_handling_flag`,
  `handover_point_flag`, `validity_begin`, `validity_end`, `validity_status`,
  `position_wkt` (from `era:netReference/geo:hasGeometry/geo:asWKT`, else a
  direct `geo:hasGeometry`; a `POINT` from either source wins), `longitude`,
  `latitude`, `position_source`, `nuts3` (the code, e.g. `EL307`),
  `operating_language`, `not_yet_available` and `not_applicable` (the
  properties declared so with `era:notYetAvailable` / `era:notApplicable`),
  `dataset_graphs`, `linked_op_uopids` and `linked_op_names` (one per
  `era:uopid`), `linked_op_count`, `primary_location_iris`, `iri_count` and,
  with lines, `selected_lines`.
- **Empty values.** A value the graph does not carry reads `no data`, never an
  empty cell, as in the Eurostat export. Where the manager declares the property
  not yet available or not applicable, that cell reads `not yet available` or
  `not applicable` instead (names and NUTS 3). Dates are ISO 8601; an open end
  reads `no data`. Text that a spreadsheet could run as a formula gets a leading
  apostrophe; numbers stay numbers.

**[era-shacl-viewer.html](scripts/assets/era-shacl-viewer.html)** — shows
what a SHACL shapes graph asks of the data. Each node shape is a card listing
its property shapes (path in SPARQL property-path syntax, value type,
cardinality, severity), with connectors to the shapes its values must conform
to (`sh:node`, or `sh:class` when another shape targets that class, including
inside `sh:or` / `sh:xone` / `sh:and`) and from the shapes that point to it.
Click any shape to follow it. ERA's SHACL-SPARQL constraints are listed under
the property they name with `era:affectedProperty`, each with its full query.
Four ERA views:
- **PROD**: the production shapes, live (`graph/shacl` in `ERA-Onto`, one
  `CONSTRUCT`).
- **UAT**: the shapes in acceptance testing for the next release, from the
  published file `rinf.uat.data.test-era.europa.eu/era-vocabulary/era-shapes`.
- **Compare**: what UAT changes. Shapes and property shapes are marked new,
  changed or removed, and a changed row shows the statements removed and
  added, plus a line diff of each changed SHACL-SPARQL query. Queries are
  compared by body and message; differences only in their `PREFIX`
  declarations are ignored.
- **OWL gaps**: the UAT release candidate's shapes (`graph/shacl`) set against
  its ontology's OWL axioms (`graph/ontology`), both from the UAT SPARQL
  endpoint, with the latest release named from the GitLab API. 28 checks find
  where data the shapes accept is inconsistent with the axioms (functional
  super-properties, datatypes and classes outside a range, domains a shape
  contradicts, …), where the two name terms the other lacks, and what OWL 2
  reasoners reject in the axioms on their own. The report lists the immediate
  actions, most severe first (BLOCKER, MAJOR, MINOR, SUGGESTION), each with
  why it matters, the fix and every finding. It exports as Markdown and CSV,
  and the shapes below carry a badge where they have gaps. The analysis is a
  pure function of the two graphs, tested in
  [scripts/tests/shacl-viewer-gaps.test.js](scripts/tests/shacl-viewer-gaps.test.js)
  (`npm install --no-save n3@1.17.2 && node --test scripts/tests/shacl-viewer-gaps.test.js`).

You can also open, drop or paste any Turtle, N-Triples, N-Quads or TriG file;
it is parsed in the browser with N3.js (pinned, with SRI) and never uploaded.

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
  from ERADIS-KG and era-lex, with the queries in `eradis/` (about a minute,
  anonymous access to the development endpoint).
- `scripts/build-eurostat-queries.py` — generates the optimised Eurostat
  queries in `eurostat/` and the copies embedded in the Eurostat Exporter, so
  the two never drift apart.
- `scripts/build-era-answers-pptx.py` — regenerates
  `interop-europe/ERA-ontology-reusability.pptx` from the answers (needs
  `python-pptx`).
- `scripts/tests/` — `node --test` unit tests for the SHACL Shape Viewer's gap
  analysis and the ERATV Explorer's search, and `eratv-live-parity.js`, which
  runs 23 ERATV searches both in the page's matcher and as SPARQL against
  ERATV-KG and fails on any difference.
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
  (publisher variations, validity rules, query shapes), and where ERA's PROD and
  UAT SHACL shapes live and how they differ. It is kept for anyone, human or AI
  assistant, writing queries against the graph.
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
