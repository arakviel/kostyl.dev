<script setup>
import { ref, computed, useSlots, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute } from 'nuxt/app'

const props = defineProps({
    /** Window / device label */
    title: { type: String, default: 'React Native' },
    /** Phone frame style */
    device: {
        type: String,
        default: 'iphone',
        validator: (v) => ['iphone', 'android', 'plain'].includes(v),
    },
    /** Screen height inside the phone (px) */
    height: { type: [String, Number], default: 640 },
    /** Filename shown above the code panel */
    filename: { type: String, default: 'App.tsx' },
    /** Force light/dark inside preview; omit to follow site color mode */
    theme: {
        type: String,
        default: undefined,
        validator: (v) => v === undefined || ['light', 'dark'].includes(v),
    },
})

const slots = useSlots()
const route = useRoute()
const iframeRef = ref(null)
const slotRootRef = ref(null)
const splitBodyRef = ref(null)

/**
 * Layout mode:
 * - split: code | phone (default)
 * - code: full code
 * - preview: full phone
 */
const layoutMode = ref('split')
/** Code panel share of split width (0.22–0.78). Default ~65% code / 35% phone. */
const codeRatio = ref(0.65)
const isDragging = ref(false)
/** Desktop row layout (resizer active) */
const isLg = ref(false)

const instanceId = ref(
    typeof window !== 'undefined' ? Math.random().toString(36).slice(2, 9) : '',
)
const hostReady = ref(false)
const isLoading = ref(true)
const lastError = ref('')
const hostVersion = ref(Date.now())
const copied = ref(false)
const domTheme = ref('light')
const domFallbackCode = ref('')
let pingInterval = null
let themeObserver = null
let copyTimer = null
let lgMqlCleanup = null

const colorMode =
    typeof useColorMode === 'function' ? useColorMode() : { value: 'light' }

const readDomTheme = () => {
    if (!import.meta.client) return 'light'
    const el = document.documentElement
    if (el.classList.contains('dark')) return 'dark'
    if (el.classList.contains('light')) return 'light'
    const attr =
        el.getAttribute('data-theme') ||
        el.getAttribute('data-color-mode') ||
        el.getAttribute('data-mode')
    if (attr === 'dark' || attr === 'light') return attr
    const scheme = getComputedStyle(el).colorScheme
    if (scheme?.includes('dark') && !scheme.includes('light')) return 'dark'
    return 'light'
}

const resolvedTheme = computed(() => {
    if (props.theme === 'light' || props.theme === 'dark') return props.theme
    if (import.meta.client && (domTheme.value === 'dark' || domTheme.value === 'light')) {
        return domTheme.value
    }
    const v = colorMode?.value
    if (v === 'dark' || v === 'light') return v
    const pref = colorMode?.preference
    if (pref === 'dark' || pref === 'light') return pref
    return 'light'
})

const isDark = computed(() => resolvedTheme.value === 'dark')

const screenPalette = computed(() =>
    isDark.value
        ? {
              statusBg: '#000000',
              statusFg: '#f5f5f7',
              screenBg: '#000000',
              iframeBg: '#000000',
              loadingBg: '#000000',
              loadingFg: '#a1a1aa',
          }
        : {
              statusBg: '#f2f2f7',
              statusFg: '#1c1c1e',
              screenBg: '#f2f2f7',
              iframeBg: '#f2f2f7',
              loadingBg: '#f2f2f7',
              loadingFg: '#71717a',
          },
)

const screenHeight = computed(() => {
    const n = Number(props.height)
    return Number.isFinite(n) && n > 0 ? n : 640
})

/**
 * Extra vertical space around the phone so the preview column never needs scroll:
 * status bar + home indicator + borders + device label + caption + compact padding.
 */
const PHONE_COLUMN_CHROME = 148

/** Body height fits the phone column exactly (code scrolls independently). */
const panelMinHeight = computed(() =>
    Math.max(screenHeight.value + PHONE_COLUMN_CHROME, 400),
)

/** Phone chrome max width — wider default */
const phoneFrameMax = 390

const findCodesInVNodes = (vnodes) => {
    let snippet = ''
    let snippetRank = -1
    const matchedVNodes = []
    const rankOf = (lang) => {
        if (!lang) return 0
        if (lang === 'tsx' || lang === 'jsx') return 3
        if (lang === 'typescript' || lang === 'ts') return 2
        if (lang === 'javascript' || lang === 'js') return 1
        return 0
    }
    const langFromClass = (cls) => {
        if (!cls || typeof cls !== 'string') return ''
        const m = cls.match(/language-([a-z0-9+#-]+)/i)
        return (m?.[1] || '').toLowerCase()
    }
    const consider = (lang, code, vnode) => {
        if (!code || typeof code !== 'string') return
        const rank = rankOf((lang || '').toLowerCase())
        if (rank > snippetRank) {
            snippet = code
            snippetRank = rank
            matchedVNodes.length = 0
            matchedVNodes.push(vnode)
        }
    }
    const find = (nodes) => {
        if (!nodes) return
        const list = Array.isArray(nodes) ? nodes : [nodes]
        for (const vnode of list) {
            if (!vnode) continue
            const p = vnode.props || {}
            const lang = (
                p.language ||
                p.lang ||
                langFromClass(p.className || p.class) ||
                ''
            ).toLowerCase()
            const code = p.code || ''
            if (code) {
                consider(lang, code, vnode)
            } else {
                const tag = vnode.type || ''
                const children = vnode.children || ''
                const cls = p.className || p.class || ''
                if (typeof children === 'string' && (tag === 'code' || langFromClass(cls))) {
                    consider(lang || langFromClass(cls), children, vnode)
                }
            }
            if (vnode.children && Array.isArray(vnode.children)) {
                find(vnode.children)
            } else if (vnode.children && typeof vnode.children === 'object' && vnode.children.default) {
                try {
                    find(vnode.children.default())
                } catch {
                    /* ignore */
                }
            }
            if (vnode.component?.subTree) {
                find(vnode.component.subTree)
            }
        }
    }
    find(vnodes)
    return { snippet: snippet.trim(), vnodes: matchedVNodes }
}

const extracted = computed(() => {
    const defaultSlot = slots.default?.() || []
    return findCodesInVNodes(defaultSlot)
})

const sourceCode = computed(() => extracted.value.snippet || domFallbackCode.value || '')
const codeVnodes = computed(() => extracted.value.vnodes)
const hasCode = computed(() => Boolean(sourceCode.value?.trim() || codeVnodes.value?.length))

const showCode = computed(
    () => hasCode.value && (layoutMode.value === 'split' || layoutMode.value === 'code'),
)
const showPreview = computed(
    () => layoutMode.value === 'split' || layoutMode.value === 'preview' || !hasCode.value,
)
const showResizer = computed(() => hasCode.value && layoutMode.value === 'split' && isLg.value)

const codePanelStyle = computed(() => {
    if (layoutMode.value === 'code') {
        return { flex: '1 1 100%', width: '100%' }
    }
    if (layoutMode.value === 'split' && hasCode.value) {
        if (isLg.value) {
            const pct = `${(codeRatio.value * 100).toFixed(2)}%`
            return {
                flex: `0 0 ${pct}`,
                width: pct,
                maxWidth: '78%',
                minWidth: '180px',
            }
        }
        return { width: '100%', flex: '0 0 auto' }
    }
    return {}
})

const previewPanelStyle = computed(() => {
    if (layoutMode.value === 'preview' || !hasCode.value) {
        return { flex: '1 1 100%', width: '100%' }
    }
    if (layoutMode.value === 'split' && isLg.value) {
        return {
            flex: '1 1 0%',
            minWidth: '200px',
        }
    }
    if (layoutMode.value === 'split') {
        return { width: '100%', flex: '0 0 auto' }
    }
    return {}
})

/** Same height for Split / Code / Preview — no jump when switching layout mode. */
const bodyHeightPx = computed(() => panelMinHeight.value)

const extractCodeFromDom = () => {
    const root = slotRootRef.value
    if (!root || !import.meta.client) return ''
    const pre = root.querySelector('pre[class*="language-"], pre')
    if (!pre) return ''
    return (pre.textContent || '').trim()
}

const CodeRenderer = {
    props: ['vnodes'],
    render() {
        return this.vnodes
    },
}

const postToHost = (payload) => {
    const win = iframeRef.value?.contentWindow
    if (!win) return
    win.postMessage({ ...payload, id: instanceId.value }, '*')
}

const sendCode = () => {
    if (!hostReady.value) return
    if (!sourceCode.value?.trim()) return
    postToHost({
        type: 'run-code',
        code: sourceCode.value,
        theme: resolvedTheme.value,
    })
}

const sendTheme = () => {
    if (!hostReady.value) return
    postToHost({
        type: 'set-theme',
        theme: resolvedTheme.value,
    })
}

const handleMessage = (event) => {
    const data = event.data
    if (!data || typeof data !== 'object') return
    const win = iframeRef.value?.contentWindow
    if (win && event.source && event.source !== win) return
    if (data.id && instanceId.value && data.id !== instanceId.value) return

    switch (data.type) {
        case 'rn-preview-ready':
        case 'rn-preview-pong':
            hostReady.value = true
            nextTick(() => sendCode())
            break
        case 'rn-preview-success':
            lastError.value = ''
            isLoading.value = false
            break
        case 'rn-preview-error':
            lastError.value = data.message || 'Unknown error'
            isLoading.value = false
            break
    }
}

const reloadHost = () => {
    hostReady.value = false
    isLoading.value = true
    lastError.value = ''
    hostVersion.value = Date.now()
}

const copyCode = async () => {
    if (!sourceCode.value || !navigator.clipboard) return
    try {
        await navigator.clipboard.writeText(sourceCode.value)
        copied.value = true
        if (copyTimer) clearTimeout(copyTimer)
        copyTimer = setTimeout(() => {
            copied.value = false
        }, 1600)
    } catch {
        /* ignore */
    }
}

const setLayoutMode = (mode) => {
    layoutMode.value = mode
}

const clampRatio = (r) => Math.min(0.78, Math.max(0.22, r))

const onResizerPointerDown = (e) => {
    if (layoutMode.value !== 'split' || !isLg.value) return
    e.preventDefault()
    isDragging.value = true
    const target = e.currentTarget
    target.setPointerCapture?.(e.pointerId)

    const onMove = (ev) => {
        const el = splitBodyRef.value
        if (!el) return
        const rect = el.getBoundingClientRect()
        if (rect.width < 80) return
        codeRatio.value = clampRatio((ev.clientX - rect.left) / rect.width)
    }

    const onUp = (ev) => {
        isDragging.value = false
        try {
            target.releasePointerCapture?.(ev.pointerId)
        } catch {
            /* ignore */
        }
        window.removeEventListener('pointermove', onMove)
        window.removeEventListener('pointerup', onUp)
        window.removeEventListener('pointercancel', onUp)
    }

    window.addEventListener('pointermove', onMove)
    window.addEventListener('pointerup', onUp)
    window.addEventListener('pointercancel', onUp)
}

const nudgeRatio = (delta) => {
    codeRatio.value = clampRatio(codeRatio.value + delta)
}

const deviceLabel = computed(() => {
    if (props.device === 'android') return 'Android'
    if (props.device === 'plain') return 'Preview'
    return 'iPhone'
})

let mqlCleanup = null

onMounted(() => {
    if (!instanceId.value) {
        instanceId.value = Math.random().toString(36).slice(2, 9)
    }
    window.addEventListener('message', handleMessage)

    const lgMql = window.matchMedia('(min-width: 1024px)')
    const onLg = () => {
        isLg.value = lgMql.matches
    }
    onLg()
    lgMql.addEventListener('change', onLg)
    lgMqlCleanup = () => lgMql.removeEventListener('change', onLg)

    domTheme.value = readDomTheme()
    themeObserver = new MutationObserver(() => {
        const next = readDomTheme()
        if (next !== domTheme.value) domTheme.value = next
    })
    themeObserver.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['class', 'data-theme', 'data-color-mode', 'data-mode', 'style'],
    })

    const mql = window.matchMedia?.('(prefers-color-scheme: dark)')
    const onMql = () => {
        const el = document.documentElement
        if (!el.classList.contains('dark') && !el.classList.contains('light')) {
            domTheme.value = mql.matches ? 'dark' : 'light'
        }
    }
    mql?.addEventListener?.('change', onMql)
    mqlCleanup = () => mql?.removeEventListener?.('change', onMql)

    nextTick(() => {
        if (!extracted.value.snippet) {
            const fromDom = extractCodeFromDom()
            if (fromDom) domFallbackCode.value = fromDom
        }
        if (hostReady.value) sendCode()
    })

    pingInterval = setInterval(() => {
        if (!hostReady.value && iframeRef.value?.contentWindow) {
            postToHost({ type: 'ping' })
        }
        if (hostReady.value && sourceCode.value?.trim() && isLoading.value) {
            sendCode()
        }
        if (!sourceCode.value?.trim()) {
            const fromDom = extractCodeFromDom()
            if (fromDom) domFallbackCode.value = fromDom
        }
    }, 400)

    setTimeout(() => {
        if (isLoading.value) {
            isLoading.value = false
            if (!hostReady.value) {
                lastError.value =
                    'Preview host did not respond. Rebuild tools/rn-preview → public/rn-preview.'
            } else if (!sourceCode.value?.trim()) {
                lastError.value =
                    'No TSX/JS code found in preview slot. Use a ```tsx fenced block inside ::react-native-preview.'
            }
        }
    }, 15000)
})

onUnmounted(() => {
    window.removeEventListener('message', handleMessage)
    if (pingInterval) clearInterval(pingInterval)
    if (themeObserver) {
        themeObserver.disconnect()
        themeObserver = null
    }
    if (mqlCleanup) {
        mqlCleanup()
        mqlCleanup = null
    }
    if (lgMqlCleanup) {
        lgMqlCleanup()
        lgMqlCleanup = null
    }
    if (copyTimer) clearTimeout(copyTimer)
})

watch(sourceCode, (code) => {
    if (hostReady.value && code?.trim()) sendCode()
})

watch(resolvedTheme, (theme, prev) => {
    if (theme === prev) return
    sendTheme()
})

watch(
    () => route.path,
    () => {
        layoutMode.value = 'split'
    },
)
</script>

<template>
    <div
        class="my-8 rounded-xl shadow-2xl overflow-hidden bg-white dark:bg-[#202124] border border-gray-200 dark:border-white/5 flex flex-col not-prose font-sans"
        :class="isDragging && 'select-none'"
    >
        <!-- Header -->
        <div
            class="bg-[#f3f3f3] dark:bg-[#2d2d2d] border-b border-gray-300 dark:border-black/50 select-none shrink-0"
        >
            <div class="flex items-center justify-between gap-2 px-2 sm:px-3 h-11 min-w-0">
                <div class="flex items-center gap-2 min-w-0">
                    <span class="text-[#61dafb] font-bold text-[12px] shrink-0">TSX</span>
                    <span class="truncate text-[12px] font-medium text-gray-700 dark:text-gray-200">
                        {{ filename }}
                    </span>
                    <span
                        v-if="title"
                        class="hidden md:inline text-[10px] font-mono text-gray-400 dark:text-gray-500 truncate max-w-[10rem]"
                    >
                        · {{ title }}
                    </span>
                </div>

                <div class="flex items-center gap-1.5 shrink-0">
                    <div
                        v-if="hasCode"
                        class="flex items-center rounded-lg p-0.5 bg-black/5 dark:bg-white/5 border border-black/5 dark:border-white/10"
                        role="group"
                        aria-label="Layout mode"
                    >
                        <button
                            type="button"
                            title="Split: code + preview"
                            :aria-pressed="layoutMode === 'split'"
                            :class="[
                                'flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-colors',
                                layoutMode === 'split'
                                    ? 'bg-white dark:bg-[#3a3a3c] text-sky-600 dark:text-sky-400 shadow-sm'
                                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200',
                            ]"
                            @click="setLayoutMode('split')"
                        >
                            <svg
                                class="w-3.5 h-3.5"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <rect x="3" y="3" width="18" height="18" rx="2" />
                                <line x1="12" y1="3" x2="12" y2="21" />
                            </svg>
                            <span class="hidden sm:inline">Split</span>
                        </button>
                        <button
                            type="button"
                            title="Code only"
                            :aria-pressed="layoutMode === 'code'"
                            :class="[
                                'flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-colors',
                                layoutMode === 'code'
                                    ? 'bg-white dark:bg-[#3a3a3c] text-sky-600 dark:text-sky-400 shadow-sm'
                                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200',
                            ]"
                            @click="setLayoutMode('code')"
                        >
                            <svg
                                class="w-3.5 h-3.5"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <polyline points="16 18 22 12 16 6" />
                                <polyline points="8 6 2 12 8 18" />
                            </svg>
                            <span class="hidden sm:inline">Code</span>
                        </button>
                        <button
                            type="button"
                            title="Preview only"
                            :aria-pressed="layoutMode === 'preview'"
                            :class="[
                                'flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-colors',
                                layoutMode === 'preview'
                                    ? 'bg-white dark:bg-[#3a3a3c] text-sky-600 dark:text-sky-400 shadow-sm'
                                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200',
                            ]"
                            @click="setLayoutMode('preview')"
                        >
                            <svg
                                class="w-3.5 h-3.5"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
                                <line x1="12" y1="18" x2="12.01" y2="18" />
                            </svg>
                            <span class="hidden sm:inline">Preview</span>
                        </button>
                    </div>

                    <button
                        v-if="hasCode"
                        type="button"
                        class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-[11px] font-medium text-gray-600 dark:text-gray-300 bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 transition-colors"
                        @click="copyCode"
                    >
                        {{ copied ? 'Copied' : 'Copy' }}
                    </button>

                    <button
                        type="button"
                        title="Reload preview host"
                        class="p-1.5 rounded-md hover:bg-black/10 dark:hover:bg-white/10 text-gray-500 transition-colors"
                        @click="reloadHost"
                    >
                        <svg
                            class="w-4 h-4"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                            <path d="M3 3v5h5" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Body -->
        <div
            ref="splitBodyRef"
            class="flex bg-[#e8e8ed] dark:bg-[#111111] min-h-0"
            :class="[
                layoutMode === 'split' && hasCode ? 'flex-col lg:flex-row' : 'flex-row',
                isDragging && 'cursor-col-resize',
            ]"
            :style="{ height: bodyHeightPx + 'px', minHeight: bodyHeightPx + 'px' }"
        >
            <!-- Code -->
            <div
                v-show="showCode"
                class="flex flex-col min-w-0 min-h-0 h-full bg-white dark:bg-[#1e1e1e] border-b lg:border-b-0 border-gray-200 dark:border-white/5"
                :style="codePanelStyle"
            >
                <div
                    class="code-panel-scroll min-h-0 flex-1 overflow-auto w-full px-3 sm:px-4 pt-2 pb-0"
                >
                    <ClientOnly>
                        <CodeRenderer v-if="codeVnodes?.length" :vnodes="codeVnodes" />
                        <pre
                            v-else-if="sourceCode"
                            class="m-0 p-0 text-[13px] leading-relaxed font-mono text-gray-800 dark:text-gray-200 whitespace-pre-wrap break-words"
                        >{{ sourceCode }}</pre>
                    </ClientOnly>
                </div>
            </div>

            <!-- Resizer -->
            <div
                v-if="showResizer"
                class="flex group relative w-2.5 shrink-0 cursor-col-resize items-stretch justify-center z-10 bg-transparent hover:bg-sky-500/15 active:bg-sky-500/25 transition-colors"
                role="separator"
                aria-orientation="vertical"
                aria-label="Resize code and preview"
                :aria-valuenow="Math.round(codeRatio * 100)"
                aria-valuemin="22"
                aria-valuemax="78"
                tabindex="0"
                @pointerdown="onResizerPointerDown"
                @keydown.left.prevent="nudgeRatio(-0.03)"
                @keydown.right.prevent="nudgeRatio(0.03)"
            >
                <div
                    class="w-px self-stretch bg-gray-300 dark:bg-white/10 group-hover:bg-sky-500 group-active:bg-sky-500 transition-colors"
                />
                <div
                    class="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col gap-0.5 items-center opacity-70 group-hover:opacity-100"
                >
                    <span class="w-1 h-1 rounded-full bg-gray-500 dark:bg-gray-300 group-hover:bg-sky-500" />
                    <span class="w-1 h-1 rounded-full bg-gray-500 dark:bg-gray-300 group-hover:bg-sky-500" />
                    <span class="w-1 h-1 rounded-full bg-gray-500 dark:bg-gray-300 group-hover:bg-sky-500" />
                </div>
            </div>

            <!-- Phone (never scrolls — body height is sized to fit this column) -->
            <div
                v-show="showPreview"
                class="flex flex-col items-center justify-center px-3 sm:px-4 py-2 bg-[#e8e8ed] dark:bg-[#111111] min-w-0 min-h-0 h-full overflow-hidden"
                :style="previewPanelStyle"
            >
                <div
                    class="flex items-center gap-1.5 mb-1.5 shrink-0 text-[11px] font-medium text-gray-500 dark:text-gray-400"
                >
                    <svg
                        class="w-3.5 h-3.5 shrink-0"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
                        <line x1="12" y1="18" x2="12.01" y2="18" />
                    </svg>
                    <span>{{ deviceLabel }}</span>
                </div>

                <div
                    :class="[
                        'relative shrink-0 bg-black shadow-2xl overflow-hidden',
                        device === 'iphone' && 'rounded-[2.5rem] border-[10px] border-[#1c1c1e]',
                        device === 'android' && 'rounded-[1.75rem] border-[8px] border-[#2c2c2c]',
                        device === 'plain' &&
                            'rounded-xl border border-gray-300 dark:border-white/10 w-full max-w-lg',
                    ]"
                    :style="{
                        width: device === 'plain' ? '100%' : `min(${phoneFrameMax}px, 100%)`,
                        maxWidth: device === 'plain' ? '100%' : phoneFrameMax + 'px',
                    }"
                >
                    <div
                        v-if="device === 'iphone'"
                        class="absolute top-0 left-1/2 -translate-x-1/2 z-20 w-[120px] h-[28px] bg-black rounded-b-2xl pointer-events-none"
                    />
                    <div
                        v-else-if="device === 'android'"
                        class="absolute top-2 left-1/2 -translate-x-1/2 z-20 w-3 h-3 rounded-full bg-[#1a1a1a] border border-white/10 pointer-events-none"
                    />

                    <div
                        v-if="device !== 'plain'"
                        class="relative z-10 h-11 flex items-end justify-between px-6 pb-1 text-[11px] font-semibold pointer-events-none select-none transition-colors duration-150"
                        :style="{
                            background: screenPalette.statusBg,
                            color: screenPalette.statusFg,
                        }"
                    >
                        <span class="tabular-nums">9:41</span>
                        <div class="flex items-center gap-1 opacity-80">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M2 17h2v4H2v-4zm4-5h2v9H6v-9zm4-4h2v13h-2V8zm4-3h2v16h-2V5zm4-2h2v18h-2V3z"
                                />
                            </svg>
                            <svg class="w-4 h-3.5" viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M15.67 4H14V2h-4v2H8.33C7.6 4 7 4.6 7 5.33v15.33C7 21.4 7.6 22 8.33 22h7.33c.74 0 1.34-.6 1.34-1.33V5.33C17 4.6 16.4 4 15.67 4z"
                                />
                            </svg>
                        </div>
                    </div>

                    <div
                        class="relative w-full transition-colors duration-150"
                        :style="{ height: screenHeight + 'px', background: screenPalette.screenBg }"
                    >
                        <ClientOnly>
                            <iframe
                                v-if="instanceId"
                                ref="iframeRef"
                                :src="`/rn-preview/index.html?v=${hostVersion}&id=${instanceId}`"
                                class="w-full h-full border-none block transition-colors duration-150"
                                :style="{ background: screenPalette.iframeBg }"
                                title="React Native Web Preview"
                                sandbox="allow-scripts allow-same-origin"
                            />
                        </ClientOnly>

                        <div
                            v-if="isLoading"
                            class="absolute inset-0 z-30 flex flex-col items-center justify-center transition-colors duration-150"
                            :style="{
                                background: screenPalette.loadingBg,
                                color: screenPalette.loadingFg,
                            }"
                        >
                            <div
                                class="w-8 h-8 border-2 border-sky-500 border-t-transparent rounded-full animate-spin mb-2"
                            />
                            <p class="text-[12px] font-medium">Loading…</p>
                        </div>
                    </div>

                    <div v-if="device === 'iphone'" class="flex justify-center py-2 bg-black">
                        <div class="w-28 h-1 rounded-full bg-white/40" />
                    </div>
                    <div
                        v-else-if="device === 'android'"
                        class="flex justify-center items-center gap-10 py-2.5 bg-black text-white/50"
                    >
                        <div class="w-3 h-3 rounded-full border border-current" />
                        <div class="w-4 h-4 rounded-sm border border-current" />
                        <div
                            class="w-0 h-0 border-y-[6px] border-y-transparent border-r-[10px] border-r-current"
                        />
                    </div>
                </div>

                <p
                    class="mt-1.5 mb-0 shrink-0 text-[10px] font-mono opacity-40 text-center text-black dark:text-white max-w-[340px]"
                >
                    react-native-web · not a real device
                </p>
            </div>
        </div>

        <div
            v-if="lastError"
            class="border-t border-red-500/30 bg-red-50 dark:bg-red-950/40 px-4 py-2 text-[11px] font-mono text-red-700 dark:text-red-300 whitespace-pre-wrap max-h-28 overflow-auto"
        >
            {{ lastError }}
        </div>

        <div ref="slotRootRef" class="hidden">
            <slot />
        </div>
    </div>
</template>

<style scoped>
.code-panel-scroll::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
.code-panel-scroll::-webkit-scrollbar-track {
    background: transparent;
}
.code-panel-scroll::-webkit-scrollbar-thumb {
    background: #3333;
    border-radius: 4px;
}
.dark .code-panel-scroll::-webkit-scrollbar-thumb {
    background: #555;
}

.code-panel-scroll :deep(*) {
    box-sizing: border-box;
}

.code-panel-scroll :deep(pre) {
    margin: 0 !important;
    margin-bottom: 0 !important;
    border-radius: 0 !important;
    border: none !important;
    background-color: transparent !important;
    padding: 0 0.25rem !important;
    padding-bottom: 0 !important;
    font-size: 13px !important;
    line-height: 1.55 !important;
}

.code-panel-scroll :deep(.code-block),
.code-panel-scroll :deep([class*='prose-pre']),
.code-panel-scroll :deep(> div),
.code-panel-scroll :deep(> div > div) {
    margin: 0 !important;
    margin-bottom: 0 !important;
    border: none !important;
    padding-bottom: 0 !important;
}

/* Nuxt UI Pre often adds footer spacing / rounded bottom chrome */
.code-panel-scroll :deep(button) {
    display: none !important;
}

.code-panel-scroll :deep(.copy-button) {
    display: none !important;
}

.code-panel-scroll :deep(pre code) {
    display: block;
    padding-bottom: 0 !important;
    margin-bottom: 0 !important;
}
</style>
