<script setup lang="ts">
/**
 * Cover illustration: three rails (blue, grey, blue, as in the ERA logo) sweep in and turn into a graph
 * whose hubs are the three W3C languages the paper keeps apart.
 */
const nodes: { x: number; y: number; r: number; k?: 'owl' | 'shacl' | 'skos'; t?: string }[] = [
  { x: 300, y: 150, r: 30, k: 'owl', t: 'OWL' },
  { x: 430, y: 290, r: 30, k: 'shacl', t: 'SHACL' },
  { x: 250, y: 380, r: 30, k: 'skos', t: 'SKOS' },
  { x: 180, y: 240, r: 9 }, { x: 420, y: 120, r: 8 }, { x: 470, y: 200, r: 10 }, { x: 360, y: 400, r: 9 },
  { x: 140, y: 340, r: 7 }, { x: 330, y: 260, r: 12 }, { x: 500, y: 380, r: 8 }, { x: 200, y: 110, r: 7 },
]
const edges = [[0, 8], [1, 8], [2, 8], [0, 4], [0, 10], [0, 3], [1, 5], [1, 9], [1, 6], [2, 6], [2, 7], [3, 7], [4, 5], [3, 8]]
</script>

<template>
  <svg viewBox="0 0 560 540" class="cv" aria-hidden="true">
    <g class="rails">
      <path d="M-20 560 C 60 420, 120 330, 330 262" class="r1" />
      <path d="M30 560 C 100 440, 160 360, 330 270" class="r2" />
      <path d="M80 560 C 140 460, 200 390, 330 278" class="r1" />
    </g>
    <g class="ed"><line v-for="([a, b], i) in edges" :key="i" :x1="nodes[a].x" :y1="nodes[a].y" :x2="nodes[b].x" :y2="nodes[b].y" /></g>
    <g v-for="(n, i) in nodes" :key="i">
      <circle :cx="n.x" :cy="n.y" :r="n.r" class="nd" :class="n.k" />
      <text v-if="n.t" :x="n.x" :y="n.y + 5" class="nt">{{ n.t }}</text>
    </g>
  </svg>
</template>

<style scoped>
.cv { width: 100%; height: 100%; }
.r1, .r2 { fill: none; stroke-width: 14; stroke-linecap: round; }
.r1 { stroke: var(--c-blue); }
.r2 { stroke: var(--c-grey); }
.ed line { stroke: var(--c-ink-subtle); stroke-width: 2; }
.nd { fill: var(--c-bg); stroke: var(--c-blue); stroke-width: 3; }
.nd.owl { fill: var(--c-owl); stroke: var(--c-bg); }
.nd.shacl { fill: var(--c-shacl); stroke: var(--c-bg); }
.nd.skos { fill: var(--c-skos); stroke: var(--c-bg); }
.nt { text-anchor: middle; font-size: 13px; font-weight: 700; fill: #fff; font-family: var(--era-font); }
html.dark .nt { fill: #111A2E; }
</style>
