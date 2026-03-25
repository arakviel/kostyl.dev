<template>
  <div class="not-prose my-8 flex w-full flex-col overflow-hidden rounded-xl border border-gray-200 bg-gray-50 shadow-2xl dark:border-gray-800 dark:bg-[#1f2023] font-sans text-sm">
    
    <!-- Title Bar (macOS style) -->
    <div class="flex h-10 items-center bg-gray-100 px-4 dark:bg-[#2b2d30] border-b border-gray-200 dark:border-gray-800">
      <div v-if="os === 'mac'" class="flex space-x-2">
        <div class="h-3 w-3 rounded-full bg-red-400"></div>
        <div class="h-3 w-3 rounded-full bg-yellow-400"></div>
        <div class="h-3 w-3 rounded-full bg-green-400"></div>
      </div>
      <div class="mx-auto flex items-center font-semibold text-gray-500 dark:text-gray-400 text-xs">
        <UIcon name="i-simple-icons-docker" class="mr-2 h-4 w-4 text-blue-500" />
        Docker Desktop
      </div>
    </div>

    <div class="flex h-[500px]">
      <!-- Sidebar -->
      <div v-if="activeTab !== 'settings'" class="flex w-52 flex-col border-r border-gray-200 bg-white dark:border-gray-800 dark:bg-[#2b2d30]">
        <!-- User Profile Area -->
        <div class="flex items-center gap-3 border-b border-gray-200 p-4 dark:border-gray-800">
          <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400 font-bold">
            U
          </div>
          <span class="font-medium text-gray-700 dark:text-gray-200">user</span>
        </div>

        <!-- Navigation Menu -->
        <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
          <template v-for="item in menuItems" :key="item.id">
            <div 
              class="flex cursor-default items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors"
              :class="activeTab === item.id ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400 font-medium' : 'text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-white/5'"
            >
              <UIcon :name="item.icon" class="h-4 w-4" />
              {{ item.label }}
            </div>
          </template>
        </nav>
      </div>

      <!-- Main Content Area -->
      <div class="flex flex-1 flex-col overflow-hidden">
        <!-- Header -->
        <header class="flex h-14 items-center justify-between border-b border-gray-200 bg-white px-6 dark:border-gray-800 dark:bg-[#1f2023]">
          
          <!-- Search -->
          <div class="flex w-64 items-center rounded-md border border-gray-300 bg-gray-50 px-3 py-1.5 dark:border-gray-700 dark:bg-[#141415]">
            <UIcon name="i-heroicons-magnifying-glass" class="mr-2 h-4 w-4 text-gray-400" />
            <span class="text-xs text-gray-400">Search</span>
            <div class="ml-auto flex items-center rounded border border-gray-200 px-1.5 py-0.5 text-[10px] text-gray-400 dark:border-gray-700">
              ⌘ K
            </div>
          </div>

          <!-- Top Right Actions -->
          <div class="flex items-center gap-4 text-gray-500 dark:text-gray-400">
            <UIcon name="i-heroicons-bug-ant" class="h-5 w-5" />
            <UIcon name="i-heroicons-cog-8-tooth" class="h-5 w-5" />
          </div>
        </header>

        <!-- Dynamic Content Slot -->
        <main class="flex-1 overflow-y-auto relative p-6 bg-gray-50 dark:bg-[#1f2023]">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  activeTab: {
    type: String,
    default: 'containers'
  },
  os: {
    type: String,
    default: 'mac' // 'mac' or 'windows'
  }
})

const menuItems = [
  { id: 'containers', label: 'Containers', icon: 'i-lucide-box' },
  { id: 'images', label: 'Images', icon: 'i-lucide-layers' },
  { id: 'volumes', label: 'Volumes', icon: 'i-lucide-database' },
  { id: 'builds', label: 'Builds', icon: 'i-lucide-hammer' },
  { id: 'dev-envs', label: 'Dev Environments', icon: 'i-lucide-monitor' },
  { id: 'extensions', label: 'Extensions', icon: 'i-lucide-puzzle' }
]
</script>
