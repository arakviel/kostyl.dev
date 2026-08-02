export default defineNuxtConfig({
  extends: ['docus'],

  // Explicit: Docus/OG Image need useSiteConfig(); pnpm may not auto-register transitive module.
  modules: ['nuxt-site-config'],

  devtools: {
    enabled: true,
  },

  // Не сканувати/стежити за референс-додатками та службовими каталогами.
  // Інакше Vite/chokidar відкриває десятки тисяч файлів у projects/**/node_modules
  // і на macOS падає з EMFILE: too many open files, watch.
  // Не додавати сюди загальний '**/node_modules/**' — ламає шари модулів Nuxt.
  ignore: [
    'projects/**',
    'temp/**',
    'tests/**',
    'scripts/**',
    'screenshoter/**',
    'tools/**',
    // host source only; built assets live in public/rn-preview
    'tools/rn-preview/**',
    'answer_images/**',
    '**/.git/**',
  ],

  app: {
    baseURL: '/',
    buildAssetsDir: '/_nuxt/',
    head: {
      link: [{ rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    },
  },

  // nuxt-site-config / Docus SEO (useSiteConfig)
  site: {
    name: 'kostyl.dev',
    url: 'https://kostyl.dev',
    description: 'Навчальні матеріали з програмування',
    defaultLocale: 'uk',
  },

  nitro: {
    preset: 'github-pages',
    prerender: {
      routes: [],
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
            'php',
            // Shell/Script Languages
            'bash',
            'shell',
            'powershell',
            'docker',
            'dockerfile',
            // Data/Config Languages
            'json',
            'jsonc',
            'yaml',
            'xml',
            'toml',
            'ini',
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
            'http',
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
      watch: {
        // Подвійний захист: не вішати fs.watch на RN-проєкти та їхні node_modules
        ignored: [
          '**/node_modules/**',
          '**/projects/**',
          '**/temp/**',
          '**/tests/**',
          '**/scripts/**',
          '**/screenshoter/**',
          '**/tools/**',
          '**/.git/**',
          '**/.nuxt/**',
          '**/.output/**',
          '**/dist/**',
        ],
      },
    },
    // manualChunks через rollupOptions ламає CSS chunk refs у Vite 8/Rolldown
    // (entry-styles-1.mjs-!~{...}~.js не резолвиться під час Nitro prerender).
  },
})
