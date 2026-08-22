# onto-dissemination

This repository collects materials and demo assets used to disseminate the ERA ontology (ERA vocabulary) and demonstrate "follow your nose" Linked Data navigation for railway infrastructure data.

Contents
- `scripts/innotrans2026-era-ontology-script.md`: booth/demo script, elevator pitch, demo queries, and checklist for InnoTrans 2026.
- `scripts/assets/era-follow-your-nose-scene.html`: demo scene / explainer mockup (video/animation source).
- `scripts/assets/era-graph-explorer-app.html`: interactive offline demo app (single-file HTML) for the bubble-graph explorer.
- `scripts/assets/era-rdf-exporter.html`: single-file tool to export any ERA/RINF resource URI as RDF/XML, recursed to real leaf values — see the dedicated section below.
- `scripts/assets/era-rinf-value-explorer.html`: single-file tool that lists every distinct value reported for any RINF parameter, per country or across all of RINF, and downloads it as CSV or Excel — see the dedicated section below.
- `scripts/build-rinf-parameter-catalog.py`: regenerates the parameter/country snapshot embedded in that tool; run nightly by [.github/workflows/refresh-rinf-catalog.yml](.github/workflows/refresh-rinf-catalog.yml).
- `scripts/assets/era-interop-answers.html`: the ERA reusability answers for the Interoperable Europe assessment, as a standalone page (source text in `interop-europe/answers.md`).
- `interop-europe/`: the assessment questions, the drafted answers, and the extracted Data Stories query catalogue.
- `sample-data/`: example SPARQL query + RDF/XML result pairs, with the engineering rationale behind them documented in `sample-data/README.md`.

Live demo
- **https://gatemezing.github.io/onto-dissemination/** — the GitHub Pages deployment of `era-graph-explorer-app.html`, rebuilt automatically by [.github/workflows/pages.yml](.github/workflows/pages.yml) on every push to `main` that touches the app file.
- **https://gatemezing.github.io/onto-dissemination/exporter.html** — the RDF Exporter.
- **https://gatemezing.github.io/onto-dissemination/values.html** — the RINF Parameter Values explorer.
- **https://gatemezing.github.io/onto-dissemination/interopable-eu-portal-answers.html** — the Interoperable Europe reusability answers.

The three tools cross-link: the landing page carries a tools nav in its top bar, and each tool links back. The answers page links to all three.

Quick start
- To view the offline interactive demo, open [scripts/assets/era-graph-explorer-app.html](scripts/assets/era-graph-explorer-app.html) in a modern browser. For best results run a local HTTP server from the repository root and open the file URL in your browser:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/scripts/assets/era-graph-explorer-app.html
```

- The `era-follow-your-nose-scene.html` file is a stylised demo/scene used to create a short explainer video. Open it the same way or use the `era-graph-explorer-app.html` for interactive navigation.

What this repo is for
- Provide a rehearsable booth script and demo assets to explain the ERA ontology (see `scripts/innotrans2026-era-ontology-script.md`).
- Ship an offline, clickable graph demo so the booth can run without relying on external network or CORS — plus an experimental live SPARQL mode for visitors who want to query the real graph.

Notes & checklist
- **Offline demo rebuilt around Oslo S (2026-08-16):** the curated offline dataset now centres on `https://data.banenor.no/data/_station_c0576848-8f76-4489-aa6e-ae95b98c1a1c` (Oslo Central Station, published by Bane NOR using the ERA ontology), replacing the original Brussels Airport walkthrough. Every node/edge was fetched live over HTTP during this session — Bane NOR's own Linked Data server plus the ERA SPARQL endpoint for shared `era:` URIs — not screenshots or invented data. See Section 6 of `scripts/innotrans2026-era-ontology-script.md` for the full worked example and reuse-hub findings.
- **Live SPARQL mode fixed and verified (2026-08-16):** the app's "Try live ERA SPARQL" data source points at `https://graph.data.era.europa.eu/repositories/rinf-plus`, the GraphDB repository behind ERA's own graph browser. Confirmed reachable with a real browser-shaped request (GET, with an `Origin` header) — it returns correct data and sends back an `Access-Control-Allow-Origin` header that allows cross-origin `fetch()`, so it works from the GitHub Pages deployment. The previously-configured endpoint (`rinf.data.era.europa.eu/api/v1/sparql/rinf`) does not work from a browser: GET requests to it hang with no response, and its CORS policy only allows its own app's origin. **Correction (2026-08-17):** this endpoint does mirror non-ERA data too — pasting a Bane NOR URI directly into live mode works and returns real matching data, though only the subset of properties that map onto the shared ERA vocabulary (Bane NOR's native railML3/`bno:` extension properties aren't mirrored here).
- Live mode explicitly pulls from two ERA named graphs for any `http://data.europa.eu/949/` URI: the ontology graph (class definitions, comments, subclass hierarchy) and the SKOS graph (the ~14,700-concept controlled vocabulary — station types, organisation roles, track directions, etc.). The offline dataset's own class and SKOS-concept nodes carry the same real, fetched data.
- **Fixed 2026-08-17:** two curated offline nodes (`primaryLocationNO00100`, `trackOB2`) were missing real edges present in the source data (`era:netReference` entirely missing from the primary-location node; `validity`, `netReference`, and the "Not applicable"/"not yet available" honesty-gap fields missing from the track), caught by comparing them directly against `graph.data.era.europa.eu`'s own view of those exact URIs.
- **Added 2026-08-17:** dereferenced the `era:netReference` targets that were previously inert leaves, following the real chain era:NetLinearReference → era:NetPointReference → era:TopologicalCoordinate → era:LinearElement (plus era:NetAreaReference and era:NetPointReference as area/point siblings) — all real data fetched live from `graph.data.era.europa.eu`, genuinely connected to Track ØB2's own linear location, with the LinearElement reusing the same 2019 validity record as its parent track. Followed up by dereferencing the remaining leaves: both `era:hasLrsCoordinate` targets, the `endsAt` NetPointReference, and the `validityInterval2019` era:TemporalFeature instance itself (a bigger reuse hub than the 2023 one — 21,860 real incoming links).
- The "Known demo nodes" panel can overlap the graph on some viewport sizes — it's now collapsible (state persists across reloads) via a Hide/Show toggle.
- **Fixed 2026-08-17:** the bubble graph itself now scales to fit the available screen space (recalculated on window resize), instead of being silently clipped by `overflow:hidden` on narrow viewports — verified on a 375px-wide mobile viewport with zero bubbles left out of bounds. Also dereferenced the remaining leaves: `era:hasSequence` (a real single-element RDF List reusing the LinearElement node), both `era:kmPost` targets, and the `era:ContactLineSystem` instance (another large reuse hub — 2,873 real tracks share it).
- Bubbles now size themselves to their label content and connecting edges trim to the visible gap between bubbles instead of running underneath them; the breadcrumb tags live-fetched nodes and never mixes a live trail with an offline one.
- Verify remaining live queries (Section 5 of the script) and legal/version wording before publishing or printing — see the checklist inside `scripts/innotrans2026-era-ontology-script.md`.

## RDF Exporter tool

`scripts/assets/era-rdf-exporter.html` — a small standalone UI wrapping the
recursive-to-leaves export queries developed in `sample-data/`. Paste any
ERA/RINF resource URI, pick an export mode (or leave it on the recommended
"Smart" auto-detect), and download the result as RDF/XML directly from the
browser — no server involved, queries `graph.data.era.europa.eu` directly
(confirmed open CORS).

- **Smart mode** detects `/track/` URIs and switches to track-centric
  export automatically; everything else gets the full recursive export.
  Both modes can be selected manually to override the detection.
- **Generalizes beyond the two originally-built examples** — verified
  against a `primaryLocation` URI (a resource type with no dedicated query
  ever written for it) and a second, different operational point, both via
  the same generic query builder.
- Tested (Playwright, before committing): output triple/description counts
  match the hand-verified `sample-data/*.rdf` files exactly; mode override
  produces a real, verified difference (44 distinct track URIs pulled in
  when forcing full-recursive on a track URI, vs. 2 in track-centric mode);
  invalid/malformed/injection-shaped input is rejected before any network
  call; a well-formed but nonexistent URI fails gracefully with a clear
  message instead of a blank "success"; download produces valid, correctly-
  named RDF/XML; no horizontal overflow at a 375px mobile viewport.

## RINF Parameter Values explorer

`scripts/assets/era-rinf-value-explorer.html` — pick any set of RINF
parameters (ERA properties carrying an `era:rinfIndex`, up to 15 at a time),
pick any set of countries, and get every distinct value actually reported,
with how many resources carry each.
Downloads as CSV or as a real `.xlsx` workbook, optionally with a **full-data
sheet**: one row per location, carrying country, start operational point, end
operational point and the value. Single file, no build step, no server: it
queries `graph.data.era.europa.eu` straight from the browser.

Why a railway expert would reach for it: the distinct-value list for a
parameter is what exposes national practice and data-quality drift. Running
`opType` across all countries, for instance, shows Croatia publishing
`concepts/op-types/OperationalPointTypes/70` where every other country
publishes `concepts/op-types/70` — a different concept scheme for the same
RINF parameter, with typos in the labels ("Tehnical change", "Shuting yard")
to match.

**Several parameters at once.** Each parameter is queried separately rather
than batched into one `VALUES ?prop` query, which is the faster arrangement by
a wide margin — five parameters over all 27 countries took 12.1 s batched
against 1.1 s as separate parallel queries. Results and exports gain a
Parameter column, rows never interleave between parameters, and a share
percentage is always computed against its own parameter's total rather than a
meaningless mixed denominator. Queries run through a pool capped at six in
flight, since a 15-parameter run is around 45 of them.

**Labels are their own query.** Profiling the batched form showed the cost was
not the parameters at all but the inline label join: 12.1 s with
`OPTIONAL { ?value skos:prefLabel ?l }` against 2.6 s without it. Labels
resolve over a small fixed set of SKOS concepts, so they are now fetched in one
`VALUES`-bounded query over the distinct URI values that came back — 0.07 s for
the 51 concepts behind those five parameters. That change made the
single-parameter path faster too.

**The full-data sheet, and how it stays fast.** Reaching a start/end
operational point depends on what the parameter hangs off, and the naive
generic form is what kills the endpoint: walking back through an *unbound*
predicate (`?parent ?anyPred ?res`) was killed server-side at 120 s. So
`build-rinf-parameter-catalog.py` resolves the path once, offline, and stores
it per parameter — `self` for a section of line, `part` for a track, or
`via:<predicate>` for a value on a shared sub-object. The app then emits only
that one bound-predicate shape, and every case returns in about two seconds
across all 27 countries. 216 of the 227 populated parameters have such a path;
the remaining 11 have the option greyed out rather than silently returning
nothing.

A single reverse step covers two situations at once: a running track hangs off
a section of line (giving start and end OP), a station track hangs off an
operational point (which is named instead). Where the value sits on a shared
sub-object — a contact line system reused across thousands of tracks — the row
reports the *track*, since the sub-object has no location of its own.

The row budget is split evenly across the countries selected, which is not a
cosmetic choice: a single `LIMIT` over the whole scope returned a DEU+FRA+ITA
export **containing no Italian rows at all**, because the endpoint filled the
cap before reaching them. Anyone comparing countries would have read that as
"Italy reports nothing". Each country now gets its own slice, and the app names
which countries filled theirs.

**What "country" means here — and why.** RINF is published as national
datasets, one named graph per infrastructure manager, so a country's scope is
the union of its IMs' graphs (27 countries over 54 datasets, from 1 for
Belgium to 9 for Italy). The obvious alternative — filtering on the
per-resource `era:inCountry` property — is *wrong* for a large share of
parameters, because many of them sit on sub-objects that carry no country of
their own: `era:maximumPermittedSpeed` for Austria returns **zero** values by
`era:inCountry`, against the real 43 by dataset. It is also far slower (a
dataset-scoped query on the largest parameter runs in ~2 s; the `inCountry`
join with a fallback took 40 s, and an unbounded reverse-edge variant timed
out server-side at 120 s).

Honest limits, all stated in the app and on the Excel *About* sheet:

- Austria's dataset `0081` is 99.76 % Austrian — 13 of 5,402 country-tagged
  resources are Liechtenstein, Swiss or German border objects.
- Liechtenstein and the United Kingdom appear in the data but publish no
  dataset of their own, so they get no country entry.
- Two operational points are genuinely registered by two countries at once
  (the Sweden–Finland border at Tornio, and the France–Italy border at
  Menton/Ventimiglia). The per-country columns credit each register, so they
  can sum to more than the de-duplicated total; the app says so on screen
  whenever that happens rather than quietly reconciling it.

Design notes for the booth: parameter search matches RINF index, property
name, label text or full URI; the 104 parameters that RINF defines but nobody
populates are hidden by default and one tick away; parameters that are really
identifiers rather than code lists (`gradientProfile` has 482,326 distinct
values) are flagged, capped, and have the per-country matrix disabled; every
result carries the exact SPARQL that produced it, and "Copy shareable link"
reproduces a query for a colleague.

Tested before committing — 177 Playwright checks, 26 that re-verify the app's
aggregate numbers against independent SPARQL, and 13 that re-verify individual
full-data rows the same way (every start/end OP checked against the endpoint
per row, and a small scope confirmed complete at 98 rows = 98 resources):

- Counts match direct SPARQL for 11 parameter/country pairs across 10
  countries, including the empty case (Poland reports no GSM-R coverage).
- Per-country counts sum exactly to the RINF-wide statement count for every
  parameter checked, so the country partition is complete and non-overlapping;
  single-country runs return values identical to the all-countries matrix.
- Six bugs were caught this way and fixed: the matrix grouped by dataset
  rather than country, double-counting the ~7,400 German stations that appear
  in both `0080` and `1080`; values were rendered by local name only, so
  Croatia's `.../OperationalPointTypes/70` and everyone else's `.../70` both
  showed as "70"; the capped full-data export dropped whole countries (above);
  a breakdown box auto-disabled for a single country stayed unticked after
  more countries were selected, silently omitting the matrix; an open
  suggestion list covered the parameter chips below it, so clicking a chip's
  remove button selected a parameter instead of removing one; and the
  full-data sheet kept its single-parameter header in multi-parameter runs.
- Downloads verified as artefacts, not just as clicks: the CSV parsed for BOM,
  CRLF, RFC 4180 quoting and non-ASCII round-trip; the `.xlsx` opened with
  openpyxl and checked sheet by sheet (numeric cells really numeric, frozen
  bold header, autofilter, the matrix's Total column equal to its row sum, and
  the full query on the About sheet).
- Malformed and injection-shaped property URIs are refused before any request
  is built; a 500 and a dropped connection both surface a readable message and
  leave the app usable; no horizontal overflow at 375 px, 768 px or 1440 px.

### Keeping the snapshot fresh

`python3 scripts/build-rinf-parameter-catalog.py` re-derives the whole block
from the live endpoint in about 80 s and rewrites it in place. Verified
reproducible: re-running it against an unchanged endpoint reproduces the
committed file byte for byte.

[.github/workflows/refresh-rinf-catalog.yml](.github/workflows/refresh-rinf-catalog.yml)
runs it nightly at **19:00 UTC — 21:00 Europe/Paris while CEST is in force**.
GitHub cron has no timezone field, so from the October changeover it lands at
20:00 Paris until spring; add a second `0 20 * * *` line if that hour matters,
since the job is idempotent and an extra firing costs nothing. Scheduled runs
are also queued best-effort and can start a few minutes late.

The job **only commits when the parameter list or the country/dataset map
actually changed** — the snapshot date moves every night by construction, and
committing that alone would mean a commit and a Pages redeploy every day for
no real change. Quiet nights still leave a "checked — no change" note in the
run summary, so there is an audit trail without repo noise. When there is a
real change it commits, then explicitly triggers `pages.yml`, because a push
made with `GITHUB_TOKEN` deliberately does not trigger other workflows and the
deploy would otherwise never see the commit.

Because it runs unattended, the script refuses to write a bad snapshot rather
than failing quietly — the failure mode that matters here is a half-answered
endpoint silently marking most parameters "no data". All three guards were
tested by injecting the fault:

- **Non-200 responses.** `curl` exits 0 for an HTTP 500 that carries a body, so
  the status code is checked explicitly (verified: a bad repository name is
  refused with `HTTP 401`, not parsed as an empty result).
- **Right status, wrong shape.** Every query declares the columns it must get
  back and fails if they are missing.
- **Material shrink.** A drop of more than 20 % in properties, populated
  properties or countries aborts *before* writing (verified: a crippled run
  returning a tenth of the parameters was refused with "properties fell from
  331 to 33", and the committed file was left untouched). Pass
  `--allow-shrink`, or tick the box on a manual run, when the drop is real.

Failures retry twice with a two-minute pause before giving up, since the
endpoint occasionally times out a batch under load.

## Links
- Oslo OP: https://data.banenor.no/data/_station_c0576848-8f76-4489-aa6e-ae95b98c1a1c
- Paris Nord: http://data.europa.eu/949/operationalPoint/e09280af18
- http://data.europa.eu/949/tentCorridor/ada4f64a55 (track in France with TenT information)
-  https://gatemezing.github.io/onto-dissemination/
- https://graph.data.era.europa.eu/graphs-visualizations?uri=https:%2F%2Fdata.banenor.no%2Fdata%2F_station_c0576848-8f76-4489-aa6e-ae95b98c1a1c&role=subject