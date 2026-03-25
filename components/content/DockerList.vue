<template>
  <div class="flex flex-col h-full w-full">
    <!-- Title and Actions -->
    <div class="mb-4 flex items-center justify-between">
      <h1 class="text-xl font-semibold text-gray-900 dark:text-white">{{ title }}</h1>
      <div v-if="showActions" class="flex gap-2">
        <div class="flex h-8 items-center rounded-md border border-gray-300 bg-white px-3 text-xs dark:border-gray-700 dark:bg-[#2b2d30] dark:text-gray-300">
          <UIcon name="i-heroicons-play" class="mr-1 h-3 w-3" /> Start all
        </div>
      </div>
    </div>

    <!-- Table Header -->
    <div class="grid grid-cols-12 gap-4 rounded-t-md border border-gray-200 bg-gray-100 px-4 py-2 text-xs font-semibold text-gray-500 dark:border-gray-800 dark:bg-[#2b2d30] dark:text-gray-400">
      <div class="col-span-1 border-r border-gray-300 dark:border-gray-700">
        <input type="checkbox" class="rounded border-gray-300" disabled />
      </div>
      <div class="col-span-3">Name</div>
      <div class="col-span-3">Image</div>
      <div class="col-span-2">Status</div>
      <div class="col-span-2">Port(s)</div>
      <div class="col-span-1 text-center">Actions</div>
    </div>

    <!-- List Items Slot -->
    <div class="flex flex-col border-x border-b border-gray-200 bg-white rounded-b-md dark:border-gray-800 dark:bg-[#141415] overflow-hidden">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'Containers'
  },
  showActions: {
    type: Boolean,
    default: true
  }
})
</script>
