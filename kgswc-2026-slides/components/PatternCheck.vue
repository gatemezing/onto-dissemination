<script setup lang="ts">
import { computed, ref } from 'vue'

/**
 * The CompanyCode pattern checked two ways:
 *  - as XSD reads it (patterns are implicitly anchored: the whole value must match),
 *  - as sh:pattern reads the generated, unanchored string (SPARQL REGEX: a match anywhere is enough).
 * The difference is the constraint-fidelity gap of Sect. 4.2 (1.x output); xsd2rdf 2.0 closes it by emitting ^(...)$.
 * Click a sample or type a value.
 */
const pattern = '[0-9A-Z]{4}'
const xsdRe = new RegExp(`^(?:${pattern})$`)
const shRe = new RegExp(pattern)
const samples = [
  { v: '2171', why: 'legacy numeric code' },
  { v: '0071', why: 'legacy numeric code' },
  { v: 'X7K2', why: 'alphanumeric, Organization Code style (illustrative)' },
  { v: '07A', why: 'malformed: 3 characters' },
]
const val = ref('2171')
const why = computed(() => samples.find(x => x.v === val.value)?.why ?? 'your value')
const xsdOk = computed(() => xsdRe.test(val.value))
const shOk = computed(() => shRe.test(val.value))
</script>

<template>
  <div class="pc">
    <div class="row">
      <button v-for="x in samples" :key="x.v" class="smp" :class="{ on: val === x.v }" @click="val = x.v">{{ x.v }}</button>
      <input v-model="val" class="inp" maxlength="12" spellcheck="false" aria-label="Company code to check" />
    </div>
    <div class="why">{{ why }}</div>
    <div class="res">
      <div class="r" :class="xsdOk ? 'ok' : 'ko'">
        <div class="h">XSD <code>pattern</code> · anchored</div>
        <div class="v">{{ xsdOk ? '✓ valid' : '✗ rejected' }}</div>
      </div>
      <div class="r" :class="shOk ? 'ok' : 'ko'">
        <div class="h">generated <code>sh:pattern</code> · xsd2rdf 1.x, unanchored</div>
        <div class="v">{{ shOk ? '✓ conforms' : '✗ violation' }}</div>
      </div>
    </div>
    <div class="gap" :class="{ show: xsdOk !== shOk }">⚠ the two disagree: xsd2rdf 2.0 anchors the pattern as <code>^([0-9A-Z]{4})$</code></div>
  </div>
</template>

<style scoped>
.pc { font-size: 14px; }
.row { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
.smp { font-family: ui-monospace, Menlo, monospace; font-size: 13px; padding: 3px 10px; border-radius: 14px;
  border: 1.5px solid var(--c-stroke); background: var(--c-surface); color: var(--c-ink); cursor: pointer; }
.smp.on { border-color: var(--c-blue); background: var(--c-blue-bg); color: var(--c-blue-strong); font-weight: 700; }
.inp { font-family: ui-monospace, Menlo, monospace; font-size: 13px; width: 86px; padding: 3px 8px; border-radius: 6px;
  border: 1.5px solid var(--c-stroke); background: var(--c-bg); color: var(--c-ink); }
.why { font-size: 12px; color: var(--c-ink-mod); margin: 4px 2px 6px; min-height: 16px; }
.res { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.r { border-radius: 8px; padding: 6px 10px; border: 1.5px solid; }
.r.ok { background: var(--c-good-bg); border-color: var(--c-good); }
.r.ko { background: var(--c-bad-bg); border-color: var(--c-bad); }
.h { font-size: 11.5px; color: var(--c-ink-mod); }
.h code { font-size: 11px; }
.v { font-weight: 700; font-size: 15px; }
.r.ok .v { color: var(--c-good); } .r.ko .v { color: var(--c-bad); }
.gap { margin-top: 6px; font-size: 12.5px; padding: 4px 10px; border-radius: 6px; background: var(--c-warn-bg); color: var(--c-warn-ink);
  opacity: 0; transition: opacity .3s; }
.gap.show { opacity: 1; }
.gap code { font-size: 12px; color: inherit; }
</style>
