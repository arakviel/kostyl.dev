<template>
  <div class="box-diagram-wrapper not-prose my-8">
    <div 
      class="box-diagram-container relative overflow-hidden border border-gray-200 dark:border-white/5 rounded-xl bg-white dark:bg-[#111113] shadow-sm p-8"
    >
      <!-- Container -->
      <div 
        v-if="config.type === 'container'"
        class="box-container relative"
        :class="containerThemeClass"
      >
        <!-- Container Label -->
        <div class="container-label absolute -top-3 left-4 px-2 bg-white dark:bg-[#111113] text-sm font-semibold">
          {{ config.label }}
        </div>

        <!-- Items inside container -->
        <div 
          class="flex gap-4 p-6"
          :class="layoutClass"
        >
          <div 
            v-for="(item, index) in config.items" 
            :key="index"
            class="box-item flex flex-col items-center justify-center gap-2 px-6 py-4 rounded-lg border-2 bg-white dark:bg-[#1e1e1e] transition-all hover:shadow-md"
            :class="itemThemeClass"
          >
            <UIcon v-if="item.icon" :name="item.icon" class="w-6 h-6" />
            <span class="text-sm font-medium">{{ item.label }}</span>
          </div>
        </div>

        <!-- Annotation -->
        <div 
          v-if="config.annotation"
          class="annotation-text text-center mt-4 text-sm font-medium flex flex-col items-center gap-1"
          :class="annotationThemeClass"
        >
          <div class="annotation-arrow text-2xl">↑</div>
          <span>{{ config.annotation }}</span>
        </div>
      </div>

      <!-- Comparison Layout -->
      <div 
        v-else-if="config.type === 'comparison'"
        class="comparison-layout flex gap-8"
        :class="config.layout === 'vertical' ? 'flex-col' : 'flex-row'"
      >
        <div 
          v-for="(item, index) in config.items"
          :key="index"
          class="comparison-item flex-1"
        >
          <div 
            class="box-container relative"
            :class="getItemTheme(item.theme)"
          >
            <div class="container-label absolute -top-3 left-4 px-2 bg-white dark:bg-[#111113] text-sm font-semibold">
              {{ item.label }}
            </div>
            
            <div class="flex flex-col gap-3 p-6">
              <div 
                v-for="(box, boxIndex) in item.boxes"
                :key="boxIndex"
                class="box-item flex items-center gap-2 px-4 py-3 rounded-lg border-2 bg-white dark:bg-[#1e1e1e]"
                :class="getItemTheme(item.theme, true)"
              >
                <UIcon v-if="box.icon" :name="box.icon" class="w-5 h-5" />
                <span class="text-sm font-medium">{{ box.label }}</span>
                
                <!-- Nested items -->
                <div v-if="box.items" class="ml-auto flex gap-1">
                  <span 
                    v-for="(nested, nestedIndex) in box.items"
                    :key="nestedIndex"
                    class="text-xs px-2 py-1 rounded bg-gray-100 dark:bg-gray-800"
                  >
                    {{ nested }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- VS Divider -->
        <div 
          v-if="config.layout !== 'vertical' && config.items.length === 2"
          class="flex items-center justify-center"
        >
          <div class="text-2xl font-bold text-gray-400 dark:text-gray-600">VS</div>
        </div>
      </div>

      <!-- Simple Boxes Layout -->
      <div 
        v-else-if="config.type === 'boxes'"
        class="boxes-layout flex gap-4"
        :class="layoutClass"
      >
        <div 
          v-for="(item, index) in config.items"
          :key="index"
          class="box-item flex flex-col items-center justify-center gap-2 px-6 py-4 rounded-lg border-2 bg-white dark:bg-[#1e1e1e] transition-all hover:shadow-md"
          :class="getItemTheme(item.theme || config.theme)"
        >
          <UIcon v-if="item.icon" :name="item.icon" class="w-6 h-6" />
          <span class="text-sm font-medium">{{ item.label }}</span>
          <span v-if="item.description" class="text-xs text-gray-500 dark:text-gray-400 text-center">
            {{ item.description }}
          </span>
        </div>
      </div>
    </div>

    <!-- Caption -->
    <figcaption v-if="caption" class="text-center text-[13px] text-gray-500 dark:text-gray-400 font-medium mt-3">
      {{ caption }}
    </figcaption>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  config: {
    type: Object,
    required: true,
    default: () => ({
      type: 'container', // 'container', 'comparison', 'boxes'
      label: '',
      theme: 'default', // 'default', 'danger', 'warning', 'success', 'info'
      layout: 'horizontal', // 'horizontal', 'vertical'
      items: [],
      annotation: ''
    })
  },
  caption: {
    type: String,
    default: ''
  }
})

// Theme classes for container
const containerThemeClass = computed(() => {
  const themes = {
    default: 'border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300',
    danger: 'border-red-400 dark:border-red-600 text-red-600 dark:text-red-400',
    warning: 'border-orange-400 dark:border-orange-600 text-orange-600 dark:text-orange-400',
    success: 'border-green-400 dark:border-green-600 text-green-600 dark:text-green-400',
    info: 'border-blue-400 dark:border-blue-600 text-blue-600 dark:text-blue-400'
  }
  return `border-2 rounded-xl ${themes[props.config.theme] || themes.default}`
})

// Theme classes for items
const itemThemeClass = computed(() => {
  const themes = {
    default: 'border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300',
    danger: 'border-red-300 dark:border-red-700 text-red-600 dark:text-red-400',
    warning: 'border-orange-300 dark:border-orange-700 text-orange-600 dark:text-orange-400',
    success: 'border-green-300 dark:border-green-700 text-green-600 dark:text-green-400',
    info: 'border-blue-300 dark:border-blue-700 text-blue-600 dark:text-blue-400'
  }
  return themes[props.config.theme] || themes.default
})

// Theme classes for annotation
const annotationThemeClass = computed(() => {
  const themes = {
    default: 'text-gray-600 dark:text-gray-400',
    danger: 'text-red-600 dark:text-red-400',
    warning: 'text-orange-600 dark:text-orange-400',
    success: 'text-green-600 dark:text-green-400',
    info: 'text-blue-600 dark:text-blue-400'
  }
  return themes[props.config.theme] || themes.default
})

// Layout class
const layoutClass = computed(() => {
  return props.config.layout === 'vertical' ? 'flex-col' : 'flex-row flex-wrap'
})

// Get theme for individual items
const getItemTheme = (theme, isNested = false) => {
  const themes = {
    default: isNested 
      ? 'border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300'
      : 'border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300',
    danger: isNested
      ? 'border-red-300 dark:border-red-700 text-red-600 dark:text-red-400'
      : 'border-red-400 dark:border-red-600 text-red-600 dark:text-red-400',
    warning: isNested
      ? 'border-orange-300 dark:border-orange-700 text-orange-600 dark:text-orange-400'
      : 'border-orange-400 dark:border-orange-600 text-orange-600 dark:text-orange-400',
    success: isNested
      ? 'border-green-300 dark:border-green-700 text-green-600 dark:text-green-400'
      : 'border-green-400 dark:border-green-600 text-green-600 dark:text-green-400',
    info: isNested
      ? 'border-blue-300 dark:border-blue-700 text-blue-600 dark:text-blue-400'
      : 'border-blue-400 dark:border-blue-600 text-blue-600 dark:text-blue-400'
  }
  return themes[theme] || themes.default
}
</script>

<script>
export default {
  name: 'BoxDiagram'
}
</script>

<style scoped>
.box-diagram-wrapper {
  width: 100%;
}

.box-container {
  position: relative;
  min-height: 120px;
}

.container-label {
  z-index: 10;
}

.box-item {
  min-width: 100px;
  cursor: default;
}

.annotation-arrow {
  line-height: 1;
}

/* Responsive */
@media (max-width: 640px) {
  .comparison-layout {
    flex-direction: column !important;
  }
  
  .boxes-layout {
    flex-direction: column !important;
  }
}
</style>
