<script setup>
import { ref, computed, useSlots, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
    title: {
        type: String,
        default: 'WPF / Avalonia Preview'
    }
})

const slots = useSlots()
const iframeRef = ref(null)
const activeTab = ref('preview')
const isWasmLoading = ref(true)
const isWasmReady = ref(false)
const wasmLogs = ref([])

// Extract XAML and C# code from slots
const extractedData = computed(() => {
    const defaultSlot = slots.default?.() || []
    let xamlSnippet = ''
    const xVnodes = []
    const cVnodes = []
    let csharpSnippet = ''

    const findCodes = (vnodes) => {
        if (!vnodes) return;
        const nodesArray = Array.isArray(vnodes) ? vnodes : [vnodes];
        
        for (const vnode of nodesArray) {
            if (!vnode) continue;
            
            const p = vnode.props || {};
            // Nuxt Content specific: language and code might be in props or children
            const lang = p.language || p.lang || '';
            const code = p.code || '';

            if (lang && code) {
                if (lang === 'xml' || lang === 'xaml' || lang === 'html') {
                    xamlSnippet = code;
                    xVnodes.push(vnode);
                } else if (lang === 'csharp' || lang === 'cs') {
                    csharpSnippet = code;
                    cVnodes.push(vnode);
                }
            } else {
                // Fallback for standard markdown blocks if they are not pre-parsed by Prose
                const tag = vnode.type || '';
                const children = vnode.children || '';
                if (typeof children === 'string' && tag === 'code' && p.class?.includes('language-')) {
                   const matchedLang = p.class.replace('language-', '');
                   if (matchedLang === 'csharp' || matchedLang === 'cs') {
                       csharpSnippet = children;
                       cVnodes.push(vnode);
                   }
                }
            }
            
            // Recurse into children
            if (vnode.children) {
                if (Array.isArray(vnode.children)) {
                    findCodes(vnode.children);
                } else if (typeof vnode.children === 'object' && vnode.children.default) {
                    try { findCodes(vnode.children.default()); } catch (e) {}
                }
            }
            
            // Handle components like ProseCode/ProsePre
            if (vnode.component?.subTree) {
                findCodes(vnode.component.subTree);
            }
        }
    }

    findCodes(defaultSlot)
    return {
        xamlCode: xamlSnippet.trim(),
        xamlVnodes: xVnodes,
        csharpCode: csharpSnippet.trim(),
        csharpVnodes: cVnodes
    }
})

const xamlCode = computed(() => extractedData.value.xamlCode)
const xamlVnodes = computed(() => extractedData.value.xamlVnodes)
const csharpCode = computed(() => extractedData.value.csharpCode)
const csharpVnodes = computed(() => extractedData.value.csharpVnodes)

// Theme Synchronization
const colorMode = typeof useColorMode === 'function' ? useColorMode() : { value: 'dark' };
const currentTheme = computed(() => colorMode?.value === 'dark' ? 'dark' : 'light');

const sendThemeToWasm = () => {
    if (isWasmReady.value && iframeRef.value?.contentWindow) {
        iframeRef.value.contentWindow.postMessage({
            type: 'set-theme',
            theme: currentTheme.value
        }, '*');
    }
}

const sendXamlToWasm = () => {
    if (isWasmReady.value && iframeRef.value?.contentWindow) {
        let finalXaml = xamlCode.value;
        
        // Inject default Avalonia namespaces if missing, to allow rendering raw snippets without Window boilerplate
        if (finalXaml && !finalXaml.includes('xmlns=')) {
            finalXaml = finalXaml.replace(/<([a-zA-Z0-9_]+)/, '<$1 xmlns="https://github.com/avaloniaui" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"');
        }

        // Translate WPF-specific static resources for Avalonia compatibility in preview
        if (finalXaml) {
            finalXaml = finalXaml
                .replace(/\{x:Static SystemColors\.HighlightBrush\}/g, "Blue")
                .replace(/\{x:Static SystemColors\.HighlightTextBrush\}/g, "White")
                .replace(/\{x:Static SystemColors\.HotTrackBrush\}/g, "Blue")
                .replace(/\{x:Static SystemColors\.WindowBrush\}/g, "White")
                .replace(/\{x:Static SystemColors\.ActiveBorderBrush\}/g, "Gray")
                .replace(/\{x:Static SystemColors\.WindowTextBrush\}/g, "Black")
                .replace(/\{x:Static FlowDirection\.RightToLeft\}/g, "RightToLeft")
                .replace(/\bToolTip="/g, 'ToolTip.Tip="');
        }

        iframeRef.value.contentWindow.postMessage({
            type: 'update-xaml',
            xaml: finalXaml
        }, '*');
        sendThemeToWasm(); // Sync theme every time we update XAML too
    }
}

watch(currentTheme, () => {
    sendThemeToWasm();
})

watch(xamlCode, () => {
    sendXamlToWasm()
})

let pingInterval = null;

const handleMessage = (event) => {
    if (event.data && event.data.type === 'avalonia-ready') {
        isWasmLoading.value = false
        isWasmReady.value = true
        if (pingInterval) {
            clearInterval(pingInterval);
            pingInterval = null;
        }
        sendXamlToWasm()
    }
    if (event.data && event.data.type === 'wasm-log') {
        wasmLogs.value.push({
            id: Date.now() + Math.random(),
            message: event.data.message,
            time: new Date().toLocaleTimeString()
        })
        if (wasmLogs.value.length > 50) wasmLogs.value.shift()
    }
}

onMounted(() => {
    window.addEventListener('message', handleMessage)
    
    // Fallback: ping iframe until it responds
    pingInterval = setInterval(() => {
        if (!isWasmReady.value && iframeRef.value?.contentWindow) {
            iframeRef.value.contentWindow.postMessage({ type: 'ping' }, '*');
        }
    }, 500);

    setTimeout(() => {
        if (isWasmLoading.value && pingInterval) {
            clearInterval(pingInterval);
            isWasmLoading.value = false;
        }
    }, 10000);
})

onUnmounted(() => {
    window.removeEventListener('message', handleMessage)
    if (pingInterval) clearInterval(pingInterval);
})

const copyCode = () => {
    if (navigator.clipboard && xamlCode.value) {
        navigator.clipboard.writeText(xamlCode.value)
    }
}

const reloadWasm = () => {
    isWasmLoading.value = true;
    isWasmReady.value = false;
    wasmLogs.value = [];
    if (iframeRef.value) {
        iframeRef.value.src = '/avalonia/index.html';
    }
}

// Functional component for rendering VNodes
const VNodeRenderer = (props) => {
    return props.vnodes || null
}
VNodeRenderer.props = ['vnodes']

</script>

<template>
    <div class="my-8 rounded-xl shadow-2xl overflow-hidden bg-white dark:bg-[#202124] border border-gray-200 dark:border-white/5 flex flex-col not-prose transition-all duration-300 font-sans">
        <!-- Visual Studio / Rider inspired Header -->
        <div class="bg-[#f3f3f3] dark:bg-[#2d2d2d] border-b border-gray-300 dark:border-black/50 select-none">
            
            <div class="flex items-center justify-between px-3 h-10">
                <!-- Tabs -->
                <div class="flex items-end h-full pt-2 gap-1">
                    <!-- Preview Tab -->
                    <button
                        @click="activeTab = 'preview'"
                        :class="[
                            'px-4 py-1.5 rounded-t-lg text-[12px] font-medium flex items-center gap-2 transition-colors border border-b-0',
                            activeTab === 'preview'
                                ? 'bg-white dark:bg-[#1e1e1e] text-blue-600 dark:text-blue-400 border-gray-300 dark:border-black/50 z-10'
                                : 'bg-transparent text-gray-600 dark:text-gray-400 border-transparent hover:bg-black/5 dark:hover:bg-white/5'
                        ]"
                    >
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                        WASM Preview
                    </button>

                    <!-- XAML Tab -->
                    <button
                        v-if="xamlCode"
                        @click="activeTab = 'xaml'"
                        :class="[
                            'px-4 py-1.5 rounded-t-lg text-[12px] font-medium flex items-center gap-2 transition-colors border border-b-0',
                            activeTab === 'xaml'
                                ? 'bg-white dark:bg-[#1e1e1e] text-blue-600 dark:text-blue-400 border-gray-300 dark:border-black/50 z-10'
                                : 'bg-transparent text-gray-600 dark:text-gray-400 border-transparent hover:bg-black/5 dark:hover:bg-white/5'
                        ]"
                    >
                        <span class="text-[#0070c0] font-bold">&lt;/&gt;</span>
                        MainWindow.xaml
                    </button>

                    <!-- C# Tab -->
                    <button
                        v-if="csharpCode"
                        @click="activeTab = 'csharp'"
                        :class="[
                            'px-4 py-1.5 rounded-t-lg text-[12px] font-medium flex items-center gap-2 transition-colors border border-b-0',
                            activeTab === 'csharp'
                                ? 'bg-white dark:bg-[#1e1e1e] text-blue-600 dark:text-blue-400 border-gray-300 dark:border-black/50 z-10'
                                : 'bg-transparent text-gray-600 dark:text-gray-400 border-transparent hover:bg-black/5 dark:hover:bg-white/5'
                        ]"
                    >
                        <span class="text-[#0c991b] font-bold">C#</span>
                        MainWindow.xaml.cs
                    </button>

                    <!-- Output Tab -->
                    <button
                        @click="activeTab = 'output'"
                        :class="[
                            'px-4 py-1.5 rounded-t-lg text-[12px] font-medium flex items-center gap-2 transition-colors border border-b-0',
                            activeTab === 'output'
                                ? 'bg-white dark:bg-[#1e1e1e] text-blue-600 dark:text-blue-400 border-gray-300 dark:border-black/50 z-10'
                                : 'bg-transparent text-gray-600 dark:text-gray-400 border-transparent hover:bg-black/5 dark:hover:bg-white/5'
                        ]"
                    >
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 17h16M4 12h16M4 7h16"/></svg>
                        Output
                    </button>
                </div>

                <div class="flex items-center gap-3">
                    <button v-if="activeTab === 'preview'" @click="reloadWasm" title="Reload WASM Host" class="p-1.5 rounded hover:bg-black/10 dark:hover:bg-white/10 text-gray-500 transition-colors">
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
                    </button>
                    <!-- Copy Button -->
                    <button 
                        v-if="activeTab === 'xaml'"
                        @click="copyCode"
                        class="flex items-center gap-1.5 px-3 py-1.5 rounded bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 text-[11px] font-medium text-gray-600 dark:text-gray-300 transition-all"
                    >
                        Copy
                    </button>
                </div>
            </div>
        </div>

        <!-- content -->
        <div class="flex-grow relative bg-white dark:bg-[#1e1e1e] overflow-hidden min-h-[400px] flex">
            <!-- WASM Preview Area -->
            <div v-show="activeTab === 'preview'" class="w-full h-full min-h-[400px] relative flex">
                
                <!-- Real WASM iframe -->
                <iframe 
                    ref="iframeRef" 
                    src="/avalonia/index.html" 
                    class="w-full h-full border-none absolute inset-0 z-10 bg-[#f9f9f9] dark:bg-[#111111]"
                    title="Avalonia WASM Host"
                ></iframe>

                <!-- WASM Loading State Backdrop -->
                <div v-if="isWasmLoading" class="absolute inset-0 z-20 bg-[#2d2d2d] flex flex-col items-center justify-center text-white transition-opacity duration-300">
                    <div class="w-64 text-center">
                        <div class="w-10 h-10 border-4 border-purple-500 border-t-transparent flex items-center justify-center rounded-full animate-spin mx-auto mb-4"></div>
                        <p class="text-[13px] font-semibold text-purple-400">Loading Avalonia WebAssembly...</p>
                        <p class="mt-2 text-[11px] text-gray-400 font-mono">Downloading .NET runtime (10MB)...</p>
                    </div>
                </div>

                <!-- Watermark -->
                <div v-if="!isWasmLoading" class="absolute bottom-2 right-3 opacity-30 text-[10px] font-mono pointer-events-none text-black dark:text-white flex items-center gap-1 z-20">
                    <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 22h20L12 2zm0 4.5l6.5 13h-13L12 6.5z"/></svg>
                    WASM Rendered
                </div>
            </div>

            <!-- XAML View -->
            <div 
                v-show="activeTab === 'xaml'" 
                class="w-full px-6 py-4 code-tab-content animate-in fade-in duration-300 overflow-auto max-h-[600px] bg-white dark:bg-[#1e1e1e]"
            >
                <VNodeRenderer :vnodes="xamlVnodes" />
            </div>

            <!-- C# View -->
            <div 
                v-show="activeTab === 'csharp'" 
                class="w-full px-6 py-4 code-tab-content animate-in fade-in duration-300 overflow-auto max-h-[600px] bg-white dark:bg-[#1e1e1e]"
            >
                <VNodeRenderer :vnodes="csharpVnodes" />
            </div>

            <!-- Output View -->
            <div 
                v-show="activeTab === 'output'" 
                class="w-full px-6 py-4 code-tab-content animate-in fade-in duration-300 overflow-auto max-h-[600px] bg-gray-50 dark:bg-[#111111] font-mono text-[12px]"
            >
                <div v-if="wasmLogs.length === 0" class="text-gray-500 italic">No output yet. Interact with the preview to see logs...</div>
                <div v-for="log in wasmLogs" :key="log.id" class="mb-1">
                    <span class="text-gray-400 dark:text-gray-500">[{{ log.time }}]</span>
                    <span class="text-green-600 dark:text-green-400 ml-2">></span>
                    <span class="text-gray-700 dark:text-gray-300 ml-2">{{ log.message }}</span>
                </div>
            </div>
        </div>

        <div class="hidden">
            <slot />
        </div>
    </div>
</template>

<style scoped>
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    .dark ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
    ::-webkit-scrollbar-thumb { background: #ddd; border-radius: 4px; }
    .dark ::-webkit-scrollbar-thumb:hover { background: #444; }
    ::-webkit-scrollbar-thumb:hover { background: #ccc; }

    .animate-in { animation-duration: 300ms; animation-fill-mode: both; }
    .fade-in { animation-name: fade-in; }
    @keyframes fade-in {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    :deep(pre) {
        margin: 0 !important;
        border-radius: 0 !important;
        border: none !important;
        background-color: transparent !important;
        padding: 0 !important;
        font-size: 13.5px !important;
        line-height: 1.6 !important;
    }
    
    :deep(.code-block) {
        margin: 0 !important;
        border: none !important;
    }
    :deep(.copy-button) {
        display: none !important;
    }
    .code-tab-content :deep(pre) {
        background-color: transparent !important;
    }
</style>
