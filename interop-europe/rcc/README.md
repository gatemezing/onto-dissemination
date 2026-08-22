# RCC parameters with location — verified query set

The query set behind [`era-rcc-parameters.html`](../../scripts/assets/era-rcc-parameters.html)
(published as `/rcc.html`): the two supplied Data Stories queries, corrected and
tuned, plus the country → line lookup that drives its cascade. All three were run against
`graph.data.era.europa.eu/repositories/rinf-plus` on 2026-08-22.

| File | What it does | Measured |
|---|---|---|
| `lines-for-country.rq` | national lines for one country, with section count and km range | 444 lines for BEL in **0.5 s** |
| `track-rcc-parameters.rq` | RINF `1.1…` RCC parameters per track, with start/end position | **67,281 rows, 20 s** for FRA line `830000-1`; **8,281 rows (from 16,615), 24 s** for DEU `4000` |
| `op-rcc-parameters.rq` | RINF `1.2…` RCC parameters per operational-point track | **2,596 rows, 6 s** for the same line |

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
