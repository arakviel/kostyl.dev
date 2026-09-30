<script setup>
import { computed, useSlots, Comment, Text } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Locals',
  },
  /**
   * Array of variable objects or JSON/relaxed string:
   * [{ name: 'count', type: 'int', value: '42' }, ...]
   */
  variables: {
    type: [Array, String],
    default: () => [],
  },
  /**
   * Indices or variable names to highlight: [0, 2] or "0" or "count"
   */
  highlight: {
    type: [Array, String, Number],
    default: () => [],
  },
  process: {
    type: [String, Number],
    default: '12842',
  },
  status: {
    type: String,
    default: 'Running',
  },
})

const slots = useSlots()

// Helpers to inspect slot VNodes
function containsTable(vnodes) {
  if (!vnodes || !Array.isArray(vnodes)) return false
  for (const v of vnodes) {
    if (!v) continue
    const t = v.type
    if (t === 'table') return true
    if (typeof t === 'string' && t.toLowerCase().includes('table')) return true
    if (typeof t === 'object') {
      const name = t.name || t.__name || ''
      if (name.toLowerCase().includes('table')) return true
      if (t.tag === 'table') return true
    }
    if (Array.isArray(v.children)) {
      if (containsTable(v.children)) return true
    }
  }
  return false
}

function hasActualContent(vnodes) {
  if (!vnodes || !Array.isArray(vnodes)) return false
  return vnodes.some(v => {
    if (!v) return false
    if (v.type === Comment) return false
    if (v.type === Text) {
      return typeof v.children === 'string' && v.children.trim().length > 0
    }
    if (Array.isArray(v.children)) {
      return hasActualContent(v.children)
    }
    return true
  })
}

const hasSlotContent = computed(() => {
  if (!slots.default) return false
  const vnodes = slots.default()
  return hasActualContent(vnodes)
})

const isTableSlot = computed(() => {
  if (!slots.default) return false
  const vnodes = slots.default()
  return containsTable(vnodes)
})

// Robust variables parsing
function parseVariables(input) {
  if (Array.isArray(input)) {
    return input.map(item => {
      if (typeof item === 'object' && item !== null) {
        return {
          name: String(item.name ?? ''),
          type: String(item.type ?? ''),
          value: typeof item.value === 'object' ? JSON.stringify(item.value) : String(item.value ?? ''),
        }
      }
      return { name: String(item), type: '', value: '' }
    })
  }

  if (!input || typeof input !== 'string') return []
  const trimmed = input.trim()
  if (!trimmed) return []

  // 1. Try standard JSON.parse
  try {
    const res = JSON.parse(trimmed)
    if (Array.isArray(res)) return parseVariables(res)
    if (res && typeof res === 'object') return parseVariables([res])
  } catch (e) {}

  // 2. Try relaxed JS evaluation via Function
  try {
    const fn = new Function(`return (${trimmed})`)
    const res = fn()
    if (Array.isArray(res)) return parseVariables(res)
    if (res && typeof res === 'object') return parseVariables([res])
  } catch (e) {}

  // 3. Fallback: Parse object blocks { ... } with regex and token slicing
  try {
    const items = []
    const arrayMatch = trimmed.match(/^\s*\[([\s\S]*)\]\s*$/)
    const content = arrayMatch ? arrayMatch[1] : trimmed

    let depth = 0
    let inQuote = null
    let isEscaped = false
    let startIdx = -1

    for (let i = 0; i < content.length; i++) {
      const char = content[i]
      if (isEscaped) {
        isEscaped = false
        continue
      }
      if (char === '\\') {
        isEscaped = true
        continue
      }
      if (inQuote) {
        if (char === inQuote) inQuote = null
      } else {
        if (char === '"' || char === "'") {
          inQuote = char
        } else if (char === '{') {
          if (depth === 0) startIdx = i
          depth++
        } else if (char === '}') {
          depth--
          if (depth === 0 && startIdx !== -1) {
            const block = content.slice(startIdx + 1, i)
            items.push(extractFields(block))
            startIdx = -1
          }
        }
      }
    }
    if (items.length > 0) return items
  } catch (e) {}

  return []
}

function extractFields(str) {
  const getField = (field) => {
    const pattern = new RegExp(`["\']?${field}["\']?\\s*:\\s*`, 'i')
    const match = pattern.exec(str)
    if (!match) return ''
    const rest = str.slice(match.index + match[0].length).trim()
    if (rest.startsWith('"') || rest.startsWith("'")) {
      const q = rest[0]
      let end = -1
      let esc = false
      for (let j = 1; j < rest.length; j++) {
        if (esc) { esc = false; continue }
        if (rest[j] === '\\') { esc = true; continue }
        if (rest[j] === q) {
          const after = rest.slice(j + 1).trim()
          if (after === '' || after.startsWith(',') || after.startsWith('}')) {
            end = j
            break
          }
        }
      }
      if (end !== -1) {
        return rest.slice(1, end).replace(/\\n/g, '\n').replace(/\\"/g, '"').replace(/\\'/g, "'")
      }
    }
    const nextKey = rest.search(/,\s*["\']?(?:name|type|value)["\']?\s*:/i)
    if (nextKey !== -1) {
      return rest.slice(0, nextKey).trim().replace(/^["\']|["\']$/g, '')
    }
    return rest.trim().replace(/^["\']|["\']$/g, '')
  }

  return {
    name: getField('name'),
    type: getField('type'),
    value: getField('value'),
  }
}

const normalizedVariables = computed(() => {
  return parseVariables(props.variables)
})

const parsedHighlight = computed(() => {
  const h = props.highlight
  if (Array.isArray(h)) return h.map(x => String(x).trim())
  if (typeof h === 'number') return [String(h)]
  if (typeof h === 'string') {
    try {
      const parsed = JSON.parse(h)
      if (Array.isArray(parsed)) return parsed.map(x => String(x).trim())
    } catch (e) {}
    return h.split(',').map(s => s.trim().replace(/^['"\[]|['"\]]$/g, '')).filter(Boolean)
  }
  return []
})

const isHighlighted = (index, name) => {
  const hl = parsedHighlight.value
  return hl.includes(String(index)) || hl.includes(String(name).trim())
}

const isStringVal = (v) => {
  if (!v || !v.type) return false
  const t = v.type.toLowerCase()
  return t.includes('string') || t.includes('char')
}

const isBoolVal = (v) => {
  if (!v) return false
  const t = (v.type || '').toLowerCase()
  const val = String(v.value || '').trim()
  return t === 'bool' || t === 'boolean' || val === 'true' || val === 'false'
}

const isPointerVal = (v) => {
  if (!v) return false
  const t = (v.type || '').toLowerCase()
  const val = String(v.value || '').trim()
  return t.includes('*') || t.includes('ptr') || val.startsWith('0x')
}

const isStructVal = (v) => {
  if (!v) return false
  const val = String(v.value || '').trim()
  return val.startsWith('{') && val.endsWith('}')
}

const formatStringVal = (val) => {
  if (val === undefined || val === null) return '""'
  const str = String(val)
  if ((str.startsWith('"') && str.endsWith('"')) || (str.startsWith("'") && str.endsWith("'"))) {
    return str
  }
  return `"${str}"`
}
</script>

<template>
  <div class="my-8 rounded-xl shadow-2xl overflow-hidden not-prose transition-all duration-300 debugger-window">
    <!-- macOS Utility Header -->
    <div class="px-4 py-2.5 border-b flex items-center justify-between select-none debugger-header">
      <div class="flex items-center gap-2">
        <!-- Simple dots icon -->
        <div class="flex gap-1.5 mr-2">
          <div class="w-2.5 h-2.5 rounded-full bg-red-400 dark:bg-red-500/80 opacity-70"></div>
          <div class="w-2.5 h-2.5 rounded-full bg-amber-400 dark:bg-amber-500/80 opacity-70"></div>
          <div class="w-2.5 h-2.5 rounded-full bg-emerald-400 dark:bg-emerald-500/80 opacity-70"></div>
        </div>
        <h5 class="text-[11px] font-bold uppercase tracking-widest m-0 leading-none debugger-heading">
          {{ title }}
        </h5>
      </div>
      
      <!-- Search / Filter indicator -->
      <div class="flex items-center gap-2 opacity-30 debugger-heading">
        <div class="text-[10px] font-sans font-bold uppercase">Filter</div>
        <div class="w-3 h-3">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.3-4.3" />
          </svg>
        </div>
      </div>
    </div>
    
    <!-- Mode 1: Markdown Table inside slot -->
    <div v-if="isTableSlot" class="overflow-x-auto debugger-slot-wrapper">
      <slot />
    </div>

    <!-- Mode 2: Custom child rows (:debugger-var) inside slot -->
    <div v-else-if="hasSlotContent" class="overflow-x-auto">
      <table class="w-full text-left border-collapse font-mono text-[12.5px] leading-tight debugger-table">
        <thead>
          <tr class="border-b font-sans uppercase text-[9px] tracking-[0.2em] font-black">
            <th class="px-5 py-2.5 whitespace-nowrap">Name</th>
            <th class="px-5 py-2.5 whitespace-nowrap border-l">Type</th>
            <th class="px-5 py-2.5 w-full border-l">Value</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-white/5">
          <slot />
        </tbody>
      </table>
    </div>

    <!-- Mode 3: Variables prop (default / standard) -->
    <div v-else class="overflow-x-auto">
      <table class="w-full text-left border-collapse font-mono text-[12.5px] leading-tight debugger-table">
        <thead>
          <tr class="border-b font-sans uppercase text-[9px] tracking-[0.2em] font-black">
            <th class="px-5 py-2.5 whitespace-nowrap">Name</th>
            <th class="px-5 py-2.5 whitespace-nowrap border-l">Type</th>
            <th class="px-5 py-2.5 w-full border-l">Value</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-white/5">
          <tr 
            v-for="(v, i) in normalizedVariables" 
            :key="i" 
            class="transition-colors group debugger-row"
            :class="{ 'debugger-row-highlight': isHighlighted(i, v.name) }"
          >
            <td class="px-5 py-2.5 font-bold whitespace-nowrap debugger-name">
              <span class="opacity-30 mr-1.5 text-[9px]">◢</span><span class="whitespace-pre">{{ v.name }}</span>
            </td>
            <td class="px-5 py-2.5 whitespace-nowrap border-l italic opacity-80 debugger-type">
              {{ v.type }}
            </td>
            <td class="px-5 py-2.5 border-l break-all debugger-value whitespace-pre-wrap">
              <span v-if="isStringVal(v)" class="val-string">{{ formatStringVal(v.value) }}</span>
              <span v-else-if="isBoolVal(v)" class="val-bool font-bold italic">{{ v.value }}</span>
              <span v-else-if="isPointerVal(v)" class="val-pointer font-bold">{{ v.value }}</span>
              <span v-else-if="isStructVal(v)" class="val-struct">{{ v.value }}</span>
              <span v-else class="val-num">{{ v.value }}</span>
            </td>
          </tr>
          
          <!-- Empty State -->
          <tr v-if="normalizedVariables.length === 0">
            <td colspan="3" class="px-5 py-12 text-center text-gray-400 dark:text-gray-600 italic font-sans text-sm">
              No variables in current scope
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Footer / Status Bar -->
    <div class="px-4 py-1.5 border-t flex items-center justify-between opacity-50 select-none debugger-header text-[10px] font-bold uppercase tracking-wider">
      <div class="flex items-center gap-1.5">
        <div class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
        {{ status }}
      </div>
      <div class="font-mono text-[9px]">Process: {{ process }}</div>
    </div>
  </div>
</template>

<style scoped>
  .debugger-window {
    --debugger-bg: #ffffff;
    --debugger-header: #f8fafc;
    --debugger-border: #e2e8f0;
    --debugger-heading: #64748b;
    --debugger-row-hover: rgba(59, 130, 246, 0.05);
    --debugger-text: #1e293b;
    --debugger-name: #2563eb;
    --debugger-type: #7c3aed;
    --debugger-val-str: #059669;
    --debugger-val-num: #1d4ed8;
    --debugger-val-bool: #d97706;
    --debugger-val-pointer: #0284c7;
    --debugger-val-struct: #475569;
    --debugger-highlight-bg: rgba(245, 158, 11, 0.12);
    --debugger-highlight-border: #f59e0b;

    background-color: var(--debugger-bg) !important;
    border: 1px solid var(--debugger-border) !important;
  }

  :is(.dark *) .debugger-window {
    --debugger-bg: #18181b;
    --debugger-header: #202024;
    --debugger-border: rgba(255, 255, 255, 0.08);
    --debugger-heading: #9ca3af;
    --debugger-row-hover: rgba(59, 130, 246, 0.08);
    --debugger-text: #f4f4f5;
    --debugger-name: #60a5fa;
    --debugger-type: #c084fc;
    --debugger-val-str: #4ade80;
    --debugger-val-num: #93c5fd;
    --debugger-val-bool: #fbbf24;
    --debugger-val-pointer: #38bdf8;
    --debugger-val-struct: #cbd5e1;
    --debugger-highlight-bg: rgba(245, 158, 11, 0.18);
    --debugger-highlight-border: #fbbf24;
  }

  .debugger-header {
    background-color: var(--debugger-header) !important;
    border-bottom: 1px solid var(--debugger-border) !important;
  }
  .debugger-heading {
    color: var(--debugger-heading) !important;
  }
  .debugger-row:hover {
    background-color: var(--debugger-row-hover) !important;
  }
  .debugger-row-highlight {
    background-color: var(--debugger-highlight-bg) !important;
    box-shadow: inset 3px 0 0 0 var(--debugger-highlight-border);
  }
  .debugger-name {
    color: var(--debugger-name) !important;
  }
  .debugger-type {
    color: var(--debugger-type) !important;
    border-color: var(--debugger-border) !important;
  }
  .debugger-value {
    color: var(--debugger-text) !important;
    border-color: var(--debugger-border) !important;
  }
  
  .val-string { color: var(--debugger-val-str) !important; }
  .val-bool { color: var(--debugger-val-bool) !important; }
  .val-num { color: var(--debugger-val-num) !important; }
  .val-pointer { color: var(--debugger-val-pointer) !important; }
  .val-struct { color: var(--debugger-val-struct) !important; }

  .debugger-table th {
    background-color: rgba(0, 0, 0, 0.02) !important;
    color: var(--debugger-heading) !important;
    border-color: var(--debugger-border) !important;
  }
  :is(.dark *) .debugger-table th {
    background-color: rgba(255, 255, 255, 0.03) !important;
  }

  /* Reset prose and borders */
  :deep(tr), :deep(td), :deep(th) {
    margin: 0 !important;
    border-top: none !important;
    border-color: var(--debugger-border) !important;
  }
  
  :deep(.divide-y > *) {
    border-color: var(--debugger-border) !important;
  }

  table { border-spacing: 0; }

  /* Slot styling for Markdown tables inside ::debugger-view */
  .debugger-slot-wrapper :deep(table) {
    width: 100% !important;
    text-align: left !important;
    border-collapse: collapse !important;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
    font-size: 12.5px !important;
    line-height: 1.25 !important;
    margin: 0 !important;
  }

  .debugger-slot-wrapper :deep(thead) {
    border-bottom: 1px solid var(--debugger-border) !important;
    font-family: inherit !important;
    text-transform: uppercase !important;
    font-size: 9px !important;
    letter-spacing: 0.2em !important;
    font-weight: 900 !important;
  }

  .debugger-slot-wrapper :deep(th) {
    padding: 10px 20px !important;
    white-space: nowrap !important;
    background-color: rgba(0, 0, 0, 0.02) !important;
    color: var(--debugger-heading) !important;
    border-color: var(--debugger-border) !important;
  }

  :is(.dark *) .debugger-slot-wrapper :deep(th) {
    background-color: rgba(255, 255, 255, 0.03) !important;
  }

  .debugger-slot-wrapper :deep(th + th) {
    border-left: 1px solid var(--debugger-border) !important;
  }

  .debugger-slot-wrapper :deep(tbody) {
    border-top: none !important;
  }

  .debugger-slot-wrapper :deep(tbody tr) {
    transition: background-color 0.2s ease !important;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
  }

  :is(.dark *) .debugger-slot-wrapper :deep(tbody tr) {
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
  }

  .debugger-slot-wrapper :deep(tbody tr:last-child) {
    border-bottom: none !important;
  }

  .debugger-slot-wrapper :deep(tbody tr:hover) {
    background-color: var(--debugger-row-hover) !important;
  }

  .debugger-slot-wrapper :deep(tbody td) {
    padding: 10px 20px !important;
    border-top: none !important;
    vertical-align: top !important;
  }

  .debugger-slot-wrapper :deep(tbody td:first-child) {
    font-weight: bold !important;
    white-space: nowrap !important;
    color: var(--debugger-name) !important;
  }

  .debugger-slot-wrapper :deep(tbody td:first-child)::before {
    content: "◢ ";
    opacity: 0.3;
    font-size: 9px;
    margin-right: 6px;
    font-weight: normal;
  }

  .debugger-slot-wrapper :deep(tbody td:nth-child(2)) {
    white-space: nowrap !important;
    border-left: 1px solid var(--debugger-border) !important;
    font-style: italic !important;
    opacity: 0.8 !important;
    color: var(--debugger-type) !important;
  }

  .debugger-slot-wrapper :deep(tbody td:nth-child(3)) {
    border-left: 1px solid var(--debugger-border) !important;
    word-break: break-all !important;
    white-space: pre-wrap !important;
    color: var(--debugger-text) !important;
    width: 100% !important;
  }

  /* Inline code in table cells should inherit colors cleanly */
  .debugger-slot-wrapper :deep(code) {
    background: transparent !important;
    padding: 0 !important;
    font-size: inherit !important;
    color: inherit !important;
  }
</style>
