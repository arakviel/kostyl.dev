<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: '',
  },
  value: {
    type: [String, Number, Boolean],
    default: '',
  },
  highlight: {
    type: Boolean,
    default: false,
  },
})

const isStringVal = computed(() => {
  if (!props.type) return false
  const t = props.type.toLowerCase()
  return t.includes('string') || t.includes('char')
})

const isBoolVal = computed(() => {
  const t = (props.type || '').toLowerCase()
  const val = String(props.value || '').trim()
  return t === 'bool' || t === 'boolean' || val === 'true' || val === 'false'
})

const isPointerVal = computed(() => {
  const t = (props.type || '').toLowerCase()
  const val = String(props.value || '').trim()
  return t.includes('*') || t.includes('ptr') || val.startsWith('0x')
})

const isStructVal = computed(() => {
  const val = String(props.value || '').trim()
  return val.startsWith('{') && val.endsWith('}')
})

const formattedString = computed(() => {
  if (props.value === undefined || props.value === null) return '""'
  const str = String(props.value)
  if ((str.startsWith('"') && str.endsWith('"')) || (str.startsWith("'") && str.endsWith("'"))) {
    return str
  }
  return `"${str}"`
})
</script>

<template>
  <tr 
    class="transition-colors group debugger-row"
    :class="{ 'debugger-row-highlight': highlight }"
  >
    <td class="px-5 py-2.5 font-bold whitespace-nowrap debugger-name">
      <span class="opacity-30 mr-1.5 text-[9px]">◢</span><span class="whitespace-pre">{{ name }}</span>
    </td>
    <td class="px-5 py-2.5 whitespace-nowrap border-l italic opacity-80 debugger-type">
      {{ type }}
    </td>
    <td class="px-5 py-2.5 border-l break-all debugger-value whitespace-pre-wrap">
      <slot>
        <span v-if="isStringVal" class="val-string">{{ formattedString }}</span>
        <span v-else-if="isBoolVal" class="val-bool font-bold italic">{{ value }}</span>
        <span v-else-if="isPointerVal" class="val-pointer font-bold">{{ value }}</span>
        <span v-else-if="isStructVal" class="val-struct">{{ value }}</span>
        <span v-else class="val-num">{{ value }}</span>
      </slot>
    </td>
  </tr>
</template>
