<script setup>
import { ref, computed, useSlots, onMounted, onUnmounted, watch, nextTick, h } from 'vue'
import { useRoute } from 'nuxt/app'

const props = defineProps({
    /** Window / Project title */
    title: { type: String, default: 'React Project' },
    /** Entry file path for preview */
    entry: { type: String, default: '' },
    /** Screen height (px) */
    height: { type: [String, Number], default: 560 },
    /** Force light/dark inside preview; omit to follow site color mode */
    theme: {
        type: String,
        default: undefined,
        validator: (v) => v === undefined || ['light', 'dark'].includes(v),
    },
    /** Whether to enable Tailwind CSS v4 in preview */
    tailwind: { type: Boolean, default: true },
    /** Initially selected tab */
    defaultTab: { type: String, default: '' },
})

const slots = useSlots()
const route = useRoute()
const iframeRef = ref(null)
const splitBodyRef = ref(null)

/**
 * Layout modes:
 * - split: code & tree on left, preview on right
 * - code: code & tree full width
 * - preview: preview full width
 */
const layoutMode = ref('split')
/** Code panel share of split width (0.22 - 0.78). Default 55% code, 45% preview */
const codeRatio = ref(0.55)
const isDragging = ref(false)
const isLg = ref(false)

/** Sidebar file tree open state */
const isTreeOpen = ref(true)

/** Expanded folders set */
const expandedFolders = ref(new Set())

/** Selected active file */
const activeFilePath = ref('')

const instanceId = ref(
    typeof window !== 'undefined' ? Math.random().toString(36).slice(2, 9) : '',
)
const hostReady = ref(false)
const isLoading = ref(true)
const lastError = ref('')
const hostVersion = ref(Date.now())
const copied = ref(false)
const domTheme = ref('light')
const previewWidthMode = ref('full') // 'full' | 'tablet' | 'mobile'

let pingInterval = null
let themeObserver = null
let copyTimer = null
let lgMqlCleanup = null
let mqlCleanup = null

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

const panelHeight = computed(() => {
    const n = Number(props.height)
    return Number.isFinite(n) && n > 0 ? Math.max(n, 420) : 560
})

// ─── Extraction of code blocks from slots ─────────────────────────────────

const langFromClass = (cls) => {
    if (!cls || typeof cls !== 'string') return ''
    const m = cls.match(/language-([a-z0-9+#-]+)/i)
    return (m?.[1] || '').toLowerCase()
}

const parseFilenameFromMeta = (meta, propsObj) => {
    if (propsObj?.filename) return propsObj.filename
    if (meta) {
        const bracketMatch = meta.match(/\[(.*?)\]/)
        if (bracketMatch?.[1]) return bracketMatch[1].trim()
        const fileMatch = meta.match(/filename=["'](.*?)["']/)
        if (fileMatch?.[1]) return fileMatch[1].trim()
    }
    return ''
}

const extractFilesFromVNodes = (vnodes) => {
    const files = []
    let counter = 1

    const scan = (nodes) => {
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
                let filename = parseFilenameFromMeta(p.meta, p)
                if (!filename) {
                    const firstLineMatch = code.match(/^\/\/\s*(?:@filename:|\s*)([\w./-]+\.\w+)/m)
                    if (firstLineMatch?.[1]) {
                        filename = firstLineMatch[1].trim()
                    }
                }
                if (!filename) {
                    if (lang === 'tsx' || lang === 'jsx') {
                        filename = counter === 1 ? 'src/App.tsx' : `src/components/Component${counter}.tsx`
                    } else if (lang === 'css') {
                        filename = 'src/styles.css'
                    } else if (lang === 'json') {
                        filename = 'package.json'
                    } else {
                        filename = `src/file${counter}.${lang || 'ts'}`
                    }
                    counter++
                }

                if (vnode.props) {
                    vnode.props.hideHeader = true
                    vnode.props.copy = false
                }

                files.push({
                    filename,
                    language: lang || 'tsx',
                    code: code.trim(),
                    vnode,
                })
            } else {
                const tag = vnode.type || ''
                const children = vnode.children || ''
                const cls = p.className || p.class || ''
                if (typeof children === 'string' && (tag === 'code' || langFromClass(cls))) {
                    const filename = `src/file${counter}.tsx`
                    counter++
                    files.push({
                        filename,
                        language: lang || 'tsx',
                        code: children.trim(),
                        vnode,
                    })
                }
            }

            if (vnode.children && Array.isArray(vnode.children)) {
                scan(vnode.children)
            } else if (vnode.children && typeof vnode.children === 'object' && vnode.children.default) {
                try {
                    scan(vnode.children.default())
                } catch {
                    /* ignore */
                }
            }
        }
    }

    scan(vnodes)
    return files
}

const extractedFiles = computed(() => {
    const defaultSlot = slots.default?.() || []
    return extractFilesFromVNodes(defaultSlot)
})

const filesMap = computed(() => {
    const map = {}
    for (const f of extractedFiles.value) {
        map[f.filename] = f.code
    }
    return map
})

// Auto select initial active file
watch(
    extractedFiles,
    (files) => {
        if (!files.length) return
        if (props.defaultTab && files.some((f) => f.filename === props.defaultTab)) {
            activeFilePath.value = props.defaultTab
            return
        }
        if (props.entry && files.some((f) => f.filename === props.entry)) {
            activeFilePath.value = props.entry
            return
        }
        // Preferred default file
        const preferred = files.find(
            (f) =>
                f.filename === 'src/App.tsx' ||
                f.filename === 'App.tsx' ||
                f.filename.endsWith('App.tsx') ||
                f.filename.endsWith('App.jsx'),
        )
        activeFilePath.value = preferred ? preferred.filename : files[0].filename
    },
    { immediate: true },
)

const activeFileObj = computed(() => {
    return (
        extractedFiles.value.find((f) => f.filename === activeFilePath.value) ||
        extractedFiles.value[0] ||
        null
    )
})

// ─── File Tree Construction ───────────────────────────────────────────────

const fileTree = computed(() => {
    const root = []

    for (const file of extractedFiles.value) {
        const parts = file.filename.split('/').filter(Boolean)
        let currentLevel = root
        let currentPath = ''

        for (let i = 0; i < parts.length; i++) {
            const part = parts[i]
            const isFile = i === parts.length - 1
            currentPath = currentPath ? `${currentPath}/${part}` : part

            let existing = currentLevel.find((node) => node.name === part)

            if (!existing) {
                existing = {
                    name: part,
                    path: currentPath,
                    isDir: !isFile,
                    language: isFile ? file.language : undefined,
                    children: isFile ? undefined : [],
                }
                currentLevel.push(existing)
                if (!isFile) {
                    expandedFolders.value.add(currentPath)
                }
            }
            if (!isFile) {
                currentLevel = existing.children
            }
        }
    }

    // Sort: directories first, then alphabetical
    const sortNodes = (nodes) => {
        nodes.sort((a, b) => {
            if (a.isDir && !b.isDir) return -1
            if (!a.isDir && b.isDir) return 1
            if (a.name === 'App.tsx' || a.name === 'src') return -1
            if (b.name === 'App.tsx' || b.name === 'src') return 1
            return a.name.localeCompare(b.name)
        })
        for (const n of nodes) {
            if (n.children) sortNodes(n.children)
        }
    }

    sortNodes(root)
    return root
})

const toggleFolder = (folderPath) => {
    if (expandedFolders.value.has(folderPath)) {
        expandedFolders.value.delete(folderPath)
    } else {
        expandedFolders.value.add(folderPath)
    }
}

const selectFile = (filePath) => {
    activeFilePath.value = filePath
}

// ─── Iframe Communication ─────────────────────────────────────────────────

const postToHost = (payload) => {
    const win = iframeRef.value?.contentWindow
    if (!win) return
    win.postMessage({ ...payload, id: instanceId.value }, '*')
}

const sendProject = () => {
    if (!hostReady.value) return
    if (!Object.keys(filesMap.value).length) return

    postToHost({
        type: 'run-project',
        files: filesMap.value,
        entry: props.entry || activeFilePath.value,
        theme: resolvedTheme.value,
        tailwind: props.tailwind,
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
        case 'react-preview-ready':
        case 'react-preview-pong':
            hostReady.value = true
            nextTick(() => sendProject())
            break
        case 'react-preview-success':
            lastError.value = ''
            isLoading.value = false
            break
        case 'react-preview-error':
            lastError.value = data.message || 'Помилка виконання React'
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
    const code = activeFileObj.value?.code
    if (!code || !navigator.clipboard) return
    try {
        await navigator.clipboard.writeText(code)
        copied.value = true
        if (copyTimer) clearTimeout(copyTimer)
        copyTimer = setTimeout(() => {
            copied.value = false
        }, 1600)
    } catch {
        /* ignore */
    }
}

// ─── Tabs & Quick Picker logic for handling many tabs ─────────────────────

const tabsContainerRef = ref(null)
const quickPickerRef = ref(null)
const isQuickPickerOpen = ref(false)
const quickPickerSearch = ref('')

const onTabsWheel = (e) => {
    if (!tabsContainerRef.value) return
    if (e.deltaY) {
        tabsContainerRef.value.scrollLeft += e.deltaY
    }
}

const scrollActiveTabIntoView = () => {
    nextTick(() => {
        const el = tabsContainerRef.value?.querySelector('[data-active="true"]')
        el?.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' })
    })
}

const toggleQuickPicker = () => {
    isQuickPickerOpen.value = !isQuickPickerOpen.value
    if (isQuickPickerOpen.value) {
        quickPickerSearch.value = ''
    }
}

const filteredFiles = computed(() => {
    const q = quickPickerSearch.value.trim().toLowerCase()
    if (!q) return extractedFiles.value
    return extractedFiles.value.filter((f) => f.filename.toLowerCase().includes(q))
})

const selectFileFromPicker = (path) => {
    selectFile(path)
    isQuickPickerOpen.value = false
}

const onGlobalClick = (e) => {
    if (isQuickPickerOpen.value && quickPickerRef.value && !quickPickerRef.value.contains(e.target)) {
        isQuickPickerOpen.value = false
    }
}

// ─── Resizer logic ────────────────────────────────────────────────────────

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
        if (rect.width < 100) return
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

// ─── Lifecycle hooks ──────────────────────────────────────────────────────

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

    pingInterval = setInterval(() => {
        if (!hostReady.value && iframeRef.value?.contentWindow) {
            postToHost({ type: 'ping' })
        }
        if (hostReady.value && Object.keys(filesMap.value).length && isLoading.value) {
            sendProject()
        }
    }, 400)

    setTimeout(() => {
        if (isLoading.value) {
            isLoading.value = false
            if (!hostReady.value) {
                lastError.value = 'Хост превʼю не відповідає. Перевірте файл /react-preview/index.html'
            }
        }
    }, 12000)

    window.addEventListener('click', onGlobalClick)
})

onUnmounted(() => {
    window.removeEventListener('message', handleMessage)
    window.removeEventListener('click', onGlobalClick)
    if (pingInterval) clearInterval(pingInterval)
    if (themeObserver) themeObserver.disconnect()
    if (mqlCleanup) mqlCleanup()
    if (lgMqlCleanup) lgMqlCleanup()
    if (copyTimer) clearTimeout(copyTimer)
})

watch(activeFilePath, () => {
    scrollActiveTabIntoView()
})

watch(filesMap, () => {
    if (hostReady.value) sendProject()
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

const CodeVNodeRenderer = {
    props: ['vnode'],
    render() {
        return this.vnode
    },
}

const FileIcon = {
    props: {
        filename: { type: String, required: true },
    },
    setup(props) {
        return () => {
            const name = (props.filename || '').toLowerCase()
            // React files (.tsx, .jsx)
            if (name.endsWith('.tsx') || name.endsWith('.jsx')) {
                return h(
                    'svg',
                    {
                        class: 'w-3.5 h-3.5 text-[#0284c7] dark:text-[#38bdf8] shrink-0',
                        viewBox: '-11.5 -10.23174 23 20.46348',
                        fill: 'none',
                        'aria-hidden': 'true',
                    },
                    [
                        h('circle', { cx: '0', cy: '0', r: '2.05', fill: 'currentColor' }),
                        h('g', { stroke: 'currentColor', 'stroke-width': '1' }, [
                            h('ellipse', { rx: '11', ry: '4.2' }),
                            h('ellipse', { rx: '11', ry: '4.2', transform: 'rotate(60)' }),
                            h('ellipse', { rx: '11', ry: '4.2', transform: 'rotate(120)' }),
                        ]),
                    ],
                )
            }
            // CSS / SCSS files
            if (name.endsWith('.css') || name.endsWith('.scss')) {
                return h(
                    'svg',
                    {
                        class: 'w-3.5 h-3.5 text-sky-600 dark:text-sky-400 shrink-0',
                        viewBox: '0 0 24 24',
                        fill: 'none',
                        stroke: 'currentColor',
                        'stroke-width': '2.2',
                        'stroke-linecap': 'round',
                        'stroke-linejoin': 'round',
                        'aria-hidden': 'true',
                    },
                    [
                        h('line', { x1: '4', y1: '9', x2: '20', y2: '9' }),
                        h('line', { x1: '4', y1: '15', x2: '20', y2: '15' }),
                        h('line', { x1: '10', y1: '3', x2: '8', y2: '21' }),
                        h('line', { x1: '16', y1: '3', x2: '14', y2: '21' }),
                    ],
                )
            }
            // JSON files
            if (name.endsWith('.json')) {
                return h(
                    'svg',
                    {
                        class: 'w-3.5 h-3.5 text-amber-600 dark:text-amber-400 shrink-0',
                        viewBox: '0 0 24 24',
                        fill: 'none',
                        stroke: 'currentColor',
                        'stroke-width': '2',
                        'stroke-linecap': 'round',
                        'stroke-linejoin': 'round',
                        'aria-hidden': 'true',
                    },
                    [
                        h('path', { d: 'M7 4a2 2 0 0 0-2 2v3a2 2 0 0 1-2 2 2 2 0 0 1 2 2v3a2 2 0 0 0 2 2' }),
                        h('path', { d: 'M17 4a2 2 0 0 1 2 2v3a2 2 0 0 0 2 2 2 2 0 0 0-2 2v3a2 2 0 0 1-2 2' }),
                    ],
                )
            }
            // TypeScript files (.ts)
            if (name.endsWith('.ts')) {
                return h(
                    'span',
                    {
                        class: 'w-3.5 h-3.5 rounded-[2px] bg-[#3178c6] text-white flex items-center justify-center font-bold text-[8px] shrink-0 leading-none select-none shadow-sm',
                        'aria-hidden': 'true',
                    },
                    'TS',
                )
            }
            // JavaScript files (.js, .mjs)
            if (name.endsWith('.js') || name.endsWith('.mjs')) {
                return h(
                    'span',
                    {
                        class: 'w-3.5 h-3.5 rounded-[2px] bg-[#f7df1e] text-black flex items-center justify-center font-bold text-[8px] shrink-0 leading-none select-none shadow-sm',
                        'aria-hidden': 'true',
                    },
                    'JS',
                )
            }
            // Generic file fallback
            return h(
                'svg',
                {
                    class: 'w-3.5 h-3.5 text-gray-600 dark:text-gray-300 shrink-0',
                    viewBox: '0 0 24 24',
                    fill: 'none',
                    stroke: 'currentColor',
                    'stroke-width': '2',
                    'stroke-linecap': 'round',
                    'stroke-linejoin': 'round',
                    'aria-hidden': 'true',
                },
                [
                    h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
                    h('polyline', { points: '14 2 14 8 20 8' }),
                ],
            )
        }
    },
}
</script>

<template>
    <div
        class="my-8 rounded-xl shadow-2xl overflow-hidden bg-white dark:bg-[#1e1e1e] border border-gray-200 dark:border-white/10 flex flex-col not-prose font-sans text-[13px] transition-all"
        :class="isDragging && 'select-none'"
    >
        <!-- Top macOS Chrome Window Header -->
        <div
            class="bg-[#f3f4f6] dark:bg-[#252526] border-b border-gray-300 dark:border-black/50 select-none shrink-0"
        >
            <div class="flex items-center justify-between gap-2 px-3 sm:px-4 h-11 min-w-0">
                <!-- Left: macOS Buttons & Project Title -->
                <div class="flex items-center gap-3 min-w-0">
                    <div class="flex items-center gap-1.5 shrink-0">
                        <div class="w-3 h-3 rounded-full bg-[#ff5f56] border-[0.5px] border-black/10"></div>
                        <div class="w-3 h-3 rounded-full bg-[#ffbd2e] border-[0.5px] border-black/10"></div>
                        <div class="w-3 h-3 rounded-full bg-[#27c93f] border-[0.5px] border-black/10"></div>
                    </div>

                    <div class="flex items-center gap-2 min-w-0">
                        <span class="flex items-center gap-1.5 text-[#0284c7] dark:text-[#38bdf8] font-bold text-[11px] tracking-wide uppercase shrink-0">
                            <svg class="w-4 h-4 shrink-0" viewBox="-11.5 -10.23174 23 20.46348" fill="none" aria-hidden="true">
                                <circle cx="0" cy="0" r="2.05" fill="currentColor"/>
                                <g stroke="currentColor" stroke-width="1">
                                    <ellipse rx="11" ry="4.2"/>
                                    <ellipse rx="11" ry="4.2" transform="rotate(60)"/>
                                    <ellipse rx="11" ry="4.2" transform="rotate(120)"/>
                                </g>
                            </svg>
                            React
                        </span>
                        <span class="truncate text-[12px] font-semibold text-gray-800 dark:text-gray-200">
                            {{ title }}
                        </span>
                        <span class="hidden md:inline text-[10px] font-mono px-1.5 py-0.5 rounded bg-black/5 dark:bg-white/5 text-gray-500 dark:text-gray-400">
                            {{ extractedFiles.length }} {{ extractedFiles.length === 1 ? 'файл' : 'файлів' }}
                        </span>
                    </div>
                </div>

                <!-- Right: Controls -->
                <div class="flex items-center gap-1.5 shrink-0">
                    <!-- Layout Mode Switcher -->
                    <div
                        class="flex items-center rounded-lg p-0.5 bg-black/5 dark:bg-white/5 border border-black/5 dark:border-white/10"
                        role="group"
                        aria-label="Режим відображення"
                    >
                        <button
                            type="button"
                            title="Split: Код + Превʼю"
                            :class="[
                                'flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-colors',
                                layoutMode === 'split'
                                    ? 'bg-white dark:bg-[#37373d] text-sky-600 dark:text-sky-400 shadow-sm'
                                    : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white',
                            ]"
                            @click="layoutMode = 'split'"
                        >
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="3" width="18" height="18" rx="2" />
                                <line x1="12" y1="3" x2="12" y2="21" />
                            </svg>
                            <span class="hidden sm:inline">Split</span>
                        </button>
                        <button
                            type="button"
                            title="Лише код"
                            :class="[
                                'flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-colors',
                                layoutMode === 'code'
                                    ? 'bg-white dark:bg-[#37373d] text-sky-600 dark:text-sky-400 shadow-sm'
                                    : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white',
                            ]"
                            @click="layoutMode = 'code'"
                        >
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="16 18 22 12 16 6" />
                                <polyline points="8 6 2 12 8 18" />
                            </svg>
                            <span class="hidden sm:inline">Code</span>
                        </button>
                        <button
                            type="button"
                            title="Лише результат"
                            :class="[
                                'flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-colors',
                                layoutMode === 'preview'
                                    ? 'bg-white dark:bg-[#37373d] text-sky-600 dark:text-sky-400 shadow-sm'
                                    : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white',
                            ]"
                            @click="layoutMode = 'preview'"
                        >
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10" />
                                <polygon points="10 8 16 12 10 16 10 8" />
                            </svg>
                            <span class="hidden sm:inline">Preview</span>
                        </button>
                    </div>

                    <!-- Reload Preview -->
                    <button
                        type="button"
                        title="Перезавантажити проєкт"
                        class="p-1.5 rounded-md hover:bg-black/10 dark:hover:bg-white/10 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                        @click="reloadHost"
                    >
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                            <path d="M3 3v5h5" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Main Body -->
        <div
            ref="splitBodyRef"
            class="flex flex-col lg:flex-row bg-[#f8fafc] dark:bg-[#18181b] min-h-0"
            :class="isDragging && 'cursor-col-resize'"
            :style="{ height: panelHeight + 'px', minHeight: panelHeight + 'px' }"
        >
            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- LEFT PANEL: File Tree + Tabs + Code Editor                -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <div
                v-show="layoutMode === 'split' || layoutMode === 'code'"
                class="flex flex-row min-w-0 min-h-0 h-full bg-white dark:bg-[#1e1e1e] border-b lg:border-b-0 border-gray-200 dark:border-white/10 overflow-hidden"
                :style="
                    layoutMode === 'code'
                        ? { flex: '1 1 100%', width: '100%' }
                        : isLg
                          ? {
                                flex: `0 0 ${(codeRatio * 100).toFixed(2)}%`,
                                width: `${(codeRatio * 100).toFixed(2)}%`,
                                minWidth: '240px',
                                maxWidth: '80%',
                            }
                          : { width: '100%', flex: '0 0 auto', height: '50%' }
                "
            >
                <!-- File Tree Sidebar -->
                <div
                    v-show="isTreeOpen"
                    class="w-48 sm:w-52 shrink-0 border-r border-gray-200 dark:border-[#2b2b2b] bg-[#f9fafb] dark:bg-[#181818] flex flex-col select-none text-[12px]"
                >
                    <!-- Sidebar Header -->
                    <div
                        class="h-9 px-3 flex items-center justify-between border-b border-gray-200 dark:border-[#2b2b2b] text-[11px] font-semibold text-gray-600 dark:text-gray-400 tracking-wider uppercase"
                    >
                        <span>Файли проєкту</span>
                        <button
                            type="button"
                            title="Згорнути дерево"
                            class="p-1 rounded hover:bg-black/5 dark:hover:bg-white/5 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                            @click="isTreeOpen = false"
                        >
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="15 18 9 12 15 6"></polyline>
                            </svg>
                        </button>
                    </div>

                    <!-- Tree Nodes Recursive View -->
                    <div class="flex-1 overflow-y-auto py-1 px-1 space-y-0.5 custom-scrollbar">
                        <template v-for="node in fileTree" :key="node.path">
                            <!-- Directory Node -->
                            <div v-if="node.isDir" class="space-y-0.5">
                                <div
                                    class="flex items-center gap-1.5 px-2 py-1 rounded cursor-pointer text-gray-800 dark:text-gray-200 hover:bg-black/5 dark:hover:bg-white/5 transition-colors font-medium text-[11.5px]"
                                    @click="toggleFolder(node.path)"
                                >
                                    <svg
                                        class="w-3 h-3 text-gray-600 dark:text-gray-300 transition-transform duration-150 shrink-0"
                                        :class="expandedFolders.has(node.path) ? 'rotate-90' : ''"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="2.5"
                                        aria-hidden="true"
                                    >
                                        <polyline points="9 18 15 12 9 6"></polyline>
                                    </svg>
                                    <svg
                                        class="w-4 h-4 text-amber-500 dark:text-amber-400 shrink-0"
                                        viewBox="0 0 24 24"
                                        fill="currentColor"
                                        aria-hidden="true"
                                    >
                                        <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z" />
                                    </svg>
                                    <span class="truncate">{{ node.name }}</span>
                                </div>

                                <!-- Children Nodes -->
                                <div v-show="expandedFolders.has(node.path)" class="pl-4 space-y-0.5">
                                    <template v-for="child in node.children" :key="child.path">
                                        <!-- Subdirectory -->
                                        <div v-if="child.isDir" class="space-y-0.5">
                                            <div
                                                class="flex items-center gap-1.5 px-2 py-1 rounded cursor-pointer text-gray-800 dark:text-gray-200 hover:bg-black/5 dark:hover:bg-white/5 transition-colors font-medium text-[11.5px]"
                                                @click="toggleFolder(child.path)"
                                            >
                                                <svg
                                                    class="w-3 h-3 text-gray-600 dark:text-gray-300 transition-transform duration-150 shrink-0"
                                                    :class="expandedFolders.has(child.path) ? 'rotate-90' : ''"
                                                    viewBox="0 0 24 24"
                                                    fill="none"
                                                    stroke="currentColor"
                                                    stroke-width="2.5"
                                                    aria-hidden="true"
                                                >
                                                    <polyline points="9 18 15 12 9 6"></polyline>
                                                </svg>
                                                <svg
                                                    class="w-3.5 h-3.5 text-amber-500 dark:text-amber-400 shrink-0"
                                                    viewBox="0 0 24 24"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z" />
                                                </svg>
                                                <span class="truncate">{{ child.name }}</span>
                                            </div>
                                            <!-- Sub-children -->
                                            <div v-show="expandedFolders.has(child.path)" class="pl-4 space-y-0.5">
                                                <div
                                                    v-for="subChild in child.children"
                                                    :key="subChild.path"
                                                    class="flex items-center gap-2 px-2 py-1 rounded cursor-pointer transition-colors text-[11.5px]"
                                                    :class="[
                                                        activeFilePath === subChild.path
                                                            ? 'bg-sky-500/10 text-sky-600 dark:text-sky-400 font-semibold'
                                                            : 'text-gray-700 dark:text-gray-300 hover:bg-black/5 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white',
                                                    ]"
                                                    @click="selectFile(subChild.path)"
                                                >
                                                    <FileIcon :filename="subChild.name" />
                                                    <span class="truncate">{{ subChild.name }}</span>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Regular File in Directory -->
                                        <div
                                            v-else
                                            class="flex items-center gap-2 px-2 py-1 rounded cursor-pointer transition-colors text-[11.5px]"
                                            :class="[
                                                activeFilePath === child.path
                                                    ? 'bg-sky-500/10 text-sky-600 dark:text-sky-400 font-semibold'
                                                    : 'text-gray-700 dark:text-gray-300 hover:bg-black/5 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white',
                                            ]"
                                            @click="selectFile(child.path)"
                                        >
                                            <FileIcon :filename="child.name" />
                                            <span class="truncate">{{ child.name }}</span>
                                        </div>
                                    </template>
                                </div>
                            </div>

                            <!-- Root File Node -->
                            <div
                                v-else
                                class="flex items-center gap-2 px-2 py-1 rounded cursor-pointer transition-colors text-[11.5px]"
                                :class="[
                                    activeFilePath === node.path
                                        ? 'bg-sky-500/10 text-sky-600 dark:text-sky-400 font-semibold'
                                        : 'text-gray-700 dark:text-gray-300 hover:bg-black/5 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white',
                                ]"
                                @click="selectFile(node.path)"
                            >
                                <FileIcon :filename="node.name" />
                                <span class="truncate">{{ node.name }}</span>
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Code Editor Area (Tabs + Code) -->
                <div class="flex-1 flex flex-col min-w-0 min-h-0 bg-white dark:bg-[#1e1e1e]">
                    <!-- Tabs Bar -->
                    <div
                        class="h-9 flex items-center justify-between bg-[#f1f3f5] dark:bg-[#1e1e1e] border-b border-gray-200 dark:border-[#2b2b2b] px-1 select-none shrink-0 gap-1"
                    >
                        <!-- File Tabs Scrollable Area (supports mouse wheel horizontal scroll) -->
                        <div
                            ref="tabsContainerRef"
                            class="flex items-center gap-1 overflow-x-auto custom-scrollbar min-w-0 flex-1 h-full py-0.5"
                            @wheel.passive="onTabsWheel"
                        >
                            <!-- Show File Tree Toggle (if collapsed) -->
                            <button
                                v-if="!isTreeOpen"
                                type="button"
                                title="Показати дерево файлів"
                                class="p-1.5 rounded hover:bg-black/5 dark:hover:bg-white/5 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors shrink-0"
                                @click="isTreeOpen = true"
                            >
                                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z" />
                                </svg>
                            </button>

                            <!-- File Tabs -->
                            <button
                                v-for="file in extractedFiles"
                                :key="file.filename"
                                type="button"
                                :data-active="activeFilePath === file.filename ? 'true' : 'false'"
                                :title="file.filename"
                                :class="[
                                    'group flex items-center gap-1.5 px-3 py-1.5 rounded-t text-[11.5px] font-medium transition-all shrink-0 border-b-2',
                                    activeFilePath === file.filename
                                        ? 'bg-white dark:bg-[#1e1e1e] text-sky-600 dark:text-sky-400 border-sky-500 shadow-sm'
                                        : 'bg-transparent text-gray-700 dark:text-gray-300 border-transparent hover:bg-black/5 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white',
                                ]"
                                @click="selectFile(file.filename)"
                            >
                                <FileIcon :filename="file.filename" />
                                <span class="truncate max-w-[140px]">{{ file.filename.split('/').pop() }}</span>
                            </button>
                        </div>

                        <!-- Right Actions: Quick File Picker (for many tabs) + Copy Button -->
                        <div class="flex items-center shrink-0 pr-1 pl-1 gap-1 border-l border-gray-200 dark:border-[#2b2b2b]">
                            <!-- Quick File Picker Dropdown -->
                            <div ref="quickPickerRef" class="relative flex items-center">
                                <button
                                    type="button"
                                    title="Швидкий вибір файлу проєкту"
                                    class="flex items-center gap-1 px-1.5 py-1 rounded text-[11px] font-medium transition-colors border"
                                    :class="[
                                        isQuickPickerOpen
                                            ? 'bg-sky-500/10 text-sky-600 dark:text-sky-400 border-sky-500/30'
                                            : 'text-gray-700 dark:text-gray-300 border-transparent hover:bg-black/5 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white',
                                    ]"
                                    @click.stop="toggleQuickPicker"
                                >
                                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <line x1="8" y1="6" x2="21" y2="6"></line>
                                        <line x1="8" y1="12" x2="21" y2="12"></line>
                                        <line x1="8" y1="18" x2="21" y2="18"></line>
                                        <line x1="3" y1="6" x2="3.01" y2="6"></line>
                                        <line x1="3" y1="12" x2="3.01" y2="12"></line>
                                        <line x1="3" y1="18" x2="3.01" y2="18"></line>
                                    </svg>
                                    <span class="text-[10px] font-mono opacity-80">{{ extractedFiles.length }}</span>
                                    <svg
                                        class="w-3 h-3 transition-transform"
                                        :class="isQuickPickerOpen ? 'rotate-180' : ''"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="2"
                                    >
                                        <polyline points="6 9 12 15 18 9"></polyline>
                                    </svg>
                                </button>

                                <!-- Dropdown Menu -->
                                <div
                                    v-if="isQuickPickerOpen"
                                    class="absolute right-0 top-full mt-1.5 w-64 max-h-72 overflow-hidden bg-white dark:bg-[#252526] border border-gray-200 dark:border-white/10 rounded-lg shadow-2xl z-50 flex flex-col text-[12px]"
                                    @click.stop
                                >
                                    <div v-if="extractedFiles.length > 4" class="p-1.5 border-b border-gray-200 dark:border-white/10">
                                        <input
                                            v-model="quickPickerSearch"
                                            type="text"
                                            placeholder="Пошук файлу..."
                                            class="w-full px-2 py-1 text-[11.5px] rounded bg-gray-100 dark:bg-[#1e1e1e] text-gray-800 dark:text-gray-200 border border-transparent focus:border-sky-500 focus:outline-none"
                                            autofocus
                                        />
                                    </div>
                                    <div class="overflow-y-auto max-h-56 p-1 space-y-0.5 custom-scrollbar">
                                        <button
                                            v-for="file in filteredFiles"
                                            :key="file.filename"
                                            type="button"
                                            class="w-full flex items-center justify-between gap-2 px-2 py-1.5 rounded text-left transition-colors text-[11.5px]"
                                            :class="[
                                                activeFilePath === file.filename
                                                    ? 'bg-sky-500/10 text-sky-600 dark:text-sky-400 font-semibold'
                                                    : 'text-gray-700 dark:text-gray-300 hover:bg-black/5 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white',
                                            ]"
                                            @click="selectFileFromPicker(file.filename)"
                                        >
                                            <div class="flex items-center gap-2 truncate min-w-0">
                                                <FileIcon :filename="file.filename" />
                                                <span class="truncate">{{ file.filename }}</span>
                                            </div>
                                            <svg
                                                v-if="activeFilePath === file.filename"
                                                class="w-3.5 h-3.5 text-sky-500 shrink-0"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="2.5"
                                            >
                                                <polyline points="20 6 9 17 4 12" />
                                            </svg>
                                        </button>
                                        <div
                                            v-if="!filteredFiles.length"
                                            class="px-3 py-2 text-center text-[11px] text-gray-500 dark:text-gray-400"
                                        >
                                            Файлів не знайдено
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Sticky Copy Code Button -->
                            <button
                                type="button"
                                :title="copied ? 'Скопійовано!' : 'Копіювати вміст файлу'"
                                class="flex items-center gap-1.5 px-2 py-1 rounded text-[11px] font-medium transition-all"
                                :class="[
                                    copied
                                        ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-semibold'
                                        : 'text-gray-700 dark:text-gray-300 hover:bg-black/5 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white',
                                ]"
                                @click="copyCode"
                            >
                                <svg v-if="copied" class="w-3.5 h-3.5 text-emerald-500 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                                    <polyline points="20 6 9 17 4 12" />
                                </svg>
                                <svg v-else class="w-3.5 h-3.5 shrink-0 text-gray-700 dark:text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                                </svg>
                                <span class="hidden sm:inline">{{ copied ? 'Скопійовано' : 'Копіювати' }}</span>
                            </button>
                        </div>
                    </div>

                    <!-- Code Files Container (v-show keeps all code blocks mounted stably) -->
                    <div class="code-editor-body flex-1 overflow-auto p-4 custom-scrollbar bg-white dark:bg-[#1e1e1e]">
                        <ClientOnly>
                            <div
                                v-for="file in extractedFiles"
                                :key="file.filename"
                                v-show="activeFilePath === file.filename"
                                class="code-file-pane h-full"
                            >
                                <CodeVNodeRenderer
                                    v-if="file.vnode"
                                    :vnode="file.vnode"
                                />
                                <pre
                                    v-else-if="file.code"
                                    class="m-0 p-0 text-[12.5px] font-mono leading-relaxed text-gray-800 dark:text-gray-200 whitespace-pre-wrap break-words"
                                >{{ file.code }}</pre>
                            </div>
                        </ClientOnly>
                    </div>
                </div>
            </div>

            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- SPLIT RESIZER BAR                                          -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <div
                v-if="layoutMode === 'split' && isLg"
                class="flex group relative w-2.5 shrink-0 cursor-col-resize items-stretch justify-center z-10 bg-transparent hover:bg-sky-500/15 active:bg-sky-500/25 transition-colors select-none"
                role="separator"
                aria-orientation="vertical"
                aria-label="Змінити розмір панелей"
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

            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- RIGHT PANEL: Live React Rendered Preview                   -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <div
                v-show="layoutMode === 'split' || layoutMode === 'preview'"
                class="flex-1 flex flex-col min-w-0 min-h-0 h-full bg-[#f8fafc] dark:bg-[#121316] overflow-hidden"
            >
                <!-- Browser-like URL / Status Bar -->
                <div
                    class="h-9 px-3 flex items-center justify-between border-b border-gray-200 dark:border-white/5 bg-[#f1f5f9] dark:bg-[#1c1d22] shrink-0 select-none text-[11px]"
                >
                    <div class="flex items-center gap-2 min-w-0">
                        <!-- Status indicator dot -->
                        <span
                            class="w-2 h-2 rounded-full shrink-0"
                            :class="[
                                lastError
                                    ? 'bg-red-500 animate-pulse'
                                    : isLoading
                                      ? 'bg-amber-400 animate-spin'
                                      : 'bg-emerald-500',
                            ]"
                        ></span>
                        <span class="font-mono text-gray-500 dark:text-gray-400 truncate">
                            localhost:3000
                        </span>
                    </div>

                    <!-- Viewport size toggle buttons -->
                    <div class="flex items-center gap-1 bg-black/5 dark:bg-white/5 p-0.5 rounded border border-black/5 dark:border-white/5">
                        <button
                            type="button"
                            title="Full width"
                            :class="[
                                'p-1 rounded transition-colors',
                                previewWidthMode === 'full'
                                    ? 'bg-white dark:bg-[#37373d] text-sky-600 dark:text-sky-400 shadow-sm'
                                    : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white',
                            ]"
                            @click="previewWidthMode = 'full'"
                        >
                            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                                <line x1="8" y1="21" x2="16" y2="21"></line>
                                <line x1="12" y1="17" x2="12" y2="21"></line>
                            </svg>
                        </button>
                        <button
                            type="button"
                            title="Планшет (768px)"
                            :class="[
                                'p-1 rounded transition-colors',
                                previewWidthMode === 'tablet'
                                    ? 'bg-white dark:bg-[#37373d] text-sky-600 dark:text-sky-400 shadow-sm'
                                    : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white',
                            ]"
                            @click="previewWidthMode = 'tablet'"
                        >
                            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect>
                                <line x1="12" y1="18" x2="12.01" y2="18"></line>
                            </svg>
                        </button>
                        <button
                            type="button"
                            title="Мобільний (375px)"
                            :class="[
                                'p-1 rounded transition-colors',
                                previewWidthMode === 'mobile'
                                    ? 'bg-white dark:bg-[#37373d] text-sky-600 dark:text-sky-400 shadow-sm'
                                    : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white',
                            ]"
                            @click="previewWidthMode = 'mobile'"
                        >
                            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect>
                                <line x1="12" y1="18" x2="12.01" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                </div>

                <!-- Preview Viewport Area -->
                <div class="flex-1 relative flex items-center justify-center bg-[#f8fafc] dark:bg-[#121316] overflow-auto p-2">
                    <div
                        class="h-full transition-all duration-300 relative shadow-sm rounded-lg overflow-hidden bg-white dark:bg-[#18181b] border border-gray-200 dark:border-white/10"
                        :style="{
                            width:
                                previewWidthMode === 'mobile'
                                    ? '375px'
                                    : previewWidthMode === 'tablet'
                                      ? '768px'
                                      : '100%',
                            maxWidth: '100%',
                        }"
                    >
                        <ClientOnly>
                            <iframe
                                v-if="instanceId"
                                ref="iframeRef"
                                :src="`/react-preview/index.html?v=${hostVersion}&id=${instanceId}`"
                                class="w-full h-full border-none block"
                                title="React Live Preview"
                                sandbox="allow-scripts allow-same-origin"
                            />
                        </ClientOnly>

                        <!-- Loading Overlay -->
                        <div
                            v-if="isLoading"
                            class="absolute inset-0 z-20 flex flex-col items-center justify-center bg-white/80 dark:bg-[#18181b]/80 backdrop-blur-sm transition-opacity"
                        >
                            <div class="w-7 h-7 border-2 border-sky-500 border-t-transparent rounded-full animate-spin mb-2" />
                            <p class="text-[12px] font-medium text-gray-600 dark:text-gray-300">
                                Збирання React застосунку…
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
/* Scrollbar styling */
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: rgba(150, 150, 150, 0.25);
    border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: rgba(150, 150, 150, 0.45);
}

/* ─── Hide internal code headers & copy buttons (from Nuxt UI / Docus Pre) ─── */
.code-editor-body :deep([class*="border-b-0"]),
.code-editor-body :deep([class*="rounded-t-md"]),
.code-editor-body :deep(div:has(> span[class*="filename"])),
.code-editor-body :deep([class*="filename"]),
.code-editor-body :deep(header),
.code-editor-body :deep(button[class*="absolute"]),
.code-editor-body :deep(button:has(svg)),
.code-editor-body :deep(.copy-button) {
    display: none !important;
}

/* Ensure pre has no duplicate margins or borders */
.code-editor-body :deep([class*="my-5"]),
.code-editor-body :deep([class*="group"]) {
    margin: 0 !important;
}

.code-editor-body :deep(pre) {
    margin: 0 !important;
    border-radius: 0 !important;
    border: none !important;
    background-color: transparent !important;
    padding: 0 !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}

.code-editor-body :deep(.code-block) {
    margin: 0 !important;
    border: none !important;
}
</style>
