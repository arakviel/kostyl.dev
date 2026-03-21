<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
    title: {
        type: String,
        default: 'bash',
    },
    showButtons: {
        type: Boolean,
        default: true,
    },
    cursor: {
        type: Boolean,
        default: false,
    }
});

const bodyStyle = computed(() => {
    return {};
});
</script>

<template>
    <div class="my-8 rounded-xl shadow-2xl overflow-hidden terminal-window border border-white/5 border-t-white/10 not-prose relative">
        <!-- macOS Header -->
        <div
            class="flex items-center h-10 px-4 terminal-header border-b border-black/20 select-none relative"
        >
            <!-- Window Buttons -->
            <div v-if="showButtons" class="flex gap-2 z-10 font-sans">
                <div class="w-3 h-3 rounded-full btn-red border-[0.5px] border-black/10 transition-colors hover:brightness-90"></div>
                <div class="w-3 h-3 rounded-full btn-yellow border-[0.5px] border-black/10 transition-colors hover:brightness-90"></div>
                <div class="w-3 h-3 rounded-full btn-green border-[0.5px] border-black/10 transition-colors hover:brightness-90"></div>
            </div>
            <!-- Title -->
            <div class="absolute inset-x-0 text-center text-[13px] terminal-title font-sans tracking-tight pointer-events-none">
                {{ title }}
            </div>
        </div>

        <!-- Terminal Body -->
        <div 
            class="p-6 font-mono text-[13.5px] leading-relaxed terminal-body overflow-x-auto whitespace-pre-wrap transition-[max-height] duration-500 ease-in-out relative"
            :style="bodyStyle"
        >
            <slot />
            <span v-if="cursor" class="inline-block w-2 h-[1.1em] bg-current ml-0.5 align-middle animate-cursor"></span>
        </div>

    </div>
</template>
<style scoped>
    @keyframes cursor-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    .animate-cursor {
        animation: cursor-blink 1s step-end infinite;
    }
    .terminal-window {
        /* Light Theme (Default) Variables */
        --terminal-bg: #ffffff;
        --terminal-header: #f3f4f6;
        --terminal-text: #18181b;
        --terminal-title: #71717a;
        --terminal-border: #e4e4e7;
        --terminal-red: #ef4444;
        --terminal-green: #10b981;
        --terminal-blue: #3b82f6;
        --terminal-yellow: #f59e0b;
        --terminal-purple: #8b5cf6;
        --terminal-cyan: #06b6d4;

        background-color: var(--terminal-bg) !important;
        border: 1px solid var(--terminal-border) !important;
    }

    /* Dark Theme Overrides */
    :is(.dark *) .terminal-window {
        --terminal-bg: #1c1c1c;
        --terminal-header: #323232;
        --terminal-text: #f8f8f2;
        --terminal-title: #9ca3af;
        --terminal-border: rgba(255, 255, 255, 0.05);
        --terminal-red: #f87171;
        --terminal-green: #4ade80;
        --terminal-blue: #60a5fa;
        --terminal-yellow: #facc15;
        --terminal-purple: #c084fc;
        --terminal-cyan: #22d3ee;
    }

    .terminal-header {
        background-color: var(--terminal-header) !important;
        border-bottom: 1px solid var(--terminal-border) !important;
    }
    .terminal-title {
        color: var(--terminal-title) !important;
    }
    .terminal-body {
        color: var(--terminal-text) !important;
    }

    .btn-red { background-color: #ff5f56 !important; }
    .btn-yellow { background-color: #ffbd2e !important; }
    .btn-green { background-color: #27c93f !important; }

    /* Reset common prose styles */
    :deep(p) {
        margin: 0 !important;
        padding: 0 !important;
    }
    :deep(pre),
    :deep(code),
    :deep(.code-block) {
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        font-family: inherit !important;
        font-size: inherit !important;
        line-height: inherit !important;
        box-shadow: none !important;
    }

    /* Standard terminal colors with theme adaptation */
    :deep(.text-red-400) { color: var(--terminal-red) !important; }
    :deep(.text-green-400) { color: var(--terminal-green) !important; }
    :deep(.text-blue-400) { color: var(--terminal-blue) !important; }
    :deep(.text-yellow-400) { color: var(--terminal-yellow) !important; }
    :deep(.text-purple-400) { color: var(--terminal-purple) !important; }
    :deep(.text-gray-400) { color: var(--terminal-title) !important; }
    :deep(.font-bold),
    :deep(strong),
    :deep(b) {
        font-weight: 700 !important;
    }
    
    /* Support for manual line breaks/rows */
    :deep(.line),
    .terminal-body :deep(> *:not(.animate-cursor)) {
        display: block;
        min-height: 1.25em;
    }
</style>
