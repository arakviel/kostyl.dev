<script setup>
// Рамка для поглибленого матеріалу лекції: поза програмою модуля,
// не входить у тести й домашні. Використання в Markdown:
//   ::deep-dive
//   ### Заголовок підрозділу
//   текст...
//   ::
</script>

<template>
    <section class="deep-dive my-8 rounded-xl border-2 border-violet-400/70 dark:border-violet-500/60 bg-violet-50/50 dark:bg-violet-950/20 px-5 pt-3 pb-2">
        <div class="not-prose flex flex-wrap items-center gap-x-2 gap-y-1 text-sm select-none">
            <span class="inline-flex items-center gap-1.5 rounded-md bg-violet-600 dark:bg-violet-500 px-2 py-0.5 font-semibold text-white">
                <UIcon name="i-lucide-telescope" class="size-4" />
                Поглиблено
            </span>
        </div>
        <div class="deep-dive-body">
            <slot />
        </div>
    </section>
</template>

<style scoped>
.deep-dive-body > :deep(:first-child) {
    margin-top: 0.75rem;
}
.deep-dive-body > :deep(:last-child) {
    margin-bottom: 0.5rem;
}
</style>
