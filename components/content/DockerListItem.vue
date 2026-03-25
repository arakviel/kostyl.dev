<template>
  <div class="grid grid-cols-12 items-center gap-4 border-b border-gray-100 px-4 py-3 text-sm last:border-0 hover:bg-gray-50 dark:border-gray-800/60 dark:hover:bg-white/5 transition-colors">
    <div class="col-span-1">
      <input type="checkbox" class="rounded border-gray-300" disabled />
    </div>
    
    <div class="col-span-3 flex items-center gap-3 overflow-hidden font-medium text-gray-900 dark:text-gray-100">
      <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded bg-gray-100 dark:bg-[#2b2d30]">
        <UIcon :name="iconName" class="h-4 w-4 text-blue-500" />
      </div>
      <span class="truncate">{{ name }}</span>
    </div>
    
    <div class="col-span-3 truncate text-gray-500 dark:text-gray-400">
      {{ image }}
    </div>
    
    <div class="col-span-2 flex items-center gap-2">
      <span class="relative flex h-2.5 w-2.5">
        <span v-if="status === 'running'" class="absolute inline-flex h-full w-full animate-ping rounded-full bg-green-400 opacity-75"></span>
        <span class="relative inline-flex h-2.5 w-2.5 rounded-full" :class="statusColorClass"></span>
      </span>
      <span class="capitalize text-gray-600 dark:text-gray-300 text-xs">{{ status }}</span>
    </div>
    
    <div class="col-span-2 truncate text-xs text-blue-500">
      <a v-if="ports" href="#" class="hover:underline">{{ ports }}</a>
      <span v-else class="text-gray-400 dark:text-gray-600">-</span>
    </div>
    
    <div class="col-span-1 flex items-center justify-center gap-2">
      <button 
        class="flex h-7 w-7 items-center justify-center rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
        :class="{'ring-2 ring-blue-500 ring-offset-2 dark:ring-offset-[#141415]': highlight === 'play'}"
        title="Start/Stop"
      >
        <UIcon :name="status === 'running' ? 'i-heroicons-stop-solid' : 'i-heroicons-play-solid'" 
               :class="status === 'running' ? 'text-gray-500' : 'text-green-500'" class="h-4 w-4" />
      </button>
      <button 
        class="flex h-7 w-7 items-center justify-center rounded-full hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
        :class="{'ring-2 ring-blue-500 ring-offset-2 dark:ring-offset-[#141415]': highlight === 'delete'}"
        title="Delete"
      >
        <UIcon name="i-heroicons-trash" class="h-4 w-4 text-red-500" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: { type: String, required: true },
  image: { type: String, required: true },
  status: { type: String, default: 'running' }, // 'running', 'exited', 'created'
  ports: { type: String, default: '' },
  highlight: { type: String, default: '' } // 'play', 'delete', or empty
})

const iconName = computed(() => {
  if (props.image.includes('postgres') || props.image.includes('mysql') || props.image.includes('redis') || props.image.includes('db')) return 'i-lucide-database'
  if (props.image.includes('node') || props.image.includes('python') || props.image.includes('go')) return 'i-lucide-code'
  if (props.image.includes('nginx') || props.image.includes('apache')) return 'i-lucide-globe'
  return 'i-lucide-box'
})

const statusColorClass = computed(() => {
  if (props.status === 'running') return 'bg-green-500'
  if (props.status === 'exited') return 'bg-gray-400'
  if (props.status === 'error') return 'bg-red-500'
  return 'bg-blue-400'
})
</script>
