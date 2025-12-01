export default defineNuxtConfig({
    extends: ['docus'],

    devtools: {
        enabled: true,
    },

    app: {
        baseURL: '/kostyl.dev/', // Default GitHub Pages URL: https://arakviel.github.io/kostyl.dev/
        buildAssetsDir: '/_nuxt/',
    },

    nitro: {
        preset: 'github-pages',
    },

    css: ['~/assets/css/content-images.css', '~/assets/css/code-line-numbers.css', '~/assets/css/content-width.css'],

    content: {
        build: {
            markdown: {
                highlight: {
                    theme: {
                        default: 'light-plus',
                        dark: 'dark-plus',
                    },
                    langs: [
                        // .NET Languages
                        'csharp',
                        'fsharp',
                        'vb',
                        // Web Languages
                        'typescript',
                        'javascript',
                        'html',
                        'css',
                        'vue',
                        // Shell/Script Languages
                        'bash',
                        'shell',
                        'powershell',
                        // Data/Config Languages
                        'json',
                        'yaml',
                        'xml',
                        'toml',
                        // Other Programming Languages
                        'cpp',
                        'c',
                        'java',
                        'python',
                        'rust',
                        'go',
                        'asm',
                        // Markup/Documentation
                        'markdown',
                        // Database
                        'sql',
                        // Utility
                        'diff',
                    ],
                },
            },
        },
    },

    compatibilityDate: '2025-01-26',

    vite: {
        server: {
            allowedHosts: ['865fb62d150c.ngrok-free.app'],
        },
    },
})
