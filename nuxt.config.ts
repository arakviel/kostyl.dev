export default defineNuxtConfig({
    extends: ['docus'],

    devtools: {
        enabled: true,
    },

    app: {
        baseURL: '/',
        buildAssetsDir: '/_nuxt/',
        head: {
            link: [{ rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
        },
    },

    site: {
        name: 'kostyl.dev',
    },

    nitro: {
        preset: 'github-pages',
        prerender: {
            routes: [
                '/_ipx/_/images/se/domain-analysis.png',
                '/_ipx/_/images/se/subdomains-types.png',
                '/_ipx/_/images/se/subdomains-types-levels.png',
                '/_ipx/_/images/se/knowledge-crunching.png',
                '/_ipx/_/images/se/ubiquitous-language.png',
                '/_ipx/_/images/se/map-model.png',
                '/_ipx/_/images/se/leads-process.png',
                '/_ipx/_/images/se/bounded-context.png',
                '/_ipx/_/images/se/core-subdomain.png',
                '/_ipx/_/images/se/generic-subdomain.png',
                '/_ipx/_/images/se/supporting-subdomain.png',
            ],
        },
    },

    css: [
        '~/assets/css/content-images.css',
        '~/assets/css/code-line-numbers.css',
        '~/assets/css/content-width.css',
        '~/assets/css/zen-mode.css',
    ],

    content: {
        markdown: {
            tags: {
                'code-block': 'CodeBlock',
                callout: 'Callout',
                mermaid: 'Mermaid',
            },
        },
        build: {
            markdown: {
                highlight: {
                    theme: {
                        default: 'dark-plus',
                        dark: 'dark-plus',
                        light: 'light-plus',
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

    icon: {
        serverBundle: 'auto',
        fetchTimeout: 5000,
    },

    vite: {
        server: {
            allowedHosts: ['865fb62d150c.ngrok-free.app'],
        },
    },
})
