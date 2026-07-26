declare module 'react-native' {
  export * from 'react-native-web'
}

declare module '@babel/standalone' {
  interface TransformOptions {
    filename?: string
    presets?: unknown[]
    plugins?: unknown[]
    sourceType?: string
    compact?: boolean
  }
  interface TransformResult {
    code: string | null
  }
  const Babel: {
    transform(code: string, options?: TransformOptions): TransformResult
  }
  export default Babel
}
