---
name: era-graph
description: Query the ERA (European Union Agency for Railways) knowledge graph correctly and fast — RINF infrastructure data and the Organisation Codes Register. Use when writing SPARQL against graph.data.era.europa.eu, building on the ERA ontology, or working on the era-*.html tools in this repo. Covers the publisher modelling differences that silently return zero rows, the validity rules that silently return duplicates, and the query shapes that turn a timeout into a second.
---

# Querying the ERA knowledge graph

Everything here was measured against the live endpoint, not inferred from the
ontology. The ontology says what *may* be published; the data says what *is*.

## Endpoints

| Repository | Holds |
|---|---|
| `https://graph.data.era.europa.eu/repositories/rinf-plus` | RINF: lines, sections, operational points, tracks. The default. |
| `.../repositories/OCR-KG` | Organisation Codes Register: organisation **names**, roles, sites |
| `.../repositories/era-lex` | legal acts, ELI references |
| `.../repositories/ERA-Onto` | the ontology alone |

Data is in **named graphs, one per infrastructure manager** (`graph/0080` = DB
InfraGO). 54 datasets, 27 countries. A line can appear in two graphs.

## Rule 1 — exclude deprecated properties, always

```sparql
FILTER NOT EXISTS { ?p owl:deprecated true }
```

37 of 331 RINF-indexed properties are retired, and 9 countries still publish
17 of them. Most have `dcterms:isReplacedBy` a live property under the same
index, so excluding them loses nothing — but *including* them double-counts.

## Rule 2 — five ways publishers differ

A query written against one publication style returns **nothing at all** for the
others, with no error. Check each before concluding "no data".E

| # | Variation | Majority | Exception |
|---|---|---|---|
| 1 | Line identity | `era:lineId` on the LPS (9,543 / 9,642) | HRV (55), NOR (32): identifier only in the English `rdfs:label` |
| 2 | Reaching operational points | `era:kmPost/era:hasLRS` on the line's LRS | HRV: none — but sections name them via `era:opStart`/`era:opEnd` |
| 3 | Linear referencing | `era:hasLrsCoordinate` present | HRV: net point references carry geometry only, **no position at all** |
| 4 | Part–whole link | both `era:isPartOf` and `era:hasPart` | HRV: only `era:hasPart` (645 tracks otherwise invisible) |
| 5 | Organisation URIs | `body/organisation/0087` | HRV also mints `…/0078_ORG`; NOR uses `…/organisations/0076` |

Consequences:

- **Key on the `era:LinearPositioningSystem` resource, not the line string.** A
  line identifier is unique only *within* a Member State. Resolve LPS URIs once,
  pin them with `VALUES` everywhere after.
- **LPS labels are language-tagged** (`en`, plus `hr`/`no`). Matching one as a
  plain literal never matches, and fails silently.
- **Query point reachability both ways.** Not just for Croatia: France's line
  `830000-1` goes from 327 to **603** points once section endpoints are included.
- **Make position `OPTIONAL`.** Report unpositioned places with `—` and sort them
  last rather than dropping them.
- **Join organisation names on `era:organisationCode`**, not the body URI. RINF
  has no names at all — all 660 `era:Body` there carry zero `foaf:name`.

## Rule 3 — validity: newest window **per place**, never per line

Managers republish. Without a filter you mix current and superseded descriptions.
With the *wrong* filter you delete real data.

```sparql
OPTIONAL { ?x era:validity/time:hasBeginning/time:inXSDDate ?b }
OPTIONAL { { SELECT ?key (MAX(?bb) AS ?latest) WHERE { … } GROUP BY ?key } }
FILTER(!BOUND(?b) || !BOUND(?latest) || ?b = ?latest)
```

| Side | `?key` | Why |
|---|---|---|
| sections of line | the stretch — `(startPosition, endPosition)` | DEU republishes a stretch yearly (16,615 → 8,281 rows) |
| operational points | `era:uopid`, **then** track window per point | DEU repeats the station; FRA repeats tracks inside one point |

**A line-wide `MAX` is the trap.** It is right for Germany and catastrophic for
France, which dates each section by the day it *opened* — 25 beginnings across
702 sections, so a line-wide maximum keeps **2** and reports a tidy "132 rows"
that looks like successful deduplication and is 99.6 % data loss.

Always keep resources with no validity (`!BOUND(?b)`): **ten countries publish no
dated validity at all** — SWE, ESP, IRL, EST, GRC, FIN, ROU, HRV, AUT, LUX.

## Rule 4 — the two-phase shape

One query asking for *places + properties + validity* exceeds the endpoint's
**120 s limit** (HTTP 503). Split it:

1. **Phase 1** — resolve the places (sections, points) with their positions and
   validity rule. Small, fast, no property joins.
2. **Phase 2** — pin those URIs with `VALUES` and fetch the properties. Chunk at
   ~250 URIs, run ≤ 6 in flight.

Measured, identical results:

| | Before | After |
|---|---|---|
| DEU `4000` RCC | 33 s | **3.6 s** |
| FRA `830000-1` RCC | 21 s | **6.6 s** |
| DEU `4000` route book (5 branches) | 64 s union / 30 s split | **1.9 s** |
| DEU `4000` operational points | HTTP 503 | seconds |

## Rule 5 — performance gotchas that cost real time

- **Bind the predicate set first.** Put the property lookup in a subquery so
  `?parameter` is bound before data is touched; an unbound-predicate scan is the
  usual cause of a slow query.
- **Never ask for both part–whole directions in a hot query.** In isolation a
  `UNION` is free (1.1 s vs 0.6 s); with the property join, label resolution and
  `GROUP_CONCAT` it goes **1.4 s → 57 s**. An alternation path
  (`era:hasPart|^era:isPartOf`) is the same. Probe the direction once with a
  `LIMIT 1` query, then emit one form.
- **Resolve labels in a separate `VALUES`-bounded query.** Inline
  `OPTIONAL { ?v skos:prefLabel ?l }` cost 12.1 s vs 2.6 s without; the separate
  lookup over the distinct URIs took 0.07 s.
- **`ORDER BY` on a variable that survives neither `SELECT` nor `GROUP BY` is
  silently ignored.** Group and project your sort keys.
- **`?p era:rinfIndex ?i . ?s ?p ?o` multiplies** by the number of indices a
  property has. Use a `SELECT DISTINCT ?p` subquery when counting statements.
- Parallel single-property queries beat one batched `VALUES ?prop` query — 1.1 s
  vs 12.1 s for five parameters across 27 countries.

## Legal index annotations

Properties carry their position in the legislation. These are **independent
axes** — many-to-many in both directions, neither derivable from the other.

| Annotation | Meaning | Live count |
|---|---|---|
| `era:rinfIndex` | RINF parameter number | 294 properties |
| `era:tsiOPEAppendixD2Index` | TSI OPE Appendix D2 — the **Route Book** | 46 indices |
| `era:eratvIndex` | ERATV | 174 |
| `era:usedInRCCCalculations` | route compatibility check | 87 (4 retired) |

ERA publishes the D2 *index* but **no heading per index** — there is no label for
"3.2.3" anywhere. Name elements by their ontology labels and keep the number as
the legal cross-reference; do not invent regulation wording.

Five D2 elements can be filled by nobody today: `3.2.4`, `3.2.6`, `3.3.5`,
`3.3.6` (carried only by `era:SpecialArea`) and `3.4.7` (`era:RadioBlockCenter`)
— neither class has a single instance. That is a different fact from "this line
does not publish it", and worth reporting separately.

## Working style that paid off

- **Measure before claiming.** Several confident conclusions here were wrong —
  "nothing on a line points at an `era:Body`" (`era:infrastructureManager` is on
  every section), "Croatia publishes no line identifiers" (it does, as a label).
  Each was caught by running a query rather than reasoning further.
- **A count that looks like a clean deduplication deserves suspicion.** 67,281 →
  132 rows looked like a 510× win and was data loss.
- **Report the gap rather than papering over it.** `NationalRailwayLine_M604`
  plainly contains `M604`, but a label is not an identifier and the pattern
  differs per country. Query the property the ontology defines; when it is
  absent, say so in the UI.

## The tools in this repo

Single-file HTML, no build step, deployed by `.github/workflows/pages.yml` to
<https://gatemezing.github.io/onto-dissemination/>. All query the endpoint live
from the browser and share a dependency-free XLSX writer.

| File | Page | Does |
|---|---|---|
| `era-graph-explorer-app.html` | `/` | bubble-graph "follow your nose" demo |
| `era-rdf-exporter.html` | `/exporter.html` | export any resource URI as RDF/XML |
| `era-rinf-value-explorer.html` | `/values.html` | distinct values per RINF parameter, per country |
| `era-rcc-parameters.html` | `/rcc.html` | route-compatibility parameters along one line |
| `era-route-book.html` | `/routebook.html` | TSI OPE Appendix D2 elements + coverage |

Verified query sets with measurements live in `scripts/assets/rcc/` and
`scripts/assets/routebook/`. `scripts/build-rinf-parameter-catalog.py` refreshes
the catalogue embedded in the value explorer nightly.
