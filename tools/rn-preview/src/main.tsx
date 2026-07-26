import React from 'react'
import { createRoot, type Root } from 'react-dom/client'
import * as ReactDOM from 'react-dom'
import * as ReactJSXRuntime from 'react/jsx-runtime'
import * as ReactJSXDevRuntime from 'react/jsx-dev-runtime'
import * as ReactNative from 'react-native'
import Babel from '@babel/standalone'

type ColorScheme = 'light' | 'dark'

type PreviewMessage =
  | { type: 'ping'; id?: string }
  | { type: 'run-code'; id?: string; code: string; theme?: ColorScheme }
  | { type: 'set-theme'; id?: string; theme: ColorScheme }

type HostToParent =
  | { type: 'rn-preview-ready'; id?: string }
  | { type: 'rn-preview-pong'; id?: string }
  | { type: 'rn-preview-success'; id?: string }
  | { type: 'rn-preview-error'; id?: string; message: string }
  | { type: 'rn-preview-log'; id?: string; level: 'log' | 'warn' | 'error'; message: string }

const THEME_COLORS = {
  light: {
    bg: '#f2f2f7',
    fg: '#1c1c1e',
    muted: '#8e8e93',
  },
  dark: {
    bg: '#000000',
    fg: '#f5f5f7',
    muted: '#8e8e93',
  },
} as const

const rootEl = document.getElementById('root')!
const errorEl = document.getElementById('error-overlay')!
let reactRoot: Root | null = null
let lastInstanceId: string | undefined
let currentTheme: ColorScheme = 'light'

// Bridge so we never remount HostRoot on theme change (preserves counters / inputs)
const hostBridge: {
  Component: React.ComponentType | null
  setComponent: ((updater: React.ComponentType | null) => void) | null
} = {
  Component: null,
  setComponent: null,
}

// ─── Forced Appearance (site theme, not OS prefers-color-scheme) ───────────

type AppearanceListener = (prefs: { colorScheme: ColorScheme }) => void
const appearanceListeners = new Set<AppearanceListener>()

function notifyAppearance(scheme: ColorScheme) {
  for (const listener of appearanceListeners) {
    try {
      listener({ colorScheme: scheme })
    } catch {
      /* ignore */
    }
  }
}

const ForcedAppearance = {
  getColorScheme(): ColorScheme {
    return currentTheme
  },
  setColorScheme(scheme: ColorScheme | null | undefined) {
    if (scheme === 'light' || scheme === 'dark') {
      applyTheme(scheme)
    }
  },
  addChangeListener(listener: AppearanceListener) {
    appearanceListeners.add(listener)
    return {
      remove() {
        appearanceListeners.delete(listener)
      },
    }
  },
  addListener(listener: AppearanceListener) {
    return ForcedAppearance.addChangeListener(listener)
  },
  removeChangeListener(listener: AppearanceListener) {
    appearanceListeners.delete(listener)
  },
  removeListener(listener: AppearanceListener) {
    appearanceListeners.delete(listener)
  },
}

/** Drop-in for react-native's useColorScheme — follows site theme. */
function useForcedColorScheme(): ColorScheme {
  const [scheme, setScheme] = React.useState<ColorScheme>(currentTheme)
  React.useEffect(() => {
    setScheme(currentTheme)
    const sub = ForcedAppearance.addChangeListener(({ colorScheme }) => {
      setScheme(colorScheme)
    })
    return () => sub.remove()
  }, [])
  return scheme
}

// Themed Text: RN-web defaults color to "black" which is unreadable on dark bg
const BaseText = ReactNative.Text
const ThemedText = React.forwardRef<any, any>((props, ref) => {
  const scheme = useForcedColorScheme()
  const flat = ReactNative.StyleSheet.flatten(props.style) || {}
  const style =
    flat.color != null
      ? props.style
      : [{ color: THEME_COLORS[scheme].fg }, props.style]
  return React.createElement(BaseText, { ...props, style, ref })
})
ThemedText.displayName = 'Text'

/**
 * Plain module object (not Proxy): RN-web marks some exports non-configurable,
 * so a Proxy that swaps useColorScheme/Text/Appearance throws at runtime.
 */
function createRnModule() {
  const mod: Record<string, unknown> = { ...(ReactNative as object) }
  mod.Appearance = ForcedAppearance
  mod.useColorScheme = useForcedColorScheme
  mod.Text = ThemedText
  return mod
}

const RnModule = createRnModule()

/** Instance id from parent iframe URL (?id=…) — required when many previews share one page. */
const pageInstanceId =
  typeof window !== 'undefined'
    ? new URLSearchParams(window.location.search).get('id') || undefined
    : undefined

function post(msg: HostToParent) {
  parent.postMessage(
    {
      ...msg,
      // Prefer explicit msg.id, then last run-code id, then URL id so ready/pong never broadcast "anonymous"
      id: msg.id ?? lastInstanceId ?? pageInstanceId,
    },
    '*',
  )
}

function applyDomTheme(theme: ColorScheme) {
  const colors = THEME_COLORS[theme]
  const isDark = theme === 'dark'

  document.documentElement.classList.toggle('dark', isDark)
  document.documentElement.classList.toggle('light', !isDark)
  document.documentElement.style.colorScheme = theme
  document.documentElement.style.setProperty('--rn-bg', colors.bg)
  document.documentElement.style.setProperty('--rn-fg', colors.fg)
  document.documentElement.style.setProperty('--rn-muted', colors.muted)
  document.documentElement.style.background = colors.bg
  document.body.style.background = colors.bg
  document.body.style.color = colors.fg
  rootEl.style.background = colors.bg
  rootEl.style.color = colors.fg
}

/**
 * Apply site theme. Does NOT remount the user tree —
 * Appearance listeners + HostRoot shell background update in place.
 */
function applyTheme(theme: ColorScheme | undefined) {
  if (theme !== 'light' && theme !== 'dark') return
  const changed = currentTheme !== theme
  currentTheme = theme
  applyDomTheme(theme)
  if (changed) {
    notifyAppearance(theme)
  }
}

function showError(message: string) {
  errorEl.innerHTML = `<div class="title">Preview Error</div>${escapeHtml(message)}`
  errorEl.classList.add('visible')
}

function clearError() {
  errorEl.classList.remove('visible')
  errorEl.textContent = ''
}

function escapeHtml(s: string) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/** Stable root: theme changes only re-render shell bg, not remount App */
function HostRoot() {
  const [Component, setComponent] = React.useState<React.ComponentType | null>(null)
  const scheme = useForcedColorScheme()
  const colors = THEME_COLORS[scheme]

  React.useEffect(() => {
    hostBridge.setComponent = (next) => {
      // Always functional form — Component is a function type
      setComponent(() => next)
    }
    if (hostBridge.Component) {
      setComponent(() => hostBridge.Component)
    }
    return () => {
      hostBridge.setComponent = null
    }
  }, [])

  React.useEffect(() => {
    rootEl.style.color = colors.fg
    rootEl.style.background = colors.bg
  }, [colors.fg, colors.bg])

  if (!Component) {
    return React.createElement(
      'div',
      {
        id: 'boot',
        style: {
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          color: colors.muted,
          fontSize: 13,
        },
      },
      'Waiting for code…',
    )
  }

  return React.createElement(
    (RnModule as any).View,
    {
      style: {
        flex: 1,
        width: '100%',
        height: '100%',
        backgroundColor: colors.bg,
      },
    },
    React.createElement(Component),
  )
}

function ensureHostMounted() {
  if (!reactRoot) {
    rootEl.innerHTML = ''
    reactRoot = createRoot(rootEl)
    reactRoot.render(React.createElement(HostRoot))
  }
}

function setUserComponent(Component: React.ComponentType | null) {
  hostBridge.Component = Component
  ensureHostMounted()
  if (hostBridge.setComponent) {
    hostBridge.setComponent(Component)
  }
}

function createRequire() {
  const modules: Record<string, unknown> = {
    react: React,
    'react-dom': ReactDOM,
    'react-dom/client': { createRoot },
    'react/jsx-runtime': ReactJSXRuntime,
    'react/jsx-dev-runtime': ReactJSXDevRuntime,
    'react-native': RnModule,
    'react-native-web': RnModule,
  }

  return function require(name: string) {
    if (name in modules) return modules[name]
    throw new Error(
      `Module "${name}" is not available in the React Native preview.\n` +
        `Supported: react, react-native, react-dom, react/jsx-runtime.`,
    )
  }
}

function ensureDefaultExport(code: string): string {
  if (/export\s+default\b/.test(code)) return code
  if (/export\s*\{[^}]*\bas\s+default\b/.test(code)) return code

  const names: string[] = []
  const fnRe = /(?:export\s+)?function\s+([A-Z][A-Za-z0-9_]*)\s*\(/g
  const constRe =
    /(?:export\s+)?const\s+([A-Z][A-Za-z0-9_]*)\s*=\s*(?:async\s*)?(?:\(|function\b|React\.memo|memo\b)/g

  let m: RegExpExecArray | null
  while ((m = fnRe.exec(code))) names.push(m[1])
  while ((m = constRe.exec(code))) names.push(m[1])

  const preferred =
    names.find((n) => n === 'App') ||
    names.find((n) => n === 'Example' || n === 'Demo') ||
    names[0]

  if (!preferred) return code
  return `${code.trim()}\n\nexport default ${preferred};\n`
}

function preprocessSource(code: string): string {
  let src = code.trim()
  src = src.replace(/^import\s+type\s+[\s\S]*?;?\s*$/gm, '')
  src = src.replace(/^export\s+type\s+[\s\S]*?;?\s*$/gm, '')
  src = ensureDefaultExport(src)
  return src
}

function transformCode(code: string): string {
  const source = preprocessSource(code)

  const result = Babel.transform(source, {
    filename: 'App.tsx',
    presets: [
      ['typescript', { isTSX: true, allExtensions: true, onlyRemoveTypeImports: true }],
      ['react', { runtime: 'automatic' }],
    ],
    plugins: ['transform-modules-commonjs'],
    sourceType: 'module',
    compact: false,
  })

  if (!result?.code) {
    throw new Error('Babel produced empty output')
  }

  return result.code
}

function resolveComponent(moduleExports: any): React.ComponentType {
  const candidate =
    moduleExports?.default ??
    moduleExports?.App ??
    moduleExports?.Example ??
    moduleExports?.Demo ??
    (typeof moduleExports === 'function' ? moduleExports : null)

  if (candidate && (typeof candidate === 'function' || typeof candidate === 'object')) {
    return candidate as React.ComponentType
  }

  throw new Error(
    'No component to render.\n' +
      'Export a default component, e.g.:\n\n' +
      'export default function App() {\n' +
      '  return <View>...</View>\n' +
      '}',
  )
}

function runCode(code: string, id?: string) {
  lastInstanceId = id
  clearError()

  try {
    if (!code?.trim()) {
      throw new Error('Empty code block')
    }

    const transformed = transformCode(code)
    const require = createRequire()
    const module = { exports: {} as any }
    const exports = module.exports

    const runner = new Function(
      'require',
      'module',
      'exports',
      'React',
      'console',
      `"use strict";\n${transformed}\n;return module.exports;`,
    )

    const moduleExports = runner(require, module, exports, React, console)
    const Component = resolveComponent(moduleExports ?? module.exports)

    setUserComponent(Component)
    post({ type: 'rn-preview-success', id })
  } catch (err: any) {
    setUserComponent(null)
    const message = err?.message || String(err)
    showError(message)
    post({ type: 'rn-preview-error', id, message })
  }
}

function handleMessage(event: MessageEvent) {
  const data = event.data as PreviewMessage
  if (!data || typeof data !== 'object') return

  switch (data.type) {
    case 'ping':
      post({ type: 'rn-preview-pong', id: data.id })
      break
    case 'set-theme':
      applyTheme(data.theme)
      break
    case 'run-code':
      if (data.theme === 'light' || data.theme === 'dark') {
        applyTheme(data.theme)
      }
      runCode(data.code, data.id)
      break
  }
}

window.addEventListener('message', handleMessage)

window.addEventListener('error', (e) => {
  const message = e.error?.message || e.message || 'Unknown error'
  showError(message)
  post({ type: 'rn-preview-error', id: lastInstanceId, message })
})

window.addEventListener('unhandledrejection', (e) => {
  const message = e.reason?.message || String(e.reason)
  showError(message)
  post({ type: 'rn-preview-error', id: lastInstanceId, message })
})

applyDomTheme('light')
ensureHostMounted()

// Seed lastInstanceId early so every outbound message is scoped to this iframe.
if (pageInstanceId) {
  lastInstanceId = pageInstanceId
}

post({ type: 'rn-preview-ready' })
setTimeout(() => post({ type: 'rn-preview-ready' }), 100)
setTimeout(() => post({ type: 'rn-preview-ready' }), 500)
