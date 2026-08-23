# RCC parameters with location — verified query set

The query set behind [`era-rcc-parameters.html`](../era-rcc-parameters.html)
(published as `/rcc.html`): the two supplied Data Stories queries, corrected and
tuned, plus the country → line lookup that drives its cascade. All three were run against
`graph.data.era.europa.eu/repositories/rinf-plus` on 2026-08-22.

| File | What it does | Measured |
|---|---|---|
| `lines-for-country.rq` | national lines, by `era:lineId` **or** LPS label | 0.2–2.3 s |
| `sections-for-line.rq` | phase 1: sections with position and latest window | **0.45 s**, 167 for DEU `4000` |
| `ops-for-line.rq` | phase 1: points, by kilometric post **or** section endpoint | **0.25 s**, 168 for the same line |
| `track-rcc-parameters.rq` | phase 2: RINF `1.1…` parameters on those sections | part of a **3.6 s** German run |
| `op-rcc-parameters.rq` | phase 2: RINF `1.2…` parameters at those points | as above |

## Two phases, and why the single query had to go

The original form asked for places, parameters and two validity rules at once.
The track side took 25 s; the operational-point side went **over the endpoint's
120 s limit and returned HTTP 503** for every country tried. Resolving the
places once and pinning them into the parameter query with `VALUES` gives
identical results, far faster:

| Line | Before | After | Rows |
|---|---|---|---|
| DEU `4000` | 33 s | **3.6 s** | 12,661 |
| FRA `830000-1` | 21 s | **6.6 s** | 69,877 |
| ESP `ESL010110000` | 0.7 s | **0.6 s** | 1,446 |
| HRV `NationalRailwayLine_L101` | *no lines offered* | **0.3 s** | 62 |
| NOR `B01-Østfoldbanen Vestre` | *no lines offered* | **1.3 s** | 1,104 |

## Four modelling variations, all of them absorbed

A query written against one publication style returns nothing at all for the
others, silently. The full analysis is in
[`../routebook/README.md`](../routebook/README.md); in summary:

1. **Line identity** — `era:lineId` (9,543 of 9,642 LPS) or the English
   `rdfs:label` (Croatia's 55, Norway's 32).
2. **Reaching operational points** — kilometric post or `era:opStart`/`era:opEnd`
   of a section. Not just a Croatia fix: FRA `830000-1` goes 327 → 603 points.
3. **Linear referencing, or none** — Croatia's net point references carry a
   geometry and no `era:hasLrsCoordinate`, so position is `OPTIONAL` and its
   rows show `—`.
4. **The part-whole direction** — every dataset publishes `era:isPartOf` except
   Croatia's, which publishes only `era:hasPart` (645 tracks otherwise invisible).
   Asking for **both** is correct and ruinous: by UNION or by an alternation
   path it takes the German track query from 1.4 s to **57 s**, because the
   optimiser can no longer push the parameter join. The direction is probed once
   per run with a one-row query, and a single form is emitted.

## The correction that matters: latest validity only

The supplied queries have no validity filter. Some infrastructure managers
republish the same physical place under a new validity window each year, so
without a filter the query silently mixes superseded descriptions with current
ones.

Germany is the clearest case. Line `4000` carries **167 sections valid
2025-01-01→2025-12-31 and another 167 valid 2026-01-01→2026-12-31**, over the
identical km range — so the track-side query returns **16,615 rows** as supplied
and **8,281** once each stretch keeps only its own newest window. On the
operational-point side Germany holds **294,906 station tracks in the 2025 window
against 266,157 in the 2026 window**, across ~7,600 operational points. France is
affected on the OP side too: **149 of the 327 operational points** on line
`830000-1` carry more than one window.

## The scope of the comparison is the whole problem

A first version of the track query took the **line-wide** maximum date. It gives
the right answer for Germany and a catastrophically wrong one for France, and
the failure is invisible unless you count the sections.

France does not republish sections — it dates each one by the day it opened.
Line `830000-1` spreads **25 distinct validity beginnings across its 702 section
resources** — 627 at `1800-01-01`, then 22 at `2004-03-01`, 16 at `2017-09-01`,
and a long tail down to single sections. Taking the line-wide maximum keeps the
**2** sections commissioned on `2025-10-31` and throws away the rest, reporting a
tidy "132 rows" that reads like successful deduplication and is in fact 99.6%
data loss.

The comparison must therefore be made **per place, not per line**:

| Side | Scope of the MAX | Rationale |
|---|---|---|
| along the line | per stretch — `(startPosition, endPosition)` on that line | catches the yearly republication of one stretch, leaves neighbouring sections alone |
| at operational points | per `era:uopid`, then per track within the point | see the two-rule section below |

Measured with the per-stretch rule, which is the check that distinguishes the
two failure modes:

| Scope | Unfiltered | Filtered | Sections |
|---|---|---|---|
| FRA `830000-1` | 65,274 | 65,274 | 570 → 570 (nothing to remove) |
| DEU `4000` | 16,615 | 8,281 | 334 → 167 |

The French number being unchanged is the point: a validity filter that removes
nothing where nothing is duplicated is the one you want.

## Why the filter cannot simply take the global maximum

**Eleven countries publish no dated validity at all** — Sweden, Spain, Ireland,
Estonia, Greece, Finland, Romania, Croatia, Austria, Liechtenstein and
Luxembourg. A naive "keep only rows matching the latest date" filter deletes
every row for those countries, which is the silent-zero failure again.

Both queries therefore use: *keep a resource when it has no validity at all, or
when no later window exists in its own scope* — per stretch on the section side,
per `uopid` and then per track on the OP side. Verified: Germany line `4000` goes
334 → 167 sections, while a Spanish line stays at 86 → 86.

Retired parameters (`owl:deprecated`) are excluded, consistent with the other
tools; 4 of the 83 `era:usedInRCCCalculations` parameters are retired.

## Germany: solved, and it needed two rules not one

The operational-point query originally exceeded two minutes on a German line.
Two separate causes, found by measuring rather than guessing:

1. **The aggregate was not line-scoped**, so it computed a maximum for every
   operational point in the graph. Scoping it to the selected line brought
   Germany from a timeout to ~16 s.
2. **The two countries duplicate differently.** France repeats *tracks inside
   one operational point* — 149 of the 327 points on line `830000-1` carry more
   than one window. Germany repeats *the whole station as separate OP
   resources*, one per window, each internally single-window and sharing a
   `era:uopid` (`DE95070` resolves to three OP resources). A per-OP rule fixes
   France and does nothing for Germany; a line-wide maximum fixes Germany and
   destroys France, cutting it from 2,596 rows to 1 — the same trap the track
   side fell into, in a different disguise.

The query therefore applies both: keep the latest OP resource per `uopid`, then
within it keep that point's latest track window. Measured after the fix:

| Scope | Rows | Distinct uopids | Time |
|---|---|---|---|
| FRA `830000-1` | 2,596 | 327 | 5.6 s |
| DEU `4000` | 4,404 (from 8,802) | 132 | 16.6 s |
| ESP `ESL740874000` (undated) | 182 | 87 | 0.3 s |
