# React Native Preview Host

WebAssembly-style host for the Nuxt component `ReactNativePreview.vue`.

Renders course snippets with **React + react-native-web** inside an iframe.
JSX/TSX from markdown is transformed in the browser via **@babel/standalone**.

## Build

```bash
cd tools/rn-preview
pnpm install
pnpm build
```

Output: `public/rn-preview/` (served as `/rn-preview/`).

## Protocol (postMessage)

Parent → iframe:

| type | payload |
|------|---------|
| `ping` | `{ id? }` |
| `run-code` | `{ id?, code, theme?: 'light'\|'dark' }` |
| `set-theme` | `{ id?, theme }` |

iframe → parent:

| type | payload |
|------|---------|
| `rn-preview-ready` | `{ id? }` |
| `rn-preview-pong` | `{ id? }` |
| `rn-preview-success` | `{ id? }` |
| `rn-preview-error` | `{ id?, message }` |

## Supported imports in snippets

- `react`
- `react-native` / `react-native-web`
- `react/jsx-runtime` (automatic JSX)
- `react-dom` / `react-dom/client`

Snippets should **export default** a component, or define a PascalCase component
(`App`, `Example`, `Demo`, or the first `function Foo` / `const Foo =`) — the host
will inject `export default` when missing.
