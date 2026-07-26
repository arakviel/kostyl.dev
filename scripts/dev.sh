#!/usr/bin/env sh
# Raise file-descriptor soft limit when the OS allows it (fixes EMFILE on macOS
# when Nuxt/Vite watch many files). Then start Nuxt.
# Heavy monorepo dirs are also ignored in nuxt.config.ts (projects/**, etc.).
#
# Large @nuxt/content corpora can push the default ~4GB V8 heap — raise it for dev.
ulimit -n 65536 2>/dev/null || true
cd "$(dirname "$0")/.." || exit 1
export NODE_OPTIONS="${NODE_OPTIONS:+$NODE_OPTIONS }--max-old-space-size=8192"
exec node ./node_modules/nuxt/bin/nuxt.mjs dev "$@"
