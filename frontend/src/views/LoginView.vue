<template>
  <div class="login-container">
    <q-card class="login-card">
      <q-card-section class="text-center">
        <div class="login-header">
          <q-icon name="video_library" size="3rem" color="primary" />
          <h4 class="q-my-md">Pochtecayotl Signance System</h4>
          <p class="text-grey-6">Sistema de Gestión de Contenido Digital</p>
        </div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="handleLogin" class="q-gutter-md">
          <q-input
            v-model="credentials.username"
            label="Usuario"
            outlined
            :rules="[val => !!val || 'El usuario es requerido']"
            ref="usernameRef"
          >
            <template v-slot:prepend>
              <q-icon name="person" />
            </template>
          </q-input>

          <q-input
            v-model="credentials.password"
            label="Contraseña"
            type="password"
            outlined
            :rules="[val => !!val || 'La contraseña es requerida']"
            ref="passwordRef"
          >
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
          </q-input>

          <div class="q-mt-lg">
            <q-btn
              type="submit"
              label="Iniciar Sesión"
              color="primary"
              size="md"
              class="full-width"
              :loading="isLoading"
              :disable="!credentials.username || !credentials.password"
            />
          </div>
        </q-form>
      </q-card-section>

      <q-card-section class="text-center">
        <q-btn
          flat
          label="Probar Conexión Backend"
          color="secondary"
          @click="testBackendConnection"
          size="sm"
        />
      </q-card-section>
    </q-card>

    <!-- Setup inicial del administrador -->
    <q-dialog v-model="showSetupDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center">
          <q-icon name="admin_panel_settings" size="2rem" color="orange" />
          <span class="q-ml-sm text-h6">Configuración Inicial</span>
        </q-card-section>

        <q-card-section>
          <p>El sistema necesita configuración inicial. Crea el usuario administrador:</p>
          
          <q-form @submit="handleSetupAdmin" class="q-gutter-md">
            <q-input
              v-model="setupData.username"
              label="Usuario Administrador"
              outlined
              :rules="[val => !!val || 'Requerido']"
            />
            
            <q-input
              v-model="setupData.password"
              label="Contraseña"
              type="password"
              outlined
              :rules="[val => !!val || 'Requerido']"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            label="Configurar"
            color="primary"
            @click="handleSetupAdmin"
            :loading="isSetupLoading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useToast } from 'vue-toastification'
import { authAPI } from '../services/api'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const $q = useQuasar()
    const toast = useToast()

    // Estados reactivos
    const isLoading = ref(false)
    const isSetupLoading = ref(false)
    const showSetupDialog = ref(false)
    
    const credentials = reactive({
      username: '',
      password: ''
    })
    
    const setupData = reactive({
      username: 'admin',
      password: ''
    })

    // Verificar si necesita configuración inicial
    const checkSetupStatus = async () => {
      try {
        const response = await authAPI.checkSetup()
        if (response.data.setup_required) {
          showSetupDialog.value = true
          toast.info('Se requiere configuración inicial del sistema')
        }
      } catch (error) {
        console.error('Error verificando setup:', error)
        toast.error('Error conectando con el servidor')
      }
    }

    // Configurar administrador inicial
    const handleSetupAdmin = async () => {
      if (!setupData.username || !setupData.password) {
        toast.warning('Completa todos los campos')
        return
      }

      isSetupLoading.value = true

      try {
        await authAPI.setupAdmin(setupData)
        toast.success('Administrador configurado exitosamente')
        showSetupDialog.value = false
        
        // Auto-login después del setup
        credentials.username = setupData.username
        credentials.password = setupData.password
        await handleLogin()
        
      } catch (error) {
        console.error('Error en setup:', error)
        toast.error('Error configurando administrador')
      } finally {
        isSetupLoading.value = false
      }
    }

    // Manejar login
    const handleLogin = async () => {
      isLoading.value = true

      try {
        const response = await authAPI.login(credentials)
        const { access_token } = response.data

        // Guardar token
        localStorage.setItem('signance_token', access_token)
        
        toast.success(`¡Bienvenido, ${credentials.username}!`)
        
        // Redirigir a página de prueba exitosa
        router.push('/test-ok')
        
      } catch (error) {
        console.error('Error en login:', error)
        
        if (error.response?.status === 401) {
          toast.error('Credenciales incorrectas')
        } else {
          toast.error('Error iniciando sesión')
        }
        
        // Limpiar campos en caso de error
        credentials.password = ''
        
      } finally {
        isLoading.value = false
      }
    }

    // Probar conexión con el backend
    const testBackendConnection = async () => {
      $q.loading.show({
        message: 'Probando conexión...'
      })

      try {
        const response = await fetch('http://127.0.0.1:8002/health')
        if (response.ok) {
          const data = await response.json()
          toast.success(`Conexión exitosa: ${data.status}`)
        } else {
          toast.warning('El servidor responde pero con errores')
        }
      } catch (error) {
        console.error('Error de conexión:', error)
        toast.error('No se puede conectar con el servidor')
      } finally {
        $q.loading.hide()
      }
    }

    // Verificar si ya está autenticado
    const checkExistingAuth = () => {
      const token = localStorage.getItem('signance_token')
      if (token) {
        // TODO: Verificar si el token es válido
        router.push('/test-ok')
      }
    }

    onMounted(() => {
      checkExistingAuth()
      checkSetupStatus()
    })

    return {
      credentials,
      setupData,
      isLoading,
      isSetupLoading,
      showSetupDialog,
      handleLogin,
      handleSetupAdmin,
      testBackendConnection
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #000000 0%, #784F17 10%, #E70000 25%, #FF8C00 40%, #FFEF00 55%, #00811F 70%, #00A7E4 85%, #760089 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
}

.login-header {
  padding: 20px 0;
}

.login-header h4 {
  margin: 16px 0 8px 0;
  font-weight: 600;
  color: #1976d2;
}

@media (max-width: 480px) {
  .login-container {
    padding: 10px;
  }
  
  .login-card {
    max-width: 100%;
  }
}
</style>
