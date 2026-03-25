<script setup>
    import { ref, computed, useSlots, onMounted, watch } from 'vue'
import { useRoute } from 'nuxt/app'

    const props = defineProps({
        tailwind: {
            type: Boolean,
            default: false,
        },
    })

    const slots = useSlots()
    const iframeHeight = ref(0)
    const iframeRef = ref(null)
    const activeTab = ref('preview')
    const route = useRoute()

    /**
     * Reads content height directly from the iframe's contentDocument.
     */
    const onIframeLoad = () => {
        const iframe = iframeRef.value
        if (!iframe) return

        const doc = iframe.contentDocument || iframe.contentWindow?.document
        if (!doc?.body) return

        requestAnimationFrame(() => {
            const height = doc.documentElement.scrollHeight
            iframeHeight.value = height
        })
    }

    // Stable extraction using computed to avoid infinite loops with watch
    const extractedData = computed(() => {
        const defaultSlot = slots.default?.() || []
        let htmlSnippet = '',
            cssSnippet = ''
        
        const hVnodes = []
        const cVnodes = []

        const findCodes = (vnodes) => {
            for (const vnode of vnodes) {
                // Check for MDCCodeBlock or similar props
                if (vnode.props && vnode.props.code) {
                    const lang = vnode.props.language
                    if (lang === 'html' || lang === 'markup') {
                        htmlSnippet = vnode.props.code
                        hVnodes.push(vnode)
                    } else if (lang === 'css') {
                        cssSnippet = vnode.props.code
                        cVnodes.push(vnode)
                    }
                }
                
                // Recursively look into children
                if (vnode.children && Array.isArray(vnode.children)) {
                    findCodes(vnode.children)
                } else if (vnode.children && typeof vnode.children === 'object' && vnode.children.default) {
                    // Be careful: calling default() in a computed is generally okay 
                    // as long as it doesn't trigger side effects that invalidate this computed
                    try {
                        findCodes(vnode.children.default())
                    } catch (e) {}
                }
            }
        }

        findCodes(defaultSlot)
        
        return {
            htmlCode: htmlSnippet.trim(),
            cssCode: cssSnippet.trim(),
            htmlVnodes: hVnodes,
            cssVnodes: cVnodes
        }
    })

    const htmlCode = computed(() => extractedData.value.htmlCode)
    const cssCode = computed(() => extractedData.value.cssCode)
    const htmlVnodes = computed(() => extractedData.value.htmlVnodes)
    const cssVnodes = computed(() => extractedData.value.cssVnodes)

    onMounted(() => {
        // Initial height check
        onIframeLoad()
    })

    watch(() => route.path, () => {
        // Reset tab to preview on page change
        activeTab.value = 'preview'
    })

    const srcdoc = computed(
        () => `
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML Preview</title>
    ${props.tailwind ? '<script src="https://unpkg.com/@tailwindcss/browser@4"><\/script>' : ''}
    <style>
      /* Base CSS Reset */
      *, ::before, ::after {
        box-sizing: border-box;
        border-width: 0;
        border-style: solid;
        border-color: currentColor;
      }
      
      html {
        line-height: 1.5;
        -webkit-text-size-adjust: 100%;
        -moz-tab-size: 4;
        tab-size: 4;
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
      }

      body {
        margin: 0;
        line-height: inherit;
        ${props.tailwind ? '' : 'padding: 1rem; color: #1e293b;'}
      }

      /* Tailwind 4 integrated via script if active */
      ${props.tailwind ? '' : `
      h1, h2, h3, h4, h5, h6 { font-size: inherit; font-weight: inherit; }
      a { color: inherit; text-decoration: inherit; }
      b, strong { font-weight: bolder; }
      code, kbd, samp, pre { font-family: ui-monospaced, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size: 1em; }
      small { font-size: 80%; }
      sub, sup { font-size: 75%; line-height: 0; position: relative; vertical-align: baseline; }
      sub { bottom: -0.25em; }
      sup { top: -0.5em; }
      table { text-indent: 0; border-color: inherit; border-collapse: collapse; }
      button, input, optgroup, select, textarea { font-family: inherit; font-size: 100%; font-weight: inherit; line-height: inherit; color: inherit; margin: 0; padding: 0; }
      button, select { text-transform: none; }
      button, [type='button'], [type='reset'], [type='submit'] { -webkit-appearance: button; background-color: transparent; background-image: none; }
      `}
      
      ${cssCode.value}
    </style>
  </head>
  <body>
    ${htmlCode.value}
  </body>
</html>
`,
    )

    // Helper component to render VNodes array
    const VNodeRenderer = {
        props: ['vnodes'],
        render() {
            return this.vnodes
        }
    }

    const copyCode = () => {
        const code = activeTab.value === 'html' ? htmlCode.value : cssCode.value
        if (navigator.clipboard) {
            navigator.clipboard.writeText(code)
        }
    }
</script>

<template>
    <div class="my-8 rounded-xl shadow-2xl overflow-hidden bg-white dark:bg-[#202124] border border-gray-200 dark:border-white/5 flex flex-col not-prose transition-all duration-300">
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

                <!-- Tabs -->
                <div class="flex items-end h-8 ml-2">
                    <!-- Preview Tab -->
                    <button
                        @click="activeTab = 'preview'"
                        :class="[
                            'relative pl-3 pr-1.5 py-1.5 rounded-t-lg text-[11px] font-sans flex items-center justify-between gap-2 border-x border-t min-w-[100px] transition-all',
                            activeTab === 'preview'
                                ? 'bg-white dark:bg-[#202124] text-gray-700 dark:text-gray-200 border-gray-300/40 dark:border-transparent z-10'
                                : 'bg-transparent text-gray-500 dark:text-gray-400 border-transparent hover:bg-black/5 dark:hover:bg-white/5'
                        ]"
                    >
                        <div class="flex items-center gap-2 overflow-hidden">
                            <div class="w-3.5 h-3.5 flex-shrink-0 opacity-60">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="10" />
                                    <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
                                </svg>
                            </div>
                            <span class="truncate">Preview</span>
                        </div>
                    </button>

                    <!-- HTML Tab -->
                    <button
                        v-if="htmlCode"
                        @click="activeTab = 'html'"
                        :class="[
                            'relative pl-3 pr-1.5 py-1.5 rounded-t-lg text-[11px] font-sans flex items-center justify-between gap-2 border-x border-t min-w-[100px] transition-all -ml-px',
                            activeTab === 'html'
                                ? 'bg-white dark:bg-[#202124] text-gray-700 dark:text-gray-200 border-gray-300/40 dark:border-transparent z-10'
                                : 'bg-transparent text-gray-500 dark:text-gray-400 border-transparent hover:bg-black/5 dark:hover:bg-white/5'
                        ]"
                    >
                        <div class="flex items-center gap-2 overflow-hidden">
                            <div class="w-3.5 h-3.5 flex-shrink-0 text-orange-500">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                                </svg>
                            </div>
                            <span class="truncate">index.html</span>
                        </div>
                    </button>

                    <!-- CSS Tab -->
                    <button
                        v-if="cssCode"
                        @click="activeTab = 'css'"
                        :class="[
                            'relative pl-3 pr-1.5 py-1.5 rounded-t-lg text-[11px] font-sans flex items-center justify-between gap-2 border-x border-t min-w-[100px] transition-all -ml-px',
                            activeTab === 'css'
                                ? 'bg-white dark:bg-[#202124] text-gray-700 dark:text-gray-200 border-gray-300/40 dark:border-transparent z-10'
                                : 'bg-transparent text-gray-500 dark:text-gray-400 border-transparent hover:bg-black/5 dark:hover:bg-white/5'
                        ]"
                    >
                        <div class="flex items-center gap-2 overflow-hidden">
                            <div class="w-3.5 h-3.5 flex-shrink-0 text-blue-500">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                                </svg>
                            </div>
                            <span class="truncate">styles.css</span>
                        </div>
                    </button>
                </div>
            </div>

            <!-- Bottom Row: Address Bar Toolbar -->
            <div
                class="bg-white dark:bg-[#202124] py-1.5 px-4 flex items-center gap-3 border-t border-gray-300/30 dark:border-transparent h-10 w-full"
            >
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
                    <span class="truncate">localhost:3000{{ activeTab !== 'preview' ? '/' + (activeTab === 'html' ? 'index.html' : 'styles.css') : '' }}</span>
                </div>
                
                <!-- Copy Button (visible only in code tabs) -->
                <button 
                    v-if="activeTab !== 'preview'"
                    @click="copyCode"
                    class="flex items-center gap-1.5 px-2.5 py-1 rounded bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 text-[11px] text-gray-500 dark:text-gray-400 transition-all border border-black/5 dark:border-white/5"
                >
                    <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    <span>Copy</span>
                </button>

                <div class="flex flex-col gap-0.5 opacity-50 px-1">
                    <div class="w-0.5 h-0.5 bg-gray-600 dark:bg-gray-300 rounded-full"></div>
                    <div class="w-0.5 h-0.5 bg-gray-600 dark:bg-gray-300 rounded-full"></div>
                    <div class="w-0.5 h-0.5 bg-gray-600 dark:bg-gray-300 rounded-full"></div>
                </div>
            </div>
        </div>

        <!-- content -->
        <div class="flex-grow relative bg-white dark:bg-[#1e1e1e] overflow-hidden">
            <!-- Preview Iframe -->
            <div v-show="activeTab === 'preview'" class="h-full">
                <iframe
                    ref="iframeRef"
                    :srcdoc="srcdoc"
                    class="w-full border-none block"
                    :style="{ height: iframeHeight > 0 ? iframeHeight + 'px' : '300px' }"
                    sandbox="allow-scripts allow-same-origin"
                    scrolling="no"
                    @load="onIframeLoad"
                ></iframe>
            </div>

            <!-- Code Highlighting View -->
            <div 
                v-show="activeTab === 'html'" 
                class="px-6 code-tab-content animate-in fade-in duration-300 overflow-auto max-h-[600px] bg-[#1e1e1e]"
            >
                <VNodeRenderer :vnodes="htmlVnodes" />
            </div>

            <div 
                v-show="activeTab === 'css'" 
                class="px-6 code-tab-content animate-in fade-in duration-300 overflow-auto max-h-[600px] bg-[#1e1e1e]"
            >
                <VNodeRenderer :vnodes="cssVnodes" />
            </div>
        </div>

        <!-- Hidden slot for extraction -->
        <div class="hidden">
            <slot />
        </div>
    </div>
</template>

<style scoped>
    /* Custom scrollbar for code view */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1e1e1e;
    }
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #444;
    }

    .animate-in {
        animation-duration: 300ms;
        animation-fill-mode: both;
    }
    .fade-in {
        animation-name: fade-in;
    }
    @keyframes fade-in {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Standard code block integration */
    :deep(pre) {
        margin: 0 !important;
        border-radius: 0 !important;
        border: none !important;
        background-color: transparent !important;
        padding: 0 1.5rem !important;
        font-size: 13.5px !important;
        line-height: 1.6 !important;
    }
    
    :deep(.code-block) {
        margin: 0 !important;
        border: none !important;
    }

    /* Hide the standard copy button inside our component to avoid duplication */
    :deep(.copy-button) {
        display: none !important;
    }

    /* Ensure deep integration with Docus/Nuxt Content prose styles */
    .code-tab-content :deep(pre) {
        background-color: transparent !important;
    }
</style>
