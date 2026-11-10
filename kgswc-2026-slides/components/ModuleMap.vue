<script setup lang="ts">
import { computed } from 'vue'

/**
 * Integration strategy for ERA Ontology v4.0.0 (Sect. 6), built up in clicks.
 * step 0: the ERA core today.  1: TAF and TAP merged into the core.
 * 2: NeTEx as the only separate module, curated alignments, code lists as their own modules.
 * 3: application profiles assemble what a use case needs through owl:imports.
 */
const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const s = computed(() => props.step)
const base = ['Infrastructure', 'Technical characteristics', 'Topology & referencing', 'Organisations', 'Operational locations', 'Vehicles']
const slot = (i: number) => ({ x: 304 + (i % 2) * 154, y: 138 + Math.floor(i / 2) * 32 })
</script>

<template>
  <svg viewBox="0 0 960 330" class="mm">
    <defs>
      <marker id="mm-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 z" class="ah" />
      </marker>
    </defs>

    <!-- core -->
    <rect x="290" y="100" width="324" height="170" rx="14" class="core" :class="{ v4: s >= 1 }" />
    <text x="304" y="124" class="ct">{{ s >= 1 ? 'ERA Ontology v4.0.0 · core' : 'ERA Ontology core · v3.3.x' }}</text>
    <g v-for="(b, i) in base" :key="b">
      <rect :x="slot(i).x" :y="slot(i).y" width="146" height="25" rx="6" class="chip" />
      <text :x="slot(i).x + 73" :y="slot(i).y + 17" class="cht">{{ b }}</text>
    </g>
    <g class="reveal" :class="{ on: s >= 1 }">
      <rect :x="slot(6).x" :y="slot(6).y" width="146" height="25" rx="6" class="chip new" />
      <text :x="slot(6).x + 73" :y="slot(6).y + 17" class="cht new">TAF · freight</text>
      <rect :x="slot(7).x" :y="slot(7).y" width="146" height="25" rx="6" class="chip new" />
      <text :x="slot(7).x + 73" :y="slot(7).y + 17" class="cht new">TAP · passenger</text>
    </g>

    <!-- NeTEx, alignments, code lists -->
    <g class="reveal" :class="{ on: s >= 2 }">
      <rect x="700" y="128" width="244" height="96" rx="14" class="netex" />
      <text x="716" y="154" class="ct">NeTEx module</text>
      <text x="716" y="176" class="sm">own namespace · ¾ of generated content</text>
      <text x="716" y="196" class="sm">most of the conflicts (Table 5)</text>
      <path d="M700 176 H 618" class="ln" marker-end="url(#mm-arr)" />
      <text x="659" y="168" class="lbl">owl:imports</text>

      <rect x="636" y="250" width="308" height="72" rx="10" class="align" />
      <text x="650" y="271" class="ct2">curated alignment module</text>
      <text x="650" y="290" class="sm">NeTEx stop place, quay → ERA locations</text>
      <text x="650" y="309" class="sm mono">skos:closeMatch · rdfs:subClassOf</text>

      <text x="16" y="108" class="lab">code lists · own modules, own rhythm</text>
      <g v-for="(c, i) in ['era-skos (core)', 'era-telem-skos', 'era-netex-skos']" :key="c">
        <rect x="16" :y="120 + i * 44" width="230" height="34" rx="8" class="skos" />
        <text x="30" :y="142 + i * 44" class="skt">{{ c }}</text>
      </g>
      <path d="M246 185 H 286" class="ln dash" marker-end="url(#mm-arr)" />
    </g>

    <!-- application profiles -->
    <g class="reveal" :class="{ on: s >= 3 }">
      <rect x="290" y="14" width="236" height="46" rx="10" class="prof" />
      <text x="408" y="42" class="pt">capacity-management profile</text>
      <path d="M408 60 V 96" class="ln" marker-end="url(#mm-arr)" />
      <rect x="600" y="14" width="300" height="46" rx="10" class="prof" />
      <text x="750" y="42" class="pt">passenger-information profile</text>
      <path d="M660 60 C 660 80, 600 80, 590 96" class="ln" marker-end="url(#mm-arr)" />
      <path d="M840 60 V 124" class="ln" marker-end="url(#mm-arr)" />
      <text x="850" y="96" class="lbl l">owl:imports</text>
    </g>
  </svg>
</template>

<style scoped>
.mm { width: 100%; height: auto; font-family: var(--era-font); }
.ah { fill: var(--c-ink-mod); }
.core { fill: var(--c-surface); stroke: var(--c-blue); stroke-width: 2; transition: all .4s; }
.core.v4 { fill: var(--c-blue-bg); stroke-width: 3; }
.ct { font-size: 15px; font-weight: 700; fill: var(--c-heading); }
.ct2 { font-size: 13.5px; font-weight: 700; fill: var(--c-heading); }
.chip { fill: var(--c-bg); stroke: var(--c-stroke); }
.cht { text-anchor: middle; font-size: 12px; fill: var(--c-ink); }
.chip.new { fill: var(--c-yellow); stroke: var(--c-navy); }
.cht.new { fill: #14213D; font-weight: 700; }
.reveal { opacity: 0; transition: opacity .45s; }
.reveal.on { opacity: 1; }
.netex { fill: var(--c-xsd-bg); stroke: var(--c-xsd); stroke-width: 2; }
.align { fill: var(--c-surface); stroke: var(--c-ink-subtle); stroke-dasharray: 5 4; stroke-width: 1.5; }
.sm { font-size: 12px; fill: var(--c-ink-mod); }
.mono { font-family: ui-monospace, Menlo, monospace; font-size: 11px; }
.lab { font-size: 11.5px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; fill: var(--c-ink-subtle); }
.skos { fill: var(--c-skos-bg); stroke: var(--c-skos); stroke-width: 1.5; }
.skt { font-size: 13px; font-weight: 700; fill: var(--c-skos); font-family: ui-monospace, Menlo, monospace; }
.ln { stroke: var(--c-ink-mod); stroke-width: 2; fill: none; }
.dash { stroke-dasharray: 5 4; }
.lbl { font-size: 11.5px; fill: var(--c-ink-mod); text-anchor: middle; font-family: ui-monospace, Menlo, monospace; }
.lbl.l { text-anchor: start; }
.prof { fill: var(--c-bg); stroke: var(--c-navy); stroke-width: 2; }
.pt { text-anchor: middle; font-size: 13.5px; font-weight: 700; fill: var(--c-heading); }
</style>
