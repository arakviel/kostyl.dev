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
    <div class="my-6">
        <!-- Original code blocks slot -->
        <div class="mb-1">
            <p class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
                HTML / CSS
            </p>
            <slot />
        </div>

        <!-- Resizable preview block -->
        <div
            class="border border-gray-200 dark:border-gray-800 rounded-lg bg-white dark:bg-gray-900 overflow-hidden flex flex-col"
        >
            <div
                class="bg-gray-100 dark:bg-gray-800 px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200 dark:border-gray-700 flex justify-between items-center"
            >
                <span>Preview</span>
            </div>
            <iframe
                ref="iframeRef"
                :srcdoc="srcdoc"
                class="w-full border-none bg-white text-black block"
                :style="{ height: iframeHeight > 0 ? iframeHeight + 'px' : '100px' }"
                sandbox="allow-scripts allow-same-origin"
                scrolling="no"
                @load="onIframeLoad"
            ></iframe>
        </div>
    </div>
</template>

<style scoped></style>
