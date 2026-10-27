<script setup>
/**
 * ::code-trace — покрокове виконання Python-програми (у стилі Python Tutor).
 * Дані — JSON із tools/code-trace/trace.py (реальний CPython), компонент лише програє їх.
 */
import { ref, computed, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  title: { type: String, default: '' },
  step: { type: [Number, String], default: 0 },
  inlinePrimitives: { type: Boolean, default: false },
  predict: { type: Boolean, default: true },
  height: { type: [Number, String], default: '' },
})

const data = ref(null)
const loadError = ref('')
const index = ref(Number(props.step) || 0)
const inline = ref(props.inlinePrimitives)
const root = ref(null)
const viz = ref(null)
const arrows = ref([])
const svgSize = ref({ w: 0, h: 0 })

const baseURL = useRuntimeConfig().app.baseURL || '/'
const url = computed(() => (props.src.startsWith('/') ? baseURL.replace(/\/$/, '') + props.src : props.src))

onMounted(async () => {
  try {
    const res = await fetch(url.value)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    data.value = await res.json()
    index.value = Math.min(Math.max(index.value, 0), data.value.steps.length - 1)
  } catch (e) {
    loadError.value = `Не вдалося завантажити ${props.src}: ${e.message}`
  }
})

const steps = computed(() => data.value?.steps ?? [])
const total = computed(() => steps.value.length)
const cur = computed(() => steps.value[index.value] ?? null)
const prev = computed(() => (index.value > 0 ? steps.value[index.value - 1] : null))
const isLast = computed(() => index.value === total.value - 1)
const codeLines = computed(() => (data.value?.code ?? '').replace(/\n$/, '').split('\n'))

function go(i) {
  index.value = Math.min(Math.max(i, 0), total.value - 1)
}
function onKey(e) {
  if (e.key === 'ArrowRight') { go(index.value + 1); e.preventDefault() }
  if (e.key === 'ArrowLeft') { go(index.value - 1); e.preventDefault() }
  if (e.key === 'Home') { go(0); e.preventDefault() }
  if (e.key === 'End') { go(total.value - 1); e.preventDefault() }
}

// ---- Підписи -----------------------------------------------------------------

function frameTitle(name) {
  return name === '<module>' ? 'Глобальний кадр' : `${name}()`
}

const currentFrame = computed(() => cur.value?.frames.at(-1) ?? null)

const eventLabel = computed(() => {
  const s = cur.value
  if (!s) return ''
  const fname = currentFrame.value ? frameTitle(currentFrame.value.name) : ''
  if (isLast.value && data.value.error) return `Програма впала: ${data.value.error.type}`
  if (isLast.value && s.event === 'return' && s.frames.length === 1) return 'Програму завершено'
  if (isLast.value && data.value.truncated) return 'Трасування зупинено: вичерпано ліміт кроків'
  switch (s.event) {
    case 'line': return `Наступним виконається рядок ${s.line}`
    case 'call': return `Виклик: створено кадр ${fname}`
    case 'return': return `${fname} повертає значення`
    case 'exception': return `Виняток у рядку ${s.line}`
    case 'unwind': return `Кадр ${fname} зникає через виняток`
    default: return s.event
  }
})

const output = computed(() => steps.value.slice(0, index.value).map(s => s.out || '').join(''))

// ---- Підсвічування коду --------------------------------------------------------

const KEYWORDS = new Set('False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda match case nonlocal not or pass raise return try while with yield'.split(' '))
const BUILTINS = new Set('print input len range int float str bool list dict set tuple frozendict frozenset type id isinstance sorted enumerate zip map filter sum min max abs next iter open repr hash'.split(' '))
const TOKEN = /(#.*$)|([rbfRBF]{0,2}"(?:[^"\\]|\\.)*"|[rbfRBF]{0,2}'(?:[^'\\]|\\.)*')|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_]\w*)/g

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}
function highlight(line) {
  let out = '', last = 0
  for (const m of line.matchAll(TOKEN)) {
    out += escapeHtml(line.slice(last, m.index))
    const t = escapeHtml(m[0])
    if (m[1]) out += `<span class="tk-com">${t}</span>`
    else if (m[2]) out += `<span class="tk-str">${t}</span>`
    else if (m[3]) out += `<span class="tk-num">${t}</span>`
    else if (KEYWORDS.has(m[0])) out += `<span class="tk-kw">${t}</span>`
    else if (BUILTINS.has(m[0])) out += `<span class="tk-bi">${t}</span>`
    else out += t
    last = m.index + m[0].length
  }
  return out + escapeHtml(line.slice(last))
}

const GUTTER_ICONS = { next: 'i-lucide-arrow-right', return: 'i-lucide-corner-down-left', error: 'i-lucide-x' }

const lineMark = computed(() => {
  const s = cur.value
  if (!s) return {}
  const marks = {}
  // рядки викликів у зовнішніх кадрах — приглушено
  for (const f of s.frames.slice(0, -1)) marks[f.line] = 'caller'
  const kind = (isLast.value && data.value.error) || s.event === 'exception' || s.event === 'unwind'
    ? 'error' : s.event === 'return' ? 'return' : 'next'
  marks[s.line] = kind
  return marks
})

// ---- Купа: розкладка по колонках ------------------------------------------------

function isPrimitive(key) {
  return key != null && cur.value?.heap[key]?.kind === 'primitive'
}
function shown(key) {
  return key != null && !(inline.value && isPrimitive(key))
}

function children(entry) {
  const out = []
  if (entry.items) out.push(...entry.items)
  if (entry.entries) for (const [k, v] of entry.entries) out.push(k, v)
  if (entry.freevars) out.push(...Object.values(entry.freevars))
  if (entry.kind === 'cell') out.push(entry.ref)
  if (entry.attrs) out.push(...entry.attrs.map(a => a.ref))
  if (entry.frame) out.push(...entry.frame.vars.map(v => v.ref))
  return out
}

function frameTargets(s) {
  const out = []
  for (const f of s.frames) for (const v of f.vars) out.push(v.cellRef ?? v.ref)
  if (s.returnValue) out.push(s.returnValue)
  if (s.exception) out.push(s.exception)
  return out
}

const columns = computed(() => {
  const s = cur.value
  if (!s) return []
  const depth = new Map()
  let queue = frameTargets(s).filter(shown)
  queue.forEach(k => depth.has(k) || depth.set(k, 0))
  queue = [...new Set(queue)]
  while (queue.length) {
    const next = []
    for (const key of queue) {
      const entry = s.heap[key]
      if (!entry) continue
      for (const child of children(entry)) {
        if (shown(child) && !depth.has(child)) {
          depth.set(child, depth.get(key) + 1)
          next.push(child)
        }
      }
    }
    queue = next
  }
  const cols = []
  for (const [key, d] of depth) (cols[d] ||= []).push(key)
  return cols
})

function shortId(key) {
  return '…' + key.slice(-4)
}

function inlineText(key) {
  return cur.value.heap[key]?.repr ?? '?'
}

// ---- Стрілки ----------------------------------------------------------------------

function edges(s) {
  const map = new Map()
  if (!s) return map
  for (const f of s.frames) for (const v of f.vars) map.set(`f:${f.id}:${v.name}`, v.cellRef ?? v.ref)
  for (const [key, e] of Object.entries(s.heap)) {
    e.items?.forEach((r, i) => map.set(`o:${key}:${i}`, r))
    e.entries?.forEach(([k, v], i) => { map.set(`o:${key}:k${i}`, k); map.set(`o:${key}:v${i}`, v) })
    if (e.freevars) for (const [n, r] of Object.entries(e.freevars)) map.set(`o:${key}:free:${n}`, r)
    if (e.kind === 'cell') map.set(`o:${key}:cell`, e.ref)
    e.attrs?.forEach(a => map.set(`o:${key}:a:${a.name}`, a.ref))
    e.frame?.vars.forEach(v => map.set(`o:${key}:g:${v.name}`, v.ref))
  }
  return map
}

const changed = computed(() => {
  const before = edges(prev.value)
  const now = edges(cur.value)
  const set = new Set()
  for (const [id, target] of now) if (before.get(id) !== target) set.add(id)
  return set
})

const newObjects = computed(() => {
  const before = prev.value?.heap ?? {}
  return new Set(Object.keys(cur.value?.heap ?? {}).filter(k => !(k in before)))
})

function computeArrows() {
  const c = viz.value
  if (!c) return
  const base = c.getBoundingClientRect()
  const ox = c.scrollLeft - base.left
  const oy = c.scrollTop - base.top
  const out = []
  c.querySelectorAll('[data-target]').forEach((el) => {
    const target = c.querySelector(`[data-obj="${el.dataset.target}"]`)
    if (!target) return
    const a = el.getBoundingClientRect()
    const b = target.getBoundingClientRect()
    const x1 = a.left + a.width / 2 + ox
    const y1 = a.top + a.height / 2 + oy
    const y2 = b.top + Math.min(16, b.height / 2) + oy
    // спершу виходимо праворуч за межу своєї плашки, щоб стрілка не перетинала її вміст
    const box = el.closest('.ct-obj, .ct-frame')?.getBoundingClientRect() ?? a
    const xe = Math.max(x1, box.right + ox + 10)
    let d
    if (b.left + ox > xe + 8) {
      const x2 = b.left + ox - 2
      const dx = Math.max(20, (x2 - xe) / 2)
      d = `M ${x1} ${y1} L ${xe} ${y1} C ${xe + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`
    } else {
      // посилання назад (цикл або об'єкт у тій самій колонці) — огинаємо праворуч
      const x2 = b.right + ox + 2
      const bulge = Math.max(xe, x2) + 36
      d = `M ${x1} ${y1} L ${xe} ${y1} C ${bulge} ${y1}, ${bulge} ${y2}, ${x2} ${y2}`
    }
    out.push({ id: el.dataset.src, d, hot: changed.value.has(el.dataset.src) })
  })
  arrows.value = out
  svgSize.value = { w: c.scrollWidth, h: c.scrollHeight }
}

let observer
onMounted(() => {
  observer = new ResizeObserver(() => computeArrows())
  window.addEventListener('resize', computeArrows)
})
onBeforeUnmount(() => {
  observer?.disconnect()
  window.removeEventListener('resize', computeArrows)
})
watch(viz, (el, old) => {
  if (old) observer?.unobserve(old)
  if (el) observer?.observe(el)
})
watch([index, inline, data], async () => {
  await nextTick()
  computeArrows()
}, { flush: 'post' })

const bodyStyle = computed(() => (props.height ? { minHeight: `${props.height}px` } : {}))
</script>

<template>
  <div ref="root" class="ct-window not-prose my-8" tabindex="0" @keydown="onKey">
    <div class="ct-header">
      <div class="flex gap-2">
        <span class="ct-dot bg-[#ff5f56]" /><span class="ct-dot bg-[#ffbd2e]" /><span class="ct-dot bg-[#27c93f]" />
      </div>
      <div class="ct-title">{{ title || data?.name || 'code-trace' }}</div>
      <div v-if="data" class="ct-version" :title="`Записано на ${data.implementation} ${data.python}`">
        Python {{ data.python }}
      </div>
    </div>

    <div v-if="loadError" class="p-6 text-sm ct-error-text">{{ loadError }}</div>
    <div v-else-if="!data" class="p-6 text-sm ct-muted">Завантаження трасування…</div>

    <template v-else>
      <div class="ct-body" :style="bodyStyle">
        <!-- Код -->
        <div class="ct-code">
          <div
            v-for="(line, i) in codeLines"
            :key="i"
            class="ct-line"
            :class="lineMark[i + 1] && `is-${lineMark[i + 1]}`"
          >
            <span class="ct-gutter">
              <UIcon v-if="GUTTER_ICONS[lineMark[i + 1]]" :name="GUTTER_ICONS[lineMark[i + 1]]" class="ct-icon" />
              <template v-else>{{ i + 1 }}</template>
            </span>
            <span class="ct-src" v-html="highlight(line) || '&nbsp;'" />
          </div>
        </div>

        <!-- Кадри + купа -->
        <div ref="viz" class="ct-viz">
          <svg class="ct-arrows" :width="svgSize.w" :height="svgSize.h">
            <defs>
              <marker id="ct-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M0,0 L10,5 L0,10 z" class="ct-head" />
              </marker>
              <marker id="ct-head-hot" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M0,0 L10,5 L0,10 z" class="ct-head-hot" />
              </marker>
            </defs>
            <path
              v-for="a in arrows"
              :key="a.id"
              :d="a.d"
              :class="a.hot ? 'ct-arrow-hot' : 'ct-arrow'"
              :marker-end="a.hot ? 'url(#ct-head-hot)' : 'url(#ct-head)'"
            />
          </svg>

          <div class="ct-col ct-frames">
            <div class="ct-col-title">Кадри (стек викликів)</div>
            <div
              v-for="(f, fi) in cur.frames"
              :key="f.id"
              class="ct-frame"
              :class="{ 'is-active': fi === cur.frames.length - 1, 'is-leaving': fi === cur.frames.length - 1 && (cur.event === 'return' || cur.event === 'unwind') && cur.frames.length > 1 }"
            >
              <div class="ct-frame-title">{{ frameTitle(f.name) }}</div>
              <div v-if="!f.vars.length" class="ct-empty">імен ще немає</div>
              <div v-for="v in f.vars" :key="v.name" class="ct-var">
                <span class="ct-name">{{ v.name }}</span>
                <span v-if="!shown(v.cellRef ?? v.ref)" class="ct-inline">{{ inlineText(v.ref) }}</span>
                <span
                  v-else
                  class="ct-pin"
                  :class="{ 'is-cell': v.cell }"
                  :title="v.cell ? 'Змінна живе в комірці (cell) замикання' : ''"
                  :data-src="`f:${f.id}:${v.name}`"
                  :data-target="v.cellRef ?? v.ref"
                />
              </div>
              <div v-if="fi === cur.frames.length - 1 && cur.returnValue" class="ct-var ct-special">
                <span class="ct-name">return</span>
                <span v-if="!shown(cur.returnValue)" class="ct-inline">{{ inlineText(cur.returnValue) }}</span>
                <span v-else class="ct-pin" :data-src="`f:${f.id}:return`" :data-target="cur.returnValue" />
              </div>
              <div v-if="fi === cur.frames.length - 1 && cur.exception" class="ct-var ct-special is-error">
                <span class="ct-name">виняток</span>
                <span class="ct-pin" :data-src="`f:${f.id}:exception`" :data-target="cur.exception" />
              </div>
            </div>
          </div>

          <div v-for="(col, ci) in columns" :key="ci" class="ct-col">
            <div class="ct-col-title">{{ ci === 0 ? 'Об\'єкти в пам\'яті' : '&nbsp;' }}</div>
            <div
              v-for="key in col"
              :key="key"
              class="ct-obj"
              :class="[`kind-${cur.heap[key].kind}`, { 'is-new': newObjects.has(key) }]"
              :data-obj="key"
            >
              <div class="ct-obj-head">
                <span class="ct-type">{{ cur.heap[key].type }}</span>
                <span class="ct-badges">
                  <UIcon v-if="!cur.heap[key].mutable" name="i-lucide-lock" class="ct-icon" title="Незмінний об'єкт (immutable)" />
                  <UIcon v-if="cur.heap[key].immortal" name="i-lucide-infinity" class="ct-icon" title="Безсмертний об'єкт CPython: живе до кінця роботи інтерпретатора" />
                  <span class="ct-refs" :title="`Стрілок на цей об'єкт на схемі: ${cur.heap[key].refs}`"><UIcon name="i-lucide-arrow-left" class="ct-icon" />{{ cur.heap[key].refs }}</span>
                  <span class="ct-id" :title="`id() = ${key}`">id {{ shortId(key) }}</span>
                </span>
              </div>

              <template v-for="e in [cur.heap[key]]" :key="'b' + key">
                <div v-if="e.kind === 'primitive'" class="ct-value">{{ e.repr }}</div>

                <div v-else-if="e.kind === 'sequence' || e.kind === 'set'" class="ct-slots">
                  <div v-if="!e.items.length" class="ct-empty">порожньо</div>
                  <div v-for="(r, i) in e.items" :key="i" class="ct-slot">
                    <span v-if="e.kind === 'sequence'" class="ct-idx">{{ i }}</span>
                    <span v-if="!shown(r)" class="ct-inline">{{ r && inlineText(r) }}</span>
                    <span v-else class="ct-pin" :data-src="`o:${key}:${i}`" :data-target="r" />
                  </div>
                  <div v-if="e.more" class="ct-empty">…ще {{ e.more }}</div>
                </div>

                <div v-else-if="e.kind === 'mapping'" class="ct-rows">
                  <div v-if="!e.entries.length" class="ct-empty">порожньо</div>
                  <div v-for="([k, v], i) in e.entries" :key="i" class="ct-row">
                    <span v-if="!shown(k)" class="ct-inline">{{ inlineText(k) }}</span>
                    <span v-else class="ct-pin" :data-src="`o:${key}:k${i}`" :data-target="k" />
                    <span class="ct-colon">:</span>
                    <span v-if="!shown(v)" class="ct-inline">{{ inlineText(v) }}</span>
                    <span v-else class="ct-pin" :data-src="`o:${key}:v${i}`" :data-target="v" />
                  </div>
                  <div v-if="e.more" class="ct-empty">…ще {{ e.more }}</div>
                </div>

                <div v-else-if="e.kind === 'function'" class="ct-rows">
                  <div class="ct-value ct-mono">{{ e.name }}{{ e.signature }}</div>
                  <div v-for="(r, n) in e.freevars || {}" :key="n" class="ct-row">
                    <span class="ct-name">{{ n }}</span>
                    <span class="ct-pin is-cell" :data-src="`o:${key}:free:${n}`" :data-target="r" />
                  </div>
                </div>

                <div v-else-if="e.kind === 'cell'" class="ct-rows">
                  <div class="ct-row">
                    <span class="ct-name">вміст</span>
                    <span v-if="e.ref == null" class="ct-empty">порожня</span>
                    <span v-else-if="!shown(e.ref)" class="ct-inline">{{ inlineText(e.ref) }}</span>
                    <span v-else class="ct-pin" :data-src="`o:${key}:cell`" :data-target="e.ref" />
                  </div>
                </div>

                <div v-else-if="e.kind === 'generator'" class="ct-rows">
                  <div class="ct-value ct-mono">{{ e.name }} · {{ { GEN_CREATED: 'створено', GEN_SUSPENDED: 'на паузі', GEN_RUNNING: 'виконується', GEN_CLOSED: 'завершено' }[e.state] }}</div>
                  <template v-if="e.frame">
                    <div class="ct-empty">заморожений кадр, рядок {{ e.frame.line }}</div>
                    <div v-for="v in e.frame.vars" :key="v.name" class="ct-row">
                      <span class="ct-name">{{ v.name }}</span>
                      <span v-if="!shown(v.ref)" class="ct-inline">{{ inlineText(v.ref) }}</span>
                      <span v-else class="ct-pin" :data-src="`o:${key}:g:${v.name}`" :data-target="v.ref" />
                    </div>
                  </template>
                </div>

                <div v-else-if="e.kind === 'exception'" class="ct-value ct-error-text">{{ e.message }}</div>

                <div v-else-if="e.kind === 'object'" class="ct-rows">
                  <div class="ct-value ct-mono">{{ e.repr }}</div>
                  <div v-for="a in e.attrs || []" :key="a.name" class="ct-row">
                    <span class="ct-name">.{{ a.name }}</span>
                    <span v-if="!shown(a.ref)" class="ct-inline">{{ inlineText(a.ref) }}</span>
                    <span v-else class="ct-pin" :data-src="`o:${key}:a:${a.name}`" :data-target="a.ref" />
                  </div>
                </div>

                <div v-else class="ct-value ct-mono">{{ e.name }}</div>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- Передбач -->
      <div v-if="predict && cur.ask" class="ct-ask">
        <UIcon name="i-lucide-circle-help" class="ct-ask-icon" />
        <span class="flex-1"><b>Передбачте:</b> {{ cur.ask }}</span>
        <button class="ct-btn ct-btn-primary" @click="go(index + 1)">Перевірити <UIcon name="i-lucide-arrow-right" class="ct-icon" /></button>
      </div>

      <!-- Керування -->
      <div class="ct-controls">
        <button class="ct-btn" :disabled="index === 0" title="На початок (Home)" @click="go(0)"><UIcon name="i-lucide-skip-back" class="ct-icon" /></button>
        <button class="ct-btn" :disabled="index === 0" title="Крок назад (←)" @click="go(index - 1)"><UIcon name="i-lucide-chevron-left" class="ct-icon" /></button>
        <input
          class="ct-range"
          type="range"
          min="0"
          :max="total - 1"
          :value="index"
          aria-label="Крок виконання"
          @input="go(Number($event.target.value))"
        >
        <button class="ct-btn" :disabled="isLast" title="Крок уперед (→)" @click="go(index + 1)"><UIcon name="i-lucide-chevron-right" class="ct-icon" /></button>
        <button class="ct-btn" :disabled="isLast" title="В кінець (End)" @click="go(total - 1)"><UIcon name="i-lucide-skip-forward" class="ct-icon" /></button>
        <span class="ct-counter">крок {{ index + 1 }} / {{ total }}</span>
        <label class="ct-toggle" title="Спрощення: показувати числа й рядки всередині змінних, без окремих об'єктів">
          <input v-model="inline" type="checkbox"> спрощено
        </label>
      </div>
      <div class="ct-status" :class="{ 'is-error': (isLast && data.error) || cur.event === 'exception' || cur.event === 'unwind' }">
        {{ eventLabel }}
      </div>

      <!-- Вивід -->
      <div class="ct-output">
        <div class="ct-col-title">Вивід програми</div>
        <pre class="ct-stdout">{{ output }}<span v-if="isLast && data.error" class="ct-error-text">{{ data.error.traceback }}</span><span v-if="!output && !(isLast && data.error)" class="ct-muted">(поки нічого)</span></pre>
      </div>
    </template>
  </div>
</template>

<style scoped>
.ct-window {
  --ct-bg: #ffffff;
  --ct-panel: #f8fafc;
  --ct-header: #f3f4f6;
  --ct-border: #e4e4e7;
  --ct-text: #18181b;
  --ct-muted: #71717a;
  --ct-name: #0e7490;        /* імена — cyan */
  --ct-obj: #ecfdf5;         /* об'єкти — emerald */
  --ct-obj-border: #6ee7b7;
  --ct-obj-head: #047857;
  --ct-arrow: #64748b;
  --ct-hot: #d97706;         /* стрілка змінилася — amber */
  --ct-next: #dcfce7;
  --ct-caller: #f1f5f9;
  --ct-error: #dc2626;
  --ct-error-bg: #fee2e2;
  --ct-ask-bg: #fef3c7;
  --ct-kw: #7c3aed;
  --ct-str: #15803d;
  --ct-num: #c2410c;
  --ct-com: #94a3b8;
  --ct-bi: #0369a1;

  background: var(--ct-bg);
  color: var(--ct-text);
  border: 1px solid var(--ct-border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 40px -20px rgba(0, 0, 0, 0.25);
  outline: none;
}
.ct-window:focus-visible { box-shadow: 0 0 0 2px var(--ct-name); }

:is(.dark *) .ct-window {
  --ct-bg: #1c1c1c;
  --ct-panel: #232323;
  --ct-header: #323232;
  --ct-border: rgba(255, 255, 255, 0.08);
  --ct-text: #f4f4f5;
  --ct-muted: #9ca3af;
  --ct-name: #22d3ee;
  --ct-obj: rgba(16, 185, 129, 0.1);
  --ct-obj-border: rgba(52, 211, 153, 0.45);
  --ct-obj-head: #6ee7b7;
  --ct-arrow: #94a3b8;
  --ct-hot: #fbbf24;
  --ct-next: rgba(34, 197, 94, 0.16);
  --ct-caller: rgba(255, 255, 255, 0.05);
  --ct-error: #f87171;
  --ct-error-bg: rgba(248, 113, 113, 0.14);
  --ct-ask-bg: rgba(251, 191, 36, 0.14);
  --ct-kw: #c084fc;
  --ct-str: #86efac;
  --ct-num: #fdba74;
  --ct-com: #6b7280;
  --ct-bi: #7dd3fc;
}

.ct-header {
  display: flex; align-items: center; gap: 12px;
  height: 40px; padding: 0 16px;
  background: var(--ct-header); border-bottom: 1px solid var(--ct-border);
  position: relative; user-select: none;
}
.ct-dot { width: 12px; height: 12px; border-radius: 9999px; display: inline-block; }
.ct-title {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  font-size: 13px; color: var(--ct-muted); pointer-events: none;
}
.ct-version { margin-left: auto; font-size: 11px; color: var(--ct-muted); font-family: ui-monospace, monospace; }

.ct-body { display: grid; grid-template-columns: minmax(220px, max-content) minmax(0, 1fr); }
@media (max-width: 900px) { .ct-body { grid-template-columns: minmax(0, 1fr); } }

.ct-code {
  padding: 12px 0; background: var(--ct-panel); border-right: 1px solid var(--ct-border);
  font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 13px; line-height: 1.7;
  overflow-x: auto;
}
.ct-line { display: flex; white-space: pre; padding-right: 12px; border-left: 3px solid transparent; }
.ct-line.is-next { background: var(--ct-next); border-left-color: #22c55e; }
.ct-line.is-return { background: var(--ct-next); border-left-color: var(--ct-name); }
.ct-line.is-error { background: var(--ct-error-bg); border-left-color: var(--ct-error); }
.ct-line.is-caller { background: var(--ct-caller); border-left-color: var(--ct-muted); }
.ct-gutter {
  width: 2.6em; flex: none; display: inline-flex; align-items: center; justify-content: flex-end;
  padding-right: 12px; color: var(--ct-muted); user-select: none;
}
.ct-icon { width: 1.05em; height: 1.05em; flex: none; }
.ct-line.is-return .ct-gutter { color: var(--ct-name); }
.ct-line.is-next .ct-gutter { color: #16a34a; font-weight: 700; }
.ct-line.is-error .ct-gutter { color: var(--ct-error); font-weight: 700; }
.ct-src :deep(.tk-kw) { color: var(--ct-kw); }
.ct-src :deep(.tk-str) { color: var(--ct-str); }
.ct-src :deep(.tk-num) { color: var(--ct-num); }
.ct-src :deep(.tk-com) { color: var(--ct-com); font-style: italic; }
.ct-src :deep(.tk-bi) { color: var(--ct-bi); }

.ct-viz {
  position: relative; display: flex; align-items: flex-start; gap: 44px;
  padding: 12px 56px 24px 16px; overflow: auto; min-height: 220px;
  font-size: 13px;
}
.ct-arrows { position: absolute; left: 0; top: 0; pointer-events: none; overflow: visible; z-index: 2; }
.ct-arrow { fill: none; stroke: var(--ct-arrow); stroke-width: 1.6; }
.ct-arrow-hot { fill: none; stroke: var(--ct-hot); stroke-width: 2.4; }
.ct-head { fill: var(--ct-arrow); }
.ct-head-hot { fill: var(--ct-hot); }

.ct-col { display: flex; flex-direction: column; gap: 14px; flex: none; }
.ct-col-title { font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ct-muted); }

.ct-frame {
  min-width: 150px; border: 1px solid var(--ct-border); border-radius: 8px;
  background: var(--ct-panel); padding: 6px 10px 8px; opacity: 0.75;
  position: relative; z-index: 1;
}
.ct-frame.is-active { opacity: 1; border-color: var(--ct-name); }
.ct-frame.is-leaving { border-style: dashed; }
.ct-frame-title { font-weight: 600; font-size: 12px; margin-bottom: 4px; }
.ct-var, .ct-row, .ct-slot { display: flex; align-items: center; gap: 8px; min-height: 26px; }
.ct-var { justify-content: space-between; border-top: 1px dashed var(--ct-border); }
.ct-frame-title + .ct-var { border-top: none; }
.ct-name { font-family: 'JetBrains Mono', ui-monospace, monospace; color: var(--ct-name); font-weight: 600; }
.ct-special .ct-name { color: var(--ct-muted); font-style: italic; }
.ct-special.is-error .ct-name { color: var(--ct-error); }

.ct-pin {
  width: 12px; height: 12px; border-radius: 9999px; flex: none;
  background: var(--ct-arrow); box-shadow: 0 0 0 3px var(--ct-bg);
}
.ct-pin.is-cell { background: transparent; border: 2px dashed var(--ct-arrow); }
.ct-inline {
  font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 12px;
  padding: 0 6px; border-radius: 4px; background: var(--ct-obj); border: 1px solid var(--ct-obj-border);
}

.ct-obj {
  min-width: 96px; max-width: 280px; border: 1.5px solid var(--ct-obj-border); border-radius: 8px;
  /* непрозорий фон: стрілки йдуть під плашками */
  background: linear-gradient(var(--ct-obj), var(--ct-obj)), var(--ct-bg);
  position: relative; z-index: 1;
}
.ct-obj.is-new { animation: ct-pop 0.5s ease-out; }
@keyframes ct-pop { from { transform: scale(0.85); opacity: 0.2; } to { transform: scale(1); opacity: 1; } }
.ct-obj.kind-exception { border-color: var(--ct-error); background: var(--ct-error-bg); }
.ct-obj.kind-cell { border-style: dashed; }
.ct-obj-head {
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  padding: 3px 8px; border-bottom: 1px solid var(--ct-obj-border);
  font-size: 11px;
}
.ct-type { font-weight: 700; color: var(--ct-obj-head); font-family: 'JetBrains Mono', ui-monospace, monospace; }
.ct-obj.kind-exception .ct-type { color: var(--ct-error); }
.ct-badges { display: flex; align-items: center; gap: 6px; color: var(--ct-muted); white-space: nowrap; }
.ct-refs { display: inline-flex; align-items: center; gap: 1px; }
.ct-id, .ct-refs { font-family: ui-monospace, monospace; }
.ct-value { padding: 6px 10px; font-family: 'JetBrains Mono', ui-monospace, monospace; word-break: break-all; }
.ct-mono { font-size: 12px; }
.ct-slots { display: flex; flex-wrap: wrap; }
.ct-slot {
  flex-direction: column; justify-content: center; gap: 2px; min-width: 34px; padding: 4px 6px;
  border-right: 1px solid var(--ct-obj-border);
}
.ct-slot:last-child { border-right: none; }
.ct-idx { font-size: 10px; color: var(--ct-muted); }
.ct-rows { padding: 2px 0; }
.ct-row { padding: 0 10px; }
.ct-colon { color: var(--ct-muted); }
.ct-empty { font-size: 11px; color: var(--ct-muted); font-style: italic; padding: 2px 10px; }

.ct-ask {
  display: flex; align-items: center; gap: 12px; padding: 10px 16px;
  background: var(--ct-ask-bg); border-top: 1px solid var(--ct-border); font-size: 14px;
}
.ct-ask-icon { width: 22px; height: 22px; color: var(--ct-hot); flex: none; }

.ct-controls {
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
  padding: 10px 16px; border-top: 1px solid var(--ct-border); background: var(--ct-header);
}
.ct-btn {
  min-width: 34px; height: 30px; padding: 0 10px; border-radius: 6px;
  border: 1px solid var(--ct-border); background: var(--ct-bg); color: var(--ct-text);
  font-size: 13px; cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center; gap: 4px;
}
.ct-btn:hover:not(:disabled) { border-color: var(--ct-name); }
.ct-btn:disabled { opacity: 0.4; cursor: default; }
.ct-btn-primary { background: var(--ct-hot); border-color: var(--ct-hot); color: #fff; font-weight: 600; }
.ct-range { flex: 1; min-width: 120px; accent-color: var(--ct-name); }
.ct-counter { font-size: 12px; color: var(--ct-muted); font-family: ui-monospace, monospace; white-space: nowrap; }
.ct-toggle { display: flex; align-items: center; gap: 4px; font-size: 12px; color: var(--ct-muted); cursor: pointer; }

.ct-status { padding: 6px 16px; font-size: 13px; color: var(--ct-muted); border-top: 1px solid var(--ct-border); }
.ct-status.is-error { color: var(--ct-error); font-weight: 600; }

.ct-output { padding: 10px 16px 14px; border-top: 1px solid var(--ct-border); background: var(--ct-panel); }
.ct-stdout {
  margin: 6px 0 0; padding: 0; background: transparent; border: none;
  font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 13px; line-height: 1.6;
  white-space: pre-wrap; max-height: 220px; overflow: auto;
}
.ct-error-text { color: var(--ct-error); }
.ct-muted { color: var(--ct-muted); }
</style>
