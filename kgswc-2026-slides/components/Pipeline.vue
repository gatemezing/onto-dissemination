<script setup lang="ts">
import { computed } from 'vue'

/**
 * The CI pipeline of Fig. 1, built up in three clicks.
 * step 0: the four schema families and the seven stages.
 * step 1: what generation emits per family (OWL, SHACL, one SKOS file per code list).
 * step 2: merge and publish on the ERA vocabulary portal.
 * step 3: the instance side: messages lifted with RML and validated against the generated shapes.
 */
const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const s = computed(() => props.step)

const stages = ['Validate XSDs', 'Generate RDF', 'Post-process', 'Prepare docs', 'Generate docs', 'Merge', 'Publish']
const W = 112, G = 10, X0 = 150
const sx = (i: number) => X0 + i * (W + G)
const families = ['TAF', 'TAP B5', 'TAP B10', 'NeTEx']
const hot = (i: number) => (s.value === 1 && (i === 1 || i === 2)) || (s.value === 2 && (i === 5 || i === 6))
const inst = ['XML message', 'RML mapping', 'RDF message graph', 'SHACL validation', 'CQ SPARQL queries']
const ix = (i: number) => 150 + i * 168
</script>

<template>
  <svg viewBox="0 0 1010 352" class="pl">
    <!-- inputs -->
    <text x="12" y="22" class="lab">schema families</text>
    <g v-for="(f, i) in families" :key="f">
      <rect x="12" :y="34 + i * 30" width="112" height="24" rx="6" class="fam" />
      <text x="68" :y="51 + i * 30" class="famt">{{ f }}</text>
    </g>
    <path d="M124 94 H 146" class="arr" /><polygon points="144,89 152,94 144,99" class="arrh" />

    <!-- seven stages as chevrons -->
    <text :x="X0" y="22" class="lab">continuous-integration workflow · 7 stages</text>
    <g v-for="(st, i) in stages" :key="st" class="stg" :class="{ hot: hot(i) }">
      <path :d="`M${sx(i)} 72 h${W - 12} l12 22 l-12 22 h-${W - 12} ${i ? 'l12 -22 z' : 'z'}`" />
      <text :x="sx(i) + W / 2 + (i ? 4 : -2)" y="92" class="sn">{{ i + 1 }}</text>
      <text :x="sx(i) + W / 2 + (i ? 4 : -2)" y="108" class="st">{{ st }}</text>
    </g>

    <!-- step 1: generation output -->
    <g class="reveal" :class="{ on: s >= 1 }">
      <path :d="`M${sx(1) + W / 2} 118 V 150`" class="arr" />
      <g transform="translate(150,152)">
        <rect width="330" height="60" rx="10" class="outbox" />
        <text x="12" y="20" class="ot">per family</text>
        <rect x="12" y="30" width="78" height="22" rx="11" class="chip owl" /><text x="51" y="45" class="ct owl">1 × OWL</text>
        <rect x="98" y="30" width="92" height="22" rx="11" class="chip shacl" /><text x="144" y="45" class="ct shacl">1 × SHACL</text>
        <rect x="198" y="30" width="122" height="22" rx="11" class="chip skos" /><text x="259" y="45" class="ct skos">n × SKOS scheme</text>
      </g>
      <text x="494" y="168" class="note"><tspan font-weight="700">deterministic</tspan>: the same XSD release</text>
      <text x="494" y="185" class="note">gives the same artifacts, each term</text>
      <text x="494" y="202" class="note">traceable to the TEL TSI documents</text>
    </g>

    <!-- step 2: merge + publish -->
    <g class="reveal" :class="{ on: s >= 2 }">
      <path :d="`M${sx(6) + W / 2} 118 V 150`" class="arr" />
      <g :transform="`translate(${sx(5) - 6},152)`">
        <rect width="246" height="60" rx="10" class="outbox pub" />
        <text x="12" y="22" class="ot">ERA vocabulary portal</text>
        <text x="12" y="42" class="note">v4.0.0 RC · shapes per module</text>
        <text x="12" y="56" class="note">telematics + NeTEx code lists</text>
      </g>
    </g>

    <!-- step 3: instance data -->
    <g class="reveal" :class="{ on: s >= 3 }">
      <line x1="12" x2="998" y1="236" y2="236" class="sep" />
      <text x="12" y="258" class="lab">instance data</text>
      <g v-for="(t, i) in inst" :key="t">
        <rect :x="ix(i)" y="274" width="146" height="40" rx="8" class="ib" :class="{ sh: i === 3 }" />
        <text :x="ix(i) + 73" y="299" class="ibt">{{ t }}</text>
        <path v-if="i < inst.length - 1" :d="`M${ix(i) + 146} 294 H ${ix(i + 1) - 4}`" class="arr" />
      </g>
      <path :d="`M${sx(1) + 20} 212 C ${sx(1) + 20} 250, ${ix(3) + 73} 240, ${ix(3) + 73} 272`" class="arr dash" />
      <text :x="ix(3) + 80" y="258" class="note">generated shapes</text>
      <text x="12" y="340" class="note">xsd2rdf lifts the <tspan font-weight="700">schemas</tspan>; declarative mappings lift the <tspan font-weight="700">messages</tspan>, using the generated vocabulary.</text>
    </g>
  </svg>
</template>

<style scoped>
.pl { width: 100%; height: auto; font-family: var(--era-font); }
.lab { font-size: 12px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; fill: var(--c-ink-subtle); }
.fam { fill: var(--c-xsd-bg); stroke: var(--c-xsd); stroke-width: 1.5; }
.famt { text-anchor: middle; font-size: 13px; font-weight: 700; fill: var(--c-xsd); }
.arr { stroke: var(--c-ink-mod); stroke-width: 2; fill: none; }
.arrh { fill: var(--c-ink-mod); }
.dash { stroke-dasharray: 5 4; }
.stg path { fill: var(--c-surface); stroke: var(--c-blue); stroke-width: 1.5; transition: fill .35s; }
.stg .sn { text-anchor: middle; font-size: 12px; font-weight: 700; fill: var(--c-blue); }
.stg .st { text-anchor: middle; font-size: 12.5px; fill: var(--c-ink); }
.stg.hot path { fill: var(--c-blue); }
.stg.hot text { fill: #fff; }
.reveal { opacity: 0; transition: opacity .45s; }
.reveal.on { opacity: 1; }
.outbox { fill: var(--c-surface); stroke: var(--c-stroke); stroke-width: 1.5; }
.outbox.pub { stroke: var(--c-blue); }
.ot { font-size: 13px; font-weight: 700; fill: var(--c-heading); }
.chip.owl { fill: var(--c-owl-bg); } .chip.shacl { fill: var(--c-shacl-bg); } .chip.skos { fill: var(--c-skos-bg); }
.ct { text-anchor: middle; font-size: 12px; font-weight: 700; }
.ct.owl { fill: var(--c-owl); } .ct.shacl { fill: var(--c-shacl); } .ct.skos { fill: var(--c-skos); }
.note { font-size: 12.5px; fill: var(--c-ink-mod); }
.sep { stroke: var(--c-stroke); stroke-dasharray: 3 5; }
.ib { fill: var(--c-surface); stroke: var(--c-stroke); stroke-width: 1.5; }
.ib.sh { fill: var(--c-shacl-bg); stroke: var(--c-shacl); }
.ibt { text-anchor: middle; font-size: 13px; fill: var(--c-ink); }
</style>
