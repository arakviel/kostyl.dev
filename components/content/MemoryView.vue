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
  }
})

// Convert all data to hex strings and calculate rows
const rows = computed(() => {
  const bytes = props.data.map(b => {
    if (typeof b === 'number') return b.toString(16).padStart(2, '0').toUpperCase()
    return b.toString().padStart(2, '0').toUpperCase()
  })

  const result = []
  const baseAddr = parseInt(props.startAddress, 16) || 0

  for (let i = 0; i < bytes.length; i += props.rowSize) {
    const rowBytes = bytes.slice(i, i + props.rowSize)
    const addr = (baseAddr + i).toString(16).padStart(8, '0').toUpperCase()
    
    // ASCII representation
    const ascii = rowBytes.map(hex => {
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

const isHighlighted = (index) => props.highlight.includes(index)
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
            Hex Dump / ASCII
        </div>
    </div>
    
    <!-- Hex Table -->
    <div class="p-4 font-mono text-[12px] leading-relaxed overflow-x-auto whitespace-pre memory-body">
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
            Offset: {{ data.length }} bytes
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
