<template>
  <div class="flex h-full w-full rounded-md border border-gray-200 bg-white dark:border-gray-800 dark:bg-[#1f2023] overflow-hidden shadow-sm">
    <!-- Settings Sidebar -->
    <div class="w-48 bg-gray-50 border-r border-gray-200 dark:bg-[#141415] dark:border-gray-800 py-4">
      <h2 class="px-4 text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-2">Settings</h2>
      <nav class="space-y-0.5 px-2 text-sm text-gray-700 dark:text-gray-300">
        <div 
          v-for="item in menuItems" :key="item.id"
          class="cursor-default rounded-md px-3 py-1.5 transition-colors"
          :class="activeSection === item.id ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400 font-medium' : 'hover:bg-gray-200 dark:hover:bg-white/10'"
        >
          {{ item.label }}
        </div>
      </nav>
    </div>

    <!-- Settings Content -->
    <div class="flex-1 overflow-y-auto p-6 bg-white dark:bg-[#1f2023]">
      <h1 class="text-xl font-semibold mb-6 text-gray-900 dark:text-white">{{ activeTitle }}</h1>
      <slot />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  activeSection: {
    type: String,
    default: 'general'
  }
})

const menuItems = [
  { id: 'general', label: 'General' },
  { id: 'resources', label: 'Resources' },
  { id: 'docker-engine', label: 'Docker Engine' },
  { id: 'builder', label: 'Builder' },
  { id: 'kubernetes', label: 'Kubernetes' },
  { id: 'software-updates', label: 'Software Updates' }
]

const activeTitle = computed(() => {
  const item = menuItems.find(i => i.id === props.activeSection)
  return item ? item.label : 'Settings'
})
</script>
