<script setup lang="ts">
import { computed, nextTick, ref } from 'vue'
import { onSlideEnter } from '@slidev/client'

/**
 * The agenda drawn as a railway line: one station per section, a train at the current one.
 * current: index of the active section (-1 on the agenda slide itself).
 * reveal:  how many stations are visible (for click-by-click build-up on the agenda slide).
 * onDark:  white text, for the navy section slides.
 */
const props = withDefaults(defineProps<{ current?: number; reveal?: number; onDark?: boolean }>(), {
  current: -1, reveal: 99, onDark: false,
})

const stations = [
  { t: 'ERA Ontology context', s: 'registers, KG, TEL TSI', m: '≈ 4.5 min' },
  { t: 'Objective of the paper', s: 'three kinds of semantics', m: '≈ 2.5 min' },
  { t: 'Contributions', s: 'xsd2rdf and the extension', m: '≈ 5.5 min' },
  { t: 'Results', s: 'coverage, quality, CQs', m: '≈ 3 min' },
  { t: 'Future work', s: 'towards v4.0.0', m: '≈ 3.5 min' },
]
const X = (i: number) => 100 + i * 180
const trainAt = ref(props.current < 0 ? 0 : props.current)
const animate = ref(false)

onSlideEnter(async () => {
  if (props.current <= 0) return
  animate.value = false
  trainAt.value = props.current - 1
  await nextTick()
  requestAnimationFrame(() => requestAnimationFrame(() => { animate.value = true; trainAt.value = props.current }))
})

const trainX = computed(() => X(trainAt.value))
const sleepers = Array.from({ length: 44 }, (_, i) => 30 + i * 20)
</script>

<template>
  <svg viewBox="0 0 920 230" class="rail" :class="{ dark: onDark }">
    <!-- track: two rails and sleepers, echoing the stripes of the ERA logo -->
    <g class="sleepers"><line v-for="x in sleepers" :key="x" :x1="x" :x2="x" y1="74" y2="106" /></g>
    <line x1="20" x2="900" y1="82" y2="82" class="rail-a" />
    <line x1="20" x2="900" y1="98" y2="98" class="rail-b" />

    <!-- train -->
    <g class="train" :class="{ anim: animate }" :style="{ transform: `translate(${trainX - 34}px, 40px)` }">
      <rect x="0" y="0" width="68" height="26" rx="7" class="car" />
      <path d="M68 4 h6 a6 6 0 0 1 6 6 v12 h-12 z" class="nose" />
      <rect x="8" y="6" width="14" height="9" rx="2" class="win" />
      <rect x="27" y="6" width="14" height="9" rx="2" class="win" />
      <rect x="46" y="6" width="14" height="9" rx="2" class="win" />
      <rect x="0" y="20" width="80" height="3" class="stripe" />
    </g>

    <g v-for="(st, i) in stations" :key="i" class="st" :class="{ on: i === current, past: current >= 0 && i < current, hide: i >= reveal }">
      <circle :cx="X(i)" cy="90" r="17" class="dot" />
      <text :x="X(i)" y="96" class="num">{{ i + 1 }}</text>
      <text :x="X(i)" y="140" class="tt">{{ st.t }}</text>
      <text :x="X(i)" y="161" class="ss">{{ st.s }}</text>
      <text :x="X(i)" y="184" class="mm">{{ st.m }}</text>
    </g>
  </svg>
</template>

<style scoped>
.rail { width: 100%; height: auto; font-family: var(--era-font); }
.sleepers line { stroke: var(--c-stroke); stroke-width: 5; }
.rail-a { stroke: var(--c-blue); stroke-width: 5; stroke-linecap: round; }
.rail-b { stroke: var(--c-grey); stroke-width: 5; stroke-linecap: round; }
.dark .sleepers line { stroke: rgba(255,255,255,.16); }
.dark .rail-a { stroke: #7FA8F0; }
.dark .rail-b { stroke: #9AA3B5; }

.train.anim { transition: transform 1.3s cubic-bezier(.45, 0, .25, 1); }
.car { fill: var(--c-yellow); stroke: var(--c-navy); stroke-width: 2; }
.nose { fill: var(--c-yellow); stroke: var(--c-navy); stroke-width: 2; }
.win { fill: var(--c-navy); }
.stripe { fill: var(--c-blue); }

.st { transition: opacity .4s; }
.st.hide { opacity: 0; }
.dot { fill: var(--c-bg); stroke: var(--c-blue); stroke-width: 4; }
.num { text-anchor: middle; font-weight: 700; font-size: 17px; fill: var(--c-blue); }
.st.past .dot { fill: var(--c-blue); }
.st.past .num { fill: #fff; }
.st.on .dot { fill: var(--c-yellow); stroke: var(--c-navy); }
.st.on .num { fill: var(--c-navy); }
.tt { text-anchor: middle; font-weight: 700; font-size: 16px; fill: var(--c-heading); }
.ss { text-anchor: middle; font-size: 13px; fill: var(--c-ink-mod); }
.mm { text-anchor: middle; font-size: 12px; fill: var(--c-ink-subtle); font-variant-numeric: tabular-nums; }
.dark .dot { fill: var(--c-navy); stroke: #7FA8F0; }
.dark .num { fill: #CFE0FF; }
.dark .st.past .dot { fill: #7FA8F0; }
.dark .st.past .num { fill: var(--c-navy); }
.dark .st.on .dot { fill: var(--c-yellow); stroke: #fff; }
.dark .st.on .num { fill: var(--c-navy); }
.dark .tt { fill: #fff; }
.dark .ss { fill: #B9C6E0; }
.dark .mm { fill: #8EA0C4; }
.dark .st:not(.on) .tt { fill: #B9C6E0; }
</style>
