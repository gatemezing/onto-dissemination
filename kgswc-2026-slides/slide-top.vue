<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
// slide-top renders inside every slide, live and in export, so it reads that slide's own layout and number
const { $frontmatter, $page, $nav } = useSlideContext()
const currentLayout = computed(() => $frontmatter.layout ?? 'default')
const hideLogo = computed(() => !!$frontmatter.hideLogo)
const currentPage = $page
const total = computed(() => $nav.value.total)
</script>

<template>
  <!-- ERA Ontology logo on content slides: white version in light mode, blue version in dark mode -->
  <div v-if="currentLayout !== 'cover' && currentLayout !== 'section' && !hideLogo" class="abs-tr mt-2 mr-4 era-top-logo">
    <img src="/assets/era-ontology-logo-white.png" class="dark:hidden" alt="ERA Ontology · Interoperable by Design" />
    <img src="/assets/era-ontology-logo-blue.png" class="hidden dark:block" alt="ERA Ontology · Interoperable by Design" />
  </div>
  <!-- footer: event and page number -->
  <div v-if="currentLayout !== 'cover'" class="abs-bl mb-3 ml-6 era-foot" :class="{ 'on-section': currentLayout === 'section' }">
    KGSWC 2026 · ERA Ontology telematics extension
  </div>
  <div v-if="currentLayout !== 'cover'" class="abs-br mb-3 mr-6 era-foot" :class="{ 'on-section': currentLayout === 'section' }">
    {{ currentPage }} / {{ total }}
  </div>
</template>

<style>
.era-top-logo { z-index: 10; }
.era-top-logo img { height: 52px; border-radius: 4px; }
.era-foot { z-index: 10; font-size: 11px; letter-spacing: .04em; color: var(--c-ink-subtle); }
.era-foot.on-section { color: #9FB4DA; }
</style>
