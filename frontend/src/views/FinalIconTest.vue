<template>
  <div class="final-test-container">
    <div class="header">
      <h1>🎯 Prueba Final de Iconos</h1>
      <p>Verificación completa del sistema de iconos Material Icons</p>
    </div>

    <!-- Estado actual -->
    <div class="status-section">
      <div class="status-card" :class="iconStatus.overall">
        <h2>Estado General: {{ iconStatus.message }}</h2>
        <div class="status-details">
          <div>✅ Fuentes cargadas: {{ debugInfo.fontsAPI?.size || 'N/A' }}</div>
          <div>{{ debugInfo.fontsAPI?.materialIconsCheck ? '✅' : '❌' }} Material Icons disponible</div>
          <div>{{ materialIconsLinks.length > 0 ? '✅' : '❌' }} Enlaces de fuentes: {{ materialIconsLinks.length }}</div>
        </div>
      </div>
    </div>

    <!-- Pruebas de iconos principales -->
    <div class="main-tests">
      <h2>🧪 Pruebas de Iconos Principales</h2>
      <div class="icon-tests-grid">
        <div v-for="test in iconTests" :key="test.name" class="icon-test-card">
          <div class="test-header">
            <h3>{{ test.name }}</h3>
            <span :class="['status-badge', test.status]">{{ test.status }}</span>
          </div>
          
          <div class="test-content">
            <div class="icon-display">
              <q-icon :name="test.iconName" size="3rem" :color="test.status === 'success' ? 'positive' : 'negative'" />
            </div>
            <div class="icon-info">
              <p><strong>Código:</strong> <code>{{ test.iconName }}</code></p>
              <p><strong>Componente:</strong> <code>&lt;q-icon name="{{ test.iconName }}" /&gt;</code></p>
              <p v-if="test.availability !== undefined"><strong>Disponible:</strong> {{ test.availability ? 'Sí' : 'No' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Acciones de corrección -->
    <div class="actions-section">
      <h2>🔧 Acciones de Corrección</h2>
      <div class="actions-grid">
        <q-btn 
          @click="runFullTest"
          label="Ejecutar Prueba Completa"
          icon="play_arrow"
          color="primary"
          size="lg"
          :loading="testRunning"
        />
        <q-btn 
          @click="forceReloadIcons"
          label="Recargar Iconos"
          icon="refresh"
          color="secondary"
          size="lg"
        />
        <q-btn 
          @click="exportDebugReport"
          label="Exportar Reporte"
          icon="download"
          color="accent"
          size="lg"
        />
      </div>
    </div>

    <!-- Log en tiempo real -->
    <div class="log-section">
      <h2>📋 Log de Diagnóstico</h2>
      <div class="log-container">
        <div v-for="(log, index) in logs" :key="index" :class="['log-entry', log.type]">
          <span class="log-time">{{ log.time }}</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
      </div>
    </div>

    <!-- Información técnica detallada -->
    <div class="technical-section">
      <q-expansion-item label="🔍 Información Técnica Detallada" icon="info">
        <div class="tech-content">
          <h3>Debug Info</h3>
          <pre>{{ JSON.stringify(debugInfo, null, 2) }}</pre>
        </div>
      </q-expansion-item>
    </div>

    <!-- Navegación -->
    <div class="navigation">
      <q-btn 
        @click="$router.push('/')"
        label="Ir al Inicio"
        icon="home"
        color="primary"
        outline
      />
      <q-btn 
        @click="openMainApp"
        label="Abrir Aplicación"
        icon="launch"
        color="positive"
        :disable="iconStatus.overall !== 'success'"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { checkIconAvailability, getIconDebugInfo } from '../utils/iconUtils'

export default {
  name: 'FinalIconTest',
  setup() {
    const router = useRouter()
    const testRunning = ref(false)
    const logs = ref([])
    const debugInfo = ref({})
    const materialIconsLinks = ref([])
    
    const iconStatus = reactive({
      overall: 'pending',
      message: 'Ejecutando pruebas...'
    })

    const iconTests = ref([
      { name: 'Dashboard', iconName: 'dashboard', status: 'pending' },
      { name: 'Reproducir', iconName: 'play_circle_filled', status: 'pending' },
      { name: 'Siguiente', iconName: 'arrow_forward', status: 'pending' },
      { name: 'Configuración', iconName: 'settings', status: 'pending' },
      { name: 'Video', iconName: 'video_library', status: 'pending' },
      { name: 'Subir', iconName: 'cloud_upload', status: 'pending' }
    ])

    const addLog = (message, type = 'info') => {
      logs.value.unshift({
        time: new Date().toLocaleTimeString(),
        message,
        type
      })
      
      // Mantener solo los últimos 20 logs
      if (logs.value.length > 20) {
        logs.value = logs.value.slice(0, 20)
      }
    }

    const runFullTest = async () => {
      testRunning.value = true
      addLog('Iniciando prueba completa de iconos...', 'info')
      
      try {
        // Obtener información de debug
        debugInfo.value = getIconDebugInfo()
        addLog('Información de debug obtenida', 'success')
        
        // Buscar enlaces de Material Icons
        materialIconsLinks.value = debugInfo.value.materialIconsLinks || []
        addLog(`Encontrados ${materialIconsLinks.value.length} enlaces de Material Icons`, 'info')
        
        // Probar cada icono
        let successCount = 0
        for (const test of iconTests.value) {
          addLog(`Probando icono: ${test.iconName}`, 'info')
          
          try {
            const isAvailable = await checkIconAvailability(test.iconName)
            test.availability = isAvailable
            test.status = isAvailable ? 'success' : 'error'
            
            if (isAvailable) {
              successCount++
              addLog(`✅ ${test.iconName} disponible`, 'success')
            } else {
              addLog(`❌ ${test.iconName} no disponible`, 'error')
            }
          } catch (error) {
            test.status = 'error'
            addLog(`Error probando ${test.iconName}: ${error.message}`, 'error')
          }
        }
        
        // Determinar estado general
        const totalTests = iconTests.value.length
        const successRate = successCount / totalTests
        
        if (successRate >= 0.8) {
          iconStatus.overall = 'success'
          iconStatus.message = `Excelente! ${successCount}/${totalTests} iconos funcionando`
          addLog('🎉 Sistema de iconos funcionando correctamente', 'success')
        } else if (successRate >= 0.5) {
          iconStatus.overall = 'warning'
          iconStatus.message = `Parcial: ${successCount}/${totalTests} iconos funcionando`
          addLog('⚠️ Algunos iconos no cargan correctamente', 'warning')
        } else {
          iconStatus.overall = 'error'
          iconStatus.message = `Problemas: solo ${successCount}/${totalTests} iconos funcionando`
          addLog('❌ Sistema de iconos tiene problemas significativos', 'error')
        }
        
      } catch (error) {
        iconStatus.overall = 'error'
        iconStatus.message = 'Error durante las pruebas'
        addLog(`Error en prueba completa: ${error.message}`, 'error')
      } finally {
        testRunning.value = false
      }
    }

    const forceReloadIcons = () => {
      addLog('Forzando recarga de iconos...', 'info')
      
      // Recargar la página para aplicar todas las correcciones
      setTimeout(() => {
        window.location.reload()
      }, 1000)
    }

    const exportDebugReport = () => {
      const report = {
        timestamp: new Date().toISOString(),
        iconStatus: iconStatus,
        iconTests: iconTests.value,
        debugInfo: debugInfo.value,
        logs: logs.value,
        userAgent: navigator.userAgent,
        url: window.location.href
      }
      
      const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `icon-debug-report-${new Date().getTime()}.json`
      link.click()
      
      URL.revokeObjectURL(url)
      addLog('Reporte de debug exportado', 'success')
    }

    const openMainApp = () => {
      router.push('/admin')
    }

    onMounted(() => {
      addLog('Página de prueba final cargada', 'info')
      setTimeout(() => {
        runFullTest()
      }, 1000)
    })

    return {
      testRunning,
      logs,
      debugInfo,
      materialIconsLinks,
      iconStatus,
      iconTests,
      runFullTest,
      forceReloadIcons,
      exportDebugReport,
      openMainApp
    }
  }
}
</script>

<style scoped>
.final-test-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  background: #f5f5f5;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px;
}

.status-section {
  margin-bottom: 30px;
}

.status-card {
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.status-card.success {
  background: linear-gradient(135deg, #4caf50 0%, #81c784 100%);
  color: white;
}

.status-card.warning {
  background: linear-gradient(135deg, #ff9800 0%, #ffb74d 100%);
  color: white;
}

.status-card.error {
  background: linear-gradient(135deg, #f44336 0%, #e57373 100%);
  color: white;
}

.status-card.pending {
  background: linear-gradient(135deg, #2196f3 0%, #64b5f6 100%);
  color: white;
}

.status-details {
  display: flex;
  justify-content: space-around;
  margin-top: 15px;
  font-size: 0.9rem;
}

.main-tests {
  margin-bottom: 30px;
}

.icon-tests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.icon-test-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border: 1px solid #e0e0e0;
}

.test-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.status-badge.success {
  background: #4caf50;
  color: white;
}

.status-badge.error {
  background: #f44336;
  color: white;
}

.status-badge.pending {
  background: #2196f3;
  color: white;
}

.test-content {
  display: flex;
  gap: 20px;
  align-items: center;
}

.icon-display {
  flex-shrink: 0;
}

.icon-info {
  flex: 1;
}

.icon-info code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.actions-section, .log-section {
  margin-bottom: 30px;
}

.actions-grid {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.log-container {
  background: white;
  border-radius: 8px;
  padding: 15px;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
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

.log-time {
  font-family: monospace;
  font-size: 0.8rem;
  opacity: 0.7;
  min-width: 80px;
}

.technical-section {
  margin-bottom: 30px;
}

.tech-content {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}

.tech-content pre {
  background: white;
  padding: 15px;
  border-radius: 6px;
  overflow: auto;
  font-size: 0.8rem;
  border: 1px solid #e0e0e0;
}

.navigation {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 30px;
}

@media (max-width: 768px) {
  .test-content {
    flex-direction: column;
    text-align: center;
  }
  
  .actions-grid {
    flex-direction: column;
    align-items: center;
  }
  
  .status-details {
    flex-direction: column;
    gap: 5px;
  }
}
</style>
