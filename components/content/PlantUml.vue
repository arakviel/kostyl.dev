<template>
    <div class="plantuml-wrapper" :class="{ loading: loading }">
        <div v-if="loading" class="plantuml-loading">
            <span>Loading diagram...</span>
        </div>
        <div v-if="error" class="plantuml-error">
            <div class="error-title">PlantUML Render Error</div>
            <pre>{{ error }}</pre>
            <div class="source-code">
                <pre>{{ sourceCode }}</pre>
            </div>
        </div>
        <div v-show="!loading && !error" class="plantuml-diagram">
            <img v-if="imageUrl" :src="imageUrl" :alt="altText" />
        </div>
        <div ref="source" style="display: none">
            <slot />
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, nextTick } from 'vue'
    import { encode } from 'plantuml-encoder'

    const props = defineProps({
        server: {
            type: String,
            default: 'https://www.plantuml.com/plantuml',
        },
        format: {
            type: String,
            default: 'svg', // svg, png, txt
            validator: (value) => ['svg', 'png', 'txt'].includes(value),
        },
        alt: {
            type: String,
            default: 'PlantUML Diagram',
        },
    })

    const source = ref(null)
    const imageUrl = ref('')
    const error = ref('')
    const loading = ref(true)
    const sourceCode = ref('')
    const altText = ref(props.alt)

    // Функція для "розумного" витягування тексту (аналогічно Mermaid)
    const extractTextWithNewlines = (element) => {
        if (!element) return ''

        const clone = element.cloneNode(true)

        // Видаляємо сміття від Docus
        const buttons = clone.querySelectorAll('button, .iconify')
        buttons.forEach((b) => b.remove())

        // Додаємо перенос рядка після кожного блочного елемента
        const blockTags = ['p', 'div', 'pre', 'br', 'li', 'tr']
        blockTags.forEach((tag) => {
            const elements = clone.querySelectorAll(tag)
            elements.forEach((el) => {
                el.after(document.createTextNode('\n'))
            })
        })

        return clone.textContent || ''
    }

    onMounted(async () => {
        await nextTick()

        try {
            if (source.value) {
                // Витягуємо PlantUML код
                let code = extractTextWithNewlines(source.value)

                // Декодуємо HTML сутності
                const txt = document.createElement('textarea')
                txt.innerHTML = code
                code = txt.value

                code = code.trim()
                sourceCode.value = code

                if (!code) {
                    loading.value = false
                    return
                }

                // Кодуємо PlantUML код в URL-безпечний формат
                const encoded = encode(code)

                // Генеруємо URL для зображення
                imageUrl.value = `${props.server}/${props.format}/${encoded}`

                loading.value = false
            }
        } catch (e) {
            console.error('PlantUML render error:', e)
            error.value = e.message + '\n(Check the Source Code below to see what text was extracted)'
            loading.value = false
        }
    })
</script>

<style scoped>
    .plantuml-wrapper {
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

    .plantuml-loading {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        color: var(--color-gray-500);
    }

    .plantuml-diagram {
        width: 100%;
        text-align: center;
        overflow-x: auto;
        padding: 1rem;
    }

    .plantuml-diagram img {
        max-width: 100%;
        height: auto;
        display: inline-block;
    }

    .plantuml-error {
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
