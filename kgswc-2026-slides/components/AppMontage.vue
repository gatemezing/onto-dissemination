<script setup lang="ts">
import { ref } from 'vue'
import { onSlideEnter, onSlideLeave } from '@slidev/client'

/**
 * Plays a muted clip when its slide is entered (from the start), pauses it on leave.
 * Click the video to pause or resume. The poster stands in for the video in the PDF export.
 * The clip itself is recorded with tools/montage/record.mjs.
 */
const props = defineProps<{ src: string; poster?: string }>()
// Plain string props are not rewritten by Vite, so prefix public paths with the deploy base
// (the deck is served from a sub-path such as /onto-dissemination/kgswc-2026/).
const withBase = (p?: string) => (p && p.startsWith('/') ? import.meta.env.BASE_URL + p.slice(1) : p)
const videoSrc = withBase(props.src)
const posterSrc = withBase(props.poster)
const v = ref<HTMLVideoElement>()
onSlideEnter(() => {
  const el = v.value
  if (!el) return
  el.currentTime = 0
  el.play().catch(() => {})
})
onSlideLeave(() => v.value?.pause())
const toggle = () => {
  const el = v.value
  if (el) el.paused ? el.play().catch(() => {}) : el.pause()
}
</script>

<template>
  <div class="am">
    <video ref="v" :src="videoSrc" :poster="posterSrc" muted playsinline preload="auto" @click="toggle" />
  </div>
</template>

<style scoped>
.am { display: flex; justify-content: center; }
.am video { max-height: 392px; width: auto; max-width: 100%; border-radius: 10px; border: 1px solid var(--c-stroke);
  box-shadow: 0 6px 20px rgba(0, 0, 0, .12); cursor: pointer; background: #004493; }
</style>
