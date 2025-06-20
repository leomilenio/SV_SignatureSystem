<template>
  <div class="login-container">
    <!-- Toggle de tema en esquina superior derecha -->
    <div class="theme-toggle-container">
      <ThemeToggle />
    </div>
    
    <div class="login-content">
      <q-card class="login-card">
        <q-card-section class="text-center login-header-section">
          <div class="login-header">
            <div class="logo-container">
              <q-icon name="video_library" class="main-logo" />
              <div class="logo-glow"></div>
            </div>
            <h2 class="app-title">Pochtecayotl</h2>
            <h3 class="app-subtitle-main">Signance System</h3>
            <p class="app-subtitle">Sistema de Gestión de Anuncios Digitales</p>
            <div class="pride-divider"></div>
          </div>
        </q-card-section>

        <q-card-section class="login-form-section">
          <q-form @submit="handleLogin" class="login-form">
            <div class="input-group">
              <q-input
                v-model="credentials.username"
                label="Usuario"
                outlined
                dense
                :rules="[val => !!val || 'El usuario es requerido']"
                ref="usernameRef"
                class="modern-input"
              >
                <template v-slot:prepend>
                  <q-icon name="person" class="input-icon" />
                </template>
              </q-input>
            </div>

            <div class="input-group">
              <q-input
                v-model="credentials.password"
                label="Contraseña"
                type="password"
                outlined
                dense
                :rules="[val => !!val || 'La contraseña es requerida']"
                ref="passwordRef"
                class="modern-input"
              >
                <template v-slot:prepend>
                  <q-icon name="lock" class="input-icon" />
                </template>
              </q-input>
            </div>

            <div class="login-actions">
              <q-btn
                type="submit"
                label="Iniciar Sesión"
                class="login-btn"
                size="md"
                unelevated
                :loading="isLoading"
                :disable="!credentials.username || !credentials.password"
              />
            </div>
          </q-form>
        </q-card-section>

        <q-card-section class="text-center footer-section">
          <q-btn
            flat
            label="Probar Conexión"
            @click="testBackendConnection"
            size="sm"
            class="test-btn"
          />
        </q-card-section>
      </q-card>
    </div>

    <!-- Setup inicial del administrador -->
    <q-dialog v-model="showSetupDialog" persistent>
      <q-card class="setup-dialog-card" style="min-width: 400px">
        <q-card-section class="setup-header row items-center">
          <q-icon name="admin_panel_settings" size="2rem" color="orange" />
          <span class="q-ml-sm text-h6 setup-title">Configuración Inicial</span>
        </q-card-section>

        <q-card-section class="setup-content">
          <p class="setup-description">El sistema necesita configuración inicial. Crea el usuario administrador:</p>
          
          <q-form @submit="handleSetupAdmin" class="q-gutter-md">
            <q-input
              v-model="setupData.username"
              label="Usuario Administrador"
              outlined
              class="setup-input"
              :rules="[val => !!val || 'Requerido']"
            />
            
            <q-input
              v-model="setupData.password"
              label="Contraseña"
              type="password"
              outlined
              class="setup-input"
              :rules="[val => !!val || 'Requerido']"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right" class="setup-actions">
          <q-btn
            label="Configurar"
            color="primary"
            class="setup-btn"
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
import { useTheme } from '../composables/useTheme'
import ThemeToggle from '../components/ThemeToggle.vue'

export default {
  name: 'LoginView',
  components: {
    ThemeToggle
  },
  setup() {
    const router = useRouter()
    const $q = useQuasar()
    const toast = useToast()
    const { loadTheme } = useTheme()

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
        
        // Redirigir al dashboard admin después del login exitoso
        router.push('/admin')
        
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
        const response = await fetch('http://127.0.0.1:8000/health')
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
      loadTheme()
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
/* Variables CSS */
:root {
  --gradient-main: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-light: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.8) 100%);
  --gradient-text: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
  --gradient-accent: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  --gradient-button: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  --surface: rgba(255, 255, 255, 0.95);
  --background: #f8fafc;
  --border: #e2e8f0;
  --primary: #6366f1;
  --primary-alpha: rgba(99, 102, 241, 0.1);
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* Variables para modo oscuro */
.body--dark {
  --gradient-main: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  --gradient-light: linear-gradient(135deg, rgba(30,30,30,0.9) 0%, rgba(30,30,30,0.8) 100%);
  --gradient-text: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #38bdf8 100%);
  --gradient-accent: linear-gradient(90deg, #4338ca 0%, #6d28d9 100%);
  --gradient-button: linear-gradient(135deg, #4338ca 0%, #7c3aed 100%);
  --surface: rgba(30, 30, 30, 0.95);
  --background: #0f172a;
  --border: #334155;
  --primary: #818cf8;
  --primary-alpha: rgba(129, 140, 248, 0.1);
  --text-primary: #e2e8f0;
  --text-secondary: #94a3b8;
  --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--gradient-main);
  padding: 2rem;
  position: relative;
  transition: all 0.3s ease;
}

.theme-toggle-container {
  position: absolute;
  top: 2rem;
  right: 2rem;
  z-index: 100;
}

.login-content {
  width: 100%;
  max-width: 420px;
  position: relative;
}

.login-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: var(--shadow-xl);
  transition: all 0.3s ease;
}

.login-header-section {
  padding: 2.5rem 2rem 1.5rem;
  background: var(--gradient-light);
  border-bottom: 1px solid var(--border);
}

.logo-container {
  position: relative;
  display: inline-block;
  margin-bottom: 1rem;
}

.main-logo {
  font-size: 3.5rem;
  background: var(--gradient-text);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70px;
  height: 70px;
  background: radial-gradient(circle, var(--primary-alpha), transparent);
  border-radius: 50%;
  animation: pulse 3s ease-in-out infinite;
  z-index: -1;
}

@keyframes pulse {
  0%, 100% { 
    transform: translate(-50%, -50%) scale(1); 
    opacity: 0.4; 
  }
  50% { 
    transform: translate(-50%, -50%) scale(1.1); 
    opacity: 0.7; 
  }
}

.app-title {
  margin: 0 0 0.2rem 0;
  font-size: 2.2rem;
  font-weight: 700;
  line-height: 1.1;
  color: #6366f1;
  text-shadow: 0 2px 4px rgba(99, 102, 241, 0.3);
}

/* Modo oscuro */
.body--dark .app-title {
  color: #818cf8;
  text-shadow: 0 2px 4px rgba(129, 140, 248, 0.3);
}

.app-subtitle-main {
  margin: 0 0 0.8rem 0;
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.1;
}

.app-subtitle {
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
  opacity: 0.9;
  line-height: 1.3;
}

.pride-divider {
  width: 50px;
  height: 3px;
  background: var(--gradient-accent);
  border-radius: 2px;
  margin: 0 auto;
}

.login-form-section {
  padding: 1.5rem 2rem;
  background: var(--background);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.input-group {
  position: relative;
}

.modern-input {
  border-radius: 10px !important;
}

.modern-input :deep(.q-field__control) {
  border-radius: 10px !important;
  background: var(--surface);
  border: 1px solid var(--border);
  transition: all 0.3s ease;
  min-height: 48px;
}

.modern-input :deep(.q-field__control:hover) {
  border-color: var(--primary);
}

.modern-input :deep(.q-field__control.q-field__control--focused) {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--primary-alpha);
}

.modern-input :deep(.q-field__label) {
  color: var(--text-secondary);
}

.modern-input :deep(.q-field__native) {
  color: var(--text-primary);
}

.input-icon {
  color: var(--primary);
}

.login-actions {
  margin-top: 0.5rem;
}

.login-btn {
  width: 100%;
  height: 48px;
  border-radius: 10px;
  background: var(--gradient-button);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  transition: all 0.3s ease;
  border: none;
  box-shadow: var(--shadow-md);
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

.login-btn:active {
  transform: translateY(0);
}

.login-btn:disabled {
  opacity: 0.6;
  transform: none;
  box-shadow: none;
}

.footer-section {
  padding: 1rem 2rem 1.5rem;
  border-top: 1px solid var(--border);
  background: var(--background);
}

.test-btn {
  color: var(--secondary);
  transition: all 0.2s ease;
  border-radius: 8px;
}

.test-btn:hover {
  background: var(--hover-secondary);
  transform: translateY(-1px);
}

/* Dialog de configuración */
.q-dialog .q-card {
  background: var(--surface);
  color: var(--text-primary);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: var(--shadow-xl);
}

.q-dialog .q-card-section {
  background: var(--background);
}

.q-dialog .q-card-actions {
  background: var(--surface);
  border-top: 1px solid var(--border);
}

/* Input fields en el dialog */
.q-dialog .q-input :deep(.q-field__control) {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
}

.q-dialog .q-input :deep(.q-field__control:hover) {
  border-color: var(--primary);
}

.q-dialog .q-input :deep(.q-field__control.q-field__control--focused) {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--primary-alpha);
}

/* Botones del dialog */
.q-dialog .q-btn {
  border-radius: 8px;
}

/* Responsive */
@media (max-width: 768px) {
  .login-container {
    padding: 1rem;
  }
  
  .theme-toggle-container {
    top: 1rem;
    right: 1rem;
  }
  
  .login-header-section {
    padding: 2rem 1.5rem 1rem;
  }
  
  .login-form-section {
    padding: 1.2rem 1.5rem;
  }
  
  .app-title {
    font-size: 1.8rem;
  }
  
  .app-subtitle-main {
    font-size: 1.2rem;
  }
  
  .main-logo {
    font-size: 3rem;
  }
  
  .login-content {
    max-width: 100%;
  }
  
  .footer-section {
    padding: 0.8rem 1.5rem 1.2rem;
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 0.5rem;
  }
  
  .login-header-section {
    padding: 1.5rem 1rem 0.8rem;
  }
  
  .login-form-section {
    padding: 1rem;
  }
  
  .app-title {
    font-size: 1.6rem;
  }
  
  .app-subtitle-main {
    font-size: 1.1rem;
  }
  
  .app-subtitle {
    font-size: 0.85rem;
  }
  
  .main-logo {
    font-size: 2.5rem;
  }
  
  .footer-section {
    padding: 0.8rem 1rem 1rem;
  }
  
  .login-btn {
    height: 46px;
    font-size: 0.95rem;
  }
  
  .modern-input :deep(.q-field__control) {
    min-height: 46px;
  }
}

/* Estilos para el dialog de setup */
.setup-dialog-card {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  backdrop-filter: blur(20px);
}

.setup-header {
  background: var(--gradient-light) !important;
  border-bottom: 1px solid var(--border) !important;
}

.setup-title {
  color: var(--text-primary) !important;
  font-weight: 600;
}

.setup-content {
  padding: 24px !important;
}

.setup-description {
  color: var(--text-secondary) !important;
  margin-bottom: 20px;
  font-size: 0.95rem;
}

.setup-input {
  margin-bottom: 16px;
}

.setup-input :deep(.q-field__label) {
  color: var(--text-secondary) !important;
}

.setup-input :deep(.q-field__control) {
  background: var(--surface) !important;
}

.setup-input :deep(.q-field__outline) {
  border-color: var(--border) !important;
}

.setup-input :deep(.q-field--focused .q-field__outline) {
  border-color: var(--primary) !important;
}

.setup-input :deep(.q-field__native) {
  color: var(--text-primary) !important;
}

.setup-actions {
  padding: 16px 24px !important;
  border-top: 1px solid var(--border) !important;
}

.setup-btn {
  background: var(--gradient-button) !important;
  border-radius: 8px;
  font-weight: 600;
  padding: 8px 24px;
}

/* Estilos específicos para modo oscuro en el dialog */
.body--dark .setup-dialog-card {
  background: rgba(30, 30, 30, 0.95) !important;
  border-color: #374151 !important;
}

.body--dark .setup-input :deep(.q-field__control) {
  background: rgba(30, 30, 30, 0.8) !important;
  border-color: #374151 !important;
}
</style>
