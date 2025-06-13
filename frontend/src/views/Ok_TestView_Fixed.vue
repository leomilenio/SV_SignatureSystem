<template>
  <div class="test-ok-container">
    <!-- Theme Toggle -->
    <ThemeToggle class="theme-toggle" />
    
    <div class="signance-container">
      <!-- Header de éxito -->
      <div class="success-header">
        <div class="success-icon">
          <q-icon name="check_circle" size="4rem" />
        </div>
        <h2>¡Sistema Funcionando Correctamente!</h2>
        <p>Pochtecayotl Signance System - Autenticación Exitosa</p>
      </div>

      <!-- Información del usuario -->
      <div class="info-card user-info">
        <div class="card-header">
          <q-icon name="person" size="2rem" />
          <div class="header-text">
            <h3>Usuario Autenticado</h3>
            <p>{{ userInfo.username || 'Cargando...' }}</p>
          </div>
        </div>
      </div>

      <!-- Pruebas del sistema -->
      <div class="info-card tests-card">
        <div class="card-title">
          <h3>Pruebas del Sistema</h3>
        </div>
        
        <div class="tests-grid">
          <div 
            v-for="test in systemTests" 
            :key="test.name"
            class="test-item"
            :class="{ 
              'test-success': test.status === 'success',
              'test-error': test.status === 'error',
              'test-testing': test.status === 'testing'
            }"
          >
            <div class="test-icon">
              <q-icon 
                :name="test.status === 'success' ? 'check_circle' : test.status === 'error' ? 'error' : 'hourglass_empty'"
                size="1.5rem"
              />
            </div>
            
            <div class="test-info">
              <h4>{{ test.name }}</h4>
              <p>{{ test.description }}</p>
            </div>
            
            <div class="test-action">
              <q-btn 
                flat 
                round 
                :icon="test.status === 'testing' ? 'refresh' : 'play_arrow'"
                @click="runTest(test)"
                :loading="test.status === 'testing'"
                size="sm"
                :color="test.status === 'success' ? 'positive' : 'primary'"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Acciones disponibles -->
      <div class="info-card actions-card">
        <div class="card-title">
          <h3>Acciones Disponibles</h3>
        </div>
        
        <div class="actions-grid">
          <div class="action-button primary-action" @click="goToDashboard">
            <q-icon name="dashboard" size="2rem" />
            <span>Dashboard</span>
          </div>
          
          <div class="action-button secondary-action" @click="goToMediaManager">
            <q-icon name="cloud_upload" size="2rem" />
            <span>Gestión de Media</span>
          </div>
          
          <div class="action-button accent-action" @click="goToConfig">
            <q-icon name="settings" size="2rem" />
            <span>Configuración</span>
          </div>
          
          <div class="action-button warning-action" @click="goToErrorPage">
            <q-icon name="bug_report" size="2rem" />
            <span>Ver Página de Error</span>
          </div>
        </div>
        
        <div class="logout-section">
          <q-btn
            color="negative"
            icon="logout"
            label="Cerrar Sesión"
            @click="logout"
            outline
            rounded
            size="md"
          />
        </div>
      </div>

      <!-- Información del sistema -->
      <div class="info-card system-info">
        <div class="card-title">
          <h3>Información del Sistema</h3>
        </div>
        
        <div class="system-details">
          <div class="detail-item">
            <span class="detail-label">Estado del Backend</span>
            <div class="detail-value">
              <q-chip 
                :color="backendStatus.connected ? 'positive' : 'negative'"
                text-color="white"
                :icon="backendStatus.connected ? 'check' : 'close'"
                size="sm"
              >
                {{ backendStatus.connected ? 'Conectado' : 'Desconectado' }}
              </q-chip>
            </div>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">URL del Backend</span>
            <span class="detail-value">http://127.0.0.1:8002</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Fecha de Acceso</span>
            <span class="detail-value">{{ new Date().toLocaleString('es-ES') }}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Token JWT</span>
            <div class="detail-value">
              <q-chip color="info" text-color="white" size="sm">
                {{ tokenInfo }}
              </q-chip>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { authAPI, mediaAPI, businessAPI, scheduleAPI } from '../services/api'
import ThemeToggle from '../components/ThemeToggle.vue'
import { useTheme } from '../composables/useTheme'

export default {
  name: 'Ok_TestView',
  components: {
    ThemeToggle
  },
  setup() {
    const router = useRouter()
    const toast = useToast()
    const { isDarkMode } = useTheme()

    // Estados reactivos
    const userInfo = ref({})
    const backendStatus = reactive({
      connected: false,
      lastCheck: null
    })

    // Información del token
    const tokenInfo = computed(() => {
      const token = localStorage.getItem('signance_token')
      if (token) {
        return `${token.substring(0, 20)}...`
      }
      return 'No disponible'
    })

    // Pruebas del sistema
    const systemTests = ref([
      {
        name: 'Autenticación',
        description: 'Verificar ruta protegida',
        status: 'pending',
        test: () => authAPI.testProtected()
      },
      {
        name: 'Gestión de Media',
        description: 'Listar archivos multimedia',
        status: 'pending',
        test: () => mediaAPI.list(0, 5)
      },
      {
        name: 'Información de Negocio',
        description: 'Obtener configuración empresarial',
        status: 'pending',
        test: () => businessAPI.get()
      },
      {
        name: 'Programación',
        description: 'Listar horarios programados',
        status: 'pending',
        test: () => scheduleAPI.list(0, 5)
      }
    ])

    // Ejecutar una prueba específica
    const runTest = async (test) => {
      test.status = 'testing'
      
      try {
        const response = await test.test()
        test.status = 'success'
        test.result = response.data
        
        toast.success(`✅ ${test.name}: Prueba exitosa`)
        
      } catch (error) {
        test.status = 'error'
        test.error = error.message
        
        toast.error(`❌ ${test.name}: ${error.message}`)
      }
    }

    // Ejecutar todas las pruebas
    const runAllTests = async () => {
      for (const test of systemTests.value) {
        await runTest(test)
        // Pequeña pausa entre pruebas
        await new Promise(resolve => setTimeout(resolve, 500))
      }
    }

    // Obtener información del usuario actual
    const fetchUserInfo = async () => {
      try {
        const response = await authAPI.getCurrentUser()
        userInfo.value = response.data
      } catch (error) {
        console.error('Error obteniendo información del usuario:', error)
        toast.error('Error obteniendo información del usuario')
      }
    }

    // Verificar estado del backend
    const checkBackendStatus = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8002/health')
        backendStatus.connected = response.ok
        backendStatus.lastCheck = new Date()
      } catch (error) {
        backendStatus.connected = false
        backendStatus.lastCheck = new Date()
      }
    }

    // Navegación
    const goToDashboard = () => {
      router.push('/admin')
    }

    const goToMediaManager = () => {
      router.push('/media')
    }

    const goToConfig = () => {
      router.push('/config')
    }

    const goToErrorPage = () => {
      router.push('/error')
    }

    // Cerrar sesión
    const logout = async () => {
      try {
        await authAPI.logout()
      } catch (error) {
        console.error('Error en logout:', error)
      } finally {
        localStorage.removeItem('signance_token')
        toast.success('Sesión cerrada exitosamente')
        router.push('/login')
      }
    }

    onMounted(() => {
      fetchUserInfo()
      checkBackendStatus()
      // Ejecutar pruebas automáticamente después de 2 segundos
      setTimeout(runAllTests, 2000)
    })

    return {
      userInfo,
      backendStatus,
      tokenInfo,
      systemTests,
      runTest,
      runAllTests,
      goToDashboard,
      goToMediaManager,
      goToConfig,
      goToErrorPage,
      logout,
      isDarkMode
    }
  }
}
</script>

<style scoped>
.test-ok-container {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--success) 0%, var(--primary) 50%, var(--secondary) 100%);
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

.success-header {
  text-align: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 40px 20px;
  margin-bottom: 30px;
  box-shadow: var(--shadow-xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

[data-theme="dark"] .success-header {
  background: rgba(30, 30, 30, 0.95);
  color: var(--text-primary);
}

.success-icon {
  color: var(--success);
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.success-header h2 {
  margin: 0 0 12px 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.success-header p {
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
  color: var(--primary);
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

.tests-grid {
  padding: 20px;
  display: grid;
  gap: 16px;
}

.test-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.test-item:hover {
  box-shadow: var(--shadow-md);
}

.test-success {
  border-color: var(--success);
  background: var(--hover-color);
}

.test-error {
  border-color: var(--error);
  background: var(--hover-color);
}

.test-testing {
  border-color: var(--warning);
  background: var(--hover-color);
}

.test-icon {
  color: var(--text-secondary);
}

.test-success .test-icon {
  color: var(--success);
}

.test-error .test-icon {
  color: var(--error);
}

.test-testing .test-icon {
  color: var(--warning);
}

.test-info {
  flex: 1;
}

.test-info h4 {
  margin: 0 0 4px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.test-info p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.actions-grid {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.action-button {
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

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.primary-action {
  background: var(--hover-primary);
  border: 2px solid var(--primary);
  color: var(--primary);
}

.secondary-action {
  background: var(--hover-secondary);
  border: 2px solid var(--secondary);
  color: var(--secondary);
}

.accent-action {
  background: rgba(240, 210, 123, 0.1);
  border: 2px solid var(--accent);
  color: var(--accent);
}

[data-theme="dark"] .accent-action {
  background: rgba(209, 176, 95, 0.1);
}

.warning-action {
  background: rgba(251, 140, 0, 0.1);
  border: 2px solid var(--warning);
  color: var(--warning);
}

[data-theme="dark"] .warning-action {
  background: rgba(255, 167, 38, 0.1);
}

.action-button span {
  font-weight: 500;
  font-size: 0.95rem;
}

.logout-section {
  padding: 20px;
  border-top: 1px solid var(--border);
  text-align: center;
}

.system-details {
  padding: 20px;
  display: grid;
  gap: 16px;
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
}

@media (max-width: 768px) {
  .test-ok-container {
    padding: 10px;
  }
  
  .success-header {
    padding: 30px 15px;
  }
  
  .success-header h2 {
    font-size: 1.5rem;
  }
  
  .actions-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .action-button {
    padding: 20px 12px;
  }
  
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .theme-toggle {
    top: 10px;
    right: 10px;
  }
}
</style>
