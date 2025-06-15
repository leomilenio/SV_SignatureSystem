<template>
  <div class="config-container">
    <!-- Toggle de tema -->
    <div class="theme-toggle-container">
      <ThemeToggle />
    </div>
    
    <!-- Loading overlay -->
    <div v-if="initialLoading" class="loading-overlay">
      <q-spinner-dots size="3rem" />
      <p>Cargando configuración...</p>
    </div>
    
    <div v-else class="config-content">
      <div class="config-card">
        <!-- Header con información del estado -->
        <div class="config-header">
          <div class="header-content">
            <div class="logo-container">
              <q-icon name="business" class="main-logo" />
              <div class="logo-glow"></div>
            </div>
            <h2 class="page-title">
              {{ isUpdate ? 'Actualizar Negocio' : 'Configurar Negocio' }}
            </h2>
            <p class="page-subtitle">
              {{ isUpdate ? 'Modifica la información de tu negocio' : 'Configura tu espacio LGBT+ friendly' }}
            </p>
            <div class="pride-divider"></div>
            
            <!-- Status badge -->
            <div v-if="isUpdate" class="status-badge">
              <q-icon name="check_circle" />
              <span>Negocio ya configurado</span>
            </div>
          </div>
        </div>

        <!-- Form section -->
        <div class="config-form-section">
          <q-form @submit.prevent="save" class="config-form">
            <!-- Nombre del negocio -->
            <div class="input-group">
              <q-input 
                v-model="form.name" 
                label="Nombre del negocio" 
                outlined
                dense
                required 
                class="modern-input"
                :rules="[val => !!val || 'El nombre es requerido']"
              >
                <template v-slot:prepend>
                  <q-icon name="store" class="input-icon" />
                </template>
              </q-input>
            </div>

            <!-- Upload y preview del logo -->
            <div class="input-group">
              <div class="logo-upload-section">
                <div class="logo-upload-header">
                  <q-icon name="image" class="input-icon" />
                  <span>Logo del negocio</span>
                </div>
                
                <!-- Vista previa del logo actual -->
                <div v-if="currentLogoPreview" class="current-logo-preview">
                  <div class="preview-label">Logo actual:</div>
                  <div class="logo-preview-container">
                    <img :src="currentLogoPreview" alt="Logo actual" class="logo-preview" />
                    <q-btn 
                      flat 
                      round 
                      icon="close" 
                      size="sm" 
                      @click="clearCurrentLogo"
                      class="remove-logo-btn"
                    />
                  </div>
                </div>

                <!-- Upload de nuevo logo -->
                <q-file 
                  v-model="form.logo" 
                  label="Subir nuevo logo (PNG, JPG, JPEG)" 
                  accept="image/png,image/jpg,image/jpeg"
                  outlined
                  dense
                  class="modern-input"
                  @update:model-value="onLogoSelected"
                  :max-file-size="5242880"
                >
                  <template v-slot:prepend>
                    <q-icon name="upload" />
                  </template>
                </q-file>

                <!-- Vista previa del nuevo logo -->
                <div v-if="newLogoPreview" class="new-logo-preview">
                  <div class="preview-label">Nuevo logo:</div>
                  <div class="logo-preview-container">
                    <img :src="newLogoPreview" alt="Nuevo logo" class="logo-preview" />
                    <q-btn 
                      flat 
                      round 
                      icon="close" 
                      size="sm" 
                      @click="clearNewLogo"
                      class="remove-logo-btn"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="form-actions">
              <q-btn 
                v-if="isUpdate"
                flat
                color="grey"
                label="Cancelar"
                @click="goToAdmin"
                class="cancel-btn"
              />
              <q-btn 
                type="submit" 
                :label="isUpdate ? 'Actualizar Configuración' : 'Guardar Configuración'"
                class="save-btn"
                size="md"
                unelevated
                :loading="loading" 
                :disable="!form.name"
              />
            </div>
          </q-form>
        </div>

        <!-- Footer con mensaje inclusivo -->
        <div class="footer-section">
          <div class="diversity-message">
            <q-icon name="favorite" class="heart-icon" />
            <span>Programado por un gei 🏳️‍🌈</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { businessAPI } from '../services/api'
import { useToast } from 'vue-toastification'
import { useTheme } from '../composables/useTheme'
import ThemeToggle from '../components/ThemeToggle.vue'

export default {
  name: 'ConfigView',
  components: {
    ThemeToggle
  },
  setup() {
    const router = useRouter()
    const toast = useToast()
    const { loadTheme } = useTheme()
    
    // Estado reactivo
    const loading = ref(false)
    const initialLoading = ref(true)
    const isUpdate = ref(false)
    const currentBusiness = ref(null)
    const currentLogoPreview = ref(null)
    const newLogoPreview = ref(null)
    
    const form = ref({ 
      name: '', 
      logo: null 
    })

    // Cargar datos existentes del negocio
    const loadBusinessData = async () => {
      try {
        const response = await businessAPI.get()
        if (response.data) {
          currentBusiness.value = response.data
          form.value.name = response.data.name || ''
          isUpdate.value = true
          
          // Cargar logo si existe
          if (response.data.id) {
            try {
              const logoResponse = await businessAPI.getLogo()
              if (logoResponse.data?.logo) {
                currentLogoPreview.value = `data:image/png;base64,${logoResponse.data.logo}`
              }
            } catch (error) {
              console.log('No hay logo existente')
            }
          }
        }
      } catch (error) {
        // Si no existe negocio, es creación
        console.log('No hay negocio configurado, será creación')
        isUpdate.value = false
      } finally {
        initialLoading.value = false
      }
    }

    // Manejar selección de logo
    const onLogoSelected = (file) => {
      if (file) {
        // Validar tipo de archivo
        const validTypes = ['image/png', 'image/jpeg', 'image/jpg']
        if (!validTypes.includes(file.type)) {
          toast.error('Solo se permiten archivos PNG, JPG o JPEG')
          form.value.logo = null
          return
        }

        // Validar tamaño (5MB max)
        if (file.size > 5242880) {
          toast.error('El archivo es muy grande. Máximo 5MB.')
          form.value.logo = null
          return
        }

        // Crear vista previa
        const reader = new FileReader()
        reader.onload = (e) => {
          newLogoPreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      } else {
        newLogoPreview.value = null
      }
    }

    // Limpiar logo actual
    const clearCurrentLogo = () => {
      currentLogoPreview.value = null
      // Si estamos actualizando, esto significa que queremos quitar el logo
      if (isUpdate.value) {
        toast.info('El logo actual será eliminado al guardar')
      }
    }

    // Limpiar nuevo logo
    const clearNewLogo = () => {
      form.value.logo = null
      newLogoPreview.value = null
    }

    // Guardar configuración
    const save = async () => {
      if (!form.value.name) {
        toast.warning('Ingresa el nombre del negocio')
        return
      }

      loading.value = true
      
      try {
        const formData = {
          name: form.value.name,
          logo: form.value.logo
        }

        let response
        if (isUpdate.value) {
          // Si estamos actualizando
          response = await businessAPI.update(formData)
          toast.success('¡Negocio actualizado exitosamente!')
        } else {
          // Si estamos creando
          response = await businessAPI.create(formData)
          toast.success('¡Negocio configurado exitosamente!')
        }

        // Redirigir según el contexto
        if (isUpdate.value) {
          router.push('/admin')
        } else {
          router.push('/login')
        }

      } catch (err) {
        const errorMessage = isUpdate.value 
          ? 'Error actualizando la configuración del negocio'
          : 'Error guardando la configuración del negocio'
        
        toast.error(errorMessage)
        console.error('Error:', err)
      } finally {
        loading.value = false
      }
    }

    // Navegar al admin
    const goToAdmin = () => {
      router.push('/admin')
    }

    // Inicialización
    onMounted(async () => {
      loadTheme()
      await loadBusinessData()
    })

    return { 
      form, 
      save, 
      loading,
      initialLoading,
      isUpdate,
      currentBusiness,
      currentLogoPreview,
      newLogoPreview,
      onLogoSelected,
      clearCurrentLogo,
      clearNewLogo,
      goToAdmin
    }
  }
}
</script>

<style scoped>
.config-container {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
  padding: 20px 0;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.theme-toggle-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  text-align: center;
}

.loading-overlay p {
  margin-top: 16px;
  font-size: 1.1rem;
  font-weight: 500;
}

.config-content {
  width: 100%;
  max-width: 600px;
  padding: 0 20px;
}

.config-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: var(--shadow-xl);
}

.config-header {
  text-align: center;
  background: var(--surface);
  padding: 40px 24px 24px;
  border-bottom: 1px solid var(--border);
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-container {
  position: relative;
  display: inline-block;
  margin-bottom: 24px;
}

.main-logo {
  font-size: 4rem;
  color: var(--primary);
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, rgba(var(--primary-rgb), 0.3), transparent);
  border-radius: 50%;
  animation: pulse 3s ease-in-out infinite;
  z-index: -1;
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
}

.page-title {
  margin: 0 0 8px 0;
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.page-subtitle {
  margin: 0 0 24px 0;
  font-size: 0.95rem;
  color: var(--text-secondary);
}

.pride-divider {
  width: 80px;
  height: 4px;
  background: var(--primary);
  border-radius: 2px;
  margin: 0 auto 16px auto;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(var(--success-rgb), 0.1);
  border: 1px solid var(--success);
  border-radius: 20px;
  color: var(--success);
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 16px;
}

.config-form-section {
  padding: 24px;
}

.config-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-group {
  position: relative;
}

.modern-input {
  border-radius: 12px !important;
}

.modern-input :deep(.q-field__control) {
  border-radius: 12px !important;
  border-color: var(--border);
  background: var(--background);
}

.modern-input :deep(.q-field__control:hover) {
  border-color: var(--primary);
}

.modern-input :deep(.q-field__control.q-field__control--focused) {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px rgba(var(--primary-rgb), 0.2);
}

.modern-input :deep(.q-field__native) {
  color: var(--text-primary) !important;
}

.modern-input :deep(.q-field__label) {
  color: var(--text-secondary) !important;
}

.modern-input :deep(.q-field__control.q-field__control--focused .q-field__label) {
  color: var(--primary) !important;
}

.modern-input :deep(.q-field__append) {
  color: var(--text-secondary);
}

.modern-input :deep(.q-field__prepend) {
  color: var(--primary);
}

/* Estilos específicos para q-file */
.modern-input.q-file :deep(.q-field__native) {
  color: var(--text-primary) !important;
}

.modern-input.q-file :deep(.q-field__control) {
  background: var(--background) !important;
}

.modern-input.q-file :deep(.q-field__label) {
  color: var(--text-secondary) !important;
}

.modern-input.q-file :deep(.q-field__control.q-field__control--focused .q-field__label) {
  color: var(--primary) !important;
}

.modern-input.q-file :deep(.q-field__control .q-field__native) {
  color: var(--text-primary) !important;
}

.modern-input.q-file :deep(.q-field__control .q-field__suffix) {
  color: var(--text-secondary) !important;
}

/* Asegurar que el placeholder sea visible */
.modern-input :deep(.q-field__native::placeholder) {
  color: var(--text-secondary) !important;
  opacity: 0.6;
}

.input-icon {
  color: var(--primary) !important;
}

/* Logo upload section */
.logo-upload-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.logo-upload-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--text-primary) !important;
}

.logo-upload-header .input-icon {
  color: var(--primary) !important;
}

.current-logo-preview,
.new-logo-preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.preview-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-secondary) !important;
}

.logo-preview-container {
  position: relative;
  display: inline-block;
  width: fit-content;
}

.logo-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 12px;
  border: 2px solid var(--border);
  box-shadow: var(--shadow-md);
}

.remove-logo-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  background: var(--negative) !important;
  color: white !important;
  width: 24px !important;
  height: 24px !important;
  min-width: 24px !important;
  border-radius: 50% !important;
}

.form-actions {
  margin-top: 16px;
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.cancel-btn {
  flex: 1;
  min-width: 120px;
  height: 50px;
  border-radius: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-secondary);
  border: 2px solid var(--border);
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: var(--hover-surface);
  border-color: var(--text-secondary);
}

.save-btn {
  flex: 2;
  min-width: 200px;
  height: 50px;
  border-radius: 12px;
  background: var(--primary);
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  transition: all 0.3s ease;
  border: none;
}

.save-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.save-btn:active {
  transform: translateY(0);
}

.save-btn:disabled {
  background: var(--text-secondary);
  opacity: 0.6;
  cursor: not-allowed;
}

.footer-section {
  padding: 24px;
  border-top: 1px solid var(--border);
  text-align: center;
  background: var(--background);
}

.diversity-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.heart-icon {
  color: var(--primary);
  animation: heartbeat 2s ease-in-out infinite;
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .config-container {
    padding: 10px;
  }
  
  .theme-toggle-container {
    top: 10px;
    right: 10px;
  }
  
  .config-header {
    padding: 30px 20px 20px;
  }
  
  .config-form-section {
    padding: 20px;
  }
  
  .page-title {
    font-size: 1.8rem;
  }
  
  .main-logo {
    font-size: 3rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .cancel-btn,
  .save-btn {
    flex: 1;
    min-width: 100%;
  }

  .logo-preview {
    width: 100px;
    height: 100px;
  }

  .config-content {
    max-width: 100%;
    padding: 0 10px;
  }
}

/* Smooth transitions */
.config-card {
  transition: all 0.3s ease;
}

.logo-preview {
  transition: all 0.3s ease;
}

.logo-preview:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-lg);
}

/* Focus styles */
.modern-input :deep(.q-field__control--focused) {
  outline: none;
}

.save-btn:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

.cancel-btn:focus {
  outline: 2px solid var(--text-secondary);
  outline-offset: 2px;
}

/* Loading state */
.save-btn .q-spinner {
  color: white;
}
</style>

