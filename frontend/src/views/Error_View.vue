<template>
  <div class="error-container">
    <div class="signance-container">
      <!-- Header de error -->
      <div class="error-header text-center">
        <q-icon name="error" size="5rem" color="negative" />
        <h3 class="q-my-md text-negative">¡Oops! Algo salió mal</h3>
        <p class="q-mb-none text-grey-6">Pochtecayotl Signance System - Página de Error</p>
      </div>

      <!-- Información del error -->
      <q-card class="q-mb-lg">
        <q-card-section>
          <div class="row items-center q-mb-md">
            <q-icon name="bug_report" size="2rem" color="warning" class="q-mr-md" />
            <div>
              <h6 class="q-my-none">Error del Sistema</h6>
              <p class="text-grey-6 q-my-none">Detalles técnicos del problema</p>
            </div>
          </div>

          <q-separator class="q-my-md" />

          <div class="error-details">
            <q-chip color="negative" text-color="white" icon="error">
              Código: {{ errorCode }}
            </q-chip>
            
            <p class="q-mt-md"><strong>Mensaje:</strong> {{ errorMessage }}</p>
            
            <p><strong>Timestamp:</strong> {{ new Date().toLocaleString('es-ES') }}</p>
            
            <p><strong>URL:</strong> {{ currentUrl }}</p>
          </div>
        </q-card-section>
      </q-card>

      <!-- Diagnóstico del sistema -->
      <q-card class="q-mb-lg">
        <q-card-section>
          <h6 class="q-mt-none q-mb-md">Diagnóstico del Sistema</h6>
          
          <q-list separator>
            <q-item 
              v-for="check in diagnosticChecks" 
              :key="check.name"
              class="q-pa-md"
            >
              <q-item-section avatar>
                <q-icon 
                  :name="check.status === 'ok' ? 'check_circle' : check.status === 'error' ? 'error' : 'help'"
                  :color="check.status === 'ok' ? 'positive' : check.status === 'error' ? 'negative' : 'orange'"
                  size="md"
                />
              </q-item-section>
              
              <q-item-section>
                <q-item-label>{{ check.name }}</q-item-label>
                <q-item-label caption>{{ check.description }}</q-item-label>
                <q-item-label caption v-if="check.details" class="text-grey-5">
                  {{ check.details }}
                </q-item-label>
              </q-item-section>
              
              <q-item-section side>
                <q-btn 
                  flat 
                  round 
                  icon="refresh"
                  @click="runDiagnostic(check)"
                  :loading="check.checking"
                  size="sm"
                />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <!-- Posibles soluciones -->
      <q-card class="q-mb-lg">
        <q-card-section>
          <h6 class="q-mt-none q-mb-md">Posibles Soluciones</h6>
          
          <q-timeline color="secondary">
            <q-timeline-entry
              title="Verificar Conexión"
              subtitle="Paso 1"
              icon="wifi"
            >
              <div>
                Verifica que el servidor backend esté ejecutándose en 
                <code>http://127.0.0.1:8002</code>
              </div>
              <q-btn 
                flat 
                color="primary" 
                label="Probar Conexión"
                @click="testConnection"
                class="q-mt-sm"
                size="sm"
              />
            </q-timeline-entry>

            <q-timeline-entry
              title="Revisar Autenticación"
              subtitle="Paso 2"
              icon="key"
            >
              <div>
                Verifica que tu sesión no haya expirado
              </div>
              <q-btn 
                flat 
                color="primary" 
                label="Ir a Login"
                @click="goToLogin"
                class="q-mt-sm"
                size="sm"
              />
            </q-timeline-entry>

            <q-timeline-entry
              title="Recargar Página"
              subtitle="Paso 3"
              icon="refresh"
            >
              <div>
                A veces un simple recargo puede solucionar el problema
              </div>
              <q-btn 
                flat 
                color="primary" 
                label="Recargar"
                @click="reloadPage"
                class="q-mt-sm"
                size="sm"
              />
            </q-timeline-entry>

            <q-timeline-entry
              title="Contactar Soporte"
              subtitle="Paso 4"
              icon="support"
            >
              <div>
                Si el problema persiste, contacta al equipo de soporte
              </div>
              <q-btn 
                flat 
                color="primary" 
                label="Reportar Error"
                @click="reportError"
                class="q-mt-sm"
                size="sm"
              />
            </q-timeline-entry>
          </q-timeline>
        </q-card-section>
      </q-card>

      <!-- Acciones de navegación -->
      <q-card>
        <q-card-section>
          <h6 class="q-mt-none q-mb-md">Navegación</h6>
          
          <div class="row q-gutter-md">
            <q-btn
              color="primary"
              icon="home"
              label="Ir al Inicio"
              @click="goToHome"
              class="col"
            />
            
            <q-btn
              color="secondary"
              icon="login"
              label="Iniciar Sesión"
              @click="goToLogin"
              class="col"
            />
            
            <q-btn
              color="positive"
              icon="check"
              label="Página de Prueba"
              @click="goToTestPage"
              class="col"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Información técnica -->
      <q-expansion-item
        class="q-mt-lg"
        icon="code"
        label="Información Técnica"
        caption="Detalles para desarrolladores"
      >
        <q-card>
          <q-card-section>
            <pre class="technical-info">{{ technicalInfo }}</pre>
          </q-card-section>
        </q-card>
      </q-expansion-item>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import { useToast } from 'vue-toastification'

export default {
  name: 'Error_View',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const $q = useQuasar()
    const toast = useToast()

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
      reportError
    }
  }
}
</script>

<style scoped>
.error-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #000000 0%, #784F17 10%, #E70000 25%, #FF8C00 40%, #FFEF00 55%, #00811F 70%, #00A7E4 85%, #760089 100%);
  padding: 20px 0;
}

.error-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 40px 20px;
  margin-bottom: 30px;
  color: white;
}

.error-header h3 {
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.technical-info {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  font-size: 12px;
  overflow-x: auto;
  max-height: 300px;
}

code {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

@media (max-width: 768px) {
  .error-container {
    padding: 10px;
  }
  
  .error-header {
    padding: 30px 15px;
  }
}
</style>
