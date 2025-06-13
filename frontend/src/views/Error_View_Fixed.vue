<template>
  <div class="error-container">
    <!-- Theme Toggle -->
    <ThemeToggle class="theme-toggle" />
    
    <div class="signance-container">
      <!-- Header de error -->
      <div class="error-header">
        <div class="error-icon">
          <q-icon name="error" size="5rem" />
        </div>
        <h2>¡Oops! Algo salió mal</h2>
        <p>Pochtecayotl Signance System - Página de Error</p>
      </div>

      <!-- Información del error -->
      <div class="info-card error-info">
        <div class="card-header">
          <q-icon name="bug_report" size="2rem" />
          <div class="header-text">
            <h3>Error del Sistema</h3>
            <p>Detalles técnicos del problema</p>
          </div>
        </div>

        <div class="error-details">
          <div class="error-badge">
            <q-chip color="negative" text-color="white" icon="error">
              Código: {{ errorCode }}
            </q-chip>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Mensaje:</span>
            <span class="detail-value">{{ errorMessage }}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Timestamp:</span>
            <span class="detail-value">{{ new Date().toLocaleString('es-ES') }}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">URL:</span>
            <span class="detail-value">{{ currentUrl }}</span>
          </div>
        </div>
      </div>

      <!-- Diagnóstico del sistema -->
      <div class="info-card diagnostic-card">
        <div class="card-title">
          <h3>Diagnóstico del Sistema</h3>
        </div>
        
        <div class="diagnostic-grid">
          <div 
            v-for="check in diagnosticChecks" 
            :key="check.name"
            class="diagnostic-item"
            :class="{ 
              'diagnostic-ok': check.status === 'ok',
              'diagnostic-error': check.status === 'error',
              'diagnostic-checking': check.checking
            }"
          >
            <div class="diagnostic-icon">
              <q-icon 
                :name="check.status === 'ok' ? 'check_circle' : check.status === 'error' ? 'error' : 'help'"
                size="1.5rem"
              />
            </div>
            
            <div class="diagnostic-info">
              <h4>{{ check.name }}</h4>
              <p>{{ check.description }}</p>
              <p v-if="check.details" class="diagnostic-details">{{ check.details }}</p>
            </div>
            
            <div class="diagnostic-action">
              <q-btn 
                flat 
                round 
                icon="refresh"
                @click="runDiagnostic(check)"
                :loading="check.checking"
                size="sm"
                color="primary"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Posibles soluciones -->
      <div class="info-card solutions-card">
        <div class="card-title">
          <h3>Posibles Soluciones</h3>
        </div>
        
        <div class="solutions-timeline">
          <div class="solution-step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h4>Verificar Conexión</h4>
              <p>Verifica que el servidor backend esté ejecutándose en <code>http://127.0.0.1:8002</code></p>
              <q-btn 
                flat 
                color="primary" 
                label="Probar Conexión"
                @click="testConnection"
                size="sm"
                icon="wifi"
                rounded
              />
            </div>
          </div>

          <div class="solution-step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h4>Revisar Autenticación</h4>
              <p>Verifica que tu sesión no haya expirado</p>
              <q-btn 
                flat 
                color="primary" 
                label="Ir a Login"
                @click="goToLogin"
                size="sm"
                icon="key"
                rounded
              />
            </div>
          </div>

          <div class="solution-step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h4>Recargar Página</h4>
              <p>A veces un simple recargo puede solucionar el problema</p>
              <q-btn 
                flat 
                color="primary" 
                label="Recargar"
                @click="reloadPage"
                size="sm"
                icon="refresh"
                rounded
              />
            </div>
          </div>

          <div class="solution-step">
            <div class="step-number">4</div>
            <div class="step-content">
              <h4>Contactar Soporte</h4>
              <p>Si el problema persiste, contacta al equipo de soporte</p>
              <q-btn 
                flat 
                color="primary" 
                label="Reportar Error"
                @click="reportError"
                size="sm"
                icon="support"
                rounded
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Acciones de navegación -->
      <div class="info-card navigation-card">
        <div class="card-title">
          <h3>Navegación</h3>
        </div>
        
        <div class="navigation-actions">
          <div class="nav-button primary-nav" @click="goToHome">
            <q-icon name="home" size="2rem" />
            <span>Ir al Inicio</span>
          </div>
          
          <div class="nav-button secondary-nav" @click="goToLogin">
            <q-icon name="login" size="2rem" />
            <span>Iniciar Sesión</span>
          </div>
          
          <div class="nav-button success-nav" @click="goToTestPage">
            <q-icon name="check" size="2rem" />
            <span>Página de Prueba</span>
          </div>
        </div>
      </div>

      <!-- Información técnica -->
      <div class="technical-section">
        <q-expansion-item
          icon="code"
          label="Información Técnica"
          caption="Detalles para desarrolladores"
          class="technical-expansion"
        >
          <div class="technical-content">
            <pre class="technical-info">{{ technicalInfo }}</pre>
          </div>
        </q-expansion-item>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import { useToast } from 'vue-toastification'
import ThemeToggle from '../components/ThemeToggle.vue'
import { useTheme } from '../composables/useTheme'

export default {
  name: 'Error_View',
  components: {
    ThemeToggle
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const $q = useQuasar()
    const toast = useToast()
    const { isDarkMode } = useTheme()

    // Información del error
    const errorCode = ref(route.query.code || '500')
    const errorMessage = ref(route.query.message || 'Error interno del sistema')
    const currentUrl = ref(window.location.href)

    // Diagnósticos del sistema
    const diagnosticChecks = ref([
      {
        name: 'Conexión Backend',
        description: 'Verificar si el servidor está disponible',
        status: 'unknown',
        checking: false,
        test: async () => {
          const response = await fetch('http://127.0.0.1:8002/health')
          return response.ok
        }
      },
      {
        name: 'Token de Autenticación',
        description: 'Verificar validez del token JWT',
        status: 'unknown',
        checking: false,
        test: () => {
          const token = localStorage.getItem('signance_token')
          return !!token
        }
      },
      {
        name: 'Almacenamiento Local',
        description: 'Verificar disponibilidad de localStorage',
        status: 'unknown',
        checking: false,
        test: () => {
          try {
            localStorage.setItem('test', 'test')
            localStorage.removeItem('test')
            return true
          } catch {
            return false
          }
        }
      },
      {
        name: 'Conectividad de Red',
        description: 'Verificar conexión a internet',
        status: 'unknown',
        checking: false,
        test: () => navigator.onLine
      }
    ])

    // Información técnica
    const technicalInfo = computed(() => {
      return JSON.stringify({
        errorCode: errorCode.value,
        errorMessage: errorMessage.value,
        url: currentUrl.value,
        userAgent: navigator.userAgent,
        timestamp: new Date().toISOString(),
        localStorage: {
          hasToken: !!localStorage.getItem('signance_token'),
          tokenLength: localStorage.getItem('signance_token')?.length || 0
        },
        route: {
          path: route.path,
          query: route.query,
          params: route.params
        }
      }, null, 2)
    })

    // Ejecutar diagnóstico
    const runDiagnostic = async (check) => {
      check.checking = true
      
      try {
        const result = await check.test()
        check.status = result ? 'ok' : 'error'
        check.details = result ? 'Funcionando correctamente' : 'Problema detectado'
      } catch (error) {
        check.status = 'error'
        check.details = `Error: ${error.message}`
      } finally {
        check.checking = false
      }
    }

    // Ejecutar todos los diagnósticos
    const runAllDiagnostics = async () => {
      for (const check of diagnosticChecks.value) {
        await runDiagnostic(check)
        await new Promise(resolve => setTimeout(resolve, 300))
      }
    }

    // Probar conexión
    const testConnection = async () => {
      $q.loading.show({
        message: 'Probando conexión...'
      })

      try {
        const response = await fetch('http://127.0.0.1:8002/health')
        if (response.ok) {
          toast.success('✅ Conexión exitosa con el backend')
        } else {
          toast.warning('⚠️ El servidor responde pero con errores')
        }
      } catch (error) {
        toast.error('❌ No se puede conectar con el servidor')
      } finally {
        $q.loading.hide()
      }
    }

    // Navegación
    const goToHome = () => {
      router.push('/')
    }

    const goToLogin = () => {
      router.push('/login')
    }

    const goToTestPage = () => {
      router.push('/test-ok')
    }

    const reloadPage = () => {
      window.location.reload()
    }

    const reportError = () => {
      toast.info('Función de reporte de errores en desarrollo')
      console.log('Error Report:', technicalInfo.value)
    }

    onMounted(() => {
      // Ejecutar diagnósticos automáticamente
      setTimeout(runAllDiagnostics, 1000)
    })

    return {
      errorCode,
      errorMessage,
      currentUrl,
      diagnosticChecks,
      technicalInfo,
      runDiagnostic,
      runAllDiagnostics,
      testConnection,
      goToHome,
      goToLogin,
      goToTestPage,
      reloadPage,
      reportError,
      isDarkMode
    }
  }
}
</script>

<style scoped>
.error-container {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--error) 0%, var(--primary) 50%, var(--secondary) 100%);
  padding: 20px 0;
  position: relative;
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.signance-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.error-header {
  text-align: center;
  background: var(--surface);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 40px 20px;
  margin-bottom: 30px;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border);
}

.error-icon {
  color: var(--error);
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.error-header h2 {
  margin: 0 0 12px 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.error-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.info-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  border-bottom: 1px solid var(--border);
}

.card-header q-icon {
  color: var(--warning);
}

.header-text h3 {
  margin: 0 0 4px 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
}

.header-text p {
  margin: 0;
  color: var(--text-secondary);
}

.card-title {
  padding: 24px 24px 16px;
  border-bottom: 1px solid var(--border);
}

.card-title h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
}

.error-details {
  padding: 20px;
}

.error-badge {
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 500;
  color: var(--text-primary);
}

.detail-value {
  color: var(--text-secondary);
  font-family: monospace;
  word-break: break-all;
}

.diagnostic-grid {
  padding: 20px;
  display: grid;
  gap: 16px;
}

.diagnostic-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.diagnostic-item:hover {
  box-shadow: var(--shadow-md);
}

.diagnostic-ok {
  border-color: var(--success);
  background: var(--hover-color);
}

.diagnostic-error {
  border-color: var(--error);
  background: var(--hover-color);
}

.diagnostic-checking {
  border-color: var(--warning);
  background: var(--hover-color);
}

.diagnostic-icon {
  color: var(--text-secondary);
}

.diagnostic-ok .diagnostic-icon {
  color: var(--success);
}

.diagnostic-error .diagnostic-icon {
  color: var(--error);
}

.diagnostic-checking .diagnostic-icon {
  color: var(--warning);
}

.diagnostic-info {
  flex: 1;
}

.diagnostic-info h4 {
  margin: 0 0 4px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.diagnostic-info p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.diagnostic-details {
  font-size: 0.8rem !important;
  color: var(--text-secondary) !important;
  margin-top: 4px !important;
}

.solutions-timeline {
  padding: 20px;
  display: grid;
  gap: 24px;
}

.solution-step {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.step-number {
  background: var(--primary);
  color: var(--on-primary);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h4 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.step-content p {
  margin: 0 0 12px 0;
  color: var(--text-secondary);
  line-height: 1.4;
}

.step-content code {
  background: var(--background);
  border: 1px solid var(--border);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.85rem;
}

.navigation-actions {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.nav-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.nav-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.primary-nav {
  background: var(--hover-primary);
  border: 2px solid var(--primary);
  color: var(--primary);
}

.secondary-nav {
  background: var(--hover-secondary);
  border: 2px solid var(--secondary);
  color: var(--secondary);
}

.success-nav {
  background: rgba(67, 160, 71, 0.1);
  border: 2px solid var(--success);
  color: var(--success);
}

[data-theme="dark"] .success-nav {
  background: rgba(102, 187, 106, 0.1);
}

.nav-button span {
  font-weight: 500;
  font-size: 0.95rem;
}

.technical-section {
  margin-bottom: 20px;
}

.technical-expansion {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
}

.technical-content {
  padding: 20px;
}

.technical-info {
  background: var(--background);
  padding: 15px;
  border-radius: 8px;
  font-size: 12px;
  overflow-x: auto;
  max-height: 300px;
  border: 1px solid var(--border);
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .error-container {
    padding: 10px;
  }
  
  .error-header {
    padding: 30px 15px;
  }
  
  .error-header h2 {
    font-size: 1.5rem;
  }
  
  .navigation-actions {
    grid-template-columns: 1fr;
  }
  
  .nav-button {
    padding: 20px 12px;
  }
  
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .solution-step {
    flex-direction: column;
    gap: 12px;
  }
  
  .step-number {
    align-self: flex-start;
  }
  
  .theme-toggle {
    top: 10px;
    right: 10px;
  }
}
</style>
