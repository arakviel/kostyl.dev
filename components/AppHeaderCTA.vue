<template>
    <div class="flex items-center gap-2">
        <UButton
            :icon="isZenMode ? 'i-lucide-minimize-2' : 'i-lucide-maximize-2'"
            color="neutral"
            variant="ghost"
            size="sm"
            :aria-label="isZenMode ? 'Вийти з zen mode' : 'Увійти в zen mode'"
            @click="toggleZenMode"
        />
    </div>
</template>

<script setup lang="ts">
    const { isZenMode, toggleZenMode } = useZenMode()
</script>
