<script setup>
import { ref, computed, useSlots, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
    title: { type: String, default: 'WPF / Avalonia Preview' },
    height: { type: [String, Number], default: 0 }
})

const slots = useSlots()
const iframeRef = ref(null)
const activeTab = ref('preview')
const instanceId = ref('')
const version = ref(0)
const isWasmLoading = ref(true)
const isWasmReady = ref(false)
const wasmLogs = ref([])
const xamlCode = ref('')
const csharpCode = ref('')
let lastHeightValue = 0
let lastHeightTime = 0

onMounted(() => {
    instanceId.value = Math.random().toString(36).substring(7)
    version.value = Date.now()
    window.addEventListener('message', handleMessage)
    
    // Fallback: ping iframe until it responds
    pingInterval = setInterval(() => {
        if (!isWasmReady.value && iframeRef.value?.contentWindow) {
            iframeRef.value.contentWindow.postMessage({ type: 'ping', id: instanceId.value }, '*');
        }
    }, 500);

    setTimeout(() => {
        if (isWasmLoading.value && pingInterval) {
            clearInterval(pingInterval);
            isWasmLoading.value = false;
        }
    }, 20000); // 20s timeout for multiple instances
})

const findCodesInVNodes = (vnodes, targetLang) => {
    let snippet = '';
    const matchedVNodes = [];

    const find = (nodes) => {
        if (!nodes) return;
        const nodesArray = Array.isArray(nodes) ? nodes : [nodes];
        
        for (const vnode of nodesArray) {
            if (!vnode) continue;
            
            const p = vnode.props || {};
            const lang = p.language || p.lang || '';
            const code = p.code || '';

            if (lang && code) {
                if (targetLang === 'xaml' && (lang === 'xml' || lang === 'xaml' || lang === 'html')) {
                    snippet = code;
                    matchedVNodes.push(vnode);
                } else if (targetLang === 'csharp' && (lang === 'csharp' || lang === 'cs')) {
                    snippet = code;
                    matchedVNodes.push(vnode);
                }
            } else {
                const tag = vnode.type || '';
                const children = vnode.children || '';
                if (typeof children === 'string' && tag === 'code' && p.class?.includes('language-')) {
                   const matchedLang = p.class.replace('language-', '');
                   if (targetLang === 'xaml' && (matchedLang === 'xml' || matchedLang === 'xaml' || matchedLang === 'html')) {
                       snippet = children;
                       matchedVNodes.push(vnode);
                   } else if (targetLang === 'csharp' && (matchedLang === 'csharp' || matchedLang === 'cs')) {
                       snippet = children;
                       matchedVNodes.push(vnode);
                   }
                }
            }
            
            if (vnode.children && Array.isArray(vnode.children)) {
                find(vnode.children);
            } else if (vnode.children && typeof vnode.children === 'object' && vnode.children.default) {
                try { find(vnode.children.default()); } catch (e) {}
            }
            
            if (vnode.component?.subTree) {
                find(vnode.component.subTree);
            }
        }
    };
    find(vnodes);
    return { snippet: snippet.trim(), vnodes: matchedVNodes };
}

const XamlRenderer = () => {
    const vnodes = slots.default?.() || [];
    const result = findCodesInVNodes(vnodes, 'xaml');
    Promise.resolve().then(() => {
        if (xamlCode.value !== result.snippet) xamlCode.value = result.snippet;
    });
    return result.vnodes;
}

const CsharpRenderer = () => {
    const vnodes = slots.default?.() || [];
    const result = findCodesInVNodes(vnodes, 'csharp');
    Promise.resolve().then(() => {
        if (csharpCode.value !== result.snippet) csharpCode.value = result.snippet;
    });
    return result.vnodes;
}

// Theme Synchronization
const colorMode = typeof useColorMode === 'function' ? useColorMode() : { value: 'dark' };
const currentTheme = computed(() => colorMode?.value === 'dark' ? 'dark' : 'light');

const sendThemeToWasm = () => {
    if (isWasmReady.value && iframeRef.value?.contentWindow) {
        iframeRef.value.contentWindow.postMessage({
            type: 'set-theme',
            theme: currentTheme.value,
            id: instanceId.value
        }, '*');
    }
}

const iframeHeight = ref(300);

const sendXamlToWasm = () => {
    if (isWasmReady.value && iframeRef.value?.contentWindow) {
        let finalXaml = xamlCode.value.trim();
        
        // 1. Translate WPF-specific static resources for Avalonia compatibility in preview
        if (finalXaml) {
            let stylesContent = '';
            let triggerStyles = '';

            const triggerMap = {
                'IsMouseOver_True': ':pointerover',
                'IsPressed_True': ':pressed',
                'IsEnabled_False': ':disabled',
                'IsChecked_True': ':checked',
                'IsSelected_True': ':selected',
                'IsFocused_True': ':focus'
            };

            // Remove XAML comments to simplify parsing
            finalXaml = finalXaml.replace(/<!--[\s\S]*?-->/g, '');

            // Strip VisualStateManager and EventTriggers to avoid crashes
            finalXaml = finalXaml.replace(/<VisualStateManager\.VisualStateGroups>[\s\S]*?<\/VisualStateManager\.VisualStateGroups>/gi, '');
            finalXaml = finalXaml.replace(/<EventTrigger[\s\S]*?<\/EventTrigger>/gi, '');
            finalXaml = finalXaml.replace(/<(ControlTemplate|DataTemplate)\.Triggers>[\s\S]*?<\/\1\.Triggers>/gi, '');

            // Rewrite WPF Style elements and extract Triggers
            finalXaml = finalXaml.replace(/<Style([^>]*)>([\s\S]*?)<\/Style>/gi, (match, styleAttrs, innerContent) => {
                let newAttrs = styleAttrs.replace(/\sBasedOn="[^"]+"/g, '');
                let selector = '';

                let targetTypeParam = newAttrs.match(/TargetType="(?:\{x:Type\s+)?([a-zA-Z0-9_:]+)\}?"/);
                let keyParam = newAttrs.match(/x:Key="([^"]+)"/);

                if (newAttrs.includes('Selector=')) {
                    let selMatch = newAttrs.match(/Selector="([^"]+)"/);
                    if (selMatch) selector = selMatch[1];
                } else if (targetTypeParam) {
                    let type = targetTypeParam[1];
                    if (keyParam) {
                        let key = keyParam[1];
                        selector = key === 'BaseButton' ? type : `${type}.${key}`;
                    } else {
                        selector = type;
                    }
                    newAttrs = newAttrs.replace(/\s?x:Key="[^"]+"/, '').replace(/\s?TargetType="[^"]+"/, '');
                    newAttrs += ` Selector="${selector}"`;
                }

                // Process <Style.Triggers>
                let cleanedInner = innerContent.replace(/<Style\.Triggers>([\s\S]*?)<\/Style\.Triggers>/i, (tMatch, triggersContent) => {
                    // Extract <Trigger>
                    triggersContent.replace(/<Trigger\s+Property="([^"]+)"\s+Value="([^"]+)"[^>]*>([\s\S]*?)<\/Trigger>/gi, (trigMatch, prop, val, setters) => {
                        let pseudoKey = `${prop}_${val}`;
                        let pseudoClass = triggerMap[pseudoKey];
                        if (!pseudoClass && prop === 'IsChecked' && val === 'False') pseudoClass = ':unchecked';
                        
                        if (pseudoClass && selector) {
                            triggerStyles += `<Style Selector="${selector}${pseudoClass}">\n${setters}\n</Style>\n`;
                        }
                        return '';
                    });
                    
                    return ''; // Strip Style.Triggers completely to avoid WASM crash
                });

                return `<Style${newAttrs}>${cleanedInner}</Style>`;
            });

            // Extract all <Style> elements firmly with case insensitivity
            finalXaml = finalXaml.replace(/<Style[\s\S]*?<\/Style>/gi, (match) => {
                stylesContent += match + '\n';
                return '';
            });

            // Clean up empty containers
            finalXaml = finalXaml.replace(/<([a-zA-Z0-9_]+)\.(Resources|Styles)>\s*<\/\1\.\2>/g, '');
            finalXaml = finalXaml.replace(/\sBasedOn="[^"]+"/g, '');
            finalXaml = finalXaml.replace(/\bStyle="\{StaticResource\s+([^}]+)\}"/g, 'Classes="$1"');

            // Refactored Simple Regex Replacements
            const simpleReplacements = [
                { from: /<PasswordBox\b/g, to: '<TextBox PasswordChar="*"' },
                { from: /<\/PasswordBox>/g, to: '</TextBox>' },
                { from: /\{x:Static SystemColors\.HighlightBrush\}/g, to: "Blue" },
                { from: /\{x:Static SystemColors\.HighlightTextBrush\}/g, to: "White" },
                { from: /\{x:Static SystemColors\.HotTrackBrush\}/g, to: "Blue" },
                { from: /\{x:Static SystemColors\.WindowBrush\}/g, to: "White" },
                { from: /\{x:Static SystemColors\.ActiveBorderBrush\}/g, to: "Gray" },
                { from: /\{x:Static SystemColors\.WindowTextBrush\}/g, to: "Black" },
                { from: /\{x:Static FlowDirection\.RightToLeft\}/g, to: "RightToLeft" },
                { from: /\bToolTip="/g, to: 'ToolTip.Tip="' },
                { from: /<([a-zA-Z0-9_]+)\.ToolTip\b([^>]*)>/g, to: '<ToolTip.Tip$2>' },
                { from: /<\/([a-zA-Z0-9_]+)\.ToolTip\s*>/g, to: '</ToolTip.Tip>' },
                { from: /<StatusBar\b/g, to: '<Border BorderBrush="#cbd5e1" BorderThickness="0,1,0,0"' },
                { from: /<\/StatusBar>/g, to: '</Border>' },
                { from: /<StatusBarItem\b/g, to: '<ContentControl' },
                { from: /<\/StatusBarItem>/g, to: '</ContentControl>' },
                { from: /\bVisibility="Collapsed"/g, to: 'IsVisible="False"' },
                { from: /\bVisibility="Hidden"/g, to: 'IsHitTestVisible="False" Opacity="0"' },
                { from: /\bVisibility="Visible"/g, to: 'IsVisible="True" Opacity="1"' },
                { from: /<WrapPanel\b([^>]*)\bSpacing="([^"]+)"/g, to: '<WrapPanel$1ItemSpacing="$2"' },
                { from: /\bScrollViewer\.(Vertical|Horizontal)ScrollBarVisibility/g, to: '$1ScrollBarVisibility' },
                { from: /\b(Vertical|Horizontal)ScrollBarVisibility="([^"]+)"/g, to: 'ScrollViewer.$1ScrollBarVisibility="$2"' },
                { from: /\bRenderOptions\.BitmapScalingMode="([^"]+)"/g, to: 'RenderOptions.BitmapInterpolationMode="$1"' },
                { from: /\bTickPlacement="Both"/g, to: 'TickPlacement="Outside"' },
                { from: /\bTextWrapping="WrapWithOverflow"/g, to: 'TextWrapping="Wrap"' },
                { from: /\b(Click|TextChanged|SelectionChanged|Checked|Unchecked|Opened|Closed|Scroll|Pointer[a-zA-Z]*|Mouse[a-zA-Z]*|Key(Down|Up|Press))="[^"{}]*"\s?/gi, to: '' },
                { from: /\bSource="https?:\/\/[^"]+"/g, to: 'Source="avares://AvaloniaHost/Assets/placeholder.png"' },
                { from: /\bCursor="SizeWE"/g, to: 'Cursor="SizeWestEast"' },
                { from: /\bCursor="SizeNS"/g, to: 'Cursor="SizeNorthSouth"' }
            ];

            simpleReplacements.forEach(r => {
                finalXaml = finalXaml.replace(r.from, r.to);
            });

            // Special dynamic replacements
            finalXaml = finalXaml.replace(/([Pp]adding|[Mm]argin|[Cc]orner[Rr]adius)="([^"]+)"/g, (m, prop, val) => {
                return `${prop}="${val.replace(/,/g, ' ')}"`;
            });
            finalXaml = finalXaml.replace(/\b(StartPoint|EndPoint)="([0-9.-]+),([0-9.-]+)"/g, (m, prop, x, y) => {
                return `${prop}="${parseFloat(x)*100}%,${parseFloat(y)*100}%"`;
            });

            // Wrap in Grid if styles were extracted
            if (stylesContent || triggerStyles) {
                 finalXaml = `<Grid>\n<Grid.Styles>\n${stylesContent}\n${triggerStyles}</Grid.Styles>\n${finalXaml}\n</Grid>`;
            }
        }

        // 2. Inject default Avalonia namespaces if missing, to allow rendering raw snippets without Window boilerplate
        if (finalXaml && !finalXaml.includes('xmlns=')) {
            finalXaml = finalXaml.replace(/<([a-zA-Z0-9_:]+)/, '<$1 xmlns="https://github.com/avaloniaui" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:d="http://schemas.microsoft.com/expression/blend/2008" mc:Ignorable="d"');
        }

        iframeRef.value.contentWindow.postMessage({
            type: 'update-xaml',
            xaml: finalXaml,
            id: instanceId.value
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
    if (!event.data) return;
    
    if (event.data.id !== instanceId.value) return;
    
    if (event.data.type === 'set-height') {
        const height = event.data.height;
        if (height > 0 && !props.height) {
            iframeHeight.value = Math.max(150, Math.ceil(height));
        }
    }
    if (event.data.type === 'avalonia-ready') {
        console.log(`[Vue-WpfPreview] Instance ${instanceId.value} ready!`);
        isWasmLoading.value = false
        isWasmReady.value = true
        if (pingInterval) {
            clearInterval(pingInterval);
            pingInterval = null;
        }
        sendXamlToWasm()
    }
    if (event.data.type === 'wasm-log') {
        wasmLogs.value.push({
            id: Date.now() + Math.random(),
            message: event.data.message,
            time: new Date().toLocaleTimeString(),
            isError: false
        })
        if (wasmLogs.value.length > 50) wasmLogs.value.shift()
    }
    if (event.data.type === 'wasm-error') {
        let { message, xaml } = event.data;
        
        // Extract all possible line numbers (for AggregateExceptions or multiple errors)
        const lineMatches = [...message.matchAll(/,\s*(\d+),\s*\d+(?=\s*\)|$)/g)];
        const problemLineNums = lineMatches.length > 0 
            ? lineMatches.map(m => parseInt(m[1], 10)) 
            : [];
        
        // If matched via other formats, add them too
        if (problemLineNums.length === 0) {
            let altMatch = message.match(/[Ll]ine\s+(\d+)/) || message.match(/\((\d+),\d+\)/);
            if (altMatch) problemLineNums.push(parseInt(altMatch[1], 10));
        }

        // Clean up the error message
        let cleanedMessage = message
            .replace(/^AggregateException_ctor_DefaultMessage\s*/, 'Multiple XAML Errors:')
            .replace(/Xml_MessageWithErrorPosition, Xml_UserException, /g, '')
            .replace(/\(([^)]+)\)/g, '\n  • $1') // Format multiple errors as bullets
            .trim();

        // If it's the "7, 4" lone format, prefix it
        if (/^\d+,\s*\d+$/.test(cleanedMessage)) {
            cleanedMessage = 'XAML Parse Error: ' + cleanedMessage;
        }

        console.group(`%c ❌ Avalonia XAML Parse Error `, `background: #dc2626; color: #ffffff; font-weight: bold; border-radius: 4px; padding: 2px 6px;`);
        console.error(cleanedMessage);
        
        if (xaml) {
            const lines = xaml.split('\n');
            console.log('%c--- Problematic Code ---', 'color: #888; font-style: italic;');
            
            lines.forEach((line, index) => {
                const currentLineNum = index + 1;
                const isErrorLine = problemLineNums.includes(currentLineNum);
                const isNearError = problemLineNums.some(num => Math.abs(currentLineNum - num) <= 3);

                if (problemLineNums.length > 0) {
                    if (isNearError) {
                        if (isErrorLine) {
                            console.log(`%c${currentLineNum.toString().padStart(3, ' ')} | %c${line}`, 'color: #888;', 'color: #ef4444; font-weight: bold; background: rgba(239, 68, 68, 0.1); padding: 2px 2px;');
                        } else {
                            console.log(`%c${currentLineNum.toString().padStart(3, ' ')} | ${line}`, 'color: #888;');
                        }
                    }
                } else if (index < 10) {
                    console.log(`%c${currentLineNum.toString().padStart(3, ' ')} | ${line}`, 'color: #888;');
                }
            });
            
            if (problemLineNums.length === 0 && lines.length > 10) {
                console.log(`%c... (+ ${lines.length - 10} more lines)`, 'color: #888; font-style: italic;');
            }
            console.log('%c------------------------', 'color: #888; font-style: italic;');
        }
        console.groupEnd();
        
        wasmLogs.value.push({
            id: Date.now() + Math.random(),
            message: "XAML Error: " + message.split('\n')[0],
            time: new Date().toLocaleTimeString(),
            isError: true
        });
        if (wasmLogs.value.length > 50) wasmLogs.value.shift();
    }
}

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
        <div class="flex-grow relative bg-white dark:bg-[#1e1e1e] overflow-hidden flex" :style="{ minHeight: (height || iframeHeight) + 'px' }">
            <!-- WASM Preview Area -->
            <div v-show="activeTab === 'preview'" class="w-full h-full relative flex" :style="{ minHeight: iframeHeight + 'px' }">
                
                <!-- Real WASM iframe -->
                <ClientOnly>
                    <iframe 
                        v-if="instanceId"
                        ref="iframeRef" 
                        :src="`/avalonia/index.html?v=${version}&id=${instanceId}`" 
                        class="w-full h-full border-none absolute inset-0 z-10 bg-[#f9f9f9] dark:bg-[#111111]"
                        title="Avalonia WASM Host"
                    ></iframe>
                </ClientOnly>

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
                <ClientOnly>
                    <XamlRenderer />
                </ClientOnly>
            </div>

            <!-- C# View -->
            <div 
                v-show="activeTab === 'csharp'" 
                class="w-full px-6 py-4 code-tab-content animate-in fade-in duration-300 overflow-auto max-h-[600px] bg-white dark:bg-[#1e1e1e]"
            >
                <ClientOnly>
                    <CsharpRenderer />
                </ClientOnly>
            </div>

            <!-- Output View -->
            <div 
                v-show="activeTab === 'output'" 
                class="w-full px-6 py-4 code-tab-content animate-in fade-in duration-300 overflow-auto max-h-[600px] bg-gray-50 dark:bg-[#111111] font-mono text-[12px]"
            >
                <div v-if="wasmLogs.length === 0" class="text-gray-500 italic">No output yet. Interact with the preview to see logs...</div>
                <div v-for="log in wasmLogs" :key="log.id" class="mb-1">
                    <span class="text-gray-400 dark:text-gray-500">[{{ log.time }}]</span>
                    <span :class="log.isError ? 'text-red-500' : 'text-green-600 dark:text-green-400'" class="ml-2">></span>
                    <span :class="log.isError ? 'text-red-500 dark:text-red-400' : 'text-gray-700 dark:text-gray-300'" class="ml-2">{{ log.message }}</span>
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
