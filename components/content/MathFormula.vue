<template>
  <!-- Block Mode -->
  <div
    v-if="isBlock"
    class="math-formula-wrapper block-mode"
    :class="{ 'loading': loading }"
  >
    <span v-if="loading" class="math-formula-loading">
      <span>Завантаження...</span>
    </span>
    <div
      v-show="!loading"
      ref="blockContainer"
      class="math-formula-content"
    />
    <div ref="blockSource" style="display: none">
      <slot />
    </div>
  </div>

  <!-- Inline Mode -->
  <span
    v-else
    class="math-formula-wrapper"
    :class="{ 'loading': loading }"
  >
    <span v-if="loading" class="math-formula-loading">
      <span>Завантаження...</span>
    </span>
    <span
      v-show="!loading"
      ref="inlineContainer"
      class="math-formula-content"
    />
    <span ref="inlineSource" style="display: none">
      <slot />
    </span>
  </span>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, computed } from 'vue'

const props = defineProps({
  tex: {
    type: String,
    default: ''
  },
  block: {
    type: Boolean,
    default: true
  },
  inline: {
    type: Boolean,
    default: false
  }
})

const isBlock = computed(() => {
  return props.block && !props.inline
})

const blockContainer = ref(null)
const blockSource = ref(null)
const inlineContainer = ref(null)
const inlineSource = ref(null)
const loading = ref(true)

const loadKatex = () => {
  if (window.katex) {
    return Promise.resolve(window.katex)
  }

  // Inject KaTeX CSS
  if (!document.getElementById('katex-css')) {
    const link = document.createElement('link')
    link.id = 'katex-css'
    link.rel = 'stylesheet'
    link.href = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css'
    document.head.appendChild(link)
  }

  // Inject KaTeX JS
  return new Promise((resolve, reject) => {
    const existingScript = document.getElementById('katex-js')
    if (existingScript) {
      existingScript.addEventListener('load', () => resolve(window.katex))
      existingScript.addEventListener('error', reject)
    } else {
      const script = document.createElement('script')
      script.id = 'katex-js'
      script.src = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js'
      script.onload = () => resolve(window.katex)
      script.onerror = reject
      document.head.appendChild(script)
    }
  })
}

const extractTextWithNewlines = (element) => {
  if (!element) return ''
  const clone = element.cloneNode(true)
  // Видаляємо зайві кнопки Docus
  const buttons = clone.querySelectorAll('button, .iconify')
  buttons.forEach((b) => b.remove())
  return clone.textContent || ''
}

const renderFormula = async () => {
  loading.value = true
  await nextTick()

  try {
    const katex = await loadKatex()
    let formulaText = props.tex

    const sourceEl = isBlock.value ? blockSource.value : inlineSource.value
    const containerEl = isBlock.value ? blockContainer.value : inlineContainer.value

    if (!formulaText && sourceEl) {
      formulaText = extractTextWithNewlines(sourceEl).trim()
    }

    if (formulaText && containerEl) {
      katex.render(formulaText, containerEl, {
        displayMode: isBlock.value,
        throwOnError: false
      })
    }
    loading.value = false
  } catch (err) {
    console.error('KaTeX rendering failed:', err)
    const containerEl = isBlock.value ? blockContainer.value : inlineContainer.value
    const sourceEl = isBlock.value ? blockSource.value : inlineSource.value
    if (containerEl) {
      containerEl.textContent = props.tex || (sourceEl ? sourceEl.textContent : '')
    }
    loading.value = false
  }
}

onMounted(() => {
  renderFormula()
})

watch(() => props.tex, renderFormula)
watch(isBlock, renderFormula)
</script>

<style scoped>
.math-formula-wrapper {
  /* Theme variables - Light Mode Default */
  --math-bg: #f9fafb;
  --math-border: #e5e7eb;
  --math-text: #111827;
  --math-text-muted: #6b7280;
}

/* Dark Mode Overrides */
:is(.dark *) .math-formula-wrapper {
  --math-bg: #1c1c1c;
  --math-border: rgba(255, 255, 255, 0.08);
  --math-text: #f3f4f6;
  --math-text-muted: #9ca3af;
}

.math-formula-wrapper.block-mode {
  margin: 1.5rem 0;
  padding: 1.25rem;
  border-radius: 0.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
  background: var(--math-bg) !important;
  border: 1px solid var(--math-border) !important;
}

.math-formula-wrapper:not(.block-mode) {
  display: inline-block;
  margin: 0 0.125rem;
  padding: 0;
  background: transparent !important;
  border: none !important;
}

.math-formula-wrapper.block-mode.loading {
  min-height: 60px;
}

.math-formula-loading {
  color: var(--math-text-muted);
  font-size: 0.875rem;
}

.math-formula-content {
  color: var(--math-text) !important;
}

.math-formula-wrapper.block-mode .math-formula-content {
  overflow-x: auto;
  width: 100%;
  text-align: center;
}

.math-formula-wrapper.block-mode :deep(.katex) {
  font-size: 1.2rem;
}
</style>
