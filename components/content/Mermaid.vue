<template>
    <div class="mermaid-wrapper" :class="{ loading: loading }">
        <div v-if="loading" class="mermaid-loading">
            <span>Loading diagram...</span>
        </div>
        <div v-if="error" class="mermaid-error">
            <div class="error-title">Mermaid Render Error</div>
            <pre>{{ error }}</pre>
            <div class="source-code">
                <pre>{{ sourceCode }}</pre>
            </div>
        </div>
        <div v-show="!loading && !error" ref="container" class="mermaid-diagram" v-html="renderedSvg"></div>
        <div ref="source" style="display: none">
            <slot />
        </div>
    </div>
</template>

<script setup>
    import mermaid from 'mermaid'
    import { ref, onMounted, nextTick } from 'vue'

    const source = ref(null)
    const container = ref(null)
    const renderedSvg = ref('')
    const error = ref('')
    const loading = ref(true)
    const sourceCode = ref('')

    // Функція для "розумного" витягування тексту
    const extractTextWithNewlines = (element) => {
        if (!element) return ''

        // Клонуємо елемент, щоб не ламати DOM
        const clone = element.cloneNode(true)

        // 1. Видаляємо сміття від Docus (кнопки копіювання і т.д.)
        const buttons = clone.querySelectorAll('button, .iconify')
        buttons.forEach((b) => b.remove())

        // 2. Додаємо перенос рядка після кожного блочного елемента
        // Це критично, бо innerText/textContent ігнорують теги
        const blockTags = ['p', 'div', 'pre', 'br', 'li', 'tr']
        blockTags.forEach((tag) => {
            const elements = clone.querySelectorAll(tag)
            elements.forEach((el) => {
                el.after(document.createTextNode('\n'))
            })
        })

        // 3. Беремо чистий текст
        return clone.textContent || ''
    }

    onMounted(async () => {
        await nextTick()

        try {
            mermaid.initialize({
                startOnLoad: false,
                theme: 'dark',
                securityLevel: 'loose',
                fontFamily: 'inherit',
            })

            if (source.value) {
                // Використовуємо нову функцію очистки
                let code = extractTextWithNewlines(source.value)

                // Декодуємо HTML сутності (якщо &gt; замість >)
                const txt = document.createElement('textarea')
                txt.innerHTML = code
                code = txt.value

                code = code.trim()
                sourceCode.value = code // Для дебагу покажемо, що ми витягли

                if (!code) {
                    loading.value = false
                    return
                }

                const id = 'mermaid-' + Math.random().toString(36).substr(2, 9)

                // Рендер
                const { svg } = await mermaid.render(id, code)
                renderedSvg.value = svg
                loading.value = false
            }
        } catch (e) {
            console.error('Mermaid render error:', e)
            error.value = e.message + '\n(Check the Source Code below to see what text was extracted)'
            loading.value = false
        }
    })
</script>

<style scoped>
    .mermaid-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 2rem 0;
        width: 100%;
        min-height: 100px;
        background: rgba(0, 0, 0, 0.02);
        border-radius: 0.5rem;
    }

    .mermaid-loading {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        color: var(--color-gray-500);
    }

    .mermaid-diagram {
        width: 100%;
        text-align: center;
        overflow-x: auto;
    }

    .mermaid-diagram :deep(svg) {
        max-width: 100%;
        height: auto;
    }

    .mermaid-error {
        width: 100%;
        color: #ef4444;
        padding: 1rem;
        border: 1px solid #ef4444;
        border-radius: 0.5rem;
        background-color: rgba(239, 68, 68, 0.1);
        text-align: left;
        font-size: 0.875rem;
    }

    .error-title {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .source-code {
        margin-top: 1rem;
        opacity: 0.8;
    }
</style>
