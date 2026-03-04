<script setup>
    import { ref, computed, useSlots, onMounted, onUnmounted } from 'vue'

    const slots = useSlots()
    const htmlCode = ref('')
    const cssCode = ref('')
    const iframeHeight = ref(150)
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

    const onMessage = (event) => {
        if (event.data?.type === 'html-preview-resize') {
            iframeHeight.value = event.data.height
        }
    }

    onMounted(() => {
        extractCodes()
        window.addEventListener('message', onMessage)
    })

    onUnmounted(() => {
        window.removeEventListener('message', onMessage)
    })

    const srcdoc = computed(
        () => `
  <!DOCTYPE html>
  <html>
    <head>
      <meta charset="utf-8">
      <style>
        html, body { 
          font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; 
          padding: 1rem; 
          margin: 0;
          color: #333;
        }
        * { box-sizing: border-box; }
        
        /* User-provided CSS */
        ${cssCode.value}
      </style>
    </head>
    <body>
      ${htmlCode.value}
      <script>
        const notify = () => {
          const h = document.documentElement.scrollHeight
          window.parent.postMessage({ type: 'html-preview-resize', height: h }, '*')
        }
        new ResizeObserver(notify).observe(document.body)
        window.addEventListener('load', notify)
      <\/script>
    </body>
  </html>
`,
    )
</script>

<template>
    <div class="my-6">
        <!-- Original code blocks slot -->
        <div class="mb-4">
            <slot />
        </div>

        <!-- Resizable preview block -->
        <div
            class="border border-gray-200 dark:border-gray-800 rounded-lg shadow-sm bg-white dark:bg-gray-900 overflow-hidden flex flex-col"
        >
            <div
                class="bg-gray-100 dark:bg-gray-800 px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200 dark:border-gray-700 flex justify-between items-center"
            >
                <span>Preview</span>
            </div>
            <!-- Auto-height container -->
            <div
                class="w-full relative bg-white flex flex-col"
                :style="{ height: iframeHeight + 'px' }"
            >
                <iframe
                    ref="iframeRef"
                    :srcdoc="srcdoc"
                    class="w-full flex-1 border-none bg-white text-black"
                    sandbox="allow-scripts allow-same-origin"
                ></iframe>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>
