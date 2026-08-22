# RCC parameters with location — verified query set

Working material for a planned `era-rcc-parameters` tool. These are the two
supplied Data Stories queries, corrected and tuned, plus the country → line
lookup the tool needs for its cascade. All three were run against
`graph.data.era.europa.eu/repositories/rinf-plus` on 2026-08-22.

| File | What it does | Measured |
|---|---|---|
| `lines-for-country.rq` | national lines for one country, with section count and km range | 444 lines for BEL in **0.5 s** |
| `track-rcc-parameters.rq` | RINF `1.1…` RCC parameters per track, with start/end position | **132 rows, 11 s** for FRA line `830000-1` |
| `op-rcc-parameters.rq` | RINF `1.2…` RCC parameters per operational-point track | **2,596 rows, 6 s** for the same line |

## The correction that matters: latest validity only

The supplied queries have no validity filter. Because a line is described once
per validity window, they return the same physical line repeated many times over.

For FRA line `830000-1` the track-side query returns **67,281 rows / 19 MB / 25 s**
as supplied, and **132 rows / 30 KB / 11 s** once restricted to the latest
validity window — a **510×** reduction. It is a correctness problem before it is
a performance one: the unfiltered result silently mixes superseded descriptions
with current ones.

Germany is the clearest case. Line `4000` carries **167 sections valid
2025-01-01→2025-12-31 and another 167 valid 2026-01-01→2026-12-31**, over the
identical km range. On the operational-point side Germany holds **294,906 station
tracks in the 2025 window against 266,157 in the 2026 window**, across ~7,600
operational points. France is affected too, less visibly: **149 of the 327
operational points** on line `830000-1` carry more than one window.

## Why the filter cannot simply take the global maximum

**Eleven countries publish no dated validity at all** — Sweden, Spain, Ireland,
Estonia, Greece, Finland, Romania, Croatia, Austria, Liechtenstein and
Luxembourg. A naive "keep only rows matching the latest date" filter deletes
every row for those countries, which is the silent-zero failure again.

Both queries therefore use: *keep a resource when it has no validity at all, or
when no later window exists in its own scope* — per line on the section side,
per operational point on the OP side. Verified: Germany line `4000` goes 334 → 167
sections, while a Spanish line stays at 86 → 86.

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
   destroys France, cutting it from 2,596 rows to 1.

The query therefore applies both: keep the latest OP resource per `uopid`, then
within it keep that point's latest track window. Measured after the fix:

| Scope | Rows | Distinct uopids | Time |
|---|---|---|---|
| FRA `830000-1` | 2,596 | 327 | 5.6 s |
| DEU `4000` | 4,404 (from 8,802) | 132 | 16.6 s |
| ESP `ESL740874000` (undated) | 182 | 87 | 0.3 s |
