<template>
  <div class="ascii-diagram-wrapper not-prose my-8">
    <div 
      class="ascii-diagram-container relative overflow-hidden border border-gray-200 dark:border-white/5 rounded-xl bg-white dark:bg-[#111113] shadow-sm"
      :class="{ 'p-6': !frame, 'p-0': frame }"
    >
      <!-- Frame Header (optional) -->
      <div v-if="frame === 'macos' || frame === 'browser'" class="bg-[#dee1e6] dark:bg-[#2d2e32] flex flex-col gap-0 select-none border-b border-gray-200/50 dark:border-white/5">
        <div class="flex items-center px-4 h-10 relative">
          <div class="flex gap-2 items-center z-10">
            <div class="w-3 h-3 rounded-full bg-[#ff5f56] border-[0.5px] border-black/10"></div>
            <div class="w-3 h-3 rounded-full bg-[#ffbd2e] border-[0.5px] border-black/10"></div>
            <div class="w-3 h-3 rounded-full bg-[#27c93f] border-[0.5px] border-black/10"></div>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex items-center justify-center p-8">
        <div class="text-sm text-gray-500 dark:text-gray-400">Завантаження діаграми...</div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="p-6 text-red-600 dark:text-red-400">
        <div class="font-semibold mb-2">Помилка рендерингу:</div>
        <pre class="text-xs">{{ error }}</pre>
      </div>

      <!-- SVG Content (svgbob mode) -->
      <div 
        v-else-if="useSvgbob && svgContent"
        class="ascii-svg-content overflow-x-auto"
        :class="[
          frame ? 'p-6' : '',
          themeClass
        ]"
        v-html="svgContent"
      ></div>

      <!-- Plain ASCII Content (fallback) -->
      <div 
        v-else
        class="ascii-content font-mono text-sm leading-relaxed whitespace-pre overflow-x-auto"
        :class="[
          frame ? 'p-6' : '',
          themeClass
        ]"
        v-html="renderedContent"
      ></div>

      <!-- Hidden slot for content extraction -->
      <div ref="source" style="display: none">
        <slot />
      </div>
    </div>

    <!-- Caption -->
    <figcaption v-if="caption" class="text-center text-[13px] text-gray-500 dark:text-gray-400 font-medium mt-3">
      {{ caption }}
    </figcaption>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'

const props = defineProps({
  caption: {
    type: String,
    default: ''
  },
  theme: {
    type: String,
    default: 'default', // 'default', 'danger', 'warning', 'success', 'info'
    validator: (value) => ['default', 'danger', 'warning', 'success', 'info'].includes(value)
  },
  frame: {
    type: String,
    default: '', // '', 'macos', 'browser'
    validator: (value) => ['', 'macos', 'browser'].includes(value)
  },
  highlight: {
    type: Array,
    default: () => [] // Масив рядків для підсвічування
  },
  useSvgbob: {
    type: Boolean,
    default: true // За замовчуванням використовуємо svgbob
  }
})

const source = ref(null)
const renderedContent = ref('')
const svgContent = ref('')
const loading = ref(true)
const error = ref('')

// Витягування тексту з slot
const extractTextWithNewlines = (element) => {
  if (!element) return ''
  
  const clone = element.cloneNode(true)
  
  // Видаляємо кнопки та іконки
  const buttons = clone.querySelectorAll('button, .iconify')
  buttons.forEach((b) => b.remove())
  
  // Додаємо перенос рядка після блочних елементів
  const blockTags = ['p', 'div', 'pre', 'br', 'li', 'tr']
  blockTags.forEach((tag) => {
    const elements = clone.querySelectorAll(tag)
    elements.forEach((el) => {
      el.after(document.createTextNode('\n'))
    })
  })
  
  return clone.textContent || ''
}

// Обробка ASCII тексту (fallback без svgbob)
const processAsciiText = (text) => {
  if (!text) return ''
  
  // Декодуємо HTML сутності
  const txt = document.createElement('textarea')
  txt.innerHTML = text
  let processed = txt.value.trim()
  
  // Підсвічування ключових слів
  if (props.highlight.length > 0) {
    props.highlight.forEach(word => {
      const regex = new RegExp(`(${word})`, 'g')
      processed = processed.replace(regex, '<span class="ascii-highlight">$1</span>')
    })
  }
  
  // Екрануємо HTML (крім наших span тегів)
  processed = processed
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/&lt;span class="ascii-highlight"&gt;/g, '<span class="ascii-highlight">')
    .replace(/&lt;\/span&gt;/g, '</span>')
  
  return processed
}

// Перевірка чи містить текст кирилицю
const hasCyrillic = (text) => {
  return /[а-яА-ЯіІїЇєЄґҐ]/.test(text)
}

// Рендеринг через svgbob
const renderWithSvgbob = async (text) => {
  try {
    // Якщо є кирилиця, використовуємо fallback
    if (hasCyrillic(text)) {
      console.warn('Svgbob не підтримує кирилицю, використовується текстовий режим')
      return null // Поверне null, щоб використати fallback
    }
    
    // Динамічний імпорт bob-wasm
    const Bob = (await import('bob-wasm')).default
    
    // Завантажуємо WASM модуль (потрібно викликати один раз)
    await Bob.loadWASM()
    
    // Конвертуємо ASCII → SVG
    const svg = Bob.render(text)
    
    // Застосовуємо тему до SVG
    const styledSvg = applySvgTheme(svg)
    
    return styledSvg
  } catch (err) {
    console.error('Svgbob render error:', err)
    throw err
  }
}

// Застосування теми до SVG
const applySvgTheme = (svg) => {
  // Кольори для світлої та темної теми
  const themeColors = {
    default: { 
      light: { stroke: '#374151', fill: '#374151', text: '#1f2937' },
      dark: { stroke: '#d1d5db', fill: '#d1d5db', text: '#e5e7eb' }
    },
    danger: { 
      light: { stroke: '#dc2626', fill: '#dc2626', text: '#991b1b' },
      dark: { stroke: '#f87171', fill: '#f87171', text: '#fca5a5' }
    },
    warning: { 
      light: { stroke: '#ea580c', fill: '#ea580c', text: '#c2410c' },
      dark: { stroke: '#fb923c', fill: '#fb923c', text: '#fdba74' }
    },
    success: { 
      light: { stroke: '#16a34a', fill: '#16a34a', text: '#15803d' },
      dark: { stroke: '#4ade80', fill: '#4ade80', text: '#86efac' }
    },
    info: { 
      light: { stroke: '#2563eb', fill: '#2563eb', text: '#1e40af' },
      dark: { stroke: '#60a5fa', fill: '#60a5fa', text: '#93c5fd' }
    }
  }
  
  const colors = themeColors[props.theme] || themeColors.default
  
  // Замінюємо кольори у SVG для світлої теми (за замовчуванням)
  let styledSvg = svg
    .replace(/stroke="[^"]*"/g, `stroke="${colors.light.stroke}"`)
    .replace(/fill="black"/g, `fill="${colors.light.fill}"`)
  
  // Додаємо font-family для підтримки кирилиці
  styledSvg = styledSvg.replace(
    /<svg/,
    '<svg style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, \'Helvetica Neue\', Arial, sans-serif;"'
  )
  
  // Додаємо класи для темної теми через CSS змінні
  styledSvg = styledSvg.replace(
    /<svg/,
    `<svg class="ascii-svg" data-theme="${props.theme}"`
  )
  
  // Додаємо responsive атрибути
  styledSvg = styledSvg.replace(/<svg/, '<svg class="w-full h-auto"')
  
  return styledSvg
}

// Класи для тем
const themeClass = computed(() => {
  const themes = {
    default: 'text-gray-700 dark:text-gray-300',
    danger: 'text-red-600 dark:text-red-400',
    warning: 'text-orange-600 dark:text-orange-400',
    success: 'text-green-600 dark:text-green-400',
    info: 'text-blue-600 dark:text-blue-400'
  }
  return themes[props.theme] || themes.default
})

onMounted(async () => {
  await nextTick()
  
  try {
    if (source.value) {
      const text = extractTextWithNewlines(source.value)
      
      if (!text) {
        loading.value = false
        return
      }
      
      if (props.useSvgbob) {
        // Використовуємо svgbob для рендерингу
        const svg = await renderWithSvgbob(text)
        
        if (svg) {
          // SVG успішно згенеровано
          svgContent.value = svg
        } else {
          // Fallback для кирилиці або помилки
          renderedContent.value = processAsciiText(text)
        }
      } else {
        // Fallback: простий текстовий рендеринг
        renderedContent.value = processAsciiText(text)
      }
      
      loading.value = false
    }
  } catch (err) {
    console.error('ASCII diagram render error:', err)
    error.value = err.message
    loading.value = false
    
    // Fallback до простого тексту при помилці
    if (source.value) {
      const text = extractTextWithNewlines(source.value)
      renderedContent.value = processAsciiText(text)
    }
  }
})
</script>

<script>
export default {
  name: 'AsciiDiagram'
}
</script>

<style scoped>
.ascii-diagram-wrapper {
  width: 100%;
}

.ascii-content {
  tab-size: 4;
  -moz-tab-size: 4;
}

.ascii-content :deep(.ascii-highlight) {
  background: rgba(59, 130, 246, 0.1);
  color: rgb(59, 130, 246);
  padding: 0 2px;
  border-radius: 2px;
  font-weight: 600;
}

.dark .ascii-content :deep(.ascii-highlight) {
  background: rgba(96, 165, 250, 0.15);
  color: rgb(96, 165, 250);
}

/* SVG Content Styling */
.ascii-svg-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100px;
}

.ascii-svg-content :deep(svg) {
  max-width: 100%;
  height: auto;
}

/* Темна тема для SVG - перевизначаємо кольори */
.dark .ascii-svg-content :deep(svg[data-theme="default"]) {
  --svg-stroke: #d1d5db;
  --svg-fill: #d1d5db;
  --svg-text: #e5e7eb;
}

.dark .ascii-svg-content :deep(svg[data-theme="default"] path),
.dark .ascii-svg-content :deep(svg[data-theme="default"] line),
.dark .ascii-svg-content :deep(svg[data-theme="default"] polyline),
.dark .ascii-svg-content :deep(svg[data-theme="default"] rect),
.dark .ascii-svg-content :deep(svg[data-theme="default"] circle) {
  stroke: #d1d5db !important;
}

.dark .ascii-svg-content :deep(svg[data-theme="default"] text) {
  fill: #e5e7eb !important;
}

/* Danger theme - темна тема */
.dark .ascii-svg-content :deep(svg[data-theme="danger"] path),
.dark .ascii-svg-content :deep(svg[data-theme="danger"] line),
.dark .ascii-svg-content :deep(svg[data-theme="danger"] polyline),
.dark .ascii-svg-content :deep(svg[data-theme="danger"] rect),
.dark .ascii-svg-content :deep(svg[data-theme="danger"] circle) {
  stroke: #f87171 !important;
}

.dark .ascii-svg-content :deep(svg[data-theme="danger"] text) {
  fill: #fca5a5 !important;
}

/* Warning theme - темна тема */
.dark .ascii-svg-content :deep(svg[data-theme="warning"] path),
.dark .ascii-svg-content :deep(svg[data-theme="warning"] line),
.dark .ascii-svg-content :deep(svg[data-theme="warning"] polyline),
.dark .ascii-svg-content :deep(svg[data-theme="warning"] rect),
.dark .ascii-svg-content :deep(svg[data-theme="warning"] circle) {
  stroke: #fb923c !important;
}

.dark .ascii-svg-content :deep(svg[data-theme="warning"] text) {
  fill: #fdba74 !important;
}

/* Success theme - темна тема */
.dark .ascii-svg-content :deep(svg[data-theme="success"] path),
.dark .ascii-svg-content :deep(svg[data-theme="success"] line),
.dark .ascii-svg-content :deep(svg[data-theme="success"] polyline),
.dark .ascii-svg-content :deep(svg[data-theme="success"] rect),
.dark .ascii-svg-content :deep(svg[data-theme="success"] circle) {
  stroke: #4ade80 !important;
}

.dark .ascii-svg-content :deep(svg[data-theme="success"] text) {
  fill: #86efac !important;
}

/* Info theme - темна тема */
.dark .ascii-svg-content :deep(svg[data-theme="info"] path),
.dark .ascii-svg-content :deep(svg[data-theme="info"] line),
.dark .ascii-svg-content :deep(svg[data-theme="info"] polyline),
.dark .ascii-svg-content :deep(svg[data-theme="info"] rect),
.dark .ascii-svg-content :deep(svg[data-theme="info"] circle) {
  stroke: #60a5fa !important;
}

.dark .ascii-svg-content :deep(svg[data-theme="info"] text) {
  fill: #93c5fd !important;
}

/* Scrollbar styling */
.ascii-content::-webkit-scrollbar,
.ascii-svg-content::-webkit-scrollbar {
  height: 8px;
}

.ascii-content::-webkit-scrollbar-track,
.ascii-svg-content::-webkit-scrollbar-track {
  background: transparent;
}

.ascii-content::-webkit-scrollbar-thumb,
.ascii-svg-content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.dark .ascii-content::-webkit-scrollbar-thumb,
.dark .ascii-svg-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
}

.ascii-content::-webkit-scrollbar-thumb:hover,
.ascii-svg-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

.dark .ascii-content::-webkit-scrollbar-thumb:hover,
.dark .ascii-svg-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
