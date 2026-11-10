<script setup lang="ts">
import { computed } from 'vue'

/**
 * One XSD, three kinds of semantics, three W3C languages (Table 1 of the paper).
 * step 0: the schema as it is, all mixed.  1: domain concepts -> OWL.
 * 2: constraints -> SHACL.  3: code lists -> SKOS (+ a SHACL membership check).  4: the cross-links.
 */
const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const s = computed(() => props.step)

type K = 'owl' | 'shacl' | 'skos'
const xsd: { k: K; t: string; i?: number }[] = [
  { k: 'owl', t: '<xs:complexType name="CompositIdentifierPlannedType">' },
  { k: 'owl', t: '<xs:element name="Company" type="CompanyCode"', i: 1 },
  { k: 'shacl', t: 'minOccurs="1" maxOccurs="1"/>', i: 3 },
  { k: 'owl', t: '<xs:simpleType name="CompanyCode">' },
  { k: 'shacl', t: '<xs:pattern value="[0-9A-Z]{4}"/>', i: 1 },
  { k: 'owl', t: '<xs:simpleType name="BorderPointTypeCodeList">' },
  { k: 'skos', t: '<xs:enumeration value="1001"> Sarkiai(Gr)', i: 1 },
  { k: 'skos', t: '<xs:enumeration value="1002"> …', i: 1 },
]
const order: Record<K, number> = { owl: 1, shacl: 2, skos: 3 }
const boxes: { k: K; y: number; title: string; q: string; out: string }[] = [
  { k: 'owl', y: 14, title: 'OWL', q: 'What exists? Open world.', out: 'era:PathConfirmedMessage a owl:Class' },
  { k: 'shacl', y: 118, title: 'SHACL', q: 'Is this message valid? Closed world.', out: 'sh:pattern "[0-9A-Z]{4}"' },
  { k: 'skos', y: 222, title: 'SKOS', q: 'Which codes are allowed? Own release cycle.', out: 'b13:1001 skos:notation "1001"' },
]
const lineY = (i: number) => 52 + i * 31
const firstY: Record<K, number> = { owl: lineY(0), shacl: lineY(2), skos: lineY(6) }
const lit = (k: K) => s.value >= order[k]
</script>

<template>
  <svg viewBox="0 0 940 330" class="tl">
    <!-- the schema -->
    <rect x="8" y="10" width="440" height="300" rx="12" class="src" />
    <text x="24" y="34" class="srct">TAF XSD · one schema, three kinds of semantics</text>
    <g v-for="(l, i) in xsd" :key="i">
      <rect x="18" :y="lineY(i) - 15" width="420" height="25" rx="5" class="hl" :class="[l.k, { on: lit(l.k) }]" />
      <text :x="26 + (l.i ?? 0) * 14" :y="lineY(i) + 2" class="code" :class="[l.k, { on: lit(l.k) }]">{{ l.t }}</text>
    </g>

    <!-- flows -->
    <g v-for="b in boxes" :key="'f' + b.k" class="flow" :class="[b.k, { on: lit(b.k) }]">
      <path :d="`M448 ${firstY[b.k] + 4} C 500 ${firstY[b.k] + 4}, 500 ${b.y + 44}, 552 ${b.y + 44}`" />
      <polygon :points="`552,${b.y + 38} 562,${b.y + 44} 552,${b.y + 50}`" />
    </g>
    <!-- SKOS enumerations are also checked by SHACL -->
    <path v-if="s >= 3" d="M448 246 C 505 246, 505 170, 552 170" class="flow skos on dashed" />

    <!-- target languages -->
    <g v-for="b in boxes" :key="b.k" class="box" :class="[b.k, { on: lit(b.k) }]">
      <rect x="562" :y="b.y" width="290" height="88" rx="12" />
      <text x="578" :y="b.y + 26" class="bt">{{ b.title }}</text>
      <text x="578" :y="b.y + 48" class="bq">{{ b.q }}</text>
      <text x="578" :y="b.y + 72" class="bo">{{ b.out }}</text>
    </g>

    <!-- cross-links between the layers -->
    <g v-if="s >= 4" class="xl">
      <path d="M852 58 C 912 58, 912 162, 852 162" />
      <circle cx="898" cy="110" r="12" /><text x="898" y="115">1</text>
      <path d="M852 72 C 935 72, 935 266, 852 266" />
      <circle cx="921" cy="190" r="12" /><text x="921" y="195">2</text>
    </g>
  </svg>
</template>

<style scoped>
.tl { width: 100%; height: auto; font-family: var(--era-font); }
.src { fill: var(--c-surface); stroke: var(--c-xsd); stroke-width: 2; }
.srct { font-size: 13px; font-weight: 700; fill: var(--c-xsd); }
.code { font-family: ui-monospace, Menlo, monospace; font-size: 12.5px; fill: var(--c-ink-mod); transition: fill .4s; }
.hl { fill: transparent; transition: fill .4s; }
.hl.owl.on { fill: var(--c-owl-bg); } .hl.shacl.on { fill: var(--c-shacl-bg); } .hl.skos.on { fill: var(--c-skos-bg); }
.code.owl.on { fill: var(--c-owl); } .code.shacl.on { fill: var(--c-shacl); } .code.skos.on { fill: var(--c-skos); }
.code.on { font-weight: 600; }

.flow path { fill: none; stroke-width: 2.5; opacity: 0; transition: opacity .4s; }
.flow polygon { opacity: 0; transition: opacity .4s; }
.flow.on path, .flow.on polygon, path.flow.on { opacity: 1; }
.flow.owl path { stroke: var(--c-owl); } .flow.owl polygon { fill: var(--c-owl); }
.flow.shacl path { stroke: var(--c-shacl); } .flow.shacl polygon { fill: var(--c-shacl); }
.flow.skos path { stroke: var(--c-skos); } .flow.skos polygon { fill: var(--c-skos); }
path.flow.skos { stroke: var(--c-skos); fill: none; stroke-width: 2; }
.dashed { stroke-dasharray: 5 4; }

.box rect { fill: var(--c-surface); stroke: var(--c-stroke); stroke-width: 1.5; transition: all .4s; }
.box text { opacity: .35; transition: opacity .4s; }
.box.on text { opacity: 1; }
.box.owl.on rect { fill: var(--c-owl-bg); stroke: var(--c-owl); }
.box.shacl.on rect { fill: var(--c-shacl-bg); stroke: var(--c-shacl); }
.box.skos.on rect { fill: var(--c-skos-bg); stroke: var(--c-skos); }
.bt { font-size: 20px; font-weight: 700; }
.box.owl .bt { fill: var(--c-owl); } .box.shacl .bt { fill: var(--c-shacl); } .box.skos .bt { fill: var(--c-skos); }
.bq { font-size: 13.5px; fill: var(--c-ink); }
.bo { font-size: 12px; font-family: ui-monospace, Menlo, monospace; fill: var(--c-ink-mod); }

.xl path { fill: none; stroke: var(--c-ink-mod); stroke-width: 2; stroke-dasharray: 4 4; }
.xl circle { fill: var(--c-yellow); stroke: var(--c-navy); stroke-width: 1.5; }
.xl text { text-anchor: middle; font-size: 13px; font-weight: 700; fill: var(--c-navy); }
</style>
