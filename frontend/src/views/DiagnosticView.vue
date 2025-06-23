<template>
  <div class="diagnostic-container">
    <div class="header">
      <h1>🔧 Diagnóstico y Solución de Iconos</h1>
      <p>Verificando el estado de los iconos Material Icons</p>
    </div>

    <div class="diagnostic-sections">
      <!-- Estado actual -->
      <div class="section">
        <h2>Estado Actual</h2>
        <div class="test-row">
          <span class="label">Icono dashboard:</span>
          <q-icon name="dashboard" size="2rem" class="test-icon" />
          <span class="icon-text">dashboard</span>
        </div>
        <div class="test-row">
          <span class="label">Icono play_circle_filled:</span>
          <q-icon name="play_circle_filled" size="2rem" class="test-icon" />
          <span class="icon-text">play_circle_filled</span>
        </div>
        <div class="test-row">
          <span class="label">Icono arrow_forward:</span>
          <q-icon name="arrow_forward" size="2rem" class="test-icon" />
          <span class="icon-text">arrow_forward</span>
        </div>
      </div>

      <!-- Pruebas directas -->
      <div class="section">
        <h2>Pruebas Directas Material Icons</h2>
        <div class="test-row">
          <span class="label">HTML directo:</span>
          <i class="material-icons test-icon">dashboard</i>
          <span class="icon-text">dashboard</span>
        </div>
        <div class="test-row">
          <span class="label">HTML directo:</span>
          <i class="material-icons test-icon">play_circle_filled</i>
          <span class="icon-text">play_circle_filled</span>
        </div>
        <div class="test-row">
          <span class="label">HTML directo:</span>
          <i class="material-icons test-icon">arrow_forward</i>
          <span class="icon-text">arrow_forward</span>
        </div>
      </div>

      <!-- Información del navegador -->
      <div class="section">
        <h2>Información del Navegador</h2>
        <div class="info-grid">
          <div class="info-item">
            <strong>Font Available:</strong>
            <span>{{ fontCheck.materialIcons ? '✅ Disponible' : '❌ No disponible' }}</span>
          </div>
          <div class="info-item">
            <strong>CSS Computed Style:</strong>
            <span>{{ computedFontFamily }}</span>
          </div>
          <div class="info-item">
            <strong>Document Fonts:</strong>
            <span>{{ documentFontsCount }} fuentes cargadas</span>
          </div>
        </div>
      </div>

      <!-- Acciones de corrección -->
      <div class="section">
        <h2>Acciones de Corrección</h2>
        <div class="actions">
          <q-btn 
            @click="forceReloadFonts"
            label="Recargar Fuentes"
            icon="refresh"
            color="primary"
            class="action-btn"
          />
          <q-btn 
            @click="applyIconFixes"
            label="Aplicar Correcciones CSS"
            icon="build"
            color="secondary"
            class="action-btn"
          />
          <q-btn 
            @click="testIconRendering"
            label="Probar Renderizado"
            icon="visibility"
            color="accent"
            class="action-btn"
          />
        </div>
      </div>

      <!-- Log de diagnóstico -->
      <div class="section">
        <h2>Log de Diagnóstico</h2>
        <div class="log-container">
          <div v-for="(log, index) in diagnosticLogs" :key="index" :class="['log-entry', log.type]">
            <span class="log-timestamp">{{ log.timestamp }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="footer">
      <q-btn 
        @click="$router.push('/')"
        label="Volver al Inicio"
        icon="home"
        color="primary"
        outline
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'

export default {
  name: 'DiagnosticView',
  setup() {
    const fontCheck = ref({})
    const computedFontFamily = ref('')
    const documentFontsCount = ref(0)
    const diagnosticLogs = ref([])

    const addLog = (message, type = 'info') => {
      diagnosticLogs.value.push({
        timestamp: new Date().toLocaleTimeString(),
        message,
        type
      })
    }

    const checkFontAvailability = () => {
      addLog('Verificando disponibilidad de fuentes...', 'info')
      
      // Método 1: Verificar si document.fonts existe
      if (document.fonts) {
        fontCheck.value.materialIcons = document.fonts.check('1em "Material Icons"')
        documentFontsCount.value = document.fonts.size
        addLog(`Document.fonts API disponible: ${document.fonts.size} fuentes`, 'success')
      } else {
        addLog('Document.fonts API no disponible', 'warning')
      }

      // Método 2: Verificar computed style
      const testElement = document.createElement('span')
      testElement.style.fontFamily = 'Material Icons'
      testElement.style.position = 'absolute'
      testElement.style.visibility = 'hidden'
      testElement.textContent = 'test'
      document.body.appendChild(testElement)
      
      computedFontFamily.value = window.getComputedStyle(testElement).fontFamily
      document.body.removeChild(testElement)
      
      addLog(`Computed font family: ${computedFontFamily.value}`, 'info')
    }

    const forceReloadFonts = async () => {
      addLog('Forzando recarga de fuentes...', 'info')
      
      try {
        // Eliminar CSS existente
        const existingLinks = document.querySelectorAll('link[href*="material-icons"], link[href*="fonts.googleapis.com"]')
        existingLinks.forEach(link => link.remove())

        // Agregar nuevamente los enlaces
        const linkElement = document.createElement('link')
        linkElement.rel = 'stylesheet'
        linkElement.href = 'https://fonts.googleapis.com/icon?family=Material+Icons&display=swap'
        linkElement.onload = () => {
          addLog('Fuentes recargadas exitosamente', 'success')
          setTimeout(checkFontAvailability, 500)
        }
        linkElement.onerror = () => {
          addLog('Error al recargar fuentes', 'error')
        }
        document.head.appendChild(linkElement)

      } catch (error) {
        addLog(`Error al recargar fuentes: ${error.message}`, 'error')
      }
    }

    const applyIconFixes = () => {
      addLog('Aplicando correcciones CSS...', 'info')
      
      const css = `
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
        }
      `
      
      const styleElement = document.createElement('style')
      styleElement.textContent = css
      document.head.appendChild(styleElement)
      
      addLog('Correcciones CSS aplicadas', 'success')
    }

    const testIconRendering = () => {
      addLog('Probando renderizado de iconos...', 'info')
      
      const testIcons = ['dashboard', 'play_circle_filled', 'arrow_forward']
      
      testIcons.forEach(iconName => {
        const element = document.createElement('i')
        element.className = 'material-icons'
        element.textContent = iconName
        element.style.position = 'absolute'
        element.style.left = '-9999px'
        document.body.appendChild(element)
        
        setTimeout(() => {
          const rect = element.getBoundingClientRect()
          const isRendered = rect.width > 0 && rect.height > 0
          addLog(`Icono ${iconName}: ${isRendered ? '✅ Renderizado' : '❌ No renderizado'}`, isRendered ? 'success' : 'error')
          document.body.removeChild(element)
        }, 100)
      })
    }

    onMounted(async () => {
      addLog('Iniciando diagnóstico de iconos...', 'info')
      
      await nextTick()
      setTimeout(() => {
        checkFontAvailability()
        testIconRendering()
      }, 1000)
    })

    return {
      fontCheck,
      computedFontFamily,
      documentFontsCount,
      diagnosticLogs,
      forceReloadFonts,
      applyIconFixes,
      testIconRendering
    }
  }
}
</script>

<style scoped>
.diagnostic-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
}

.header h1 {
  margin: 0 0 10px 0;
  font-size: 2rem;
}

.header p {
  margin: 0;
  opacity: 0.9;
}

.diagnostic-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.section h2 {
  margin: 0 0 15px 0;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 5px;
}

.test-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.label {
  min-width: 150px;
  font-weight: 500;
}

.test-icon {
  color: #667eea;
  background: white;
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.icon-text {
  font-family: monospace;
  background: #ffe6e6;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.8rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.info-item {
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #667eea;
}

.actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.action-btn {
  min-width: 150px;
}

.log-container {
  max-height: 300px;
  overflow-y: auto;
  background: #f8f9fa;
  border-radius: 6px;
  padding: 10px;
}

.log-entry {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
  padding: 6px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.log-entry.info {
  background: #e3f2fd;
  color: #1565c0;
}

.log-entry.success {
  background: #e8f5e8;
  color: #2e7d32;
}

.log-entry.warning {
  background: #fff3e0;
  color: #ef6c00;
}

.log-entry.error {
  background: #ffebee;
  color: #c62828;
}

.log-timestamp {
  font-family: monospace;
  font-size: 0.8rem;
  opacity: 0.7;
  min-width: 80px;
}

.footer {
  margin-top: 30px;
  text-align: center;
}

/* Dark mode */
.body--dark .section {
  background: #1e1e1e;
  border-color: #333;
}

.body--dark .section h2 {
  color: #e0e0e0;
}

.body--dark .test-row,
.body--dark .info-item,
.body--dark .log-container {
  background: #2a2a2a;
}

@media (max-width: 768px) {
  .actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
  
  .test-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
