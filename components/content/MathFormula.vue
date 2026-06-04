<template>
  <div class="math-formula-wrapper" :class="{ 'block-mode': block, 'loading': loading }">
    <div v-if="loading" class="math-formula-loading">
      <span>Завантаження формули...</span>
    </div>
    <div v-show="!loading" ref="mathContainer" class="math-formula-content"></div>
    <div ref="source" style="display: none">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'

const props = defineProps({
  tex: {
    type: String,
    default: ''
  },
  block: {
    type: Boolean,
    default: true
  }
})

const mathContainer = ref(null)
const source = ref(null)
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

    if (!formulaText && source.value) {
      formulaText = extractTextWithNewlines(source.value).trim()
    }

    if (formulaText) {
      katex.render(formulaText, mathContainer.value, {
        displayMode: props.block,
        throwOnError: false
      })
    }
    loading.value = false
  } catch (err) {
    console.error('KaTeX rendering failed:', err)
    if (mathContainer.value) {
      mathContainer.value.textContent = props.tex || (source.value ? source.value.textContent : '')
    }
    loading.value = false
  }
}

onMounted(() => {
  renderFormula()
})

watch(() => props.tex, renderFormula)
watch(() => props.block, renderFormula)
</script>

<style scoped>
.math-formula-wrapper {
  margin: 1.5rem 0;
  padding: 1.25rem;
  border-radius: 0.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;

  /* Theme variables - Light Mode Default */
  --math-bg: #f9fafb;
  --math-border: #e5e7eb;
  --math-text: #111827;
  --math-text-muted: #6b7280;

  background: var(--math-bg) !important;
  border: 1px solid var(--math-border) !important;
}

/* Dark Mode Overrides */
:is(.dark *) .math-formula-wrapper {
  --math-bg: #1c1c1c;
  --math-border: rgba(255, 255, 255, 0.08);
  --math-text: #f3f4f6;
  --math-text-muted: #9ca3af;
}

.math-formula-wrapper.loading {
  min-height: 60px;
}

.math-formula-loading {
  color: var(--math-text-muted);
  font-size: 0.875rem;
}

.math-formula-content {
  overflow-x: auto;
  width: 100%;
  text-align: center;
  color: var(--math-text) !important;
}

:deep(.katex) {
  font-size: 1.2rem;
}
</style>
