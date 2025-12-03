export const useZenMode = () => {
    const isZenMode = useState<boolean>('zenMode', () => false)

    // Restore zen mode state from localStorage on client-side
    if (process.client) {
        onMounted(() => {
            const savedState = localStorage.getItem('zenMode')
            if (savedState !== null) {
                isZenMode.value = savedState === 'true'
            }
            updateBodyClass(isZenMode.value)
        })
    }

    // Update body class when zen mode changes
    watch(isZenMode, (newValue) => {
        if (process.client) {
            localStorage.setItem('zenMode', String(newValue))
            updateBodyClass(newValue)
        }
    })

    const updateBodyClass = (enabled: boolean) => {
        if (enabled) {
            document.body.classList.add('zen-mode')
        } else {
            document.body.classList.remove('zen-mode')
        }
    }

    const toggleZenMode = () => {
        isZenMode.value = !isZenMode.value
    }

    return {
        isZenMode: readonly(isZenMode),
        toggleZenMode,
    }
}
