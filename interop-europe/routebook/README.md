# Route book elements (TSI OPE Appendix D2) — verified query set

The query set behind [`era-route-book.html`](../../scripts/assets/era-route-book.html)
(published as `/routebook.html`). All measurements against
`graph.data.era.europa.eu/repositories/rinf-plus` on 2026-08-22.

| File | What it does | Measured |
|---|---|---|
| `d2-catalogue.rq` | the 46 D2 elements, and whether any manager publishes each at all | **0.15 s** |
| `infrastructure-manager.rq` | D2 1.1 — which manager publishes this line | **0.12 s** |
| `sections-for-line.rq` | phase 1: sections of line with position, latest window per stretch | **0.45 s**, 167 sections for DEU `4000` |
| `ops-for-line.rq` | phase 1: operational points with position, latest resource per `uopid` | **0.23 s**, 168 points for the same line |
| `d2-elements-for-place.rq` | phase 2: the D2 elements on those places, one query per access path | **1.4 s** for all five line-side branches |

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

## D2 1.1 has no path from a line, and that is not a bug

Nothing on a `SectionOfLine` or an `OperationalPoint` points at an `era:Body`,
so the manager cannot be reached by traversal. It is recoverable a different
way: each named graph **is** one manager's RINF submission, so the manager is
the `era:Body` with an `_IM` role inside the graph that publishes the line.
`infrastructure-manager.rq` does exactly that, and it also surfaces something a
traversal never would — German line `4000` is published in **two** datasets
(`graph/0080` and `graph/1080`), each carrying both organisation codes.

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
