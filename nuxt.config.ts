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
                '/_ipx/_/images/se/transaction-script.png',
                '/_ipx/_/images/se/distributed-transaction.png',
                '/_ipx/_/images/se/etl-process.png',
                '/_ipx/_/images/se/active-record.png',
                '/_ipx/_/images/se/bounded-context-size.png',
                '/_ipx/_/images/se/subdomains-vs-bounded-contexts.png',
                '/_ipx/_/images/se/subdomains-bounded-contexts-interaction-1.jpg',
                '/_ipx/_/images/se/subdomains-bounded-contexts-interaction-2.jpg',
                '/_ipx/_/images/se/ownership-boundary.jpg',
                '/_ipx/_/images/se/fridge-box-model.jpg',
                '/_ipx/_/images/se/fridge-doorway-model.jpg',
                '/_ipx/_/images/se/partnership-pattern.jpg',
                '/_ipx/_/images/se/shared-kernel-pattern.jpg',
                '/_ipx/_/images/se/conformist-pattern.jpg',
                '/_ipx/_/images/se/anticorruption-layer-pattern.jpg',
                '/_ipx/_/images/se/open-host-service-pattern.jpg',
                '/_ipx/_/images/se/context-map.jpg',
                '/_ipx/_/images/se/complex-context-map.jpg',
                '/_ipx/_/images/se/entity-identity.png',
                '/_ipx/_/images/se/aggregate-hierarchy.png',
                '/_ipx/_/images/se/aggregates-references.png',
                '/_ipx/_/images/se/aggregate-root.png',
                '/_ipx/_/images/se/domain-events-interaction.png',
                '/_ipx/_/images/se/event-sourced-aggregate.png',
                '/_ipx/_/images/se/event-store-segmentation.png',
                '/_ipx/_/images/se/layered-architecture.png',
                '/_ipx/_/images/se/presentation-layer.png',
                '/_ipx/_/images/se/business-logic-layer.png',
                '/_ipx/_/images/se/data-access-layer.png',
                '/_ipx/_/images/se/layered-architecture-communication.png',
                '/_ipx/_/images/se/service-layer-orchestration.png',
                '/_ipx/_/images/se/layers-vs-tiers.png',
                '/_ipx/_/images/se/37.png',
                '/_ipx/_/images/se/inverted-dependencies.png',
                '/_ipx/_/images/se/ports-and-adapters-architecture.png',
                '/_ipx/_/images/se/ports-and-adapters-integration.png',
                '/_ipx/_/images/se/cqrs-projections.png',
                '/_ipx/_/images/se/42.png',
                '/_ipx/_/images/se/asynchronous-projections.png',
                '/_ipx/_/images/se/context-modularity.png',
                '/_ipx/_/images/se/modular-monolith-context.png',
                '/_ipx/_/images/se/stateless-model-transformation.png',
                '/_ipx/_/images/se/synchronous-model-transformation.png',
                '/_ipx/_/images/se/api-gateway-versioning.png',
                '/_ipx/_/images/se/interchange-context.png',
                '/_ipx/_/images/se/asynchronous-model-transformation.png',
                '/_ipx/_/images/se/public-vs-private-events.png',
                '/_ipx/_/images/se/stateless-aggregation.png',
                '/_ipx/_/images/se/message-aggregation.png',
                '/_ipx/_/images/se/stateful-model-transformation.png',
                '/_ipx/_/images/se/backend-for-frontend-aggregation.png',
                '/_ipx/_/images/se/outbox-pattern.png',
                '/_ipx/_/images/se/sql-outbox-implementation.png',
                '/_ipx/_/images/se/saga-pattern.png',
                '/_ipx/_/images/se/process-manager-vs-saga.png',
                '/_ipx/_/images/se/booking-process-manager.png',
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
                        'jsx',
                        'tsx',
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
