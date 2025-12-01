export default defineAppConfig({
    docus: {
        title: 'kostyl.dev',
        description: 'Майбутній сайт по навчальним матеріалами по програмуванню (в розробці)',
        url: 'https://kostyl.dev',

        aside: {
            level: 1,
            collapsed: false,
            exclude: [],
        },

        header: {
            title: 'kostyl.dev',
            logo: true,
            showLinkIcon: true,
            fluid: true,
            toggle: {
                color: 'primary',
                variant: 'soft',
                class: 'rounded-full',
                icon: 'i-lucide-menu',
            },
        },

        footer: {
            credits: {
                text: 'Made with ❤️ by kostyl.dev',
                href: 'https://kostyl.dev',
            },
            textLinks: [
                {
                    text: 'GitHub',
                    href: 'https://github.com/arakviel',
                    target: '_blank',
                    rel: 'noopener',
                },
            ],
        },

        github: {
            owner: 'arakviel',
            repo: 'kostyl.dev',
            branch: 'main',
            edit: true,
        },
    },
    ui: {
        colors: {
            primary: 'blue',
            neutral: 'zinc',
        },
    },
    head: {
        link: [{ rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    },
})
