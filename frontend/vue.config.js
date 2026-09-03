const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  css: {
    // Vue 2 的 vue-loader 15 依赖 CommonJS 样式导出，避免新版 css-loader 的无效导出警告。
    loaderOptions: { css: { esModule: false } }
  },
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_TARGET || 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/media': {
        target: process.env.VUE_APP_API_TARGET || 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
