<script setup lang="ts">
import { computed } from 'vue'

/**
 * Valenciennes station as it is published in rinf-plus (graph 0087, SNCF Réseau), queried 2026-11-10:
 *   <http://data.europa.eu/949/operationalPoint/83728fa739>, its running track "Voie A de Valenciennes"
 *   (track/669db3f795) and that track's platform edge "Quai 1" (platformEdge/1e0ce8c500).
 * Each box: the property, the real value, and what it means in plain words.
 * step 0: identity.  1: where it is.  2: what it contains.  3: the primary locations telematics uses.
 */
const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const s = computed(() => props.step)

type Box = { x: number; y: number; p: string; v: string; g: string; skos?: boolean; at: number }
const H = 58
const left: Box[] = [
  { x: 14, y: 10, p: 'era:uopid', v: 'FR0000002651', g: 'its EU-wide identifier', at: 0 },
  { x: 14, y: 78, p: 'era:opType', v: 'station', g: 'a code from a controlled list', skos: true, at: 0 },
  { x: 14, y: 146, p: 'era:inCountry', v: 'France', g: 'EU country authority list', skos: true, at: 0 },
  { x: 14, y: 236, p: 'geo:asWKT', v: 'POINT(3.5162 50.3632)', g: 'where it is on a map', at: 1 },
  { x: 14, y: 304, p: 'era:kmPost', v: 'km 250 · km 242 · km 47', g: 'where it is along 3 national lines', at: 1 },
]
const trackProps: Box[] = [
  { x: 744, y: 10, p: 'era:wheelSetGauge', v: '1435 mm', g: 'distance between the rails', skos: true, at: 2 },
  { x: 744, y: 78, p: 'era:gsmrNetworkCoverage', v: '9 GSM-R networks', g: 'train-radio roaming agreements', skos: true, at: 2 },
  { x: 744, y: 146, p: 'era:freightCorridor', v: 'North Sea–Mediterranean', g: 'part of an EU rail freight corridor', skos: true, at: 2 },
  { x: 744, y: 214, p: 'era:infrastructureManager', v: 'SNCF Réseau (0087)', g: 'who manages the track', at: 2 },
]
const platformProps: Box[] = [
  { x: 744, y: 300, p: 'era:lengthOfPlatform', v: '464 m', g: 'usable length of the platform', at: 2 },
  { x: 744, y: 368, p: 'era:platformHeight', v: '580 mm', g: 'platform height above the rails', skos: true, at: 2 },
]
const S = { x: 300, y: 166, w: 210, h: 64 }
const T = { x: 560, y: 92, w: 170, h: 64 }
const P = { x: 560, y: 304, w: 170, h: 64 }
const on = (n: number) => s.value >= n
</script>

<template>
  <svg viewBox="0 0 960 432" class="sg">
    <!-- edges -->
    <g class="ed">
      <path v-for="b in left" :key="'e' + b.p" :d="`M${S.x} ${S.y + S.h / 2} C ${S.x - 40} ${S.y + S.h / 2}, ${b.x + 236} ${b.y + H / 2}, ${b.x + 206} ${b.y + H / 2}`" :class="{ on: on(b.at) }" />
      <path :d="`M${S.x + S.w} ${S.y + 20} C ${S.x + S.w + 30} ${S.y + 20}, ${T.x - 30} ${T.y + 32}, ${T.x} ${T.y + 32}`" :class="{ on: on(2) }" />
      <path v-for="b in trackProps" :key="'t' + b.p" :d="`M${T.x + T.w} ${T.y + 32} C ${T.x + T.w + 16} ${T.y + 32}, ${b.x - 16} ${b.y + H / 2}, ${b.x} ${b.y + H / 2}`" :class="{ on: on(2) }" />
      <path :d="`M${T.x + T.w / 2} ${T.y + T.h} V ${P.y}`" :class="{ on: on(2) }" />
      <path v-for="b in platformProps" :key="'p' + b.p" :d="`M${P.x + P.w} ${P.y + 32} C ${P.x + P.w + 16} ${P.y + 32}, ${b.x - 16} ${b.y + H / 2}, ${b.x} ${b.y + H / 2}`" :class="{ on: on(2) }" />
      <path :d="`M${S.x + S.w / 2} ${S.y + S.h} V 312`" :class="{ on: on(3) }" class="pl" />
    </g>
    <g class="el" :class="{ on: on(2) }">
      <text :x="S.x + S.w + 8" :y="S.y + 44" class="l">era:hasPart</text>
      <text :x="T.x + T.w / 2 + 6" :y="(T.y + T.h + P.y) / 2 + 4" class="l">era:hasPart</text>
    </g>

    <!-- the station -->
    <g class="node main">
      <rect :x="S.x" :y="S.y" :width="S.w" :height="S.h" rx="12" />
      <text :x="S.x + S.w / 2" :y="S.y + 27" class="nt">Valenciennes</text>
      <text :x="S.x + S.w / 2" :y="S.y + 48" class="nc">era:OperationalPoint</text>
    </g>

    <!-- a track and its platform edge -->
    <g class="node" :class="{ on: on(2) }">
      <rect :x="T.x" :y="T.y" :width="T.w" :height="T.h" rx="12" />
      <text :x="T.x + T.w / 2" :y="T.y + 24" class="nt sm">track "Voie A"</text>
      <text :x="T.x + T.w / 2" :y="T.y + 42" class="nc">era:RunningTrack</text>
      <text :x="T.x + T.w / 2" :y="T.y + 57" class="ng">1 of 8 tracks + 1 siding</text>
      <rect :x="P.x" :y="P.y" :width="P.w" :height="P.h" rx="12" />
      <text :x="P.x + P.w / 2" :y="P.y + 26" class="nt sm">"Quai 1"</text>
      <text :x="P.x + P.w / 2" :y="P.y + 46" class="nc">era:PlatformEdge</text>
    </g>

    <!-- property boxes -->
    <g v-for="b in [...left, ...trackProps, ...platformProps]" :key="b.p" class="pb" :class="{ on: on(b.at) }">
      <rect :x="b.x" :y="b.y" width="206" :height="H" rx="8" />
      <circle v-if="b.skos" :cx="b.x + 194" :cy="b.y + 12" r="5" class="sk" />
      <text :x="b.x + 10" :y="b.y + 16" class="pp">{{ b.p }}</text>
      <text :x="b.x + 10" :y="b.y + 35" class="pv">{{ b.v }}</text>
      <text :x="b.x + 10" :y="b.y + 51" class="pg">{{ b.g }}</text>
    </g>

    <!-- primary locations: the telematics anchor -->
    <g class="plb" :class="{ on: on(3) }">
      <rect x="270" y="312" width="270" height="112" rx="10" />
      <text x="282" y="332" class="pp">era:primaryLocation (2)</text>
      <text x="282" y="356" class="pv">FR02494 · Valenciennes-Bât Voyageurs</text>
      <text x="282" y="378" class="pv">FR08165 · Valenciennes - Poste 2</text>
      <text x="282" y="402" class="pg">the location codes that telematics</text>
      <text x="282" y="416" class="pg">messages use → next slide</text>
    </g>
  </svg>
</template>

<style scoped>
.sg { width: 100%; height: auto; font-family: var(--era-font); }
.ed path { fill: none; stroke: var(--c-ink-subtle); stroke-width: 1.6; opacity: 0; transition: opacity .4s; }
.ed path.on { opacity: 1; }
.ed path.pl { stroke: var(--c-blue); stroke-width: 2.2; stroke-dasharray: 5 4; }
.el text { font-family: ui-monospace, Menlo, monospace; font-size: 11.5px; fill: var(--c-ink-mod); text-anchor: middle; opacity: 0; transition: opacity .4s; }
.el text.l { text-anchor: start; }
.el.on text { opacity: 1; }
.node rect { fill: var(--c-surface); stroke: var(--c-blue); stroke-width: 2; }
.node.main rect { fill: var(--c-navy); stroke: var(--c-navy); }
.node.main .nt { fill: #fff; } .node.main .nc { fill: #CFE0FF; }
.node:not(.main) { opacity: 0; transition: opacity .4s; }
.node.on { opacity: 1; }
.nt { text-anchor: middle; font-size: 19px; font-weight: 700; fill: var(--c-heading); }
.nt.sm { font-size: 15px; }
.nc { text-anchor: middle; font-size: 12px; font-family: ui-monospace, Menlo, monospace; fill: var(--c-blue); }
.ng { text-anchor: middle; font-size: 11px; fill: var(--c-ink-mod); }
.pb { opacity: 0; transition: opacity .4s; }
.pb.on { opacity: 1; }
.pb rect { fill: var(--c-bg); stroke: var(--c-stroke); stroke-width: 1.5; }
.pp { font-family: ui-monospace, Menlo, monospace; font-size: 11px; fill: var(--c-blue); }
.pv { font-size: 14px; font-weight: 700; fill: var(--c-ink); }
.pg { font-size: 11.5px; fill: var(--c-ink-mod); }
.sk { fill: var(--c-skos); }
.plb { opacity: 0; transition: opacity .4s; }
.plb.on { opacity: 1; }
.plb rect { fill: var(--c-yellow); stroke: var(--c-navy); stroke-width: 2; }
.plb .pp { fill: #00336E; } .plb .pv { fill: #14213D; } .plb .pg { fill: #3D3A20; }
</style>
