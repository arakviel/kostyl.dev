<script setup>
    import { ref, computed, useSlots, onMounted } from 'vue'

    const props = defineProps({
        tailwind: {
            type: Boolean,
            default: true,
        },
    })

    const slots = useSlots()
    const htmlCode = ref('')
    const cssCode = ref('')
    const iframeHeight = ref(0)
    const iframeRef = ref(null)

    const extractCodes = () => {
        const defaultSlot = slots.default?.() || []
        let html = '',
            css = ''

        const findCodes = (vnodes) => {
            for (const vnode of vnodes) {
                if (vnode.props && vnode.props.code) {
                    if (vnode.props.language === 'html' || vnode.props.language === 'markup') {
                        html = vnode.props.code
                    } else if (vnode.props.language === 'css') {
                        css = vnode.props.code
                    }
                }
                if (vnode.children && Array.isArray(vnode.children)) {
                    findCodes(vnode.children)
                } else if (vnode.children && typeof vnode.children === 'object' && vnode.children.default) {
                    findCodes(vnode.children.default())
                }
            }
        }

        findCodes(defaultSlot)
        htmlCode.value = html.trim()
        cssCode.value = css.trim()
    }

    /**
     * Reads content height directly from the iframe's contentDocument.
     * Uses requestAnimationFrame to ensure layout is fully settled.
     * No ResizeObserver needed — srcdoc reactivity triggers onload on every change.
     */
    const onIframeLoad = () => {
        const iframe = iframeRef.value
        if (!iframe) return

        const doc = iframe.contentDocument || iframe.contentWindow?.document
        if (!doc?.body) return

        // Wait for a frame so the browser finishes layout before measuring
        requestAnimationFrame(() => {
            const height = doc.documentElement.scrollHeight
            iframeHeight.value = height
        })
    }

    onMounted(() => {
        extractCodes()
    })

    const srcdoc = computed(
        () => `
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    ${props.tailwind ? '<script src="https://unpkg.com/@tailwindcss/browser@4"><\/script>' : ''}
    <style>
      ${props.tailwind ? '@import "tailwindcss";' : ''}
      html, body {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        padding: 1rem;
        margin: 0;
        color: #333;
      }
      * { box-sizing: border-box; }
      ${cssCode.value}
    </style>
  </head>
  <body>
    ${htmlCode.value}
  </body>
</html>
`,
    )
</script>

<template>
    <div class="my-8 rounded-xl shadow-2xl overflow-hidden bg-white dark:bg-[#202124] border border-gray-200 dark:border-white/5 flex flex-col not-prose">
        <!-- macOS Chrome Header -->
        <div class="bg-[#dee1e6] dark:bg-[#2d2e32] pt-2 flex flex-col gap-0 select-none">
            <!-- Top Row: Buttons and Tabs -->
            <div class="flex items-center px-3">
                <!-- macOS Buttons -->
                <div class="flex gap-2 px-2 items-center h-8">
                    <div class="w-3 h-3 rounded-full bg-[#ff5f56] border-[0.5px] border-black/10"></div>
                    <div class="w-3 h-3 rounded-full bg-[#ffbd2e] border-[0.5px] border-black/10"></div>
                    <div class="w-3 h-3 rounded-full bg-[#27c93f] border-[0.5px] border-black/10"></div>
                </div>

                <!-- Active Tab -->
                <div class="flex items-end h-8 ml-2">
                    <div
                        class="relative bg-white dark:bg-[#202124] pl-3 pr-1.5 py-1.5 rounded-t-lg text-[11px] text-gray-700 dark:text-gray-200 font-sans flex items-center justify-between gap-2 border-x border-t border-gray-300/40 dark:border-transparent min-w-[160px]"
                    >
                        <div class="flex items-center gap-2 overflow-hidden">
                            <!-- Favicon Placeholder -->
                            <div class="w-3.5 h-3.5 flex-shrink-0 opacity-60">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="10" />
                                    <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
                                </svg>
                            </div>
                            <span class="truncate">Preview</span>
                        </div>
                        <div
                            class="w-4 h-4 flex-shrink-0 flex items-center justify-center rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 text-[10px] opacity-60 transition-colors"
                        >
                            ×
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bottom Row: Address Bar Toolbar -->
            <div
                class="bg-white dark:bg-[#202124] py-1.5 px-4 flex items-center gap-3 border-t border-gray-300/30 dark:border-transparent h-10 w-full"
            >
                <!-- Nav Icons (SVG) -->
                <div class="flex gap-4 text-gray-500 dark:text-gray-400 items-center">
                    <svg class="w-3.5 h-3.5 cursor-default opacity-40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
                    <svg class="w-3.5 h-3.5 cursor-default opacity-40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
                    <svg class="w-3.5 h-3.5 cursor-default" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
                </div>
                <!-- Address Box -->
                <div
                    class="flex-grow bg-[#f1f3f4] dark:bg-[#2d2e32] rounded-full px-4 py-1 text-[11.5px] text-gray-500 dark:text-gray-300 font-sans truncate flex items-center gap-2 border border-transparent"
                >
                    <span class="text-[10px] opacity-50">🔒</span>
                    <span class="truncate">localhost:3000</span>
                </div>
                <!-- Menu Icon -->
                <div class="flex flex-col gap-0.5 opacity-50 px-1">
                    <div class="w-0.5 h-0.5 bg-gray-600 dark:bg-gray-300 rounded-full"></div>
                    <div class="w-0.5 h-0.5 bg-gray-600 dark:bg-gray-300 rounded-full"></div>
                    <div class="w-0.5 h-0.5 bg-gray-600 dark:bg-gray-300 rounded-full"></div>
                </div>
            </div>
        </div>

        <!-- Iframe Container -->
        <div class="flex-grow relative bg-white">
            <iframe
                ref="iframeRef"
                :srcdoc="srcdoc"
                class="w-full border-none block"
                :style="{ height: iframeHeight > 0 ? iframeHeight + 'px' : '100px' }"
                sandbox="allow-scripts allow-same-origin"
                scrolling="no"
                @load="onIframeLoad"
            ></iframe>
        </div>

        <!-- Hidden slot for extraction -->
        <div class="hidden">
            <slot />
        </div>
    </div>
</template>

<style scoped></style>
