<template>
  <div class="test-ok-container">
    <div class="signance-container">
      <!-- Header de éxito -->
      <div class="signance-header text-center">
        <q-icon name="check_circle" size="4rem" color="white" />
        <h3 class="q-my-md">¡Sistema Funcionando Correctamente!</h3>
        <p class="q-mb-none">Signance System - Autenticación Exitosa</p>
      </div>

      <!-- Información del usuario -->
      <q-card class="q-mb-lg">
        <q-card-section>
          <div class="row items-center">
            <q-icon name="person" size="2rem" color="positive" class="q-mr-md" />
            <div>
              <h6 class="q-my-none">Usuario Autenticado</h6>
              <p class="text-grey-6 q-my-none">{{ userInfo.username || 'Cargando...' }}</p>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Pruebas del sistema -->
      <q-card class="q-mb-lg">
        <q-card-section>
          <h6 class="q-mt-none q-mb-md">Pruebas del Sistema</h6>
          
          <q-list separator>
            <q-item 
              v-for="test in systemTests" 
              :key="test.name"
              class="q-pa-md"
            >
              <q-item-section avatar>
                <q-icon 
                  :name="test.status === 'success' ? 'check_circle' : test.status === 'error' ? 'error' : 'hourglass_empty'"
                  :color="test.status === 'success' ? 'positive' : test.status === 'error' ? 'negative' : 'orange'"
                  size="md"
                />
              </q-item-section>
              
              <q-item-section>
                <q-item-label>{{ test.name }}</q-item-label>
                <q-item-label caption>{{ test.description }}</q-item-label>
              </q-item-section>
              
              <q-item-section side>
                <q-btn 
                  flat 
                  round 
                  :icon="test.status === 'testing' ? 'refresh' : 'play_arrow'"
                  @click="runTest(test)"
                  :loading="test.status === 'testing'"
                  size="sm"
                />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <!-- Acciones disponibles -->
      <q-card>
        <q-card-section>
          <h6 class="q-mt-none q-mb-md">Acciones Disponibles</h6>
          
          <div class="row q-gutter-md">
            <q-btn
              color="primary"
              icon="dashboard"
              label="Ir al Dashboard"
              @click="goToDashboard"
              class="col"
            />
            
            <q-btn
              color="secondary"
              icon="cloud_upload"
              label="Gestión de Media"
              @click="goToMediaManager"
              class="col"
            />
            
            <q-btn
              color="info"
              icon="settings"
              label="Configuración"
              @click="goToConfig"
              class="col"
            />
          </div>
          
          <div class="row q-gutter-md q-mt-md">
            <q-btn
              color="warning"
              icon="bug_report"
              label="Ver Página de Error"
              @click="goToErrorPage"
              class="col"
              outline
            />
            
            <q-btn
              color="negative"
              icon="logout"
              label="Cerrar Sesión"
              @click="logout"
              class="col"
              outline
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Información del sistema -->
      <q-card class="q-mt-lg">
        <q-card-section>
          <h6 class="q-mt-none q-mb-md">Información del Sistema</h6>
          
          <q-markup-table flat bordered>
            <tbody>
              <tr>
                <td class="text-weight-medium">Estado del Backend</td>
                <td>
                  <q-chip 
                    :color="backendStatus.connected ? 'positive' : 'negative'"
                    text-color="white"
                    :icon="backendStatus.connected ? 'check' : 'close'"
                  >
                    {{ backendStatus.connected ? 'Conectado' : 'Desconectado' }}
                  </q-chip>
                </td>
              </tr>
              <tr>
                <td class="text-weight-medium">URL del Backend</td>
                <td>http://127.0.0.1:8002</td>
              </tr>
              <tr>
                <td class="text-weight-medium">Fecha de Acceso</td>
                <td>{{ new Date().toLocaleString('es-ES') }}</td>
              </tr>
              <tr>
                <td class="text-weight-medium">Token JWT</td>
                <td>
                  <q-chip color="info" text-color="white">
                    {{ tokenInfo }}
                  </q-chip>
                </td>
              </tr>
            </tbody>
          </q-markup-table>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { authAPI, mediaAPI, businessAPI, scheduleAPI } from '../services/api'

export default {
  name: 'Ok_TestView',
  setup() {
    const router = useRouter()
    const toast = useToast()

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
      toast.info('Dashboard en desarrollo - próximamente disponible')
      // router.push('/admin')
    }

    const goToMediaManager = () => {
      toast.info('Gestión de Media en desarrollo - próximamente disponible')
      // router.push('/media')
    }

    const goToConfig = () => {
      toast.info('Configuración en desarrollo - próximamente disponible')
      // router.push('/config')
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
      logout
    }
  }
}
</script>

<style scoped>
.test-ok-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

@media (max-width: 768px) {
  .test-ok-container {
    padding: 10px;
  }
}
</style>
