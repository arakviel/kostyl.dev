export default defineAppConfig({
    docus: {
        title: 'kostyl.dev',
        description: 'Фундаментальне навчання програмуванню від А до Я',
        url: 'https://kostyl.dev',

        aside: {
            level: 1,
            collapsed: false,
            exclude: [],
        },

        header: {
            title: 'kostyl.dev',
            logo: false,
            showLinkIcon: true,
            fluid: true,
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
})
