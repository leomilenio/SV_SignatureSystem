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
    
    // Inicializar correcciones de iconos
    this.initializeIconFixes()
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
    },
    
    initializeIconFixes() {
      console.log('🎨 Inicializando correcciones de iconos...')
      
      // Verificar si Material Icons está disponible
      this.checkMaterialIconsAvailability()
      
      // Aplicar CSS de corrección
      this.applyIconCSS()
      
      // Aplicar correcciones de tamaños
      this.applyIconSizeCorrections()
      
      // Verificar después de un delay
      setTimeout(() => {
        this.verifyIconsAfterLoad()
      }, 2000)
    },
    
    checkMaterialIconsAvailability() {
      if (document.fonts) {
        const materialIconsLoaded = document.fonts.check('1rem "Material Icons"')
        console.log('🔍 Material Icons disponible:', materialIconsLoaded)
        
        if (!materialIconsLoaded) {
          console.log('⚠️ Material Icons no cargado, intentando forzar carga...')
          this.forceLoadMaterialIcons()
        }
      }
    },
    
    forceLoadMaterialIcons() {
      // Crear enlace directo a Google Fonts si no existe
      const existingLink = document.querySelector('link[href*="material-icons"]')
      if (!existingLink) {
        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = 'https://fonts.googleapis.com/icon?family=Material+Icons&display=swap'
        link.onload = () => {
          console.log('✅ Material Icons cargado desde Google Fonts')
        }
        document.head.appendChild(link)
      }
    },
    
    applyIconCSS() {
      const css = `
        /* Corrección global para Material Icons - SIN interferir con tamaños */
        .material-icons, .q-icon {
          font-family: 'Material Icons' !important;
          font-weight: normal !important;
          font-style: normal !important;
          line-height: 1 !important;
          letter-spacing: normal !important;
          text-transform: none !important;
          display: inline-block !important;
          white-space: nowrap !important;
          word-wrap: normal !important;
          direction: ltr !important;
          font-feature-settings: 'liga' !important;
          -webkit-font-feature-settings: 'liga' !important;
          -webkit-font-smoothing: antialiased !important;
          -moz-osx-font-smoothing: grayscale !important;
          /* NO forzamos font-size para permitir que Quasar lo maneje */
        }
      `
      
      const style = document.createElement('style')
      style.textContent = css
      document.head.appendChild(style)
    },
    
    applyIconSizeCorrections() {
      // NO aplicar correcciones de tamaños que interfieran con Quasar
      console.log('⚠️ Saltando correcciones de tamaño para permitir que Quasar las maneje')
    },
    
    verifyIconsAfterLoad() {
      const iconElements = document.querySelectorAll('.q-icon')
      console.log(`🔍 Verificando ${iconElements.length} elementos de iconos...`)
      
      iconElements.forEach((element, index) => {
        const computedStyle = window.getComputedStyle(element)
        const fontFamily = computedStyle.fontFamily
        
        if (!fontFamily.includes('Material Icons')) {
          console.warn(`⚠️ Icono ${index} no usa Material Icons:`, fontFamily)
          element.style.fontFamily = '"Material Icons" !important'
        }
      })
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
