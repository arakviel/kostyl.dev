<script setup>
import { computed, provide } from 'vue'

const props = defineProps({
  /**
   * Title of notebook file, e.g. 'linear_regression.ipynb'
   */
  title: {
    type: String,
    default: 'notebook.ipynb'
  },
  /**
   * Kernel name, e.g. 'Python 3 (ipykernel)', 'Python 3.12', 'Julia', 'R'
   */
  kernel: {
    type: String,
    default: 'Python 3 (ipykernel)'
  },
  /**
   * Kernel status: 'idle', 'busy', 'running'
   */
  kernelStatus: {
    type: String,
    default: 'idle'
  },
  /**
   * Shorthand status alias
   */
  status: {
    type: String,
    default: ''
  },
  /**
   * Show trusted badge
   */
  trusted: {
    type: Boolean,
    default: true
  },
  /**
   * Checkpoint string, e.g. 'Autosaved'
   */
  checkpoint: {
    type: String,
    default: 'Autosaved'
  },
  /**
   * Show toolbar with Run, Restart, Add Cell buttons
   */
  showToolbar: {
    type: Boolean,
    default: true
  },
  /**
   * Show macOS window control dots
   */
  showButtons: {
    type: Boolean,
    default: true
  }
})

const resolvedKernelStatus = computed(() => {
  if (props.status) return props.status
  return props.kernelStatus || 'idle'
})

const isKernelBusy = computed(() => {
  return resolvedKernelStatus.value === 'busy' || resolvedKernelStatus.value === 'running'
})

provide('jupyterNotebook', {
  title: props.title,
  kernel: props.kernel,
  status: resolvedKernelStatus
})
</script>

<template>
  <div class="jupyter-notebook-wrapper not-prose my-8 rounded-xl shadow-xl overflow-hidden border border-gray-200/90 dark:border-neutral-800 bg-[#f4f5f7] dark:bg-[#0d0e11] transition-all">
    <!-- Top Window / Jupyter Header Bar -->
    <div class="jupyter-header bg-[#eaecee] dark:bg-[#18181b] border-b border-gray-200/90 dark:border-neutral-800 select-none">
      <!-- Title Bar -->
      <div class="flex items-center justify-between px-4 py-2.5 gap-3">
        <!-- Left: macOS Buttons & Jupyter Logo & Title -->
        <div class="flex items-center gap-3 min-w-0">
          <!-- Window Dots -->
          <div v-if="showButtons" class="hidden sm:flex items-center gap-1.5 mr-1 shrink-0">
            <div class="w-3 h-3 rounded-full bg-[#ff5f56] border-[0.5px] border-black/10 transition-transform hover:scale-110"></div>
            <div class="w-3 h-3 rounded-full bg-[#ffbd2e] border-[0.5px] border-black/10 transition-transform hover:scale-110"></div>
            <div class="w-3 h-3 rounded-full bg-[#27c93f] border-[0.5px] border-black/10 transition-transform hover:scale-110"></div>
          </div>

          <!-- Jupyter Logo -->
          <div class="flex items-center justify-center w-5 h-5 shrink-0" title="Project Jupyter">
            <svg viewBox="0 0 44 50" class="w-4 h-4" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 0C16.9 0 12.3 2 9 5.3l3.6 3.6C15.1 6.4 18.3 5 22 5c8.3 0 15 6.7 15 15 0 2.8-.8 5.4-2.1 7.7l3.9 3.2C41 27.5 42 23.9 42 20 42 9 33 0 22 0z" fill="#F37726"/>
              <path d="M22 50c5.1 0 9.7-2 13-5.3l-3.6-3.6C28.9 43.6 25.7 45 22 45c-8.3 0-15-6.7-15-15 0-2.8.8-5.4 2.1-7.7l-3.9-3.2C3 22.5 2 26.1 2 30c0 11 9 20 20 20z" fill="#F37726"/>
              <circle cx="22" cy="25" r="5" fill="#616161"/>
              <circle cx="6" cy="11" r="3.5" fill="#9E9E9E"/>
              <circle cx="38" cy="39" r="3.5" fill="#9E9E9E"/>
            </svg>
          </div>

          <!-- Notebook Title & AutoSave -->
          <div class="flex items-baseline gap-2 min-w-0">
            <span class="font-semibold text-xs sm:text-sm text-gray-800 dark:text-gray-200 truncate tracking-tight">
              {{ title }}
            </span>
            <span v-if="checkpoint" class="hidden md:inline text-[11px] text-gray-500 dark:text-neutral-500 font-sans">
              ({{ checkpoint }})
            </span>
          </div>
        </div>

        <!-- Right: Kernel Indicator & Badges -->
        <div class="flex items-center gap-2.5 shrink-0 text-xs">
          <!-- Trusted Badge -->
          <div v-if="trusted" class="hidden sm:flex items-center gap-1 text-[11px] text-gray-600 dark:text-neutral-400 bg-white dark:bg-neutral-800 px-2 py-0.5 rounded border border-gray-200/90 dark:border-neutral-700 shadow-2xs">
            <UIcon name="i-heroicons-shield-check" class="w-3.5 h-3.5 text-emerald-500" />
            <span class="font-sans">Trusted</span>
          </div>

          <!-- Kernel Status Pill -->
          <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-white dark:bg-neutral-800/90 border border-gray-200/90 dark:border-neutral-700 text-gray-700 dark:text-neutral-200 font-medium text-[11px] sm:text-xs shadow-2xs">
            <span 
              class="w-2 h-2 rounded-full transition-all duration-300"
              :class="isKernelBusy ? 'bg-amber-500 animate-pulse ring-2 ring-amber-400/40' : 'border border-gray-400 dark:border-neutral-500 bg-transparent'"
              :title="isKernelBusy ? 'Kernel is busy' : 'Kernel is idle'"
            ></span>
            <span class="truncate max-w-[120px] sm:max-w-none">{{ kernel }}</span>
          </div>
        </div>
      </div>

      <!-- Jupyter Toolbar -->
      <div v-if="showToolbar" class="flex items-center justify-between px-4 py-1.5 border-t border-gray-200/80 dark:border-neutral-800 bg-[#f7f8f9] dark:bg-[#141416] text-xs text-gray-600 dark:text-neutral-400 overflow-x-auto">
        <div class="flex items-center gap-1.5">
          <!-- Save button mockup -->
          <button type="button" class="h-7 w-7 flex items-center justify-center rounded hover:bg-gray-200 dark:hover:bg-neutral-800 transition-colors" title="Save">
            <UIcon name="i-heroicons-arrow-down-tray" class="w-3.5 h-3.5" />
          </button>
          <!-- Add cell mockup -->
          <button type="button" class="h-7 px-2 flex items-center gap-1 rounded hover:bg-gray-200 dark:hover:bg-neutral-800 transition-colors" title="Insert cell below">
            <UIcon name="i-heroicons-plus" class="w-3.5 h-3.5" />
            <span class="text-[11px] font-sans">Cell</span>
          </button>
          <!-- Divider -->
          <div class="h-4 w-px bg-gray-300 dark:bg-neutral-700 mx-1"></div>
          <!-- Run mockup: uniform height h-7 matching all other buttons -->
          <button type="button" class="h-7 px-2.5 flex items-center gap-1.5 rounded bg-gray-200/80 dark:bg-neutral-800 hover:bg-blue-50 hover:text-blue-600 dark:hover:bg-blue-950/40 dark:hover:text-blue-400 transition-colors" title="Run cell">
            <UIcon name="i-heroicons-play-solid" class="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
            <span class="text-[11px] font-semibold font-sans">Run</span>
          </button>
          <!-- Interrupt -->
          <button type="button" class="h-7 w-7 flex items-center justify-center rounded hover:bg-gray-200 dark:hover:bg-neutral-800 transition-colors" title="Interrupt kernel">
            <UIcon name="i-heroicons-stop-solid" class="w-3.5 h-3.5 text-gray-500" />
          </button>
          <!-- Restart -->
          <button type="button" class="h-7 w-7 flex items-center justify-center rounded hover:bg-gray-200 dark:hover:bg-neutral-800 transition-colors" title="Restart kernel">
            <UIcon name="i-heroicons-arrow-path" class="w-3.5 h-3.5 text-gray-500" />
          </button>
        </div>

        <!-- Right toolbar: Cell Type Selector -->
        <div class="flex items-center gap-1">
          <div class="h-7 px-2.5 flex items-center gap-1.5 rounded border border-gray-300/80 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-[11px] font-sans shadow-2xs">
            <span>Code</span>
            <UIcon name="i-heroicons-chevron-down" class="w-3 h-3 opacity-60" />
          </div>
        </div>
      </div>
    </div>

    <!-- Notebook Cells Container / Canvas with authentic compact depth -->
    <div class="jupyter-canvas p-2.5 sm:p-3.5 bg-[#f3f4f6] dark:bg-[#0e0e11] space-y-2 sm:space-y-2.5">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.jupyter-notebook-wrapper {
  /* Subtle outer elevation */
  box-shadow: 0 4px 24px -2px rgba(0, 0, 0, 0.09), 0 2px 8px -1px rgba(0, 0, 0, 0.05);
}

:is(.dark *) .jupyter-notebook-wrapper {
  box-shadow: 0 4px 28px -2px rgba(0, 0, 0, 0.45), 0 2px 10px -1px rgba(0, 0, 0, 0.35);
}

/* Adaptive compact margins & elevation when nested inside accordion, card, or panel */
:global([data-slot="content"] .jupyter-notebook-wrapper),
:global([data-slot="panel"] .jupyter-notebook-wrapper),
:global(.accordion-content .jupyter-notebook-wrapper),
:global([class*="accordion"] .jupyter-notebook-wrapper),
:global(.card .jupyter-notebook-wrapper) {
  margin-top: 1rem !important;
  margin-bottom: 1rem !important;
  box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.04) !important;
}

:global(.dark [data-slot="content"] .jupyter-notebook-wrapper),
:global(.dark [data-slot="panel"] .jupyter-notebook-wrapper),
:global(.dark .accordion-content .jupyter-notebook-wrapper),
:global(.dark [class*="accordion"] .jupyter-notebook-wrapper),
:global(.dark .card .jupyter-notebook-wrapper) {
  box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.35), 0 2px 6px -1px rgba(0, 0, 0, 0.25) !important;
}
</style>
