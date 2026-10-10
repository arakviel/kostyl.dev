<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Memory',
  },
  startAddress: {
    type: String,
    default: '0x00000000',
  },
  /**
   * data can be an array of byte values (0-255) or hex strings ('00'-'FF')
   */
  data: {
    type: Array,
    default: () => [],
  },
  /**
   * Array of indices to highlight (red/blue etc.)
   */
  highlight: {
    type: Array,
    default: () => [],
  },
  rowSize: {
    type: Number,
    default: 16,
  },
  bytes: {
    type: Array,
    default: () => null,
  },
  labels: {
    type: Array,
    default: () => null,
  }
})

// Safely resolve data array even if passed as JSON string or invalid format
const parsedData = computed(() => {
  let source = props.bytes || props.data
  if (typeof source === 'string') {
    try {
      source = JSON.parse(source)
    } catch {
      return []
    }
  }
  return Array.isArray(source) ? source : []
})

// Convert all data to hex strings and calculate rows
const rows = computed(() => {
  const sourceData = parsedData.value
  if (!sourceData || sourceData.length === 0) return []

  const bytesMapped = sourceData.map(b => {
    if (b === 'pad') return 'pad'
    if (typeof b === 'number') return b.toString(16).padStart(2, '0').toUpperCase()
    const str = String(b)
    if (str.startsWith('0x')) return str.substring(2).toUpperCase()
    return str.toUpperCase()
  })

  const result = []
  const baseAddr = parseInt(props.startAddress, 16) || 0

  for (let i = 0; i < bytesMapped.length; i += props.rowSize) {
    const rowBytes = bytesMapped.slice(i, i + props.rowSize)
    const addr = (baseAddr + i).toString(16).padStart(8, '0').toUpperCase()
    
    // ASCII representation
    const ascii = rowBytes.map(hex => {
      if (hex === 'pad') return '.'
      const byte = parseInt(hex, 16)
      return (byte >= 32 && byte <= 126) ? String.fromCharCode(byte) : '.'
    }).join('')

    result.push({
      address: `0x${addr}`,
      bytes: rowBytes,
      ascii,
      startIndex: i
    })
  }
  return result
})

const highlightList = computed(() => {
  if (Array.isArray(props.highlight)) return props.highlight
  if (typeof props.highlight === 'number') return [props.highlight]
  if (typeof props.highlight === 'string') {
    try {
      const parsed = JSON.parse(props.highlight)
      if (Array.isArray(parsed)) return parsed
    } catch {}
  }
  return []
})

const isHighlighted = (index) => highlightList.value.includes(index)
</script>

<template>
  <div class="my-8 rounded-xl shadow-2xl overflow-hidden not-prose transition-all duration-300 memory-window">
    <!-- macOS Utility Header -->
    <div class="px-4 py-2.5 border-b flex items-center justify-between select-none memory-header">
        <div class="flex items-center gap-2 font-sans">
            <div class="flex gap-1.5 mr-2">
                <div class="w-2.5 h-2.5 rounded-full bg-gray-300 dark:bg-gray-600 opacity-50"></div>
                <div class="w-2.5 h-2.5 rounded-full bg-gray-300 dark:bg-gray-600 opacity-50"></div>
                <div class="w-2.5 h-2.5 rounded-full bg-gray-300 dark:bg-gray-600 opacity-50"></div>
            </div>
            <h5 class="text-[11px] font-bold uppercase tracking-widest m-0 leading-none memory-heading">
                {{ title }}
            </h5>
        </div>
        <div class="text-[10px] font-mono opacity-40 memory-heading font-bold uppercase tracking-tighter">
            {{ bytes && labels ? 'Memory Layout / Struct Map' : 'Hex Dump / ASCII' }}
        </div>
    </div>
    
    <!-- Byte Grid View (for struct layout) -->
    <div v-if="bytes && labels" class="p-6 memory-body">
      <div class="flex flex-wrap gap-2.5 justify-center sm:justify-start">
        <div 
          v-for="(b, idx) in bytes" 
          :key="idx"
          :class="[
            'flex flex-col items-center justify-between p-2 rounded-lg border text-center font-mono w-[80px] h-[80px] transition-all duration-300',
            b === 'pad' 
              ? 'border-dashed border-gray-300 dark:border-white/10 bg-gray-50/50 dark:bg-white/[0.01] opacity-60' 
              : 'border-blue-500/20 dark:border-blue-500/30 bg-blue-500/[0.01] dark:bg-blue-500/[0.04] hover:border-blue-500/50 hover:scale-[1.03]'
          ]"
        >
          <!-- Cell Header: Offset -->
          <span class="text-[9px] opacity-40 select-none font-bold">+{{ idx }}</span>
          
          <!-- Cell Value: Byte -->
          <span 
            :class="[
              'text-[13px] font-bold tracking-tight',
              b === 'pad' ? 'text-gray-400 dark:text-gray-600 font-normal italic' : 'text-blue-600 dark:text-blue-400'
            ]"
          >
            {{ b === 'pad' ? 'pad' : (b.startsWith('0x') ? b.substring(2) : b) }}
          </span>
          
          <!-- Cell Footer: Label -->
          <span 
            class="text-[8.5px] font-sans truncate w-full px-0.5" 
            :class="labels[idx] === '⬜' ? 'opacity-30' : 'font-bold text-gray-700 dark:text-gray-300'"
            :title="labels[idx]"
          >
            {{ labels[idx] }}
          </span>
        </div>
      </div>
    </div>

    <!-- Hex Table (for traditional Hex Dump) -->
    <div v-else class="p-4 font-mono text-[12px] leading-relaxed overflow-x-auto whitespace-pre memory-body">
      <div v-for="(row, rowIndex) in rows" :key="rowIndex" class="grid grid-cols-[90px_auto_1fr] gap-8 items-center px-4 py-1 hover:bg-black/5 dark:hover:bg-white/5 rounded transition-colors group">
        <!-- Address -->
        <span class="opacity-40 select-none font-bold whitespace-nowrap">{{ row.address }}</span>
        
        <!-- Hex Bytes -->
        <div class="flex gap-2 sm:gap-3 shrink-0">
          <span 
            v-for="(byte, byteIndex) in row.bytes" 
            :key="byteIndex"
            :class="[
                'w-[2ch] text-center transition-all duration-200',
                isHighlighted(row.startIndex + byteIndex) 
                    ? 'text-rose-500 dark:text-rose-400 font-bold scale-110' 
                    : 'opacity-80 group-hover:opacity-100'
            ]"
          >
            {{ byte }}
          </span>
          <!-- Padding for incomplete rows -->
          <span v-for="n in (rowSize - row.bytes.length)" :key="'pad-'+n" class="w-[2ch] opacity-0">00</span>
        </div>
        
        <!-- ASCII -->
        <div class="opacity-30 select-none border-l pl-8 border-current font-medium tracking-widest hidden md:block truncate">
          {{ row.ascii }}
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="rows.length === 0" class="py-12 text-center text-gray-400 dark:text-gray-600 italic font-sans text-sm">
        Empty memory block
      </div>
    </div>

    <!-- Footer -->
    <div class="px-4 py-1.5 border-t flex items-center justify-between opacity-40 select-none memory-header text-[9px] font-bold uppercase tracking-wider">
        <div class="flex items-center gap-1.5">
            Offset: {{ parsedData.length }} bytes
        </div>
        <div class="font-mono">Big Endian</div>
    </div>
  </div>
</template>

<style scoped>
.memory-window {
    --mem-bg: #ffffff;
    --mem-header: #f3f4f6;
    --mem-border: #e4e4e7;
    --mem-text: #27272a;
    --mem-heading: #6b7280;

    background-color: var(--mem-bg) !important;
    border: 1px solid var(--mem-border) !important;
    color: var(--mem-text) !important;
}

:is(.dark *) .memory-window {
    --mem-bg: #1c1c1c;
    --mem-header: #2d2e32;
    --mem-border: rgba(255, 255, 255, 0.08);
    --mem-text: #f8f8f2;
    --mem-heading: #9ca3af;
}

.memory-header {
    background-color: var(--mem-header) !important;
    border-color: var(--mem-border) !important;
}

.memory-heading {
    color: var(--mem-heading) !important;
}

.memory-body {
    background-color: var(--mem-bg) !important;
}
</style>
