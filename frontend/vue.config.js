const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false, // Deshabilitar ESLint durante el desarrollo
  devServer: {
    port: 8080,
    host: '0.0.0.0', // Permitir acceso desde cualquier IP de la red local
    allowedHosts: 'all', // Permitir todos los hosts
    client: {
      webSocketURL: 'auto://0.0.0.0:0/ws' // Auto-detectar WebSocket URL
    }
  },
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_OPTIONS_API__: JSON.stringify(true),
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false),
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false)
      })
    ]
  }
})
