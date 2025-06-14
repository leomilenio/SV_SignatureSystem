<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import backendDetector from './services/backendDetector'

export default {
  name: 'App',
  mounted() {
    // Configuración global de la aplicación
    console.log('🎬 Pochtecayotl Signance System - Frontend iniciado')
    
    // Verificar conectividad con el backend usando auto-detección
    this.checkBackendConnection()
  },
  methods: {
    async checkBackendConnection() {
      try {
        // Intentar detectar el backend automáticamente
        const backendInfo = await backendDetector.detectBackend()
        console.log(`✅ Conexión con backend establecida en ${backendInfo.baseUrl}`)
      } catch (error) {
        console.error('❌ No se puede conectar con el backend:', error)
        this.$q.notify({
          type: 'warning',
          message: 'No se puede conectar con el servidor',
          caption: 'Verifica que el backend esté ejecutándose en el rango de puertos 8000-8010'
        })
      }
    }
  }
}
</script>

<style>
#app {
  font-family: 'Roboto', -apple-system, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  margin: 0;
  padding: 0;
}

/* Estilos globales para el sistema */
.signance-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.signance-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin-bottom: 20px;
}

.signance-header {
  background: linear-gradient(135deg, #000000 0%, #784F17 10%, #E70000 25%, #FF8C00 40%, #FFEF00 55%, #00811F 70%, #00A7E4 85%, #760089 100%);
  color: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

/* Responsivo */
@media (max-width: 768px) {
  .signance-container {
    padding: 10px;
  }
  
  .signance-card {
    padding: 16px;
    margin-bottom: 15px;
  }
}
</style>
