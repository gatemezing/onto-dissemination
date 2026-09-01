# Route book elements (TSI OPE Appendix D2) — verified query set

The query set behind [`era-route-book.html`](../era-route-book.html)
(published as `/routebook.html`). All measurements against
`graph.data.era.europa.eu/repositories/rinf-plus` on 2026-08-22.

| File | What it does | Measured |
|---|---|---|
| `lines-for-country.rq` | national lines for one country, by `era:lineId` **or** LPS label | **0.2–2.3 s** |
| `d2-catalogue.rq` | the 46 D2 elements, and whether any manager publishes each at all | **0.15 s** |
| `infrastructure-manager.rq` | D2 1.1 — the manager each section of line declares | **0.11 s** |
| `infrastructure-manager-names.rq` | …and their names, from OCR-KG | **0.15 s** |
| `sections-for-line.rq` | phase 1: sections of line with position, latest window per stretch | **0.45 s**, 167 sections for DEU `4000` |
| `ops-for-line.rq` | phase 1: operational points, by kilometric post **or** section endpoint | **0.23 s**, 168 points for the same line |
| `section-endpoints.rq` | phase 2: each section's name and geometry, from its `era:opStart`/`era:opEnd` | **0.3 s** for 250 sections, DEU `4000` |
| `d2-elements-for-place.rq` | phase 2: the D2 elements on those places, one query per access path | **1.4 s** for all five line-side branches |

## Countries, lines and the network map are all multi-select

The page now ticks countries and picks lines the same way the RCC tool does —
lines are fetched once per country and cached, and every row in the result
carries the country and line it came from, so the D2 coverage view can
aggregate across the whole selection. The one piece the RCC tool didn't need:
the part-whole direction (`era:isPartOf` vs `era:hasPart`, see §4 below) is
probed **per line**, not once for the whole run, because two lines from
different countries can be in the same run and a shared global would silently
be wrong for whichever one didn't set it.

A network map (Leaflet, OpenStreetMap + OpenRailwayMap tiles, same approach as
the RCC tool's) draws every selected line's sections as chords between named
operational points, one colour per line, reusing the geometry already fetched
for the Section column rather than asking the endpoint again.

## What Appendix D2 is, and what the ontology gives you

`era:tsiOPEAppendixD2Index` is an `owl:AnnotationProperty` whose own definition
reads: *the index of a vocabulary term in Appendix D2 — Elements the
infrastructure manager has to provide to the railway undertaking for the Route
Book — from Commission Implementing Regulation (EU) 2019/773* (the TSI OPE).

**46 indices, 75 annotated resources, 2 of them retired.** The annotation is not
confined to properties: SHACL shapes and individual SKOS concepts carry it too,
because some D2 elements are expressed by a *particular value* rather than by a
property (`concepts/special-area-types/PowerSwitchOff` is D2 3.3.5).

The mapping to RINF is many-to-many in both directions. `organisationCode` is
D2 1.1 and carries seven different `era:rinfIndex` values; D2 3.2.3 is served by
ten different properties (tunnels, platforms, sidings, walkways, evacuation
points, fire category). Neither index can be derived from the other.

**ERA publishes the index but no heading per index.** There is no label,
`skos:prefLabel` or definition for "3.2.3" anywhere in the endpoint or the
vocabulary documentation. The tool therefore names each element by its ontology
labels and keeps the D2 number as the legal cross-reference, rather than putting
wording into the regulation's mouth.

## Where the D2 properties actually live

Every D2 index has a SHACL target class, and they are spread over eighteen
classes. Three of those classes have **zero instances** in the live endpoint:

| Class | Instances | D2 elements affected |
|---|---|---|
| `era:SpecialArea` | 0 | 3.2.4, 3.2.6, 3.3.5, 3.3.6 |
| `era:RadioBlockCenter` | 0 | 3.4.7 |
| `era:CommonCharacteristicsSubset` | 0 | none exclusively — its elements are also on `era:RunningTrack` |

So **5 of the 46 D2 elements cannot be filled by any manager today**, which is a
different fact from "this line does not publish them" and the coverage view
separates the two.

The rest are reachable from a section of line or an operational point by a
handful of paths:

| Path | D2 elements it yields |
|---|---|
| the section / point itself | 2.2.2, 2.3.1, 2.3.2, 3.1.1, 3.1.2, 3.2.3, 3.5.1 |
| `era:isPartOf` / `era:hasPart` → track | 2.2.1, 2.2.1.1, 2.2.1.4, 3.1.3, 3.1.4, 3.1.7, 3.2.1, 3.2.2, 3.4.* |
| track → `era:hasPart` → tunnel / platform / signal | 2.2.3, 2.3.3, 2.3.5–2.3.8, 3.2.3 |
| track → `era:contactLineSystem` | 3.3.1, 3.3.2, 3.3.7, 3.3.8 |
| track → `era:etcs` | 3.2.7, 3.4.11 |
| point → `era:netReference/geo:hasGeometry` | 2.1.1, 2.1.2, 2.2.2, 3.2.5 |
| point → `era:primaryLocation` | 2.2.2 |

## Two phases, because one UNION is 21× slower

The obvious query is one `SELECT` with a `UNION` per access path. It works and
it is slow: **64 s** for DEU line 4000. Splitting the branches into separate
queries helps less than it looks — **30 s** wall clock — because every branch
then re-resolves the sections of the line and recomputes the validity aggregate.

Resolving the places **once** and pinning them into each branch with `VALUES`
takes the same work down to **0.45 s + 1.4 s**. Measured on the same line:

| Approach | Wall clock | Rows |
|---|---|---|
| single query, UNION of 5 branches | 64 s | 5,195 |
| 5 separate branch queries | 30 s | 5,193 |
| phase 1 + 5 pinned branch queries | **1.9 s** | 5,193 |

The tool chunks the `VALUES` list at 250 URIs and runs at most six requests in
flight, so a French line of 570 sections and 327 points stays within one round
of the pool.

## D2 1.1 takes two registers, and the same URI opens both

Every section of line declares its manager. `era:infrastructureManager` points
at an `era:OrganisationRole` such as `.../organisationRole/0080_IM`, and
`era:roleOf` resolves that to the organisation — 1,111,592 statements
graph-wide, and 334 of 334 sections on DEU line `4000`.

**An earlier version of this tool answered it from the named graph instead**,
on the reasoning that each graph is one manager's RINF submission, so the
manager must be the `era:Body` holding the IM role inside it. That looks
equivalent and is not: both German bodies sit in both German graphs, so the
graph route named DB InfraGO **and** Deutsche Bahn AG for line 4000, where the
declared property names DB InfraGO alone. The graph is still worth reporting as
the separate fact it is — line `4000` really is published in two datasets — but
it is not the answer to "who is the infrastructure manager".

That answers *which* organisation but not *who*: *all 660 `era:Body` resources
in `rinf-plus` carry zero `foaf:name`.* The names live in the **Organisation
Codes Register**, and are fetched with the very same body URIs RINF returned:

| Register | What it knows about `body/organisation/0080` |
|---|---|
| `rinf-plus` | it is the declared infrastructure manager of every section of line `4000` |
| `OCR-KG` | it is **DB InfraGO Aktiengesellschaft**, short name DB InfraGO, in DEU, holding roles RU, IM, ECM, Keeper, Owner, CB |

No code column, no join key, no matching by hand — the identifier *is* the join.
This is the clearest demonstration in the repository of why one persistent URI
reused across registers beats a shared numeric code.

Resolved end to end: `0071` → Administrador de Infraestructuras Ferroviarias
(ADIF), `0080` → DB InfraGO, `0084` → ProRail, `0087` → SNCF Réseau, `1080` →
Deutsche Bahn AG.

## Five modelling variations, all of them absorbed

Every infrastructure manager publishes national lines. Not all publish them the
same way, and a query written against one style returns *nothing at all* for
the others — silently, which is the dangerous part. An earlier version of this
tool asked only for `era:lineId` and reported Croatia and Norway as having no
data. They have plenty; the query was too narrow.

### 1. Line identity — `era:lineId` or the LPS label

| | LPS resources | with `era:lineId` |
|---|---|---|
| all countries | 9,642 | 9,543 |
| HRV | 55 | **0** |
| NOR | 32 | **0** |

Croatia and Norway put the identifier in the English `rdfs:label` of the
`era:LinearPositioningSystem` instead — `NationalRailwayLine_M604`,
`B03-Kongsvingerbanen`. The line list takes `era:lineId` where it exists and the
label where it does not, and records which in `?src`, which the page surfaces.

Two traps here. The labels are **language-tagged** (`en`, plus `hr` for Croatia
and `no` for Norway), so matching one as a plain literal never matches. And a
line identifier is unique only *within* a Member State, so every downstream
query pins the **LPS URIs** returned by this query with `VALUES` rather than
matching the identifier string again.

### 2. Reaching operational points — kilometric post or section endpoint

Croatia's 582 operational points carry `era:uopid` and a net reference, but
nothing tying them to an LRS and no `era:inCountry` either. Its sections of line
*do* name them, with `era:opStart` and `era:opEnd`.

Querying both routes is not a Croatia workaround — it improves complete networks
too, because points at section boundaries are not all carried by a kilometric
post on that line's LRS:

| Line | via kilometric post | via section endpoint | total |
|---|---|---|---|
| DEU `4000` | 308 resources → 168 uopids | 4 | 168 |
| FRA `830000-1` | 327 | 276 | **603** |
| HRV `NationalRailwayLine_L101` | 0 | 7 | 7 |

The second branch excludes points the first already found, so nothing doubles.
`era:inCountry` is deliberately not required: pinning the LPS resources already
confines the query to the chosen country's network, and requiring it would drop
Croatia entirely.

### 3. Linear referencing, or none at all

Croatia's `era:NetPointReference` resources carry a geometry and **no**
`era:hasLrsCoordinate`, so its sections have no kilometre position whatsoever.
Position is therefore `OPTIONAL` throughout: unpositioned places are reported
with `—` and sorted after the positioned ones, rather than excluded. Setting a
kilometre range necessarily limits the result to places that have one.

### 4. The part-whole direction

A place and its tracks are joined by `era:isPartOf` in every dataset except
Croatia's, which publishes only `era:hasPart` — 645 tracks that a query written
against the inverse alone never sees:

| Dataset | tracks via `era:isPartOf` | via `era:hasPart` |
|---|---|---|
| HRV `graph/0078` | **0** | 645 |
| NOR `graph/0076` | 607 | 607 |
| DEU `graph/0080` | 36,777 | 36,777 |
| FRA `graph/0087` | 25,133 | 25,133 |
| ESP `graph/0071` | 3,530 | 3,530 |

Asking for both is correct and ruinous. In isolation a `UNION` of the two costs
nothing (1.1 s against 0.6 s), but in the real query — with the parameter join,
the label resolution and the `GROUP_CONCAT` — it takes a German line from
**1.4 s to 57 s**, and puts the operational-point side over the endpoint's
120 s limit. An alternation path (`era:hasPart|^era:isPartOf`) behaves the same.
The optimiser can no longer push the property join once the subject can arrive
from two directions.

So the direction is **probed once per run** with a one-row query and a single
form is emitted. Cost: one round trip of about 0.1 s.

### 5. Organisation URIs are not as shared as advertised

Names are joined to OCR-KG on `era:organisationCode`, not on the body URI:

| Country | URI in RINF | In the register |
|---|---|---|
| 25 of 27 | `body/organisation/0087` | same URI ✓ |
| HRV | `body/organisation/0078` **and** `…/0078_ORG` | only the first |
| NOR | `…/organisations/0076` | `body/organisation/0076` |

The URI join works for 25 of the 27 and is the better join where it holds. The
code closes the other two and collapses Croatia's duplicate into one row —
Croatia's manager resolves to *Hz Infrastruktura d.o.o.*, Norway's to *Bane NOR*.

### What this costs

Nothing measurable, and none of it is guesswork about what a manager meant:
each branch queries a property the ontology defines, and the page reports which
branch produced what. Coverage after the change:

| Line | D2 elements | Rows | Time |
|---|---|---|---|
| HRV `NationalRailwayLine_L101` | 17 / 46 | 175 | 0.5 s |
| NOR `B01-Østfoldbanen Vestre` | 22 / 46 | 1,540 | 2.3 s |
| ESP `ESL010110000` | 27 / 46 | 1,551 | 0.6 s |
| FRA `830000-1` | 27 / 46 | 40,996 | 4.3 s |
| DEU `4000` | 29 / 46 | 13,795 | 6.0 s |

## Validity

Identical to the RCC tool, and for the same reasons: the newest window **per
stretch of line** (never line-wide — France dates each section by the day it
opened), and at operational points the newest resource per `era:uopid` and then
the newest track window within the point. Ten countries publish no dated
validity at all, so a resource with no validity is always kept.

## Coverage measured end to end

| Line | D2 elements on the line | Rows | Time |
|---|---|---|---|
| ESP `ESL740874000` | 25 / 46 | 2,162 | 0.7 s |
| FRA `830000-1` (km 0–40) | 27 / 46 | 8,993 | 2.2 s |
| DEU `4000` | 29 / 46 | 13,795 | 5.5 s |

In every case the same 5 elements are unreachable by anybody, and the remainder
of the gap is what that manager has chosen not to publish.
