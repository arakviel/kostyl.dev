<script setup lang="ts">
    import { onMounted, computed } from 'vue'

    const props = defineProps({
        id: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            default: 'Tally Form',
        },
        height: {
            type: [Number, String],
            default: 500,
        },
        transparency: {
            type: Boolean,
            default: false,
        },
    })

    const embedUrl = computed(() => {
        return `https://tally.so/embed/${props.id}?alignLeft=1&hideTitle=1&transparentBackground=${
            props.transparency ? '1' : '0'
        }&dynamicHeight=1`
    })

    onMounted(() => {
        const scriptUrl = 'https://tally.so/widgets/embed.js'

        const loadEmbeds = () => {
            if (typeof (window as any).Tally !== 'undefined') {
                ;(window as any).Tally.loadEmbeds()
            } else {
                document.querySelectorAll('iframe[data-tally-src]:not([src])').forEach((e: any) => {
                    e.src = e.dataset.tallySrc
                })
            }
        }

        if (document.querySelector(`script[src="${scriptUrl}"]`) === null) {
            const s = document.createElement('script')
            s.src = scriptUrl
            s.onload = loadEmbeds
            s.onerror = loadEmbeds
            document.body.appendChild(s)
        } else {
            loadEmbeds()
        }
    })
</script>

<template>
    <div class="tally-embed-container">
        <iframe
            :data-tally-src="embedUrl"
            loading="lazy"
            width="100%"
            :height="height"
            frameborder="0"
            marginheight="0"
            marginwidth="0"
            :title="title"
        ></iframe>
    </div>
</template>

<style scoped>
    .tally-embed-container {
        width: 100%;
        margin: 2rem 0;
    }
</style>
