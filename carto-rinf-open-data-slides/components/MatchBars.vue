<script setup lang="ts">
import { ref } from 'vue'

/**
 * RINF primary locations matched to a Wikidata station, per country, before and after the matching change
 * (measured live, 20-21 Nov 2026). Same encoding as the KGSWC deck's ConflictBars: "before" is a light
 * outlined bar, "after" a solid blue one, on one shared scale, direct-labelled; hover shows the pair.
 */
const rows = [
  ['Czechia', 1, 2832, 3581], ['Germany', 2392, 2789, 9557], ['Italy', 1, 2072, 3199], ['Switzerland', 3, 1846, 3310],
  ['France', 1649, 1653, 7691], ['Hungary', 670, 1525, 1808], ['Spain', 3, 1488, 2276], ['Austria', 0, 958, 1479],
] as const
const MAX = 2900, BW = 390, LX = 92
const w = (v: number) => Math.max((v / MAX) * BW, v > 0 ? 3 : 0)
const tip = ref<string | null>(null)
</script>

<template>
  <div class="mb">
    <div class="legend">
      <span><i class="k before" /> before: PLC on items typed exactly "railway station"</span>
      <span><i class="k after" /> after: + any station type, ERA ID, UIC code within 1 km</span>
    </div>
    <svg viewBox="0 0 560 330" class="panel">
      <line :x1="LX" :x2="LX" y1="4" y2="326" class="base" />
      <g v-for="(r, i) in rows" :key="r[0]" :transform="`translate(0,${6 + i * 40})`"
         @mouseenter="tip = `${r[0]}: ${r[1].toLocaleString('en')} → ${r[2].toLocaleString('en')} of ${r[3].toLocaleString('en')} primary locations`"
         @mouseleave="tip = null" class="row">
        <rect x="0" y="-3" width="560" height="38" class="hit" />
        <text :x="LX - 8" y="20" class="rl">{{ r[0] }}</text>
        <rect :x="LX" y="2" :width="w(r[1])" height="13" rx="3" class="before" />
        <text :x="LX + w(r[1]) + 6" y="13" class="vl muted">{{ r[1].toLocaleString('en') }}</text>
        <rect :x="LX" y="18" :width="w(r[2])" height="13" rx="3" class="after" />
        <text :x="LX + w(r[2]) + 6" y="30" class="vl">{{ r[2].toLocaleString('en') }}</text>
      </g>
    </svg>
    <div class="tip">{{ tip ?? 'Hover a country for its before → after pair and its number of primary locations in RINF.' }}</div>
  </div>
</template>

<style scoped>
.mb { font-family: var(--era-font); }
.legend { display: flex; flex-direction: column; gap: 2px; font-size: 12.5px; color: var(--c-ink-mod); margin-bottom: 4px; flex-wrap: wrap; }
.k { display: inline-block; width: 18px; height: 10px; border-radius: 3px; vertical-align: middle; margin-right: 4px; }
.k.before { background: var(--c-surface); border: 1.5px solid var(--c-ink-subtle); }
.k.after { background: var(--c-blue); }
.panel { width: 100%; height: auto; }
.base { stroke: var(--c-ink-subtle); stroke-width: 1.5; }
.rl { text-anchor: end; font-size: 13.5px; fill: var(--c-ink); }
.before { fill: var(--c-surface); stroke: var(--c-ink-subtle); stroke-width: 1.5; }
.after { fill: var(--c-blue); }
.vl { font-size: 13px; font-weight: 700; fill: var(--c-ink); font-variant-numeric: tabular-nums; }
.vl.muted { font-weight: 400; fill: var(--c-ink-mod); }
.hit { fill: transparent; }
.row:hover .hit { fill: var(--c-surface); }
.tip { font-size: 12px; color: var(--c-ink-mod); min-height: 18px; }
</style>
