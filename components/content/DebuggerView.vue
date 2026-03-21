<script setup>
defineProps({
  title: {
    type: String,
    default: 'Locals',
  },
  /**
   * Array of variable objects:
   * [{ name: 'count', type: 'int', value: '42' }, ...]
   */
  variables: {
    type: Array,
    default: () => [],
  }
})
</script>

<template>
  <div class="my-8 rounded-xl shadow-2xl overflow-hidden not-prose transition-all duration-300 debugger-window">
    <!-- macOS Utility Header -->
    <div class="px-4 py-2.5 border-b flex items-center justify-between select-none debugger-header">
        <div class="flex items-center gap-2">
            <!-- Simple dots icon -->
            <div class="flex gap-1.5 mr-2">
                <div class="w-2.5 h-2.5 rounded-full bg-gray-300 dark:bg-gray-600 opacity-50"></div>
                <div class="w-2.5 h-2.5 rounded-full bg-gray-300 dark:bg-gray-600 opacity-50"></div>
                <div class="w-2.5 h-2.5 rounded-full bg-gray-300 dark:bg-gray-600 opacity-50"></div>
            </div>
            <h5 class="text-[11px] font-bold uppercase tracking-widest m-0 leading-none debugger-heading">
                {{ title }}
            </h5>
        </div>
        
        <!-- Search placeholder -->
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
    
    <!-- Variables Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse font-mono text-[12.5px] leading-tight debugger-table">
        <thead>
          <tr class="border-b font-sans uppercase text-[9px] tracking-[0.2em] font-black">
            <th class="px-5 py-2.5 whitespace-nowrap">Name</th>
            <th class="px-5 py-2.5 whitespace-nowrap border-l">Type</th>
            <th class="px-5 py-2.5 w-full border-l">Value</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-white/5">
          <tr v-for="(v, i) in variables" :key="i" class="transition-colors group debugger-row">
            <td class="px-5 py-2.5 font-bold whitespace-nowrap debugger-name">
                <span class="opacity-30 mr-1.5 text-[9px]">◢</span>{{ v.name }}
            </td>
            <td class="px-5 py-2.5 whitespace-nowrap border-l italic opacity-80 debugger-type">
                {{ v.type }}
            </td>
            <td class="px-5 py-2.5 border-l break-all debugger-value">
                <span v-if="v.type === 'string' || v.type === 'char'" class="val-string">"{{ v.value }}"</span>
                <span v-else-if="v.type === 'bool'" class="val-bool font-bold italic">{{ v.value }}</span>
                <span v-else class="val-num">{{ v.value }}</span>
            </td>
          </tr>
          
          <!-- Empty State -->
          <tr v-if="variables.length === 0">
              <td colspan="3" class="px-5 py-12 text-center text-gray-400 dark:text-gray-600 italic font-sans text-sm">
                  No variables in current scope
              </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Footer / Status Bar (Optional) -->
    <div class="px-4 py-1.5 border-t flex items-center gap-4 opacity-40 select-none debugger-header text-[10px] font-bold uppercase tracking-wider">
        <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
            Running
        </div>
        <div class="font-mono text-[9px]">Process: 12842</div>
    </div>
  </div>
</template>

<style scoped>
    .debugger-window {
        --debugger-bg: #ffffff;
        --debugger-header: #f3f4f6;
        --debugger-border: #e4e4e7;
        --debugger-heading: #6b7280;
        --debugger-row-hover: rgba(59, 130, 246, 0.05);
        --debugger-text: #27272a;
        --debugger-name: #2563eb;
        --debugger-type: #7c3aed;
        --debugger-val-str: #059669;
        --debugger-val-num: #1d4ed8;
        --debugger-val-bool: #d97706;

        background-color: var(--debugger-bg) !important;
        border: 1px solid var(--debugger-border) !important;
    }

    :is(.dark *) .debugger-window {
        --debugger-bg: #1c1c1c;
        --debugger-header: #2d2e32;
        --debugger-border: rgba(255, 255, 255, 0.08);
        --debugger-heading: #9ca3af;
        --debugger-row-hover: rgba(59, 130, 246, 0.08);
        --debugger-text: #f8f8f2;
        --debugger-name: #60a5fa;
        --debugger-type: #c084fc;
        --debugger-val-str: #4ade80;
        --debugger-val-num: #93c5fd;
        --debugger-val-bool: #fbbf24;
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

    .debugger-table th {
        background-color: rgba(0,0,0,0.02) !important;
        color: var(--debugger-heading) !important;
        border-color: var(--debugger-border) !important;
    }
    .dark .debugger-table th {
        background-color: rgba(255,255,255,0.03) !important;
    }

    /* Reset prose */
    :deep(tr), :deep(td), :deep(th) {
        margin: 0 !important;
        border-top: none !important;
        border-color: var(--debugger-border) !important;
    }
    
    :deep(.divide-y > *) {
        border-color: var(--debugger-border) !important;
    }

    table { border-spacing: 0; }
</style>
