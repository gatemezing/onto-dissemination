# Route book elements (TSI OPE Appendix D2) — verified query set

The query set behind [`era-route-book.html`](../era-route-book.html)
(published as `/routebook.html`). All measurements against
`graph.data.era.europa.eu/repositories/rinf-plus` on 2026-08-22.

| File | What it does | Measured |
|---|---|---|
| `d2-catalogue.rq` | the 46 D2 elements, and whether any manager publishes each at all | **0.15 s** |
| `infrastructure-manager.rq` | D2 1.1 — the manager each section of line declares | **0.11 s** |
| `infrastructure-manager-names.rq` | …and their names, from OCR-KG | **0.15 s** |
| `country-gap-diagnosis.rq` | why a country returned no national lines | **0.15–0.21 s** |
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

## Croatia and Norway: sections of line with no line identifiers

The tool keys a route book to `era:lineId` and finds operational points by
`era:inCountry`. Two of the 27 countries publishing sections of line populate
neither, so the country → line cascade comes back empty:

| Country | Sections | National lines | `era:lineId` | Labels instead | OPs referenced | OPs with `era:inCountry` |
|---|---|---|---|---|---|---|
| **HRV** | 583 | 55 | **0** | 110, e.g. `NationalRailwayLine_M604` | 533 | **0** |
| **NOR** | 375 | 32 | **0** | 64, e.g. `Kongsberg - Flesberg` | 235 | 235 |
| ESP *(for contrast)* | 2,520 | 466 | 466 | 466 | 2,153 | 2,153 |

Croatia's national lines are typed `era:LinearPositioningSystem` and carry only
an `rdfs:label` and a geometry. Its operational points are otherwise sound —
correctly typed, carrying `era:uopid` — but without `era:inCountry` they cannot
be found by country either, so both halves of the route book are unreachable.
Norway has only the first gap; its operational points are complete.

The other 25 countries populate `era:lineId`, from Liechtenstein's 1 to
Germany's 1,482.

**The identifier is visible in both cases, and the tool still does not use it.**
`NationalRailwayLine_M604` plainly contains `M604`, and a regular expression
would produce a line list for Croatia. That would be the wrong call: a label is
not an identifier, the pattern differs between the two countries (Norway's
labels are endpoint pairs, not codes), and parsing it would hide a reporting gap
that a route-book compiler needs to see. The tool asks for the property the
ontology defines, and when it is absent it says so — `country-gap-diagnosis.rq`
runs automatically and the figures above appear in the page.

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
