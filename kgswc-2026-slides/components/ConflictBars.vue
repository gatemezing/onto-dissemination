<script setup lang="ts">
import { ref } from 'vue'

/**
 * Critical conflicts with ERA Ontology v3.3.2 (Table 5): June 2026 release vs the preliminary xsd2rdf 1.6.0 re-run.
 * Two small multiples on one shared scale. "Before" is a light outlined bar, "after" a solid blue one,
 * so the pair reads by lightness and fill, not by hue alone. Values are direct-labelled; hover shows the pair.
 * NeTEx (38 / 20) was not re-run and is left out so it does not flatten the scale.
 */
const panels = [
  { t: 'URI collisions', rows: [['TAF', 13, 6], ['TAP B5', 9, 2], ['TAP B10', 6, 1]] },
  { t: 'Property type conflicts', rows: [['TAF', 8, 1], ['TAP B5', 9, 1], ['TAP B10', 6, 1]] },
] as const
const MAX = 14, BW = 300, LX = 70
const w = (v: number) => (v / MAX) * BW
const tip = ref<string | null>(null)
</script>

<template>
  <div class="cb">
    <div class="legend">
      <span><i class="k before" /> June 2026 release</span>
      <span><i class="k after" /> xsd2rdf 1.6.0 (preliminary re-run)</span>
    </div>
    <div class="grid">
      <svg v-for="p in panels" :key="p.t" viewBox="0 0 420 164" class="panel">
        <text x="0" y="16" class="pt">{{ p.t }}</text>
        <line :x1="LX" :x2="LX" y1="28" y2="160" class="base" />
        <g v-for="(r, i) in p.rows" :key="r[0]" :transform="`translate(0,${34 + i * 44})`"
           @mouseenter="tip = `${p.t} · ${r[0]}: ${r[1]} → ${r[2]}`" @mouseleave="tip = null" class="row">
          <rect x="0" y="-3" width="420" height="40" class="hit" />
          <text :x="LX - 8" y="20" class="rl">{{ r[0] }}</text>
          <path :d="`M${LX} 2 h${w(r[1]) - 4} a4 4 0 0 1 4 4 v6 a4 4 0 0 1 -4 4 h-${w(r[1]) - 4} z`" class="before" />
          <text :x="LX + w(r[1]) + 6" y="14" class="vl muted">{{ r[1] }}</text>
          <path :d="`M${LX} 20 h${Math.max(w(r[2]) - 4, 0)} a4 4 0 0 1 4 4 v6 a4 4 0 0 1 -4 4 h-${Math.max(w(r[2]) - 4, 0)} z`" class="after" />
          <text :x="LX + w(r[2]) + 6" y="32" class="vl">{{ r[2] }}</text>
        </g>
      </svg>
    </div>
    <div class="tip">{{ tip ?? 'Hover a module for its before → after pair. NeTEx (38 collisions, 20 type conflicts) was not re-run.' }}</div>
  </div>
</template>

<style scoped>
.cb { font-family: var(--era-font); }
.legend { display: flex; gap: 18px; font-size: 12.5px; color: var(--c-ink-mod); margin-bottom: 2px; }
.k { display: inline-block; width: 18px; height: 10px; border-radius: 3px; vertical-align: middle; margin-right: 4px; }
.k.before { background: var(--c-surface); border: 1.5px solid var(--c-ink-subtle); }
.k.after { background: var(--c-blue); }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 36px; }
.panel { width: 100%; height: auto; }
.pt { font-size: 15px; font-weight: 700; fill: var(--c-heading); }
.base { stroke: var(--c-ink-subtle); stroke-width: 1.5; }
.rl { text-anchor: end; font-size: 13.5px; fill: var(--c-ink); }
.before { fill: var(--c-surface); stroke: var(--c-ink-subtle); stroke-width: 1.5; }
.after { fill: var(--c-blue); }
html.dark .after { fill: var(--c-blue); }
.vl { font-size: 13px; font-weight: 700; fill: var(--c-ink); font-variant-numeric: tabular-nums; }
.vl.muted { font-weight: 400; fill: var(--c-ink-mod); }
.hit { fill: transparent; }
.row:hover .hit { fill: var(--c-surface); }
.tip { font-size: 12px; color: var(--c-ink-mod); min-height: 18px; }
</style>
