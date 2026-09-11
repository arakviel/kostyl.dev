<script setup>
import { computed, ref, onMounted, nextTick } from 'vue'

const mdContentRef = ref(null)
const outputBoxRef = ref(null)

const props = defineProps({
  /**
   * Cell type: 'code' (default), 'markdown', or 'raw'
   */
  type: {
    type: String,
    default: 'code',
    validator: (val) => ['code', 'markdown', 'raw'].includes(val)
  },
  /**
   * Execution counter number, e.g. 1, 2, or '*'
   */
  executionCount: {
    type: [Number, String],
    default: null
  },
  /**
   * Shorthand alias for executionCount
   */
  count: {
    type: [Number, String],
    default: null
  },
  /**
   * Execution status: 'idle', 'running', 'success', 'error'
   */
  status: {
    type: String,
    default: 'idle',
    validator: (val) => ['idle', 'running', 'success', 'error'].includes(val)
  },
  /**
   * Show In [n]: prompt
   */
  showPrompt: {
    type: Boolean,
    default: true
  },
  /**
   * Show Out [n]: prompt for output
   */
  showOutPrompt: {
    type: Boolean,
    default: true
  },
  /**
   * Type of output: 'execute_result' (default, Out[n]:), 'stdout', 'stderr', or 'error'
   */
  outputType: {
    type: String,
    default: 'execute_result',
    validator: (val) => ['execute_result', 'stdout', 'stderr', 'error'].includes(val)
  },
  /**
   * String fallback for output if slot #output is not used
   */
  output: {
    type: String,
    default: ''
  },
  /**
   * Execution time string, e.g. '0.18s'
   */
  executionTime: {
    type: String,
    default: ''
  },
  /**
   * Highlight cell with blue active border
   */
  active: {
    type: Boolean,
    default: false
  },
  /**
   * Collapse output or cell
   */
  collapsed: {
    type: Boolean,
    default: false
  }
})

const resolvedCount = computed(() => {
  if (props.count !== null && props.count !== undefined) return props.count
  if (props.executionCount !== null && props.executionCount !== undefined) return props.executionCount
  return null
})

const inputPromptText = computed(() => {
  if (props.status === 'running') return 'In [*]:'
  if (resolvedCount.value !== null && resolvedCount.value !== '') {
    return `In [${resolvedCount.value}]:`
  }
  return 'In [ ]:'
})

const outputPromptText = computed(() => {
  if (resolvedCount.value !== null && resolvedCount.value !== '') {
    return `Out[${resolvedCount.value}]:`
  }
  return 'Out[ ]:'
})

const isError = computed(() => {
  return props.status === 'error' || props.outputType === 'error' || props.outputType === 'stderr'
})

const isStdout = computed(() => {
  return props.outputType === 'stdout'
})

const parsedTable = computed(() => {
  if (!props.output || typeof props.output !== 'string') return null
  const lines = props.output.trim().split('\n').map(l => l.trim()).filter(Boolean)
  if (lines.length < 2) return null
  if (!lines[0].startsWith('|') || (!lines[1].includes('|---') && !lines[1].includes('|:--') && !lines[1].includes('| ---'))) return null

  const parseLine = (line) => {
    const cells = line.split('|').map(c => c.trim())
    if (cells.length > 0 && cells[0] === '') cells.shift()
    if (cells.length > 0 && cells[cells.length - 1] === '') cells.pop()
    return cells
  }

  const headers = parseLine(lines[0])
  const rows = lines.slice(2).map(parseLine)
  return { headers, rows }
})

/**
 * Dynamic KaTeX loader matching MathFormula.vue CDN source
 */
const loadKatex = () => {
  if (typeof window === 'undefined') return Promise.reject()
  if (window.katex) return Promise.resolve(window.katex)

  if (!document.getElementById('katex-css')) {
    const link = document.createElement('link')
    link.id = 'katex-css'
    link.rel = 'stylesheet'
    link.href = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css'
    document.head.appendChild(link)
  }

  const existingScript = document.getElementById('katex-js')
  if (existingScript) {
    if (window.katex) return Promise.resolve(window.katex)
    return new Promise((resolve, reject) => {
      existingScript.addEventListener('load', () => resolve(window.katex))
      existingScript.addEventListener('error', reject)
      const timer = setInterval(() => {
        if (window.katex) {
          clearInterval(timer)
          resolve(window.katex)
        }
      }, 20)
    })
  }

  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.id = 'katex-js'
    script.src = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js'
    script.onload = () => resolve(window.katex)
    script.onerror = reject
    document.head.appendChild(script)
  })
}

/**
 * Walks text nodes and converts $...$ (inline) and $$...$$ (block) to rendered KaTeX
 */
const renderMathInElement = (rootEl, katex) => {
  if (!rootEl) return
  const text = rootEl.textContent || ''
  if (!text.includes('$')) return

  const walker = document.createTreeWalker(
    rootEl,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode(node) {
        const parent = node.parentElement
        if (!parent) return NodeFilter.FILTER_REJECT
        const tag = parent.tagName.toLowerCase()
        if (['code', 'pre', 'script', 'style', 'textarea'].includes(tag)) return NodeFilter.FILTER_REJECT
        if (parent.closest('.math-formula-content') || parent.closest('.katex')) return NodeFilter.FILTER_REJECT
        return node.nodeValue && node.nodeValue.includes('$') ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT
      }
    }
  )

  const nodesToReplace = []
  let currentNode
  while ((currentNode = walker.nextNode())) {
    nodesToReplace.push(currentNode)
  }

  for (const node of nodesToReplace) {
    const content = node.nodeValue
    if (!content || !content.includes('$')) continue

    const parts = []
    let lastIndex = 0
    const mathRegex = /(\$\$[\s\S]+?\$\$|\$(?:\\\$|[^\$\n])+?\$)/g
    let match

    while ((match = mathRegex.exec(content)) !== null) {
      if (match.index > lastIndex) {
        parts.push(document.createTextNode(content.slice(lastIndex, match.index)))
      }

      const raw = match[0]
      const isDisplay = raw.startsWith('$$')
      const tex = isDisplay ? raw.slice(2, -2).trim() : raw.slice(1, -1).trim()

      try {
        const span = document.createElement('span')
        span.className = isDisplay 
          ? 'inline-block my-1 text-center w-full' 
          : 'inline-math inline-block mx-0.5 align-baseline'
        katex.render(tex, span, {
          displayMode: isDisplay,
          throwOnError: false
        })
        parts.push(span)
      } catch (e) {
        parts.push(document.createTextNode(raw))
      }

      lastIndex = match.index + raw.length
    }

    if (lastIndex < content.length) {
      parts.push(document.createTextNode(content.slice(lastIndex)))
    }

    if (parts.length > 0) {
      const parent = node.parentNode
      if (parent) {
        for (const part of parts) {
          parent.insertBefore(part, node)
        }
        parent.removeChild(node)
      }
    }
  }
}

const renderAllMath = async () => {
  if (typeof window === 'undefined') return
  const target = mdContentRef.value || outputBoxRef.value
  if (!target) return
  if (!target.textContent?.includes('$')) return

  try {
    const katex = await loadKatex()
    if (mdContentRef.value) renderMathInElement(mdContentRef.value, katex)
    if (outputBoxRef.value) renderMathInElement(outputBoxRef.value, katex)
  } catch (err) {
    console.error('KaTeX auto-render in JupyterCell failed:', err)
  }
}

onMounted(() => {
  nextTick(() => {
    renderAllMath()
  })
})
</script>

<template>
  <div 
    class="jupyter-cell not-prose rounded-lg border transition-all duration-200 shadow-2xs relative bg-white dark:bg-[#18181b] overflow-hidden"
    :class="[
      active 
        ? 'border-l-[4px] border-l-blue-500 dark:border-l-blue-400 border-t-gray-200 border-r-gray-200 border-b-gray-200 dark:border-t-neutral-800 dark:border-r-neutral-800 dark:border-b-neutral-800 ring-1 ring-blue-500/15' 
        : 'border-l-[4px] border-l-transparent border-gray-200/90 dark:border-neutral-800 hover:border-l-gray-300 dark:hover:border-l-neutral-700'
    ]"
  >
    <!-- Code Cell Layout -->
    <template v-if="type === 'code'">
      <div class="p-1.5 sm:p-2 space-y-1.5">
        <!-- Input Row -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-start gap-1 sm:gap-2">
          <!-- In Prompt -->
          <div 
            v-if="showPrompt" 
            class="sm:w-16 sm:min-w-[4.25rem] text-left sm:text-right pr-2 pt-1 sm:pt-1.5 font-mono text-[11.5px] sm:text-[12px] select-none font-semibold leading-tight shrink-0"
            :class="[
              status === 'running' 
                ? 'text-amber-500 animate-pulse' 
                : resolvedCount !== null && resolvedCount !== ''
                  ? 'text-[#303f9f] dark:text-[#7aa2f7]'
                  : 'text-gray-400 dark:text-neutral-500'
            ]"
          >
            {{ inputPromptText }}
          </div>
          <div v-else class="sm:w-2 shrink-0"></div>

          <!-- Code Input Box with solid border and editor background -->
          <div 
            class="jupyter-input-box flex-1 min-w-0 bg-[#f8f9fa] dark:bg-[#121316] border border-gray-300 dark:border-neutral-700 rounded overflow-hidden relative shadow-2xs focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-colors"
          >
            <!-- Cell Top Action Bar (Execution time badge only, no copy button) -->
            <div v-if="executionTime" class="absolute right-2 top-1 z-10 flex items-center">
              <span class="text-[10px] font-mono text-gray-400 dark:text-neutral-500 bg-white/90 dark:bg-neutral-900/90 px-1 py-0.2 rounded border border-gray-200 dark:border-neutral-800">
                {{ executionTime }}
              </span>
            </div>

            <!-- Code Content Slot with compact padding and line height -->
            <div class="jupyter-code-content text-[12.5px] sm:text-[13px] leading-snug py-1 px-2.5 sm:py-1.5 sm:px-3 overflow-x-auto font-mono">
              <slot />
            </div>
          </div>
        </div>

        <!-- Output Row -->
        <div 
          v-if="($slots.output || output) && !collapsed" 
          class="flex flex-col sm:flex-row items-stretch sm:items-start gap-1 sm:gap-2 pt-1 border-t border-gray-100 dark:border-neutral-800/60"
        >
          <!-- Out Prompt -->
          <div 
            v-if="showOutPrompt && !isStdout" 
            class="sm:w-16 sm:min-w-[4.25rem] text-left sm:text-right pr-2 pt-0.5 sm:pt-1 font-mono text-[11.5px] sm:text-[12px] select-none font-semibold leading-tight shrink-0"
            :class="isError ? 'text-red-600 dark:text-red-400' : 'text-[#d84315] dark:text-[#ea580c]'"
          >
            {{ outputPromptText }}
          </div>
          <div v-else class="sm:w-16 sm:min-w-[4.25rem] shrink-0"></div>

          <!-- Output Box -->
          <div 
            ref="outputBoxRef"
            class="flex-1 min-w-0 rounded text-[12.5px] sm:text-[13px] overflow-x-auto"
            :class="[
              isError 
                ? 'bg-red-50/80 dark:bg-red-950/20 border border-red-200 dark:border-red-900/40 text-red-900 dark:text-red-300 p-2 font-mono' 
                : 'py-0.5 px-2 text-gray-800 dark:text-gray-200 jupyter-output-clean'
            ]"
          >
            <!-- Error Badge if error -->
            <div v-if="isError" class="flex items-center gap-2 mb-1.5 pb-1 border-b border-red-200 dark:border-red-900/40 text-red-700 dark:text-red-400 font-sans text-xs font-bold uppercase tracking-wider">
              <UIcon name="i-heroicons-exclamation-triangle" class="w-3.5 h-3.5" />
              Traceback / Помилка виконання
            </div>

            <slot name="output">
              <div v-if="parsedTable" class="overflow-x-auto my-1">
                <table>
                  <thead>
                    <tr>
                      <th v-for="(col, ci) in parsedTable.headers" :key="ci">
                        {{ col }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(row, ri) in parsedTable.rows" :key="ri">
                      <td v-for="(cell, ci) in row" :key="ci">
                        {{ cell }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <pre v-else class="font-mono text-xs sm:text-[12.5px] whitespace-pre-wrap leading-snug m-0 p-0">{{ output }}</pre>
            </slot>
          </div>
        </div>
      </div>
    </template>

    <!-- Markdown Cell Layout -->
    <template v-else-if="type === 'markdown'">
      <div class="p-2 sm:p-2.5 flex flex-col sm:flex-row items-stretch sm:items-start gap-1 sm:gap-2">
        <!-- Markdown indicator -->
        <div class="sm:w-16 sm:min-w-[4.25rem] text-left sm:text-right pr-2 pt-0.5 font-mono select-none text-gray-400 dark:text-neutral-500 shrink-0">
          <span class="inline-block px-1.5 py-0.2 rounded text-[10px] font-sans font-semibold uppercase tracking-wide bg-gray-100 dark:bg-neutral-800 text-gray-500 dark:text-neutral-400 border border-gray-200/60 dark:border-neutral-700">
            md
          </span>
        </div>

        <!-- Rendered Markdown Body -->
        <div 
          ref="mdContentRef"
          class="flex-1 min-w-0 text-gray-800 dark:text-gray-200 leading-snug jupyter-md-content pt-0.5"
        >
          <slot />
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
/* Reset Prose & Codeblock styling to prevent nested borders/boxes and remove my-5 margins */
.jupyter-code-content :deep(> div),
.jupyter-code-content :deep(.relative),
.jupyter-code-content :deep(.my-5),
.jupyter-code-content :deep([class*='my-']) {
  margin: 0 !important;
  margin-top: 0 !important;
  margin-bottom: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.jupyter-code-content :deep(pre),
.jupyter-code-content :deep(code),
.jupyter-code-content :deep(.code-block),
.jupyter-code-content :deep([class*='prose-pre']) {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  border-radius: 0 !important;
  margin: 0 !important;
  margin-top: 0 !important;
  margin-bottom: 0 !important;
  padding: 0 !important;
}

.jupyter-code-content :deep(pre) {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: inherit !important;
  line-height: 1.38 !important;
}

.jupyter-code-content :deep(button) {
  display: none !important;
}

:deep(.jupyter-md-content h1),
:deep(.jupyter-md-content h2),
:deep(.jupyter-md-content h3),
:deep(.jupyter-md-content h4) {
  margin-top: 0 !important;
  margin-bottom: 0.25rem !important;
  line-height: 1.25 !important;
}

:deep(.jupyter-md-content p) {
  margin-top: 0 !important;
  margin-bottom: 0.25rem !important;
  line-height: 1.4 !important;
}

:deep(.jupyter-md-content p:last-child) {
  margin-bottom: 0 !important;
}

:deep(.jupyter-md-content ul),
:deep(.jupyter-md-content ol) {
  margin-top: 0 !important;
  margin-bottom: 0.25rem !important;
  padding-left: 1.25rem !important;
}

:deep(.jupyter-md-content li) {
  margin-top: 0 !important;
  margin-bottom: 0.1rem !important;
}

/* Hide any internal copy button from Docus or other layers */
:deep(button.copy-button),
:deep(button[aria-label*="copy" i]),
:deep(button[title*="copy" i]),
:deep(.code-block > div > button),
:deep(.code-block button) {
  display: none !important;
}

/* Pandas DataFrame & HTML Table styling inside Output & Markdown */
.jupyter-output-clean :deep(> div),
.jupyter-output-clean :deep(.relative.my-5),
.jupyter-output-clean :deep([class*='my-']),
.jupyter-md-content :deep(.relative.my-5),
.jupyter-md-content :deep([class*='my-']) {
  margin-top: 0.25rem !important;
  margin-bottom: 0.25rem !important;
}

.jupyter-output-clean :deep(table),
.jupyter-md-content :deep(table) {
  width: auto !important;
  max-width: 100% !important;
  border-collapse: collapse !important;
  margin: 0.25rem 0 !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: 12px !important;
  line-height: 1.4 !important;
  border: 1px solid #e5e7eb !important;
  background-color: #ffffff !important;
  color: #1f2937 !important;
}

.jupyter-output-clean :deep(thead),
.jupyter-md-content :deep(thead) {
  background-color: #f9fafb !important;
}

.jupyter-output-clean :deep(th),
.jupyter-md-content :deep(th) {
  background-color: #f9fafb !important;
  color: #111827 !important;
  font-weight: 700 !important;
  text-align: right !important;
  padding: 5px 12px !important;
  border: 1px solid #e5e7eb !important;
}

.jupyter-output-clean :deep(td),
.jupyter-md-content :deep(td) {
  padding: 4px 12px !important;
  border: 1px solid #e5e7eb !important;
  text-align: right !important;
  color: #374151 !important;
  background-color: #ffffff !important;
}

.jupyter-output-clean :deep(tbody tr:nth-child(even)),
.jupyter-output-clean :deep(tbody tr:nth-child(even) td),
.jupyter-md-content :deep(tbody tr:nth-child(even)),
.jupyter-md-content :deep(tbody tr:nth-child(even) td) {
  background-color: #f9fafb !important;
}

.jupyter-output-clean :deep(tbody tr:hover),
.jupyter-output-clean :deep(tbody tr:hover td),
.jupyter-md-content :deep(tbody tr:hover),
.jupyter-md-content :deep(tbody tr:hover td) {
  background-color: #f3f4f6 !important;
}

/* Dark Mode adaptation for DataFrame / Table */
html.dark .jupyter-output-clean :deep(table),
.dark .jupyter-output-clean :deep(table),
html.dark .jupyter-md-content :deep(table),
.dark .jupyter-md-content :deep(table) {
  border: 1px solid #27272a !important;
  background-color: #121316 !important;
  color: #e4e4e7 !important;
}

html.dark .jupyter-output-clean :deep(thead),
.dark .jupyter-output-clean :deep(thead),
html.dark .jupyter-md-content :deep(thead),
.dark .jupyter-md-content :deep(thead) {
  background-color: #18191d !important;
}

html.dark .jupyter-output-clean :deep(th),
.dark .jupyter-output-clean :deep(th),
html.dark .jupyter-md-content :deep(th),
.dark .jupyter-md-content :deep(th) {
  background-color: #18191d !important;
  color: #f4f4f5 !important;
  border: 1px solid #27272a !important;
}

html.dark .jupyter-output-clean :deep(td),
.dark .jupyter-output-clean :deep(td),
html.dark .jupyter-md-content :deep(td),
.dark .jupyter-md-content :deep(td) {
  color: #d4d4d8 !important;
  border: 1px solid #27272a !important;
  background-color: #121316 !important;
}

html.dark .jupyter-output-clean :deep(tbody tr:nth-child(even)),
.dark .jupyter-output-clean :deep(tbody tr:nth-child(even)),
html.dark .jupyter-output-clean :deep(tbody tr:nth-child(even) td),
.dark .jupyter-output-clean :deep(tbody tr:nth-child(even) td),
html.dark .jupyter-md-content :deep(tbody tr:nth-child(even)),
.dark .jupyter-md-content :deep(tbody tr:nth-child(even)),
html.dark .jupyter-md-content :deep(tbody tr:nth-child(even) td),
.dark .jupyter-md-content :deep(tbody tr:nth-child(even) td) {
  background-color: #18191e !important;
}

html.dark .jupyter-output-clean :deep(tbody tr:hover),
.dark .jupyter-output-clean :deep(tbody tr:hover),
html.dark .jupyter-output-clean :deep(tbody tr:hover td),
.dark .jupyter-output-clean :deep(tbody tr:hover td),
html.dark .jupyter-md-content :deep(tbody tr:hover),
.dark .jupyter-md-content :deep(tbody tr:hover),
html.dark .jupyter-md-content :deep(tbody tr:hover td),
.dark .jupyter-md-content :deep(tbody tr:hover td) {
  background-color: #22242b !important;
}

:deep(img) {
  max-width: 100% !important;
  height: auto !important;
  margin: 0.5rem auto !important;
  border-radius: 6px !important;
}
</style>
