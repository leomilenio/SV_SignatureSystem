<template>
  <div class="media-manager">
    <!-- Theme Toggle -->
    <ThemeToggle class="theme-toggle" />
    
    <!-- Header Section -->
    <div class="manager-header">
      <div class="header-content">
        <div class="header-info">
          <h1>
            <q-icon name="perm_media" class="header-icon" />
            Gestión de Medios
          </h1>
          <p>Administra tu biblioteca multimedia completa</p>
        </div>
        <div class="header-actions">
          <q-btn
            label="Volver al Admin"
            icon="arrow_back"
            color="white"
            unelevated
            class="back-btn"
            @click="$router.push('/admin')"
          />
        </div>
      </div>
    </div>

    <!-- Content Section -->
    <div class="manager-content">
      <!-- Upload Section -->
      <div class="upload-section">
        <div class="section-title">
          <h3>
            <q-icon name="cloud_upload" />
            Subir Nuevo Contenido
          </h3>
        </div>
        <MediaUploader 
          @upload-complete="handleUploadComplete"
          @upload-error="handleUploadError"
        />
      </div>

      <!-- Media Gallery Section -->
      <div class="gallery-section">
        <MediaGallery
          :media-files="mediaFiles"
          :backend-base-url="backendBaseUrl"
          :loading="mediaLoading"
          mode="full"
          title="Biblioteca Multimedia"
          subtitle="Gestiona tu biblioteca completa"
          @refresh="loadMedia"
          @edit="editMedia"
          @delete="deleteMedia"
        />
      </div>
    </div>

    <!-- Edit Media Dialog -->
    <EditMediaDialog
      v-model="editDialog"
      :media="selectedMedia"
      @save="handleEditSave"
    />

    <!-- Edit Media Dialog -->
    <EditMediaDialog
      v-model="editDialog"
      :media="selectedMedia"
      @save="handleEditSave"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useQuasar } from 'quasar'

// Componentes
import ThemeToggle from '../components/ThemeToggle.vue'
import MediaUploader from '../components/MediaUploader.vue'
import MediaGallery from '../components/dashboard/MediaGallery.vue'
import EditMediaDialog from '../components/dashboard/dialogs/EditMediaDialog.vue'

// Composables y servicios
import { useTheme } from '../composables/useTheme'
import { useMediaUrl } from '../composables/useMediaUrl'
import { mediaAPI } from '../services/api'

export default {
  name: 'MediaManager',
  components: {
    ThemeToggle,
    MediaUploader,
    MediaGallery,
    EditMediaDialog
  },
  setup() {
    console.log('🎬 MediaManager component setup() called')
    console.log('📍 Current URL:', window.location.href)
    
    const $router = useRouter()
    const $route = useRoute()
    const toast = useToast()
    const $q = useQuasar()
    const { isDarkMode } = useTheme()
    const { backendBaseUrl } = useMediaUrl()
    
    // Estados reactivos
    const mediaFiles = ref([])
    const mediaLoading = ref(false)
    const editDialog = ref(false)
    const selectedMedia = ref(null)

    // Cargar medios
    const loadMedia = async () => {
      console.log('📁 Cargando medios...')
      mediaLoading.value = true
      try {
        const response = await mediaAPI.list()
        mediaFiles.value = response.data || []
        console.log(`✅ ${mediaFiles.value.length} archivos multimedia cargados`)
      } catch (error) {
        console.error('❌ Error cargando medios:', error)
        toast.error('Error al cargar los archivos multimedia')
        mediaFiles.value = []
      } finally {
        mediaLoading.value = false
      }
    }

    // Actualizar medio
    const updateMedia = async (mediaId, updateData) => {
      try {
        await mediaAPI.update(mediaId, updateData)
        return true
      } catch (error) {
        console.error('❌ Error actualizando medio:', error)
        throw error
      }
    }

    // Eliminar medio
    const deleteMediaFile = async (mediaId) => {
      try {
        await mediaAPI.delete(mediaId)
        return true
      } catch (error) {
        console.error('❌ Error eliminando medio:', error)
        throw error
      }
    }

    // Manejar subida exitosa
    const handleUploadComplete = (newMedia) => {
      console.log('✅ Archivo subido exitosamente:', newMedia)
      toast.success(`Archivo "${newMedia.filename}" subido correctamente`)
      loadMedia() // Recargar la lista
    }

    // Manejar error de subida
    const handleUploadError = (error) => {
      console.error('❌ Error en subida:', error)
      toast.error('Error al subir el archivo')
    }

    // Editar medio
    const editMedia = (media) => {
      console.log('✏️ Editando medio:', media)
      selectedMedia.value = media
      editDialog.value = true
    }

    // Manejar guardado de edición
    const handleEditSave = async (updatedMedia) => {
      try {
        await updateMedia(updatedMedia.id, updatedMedia)
        toast.success('Medio actualizado correctamente')
        editDialog.value = false
        loadMedia() // Recargar la lista
      } catch (error) {
        console.error('❌ Error actualizando medio:', error)
        toast.error('Error al actualizar el medio')
      }
    }

    // Eliminar medio
    const deleteMedia = async (mediaId) => {
      $q.dialog({
        title: 'Confirmar eliminación',
        message: '¿Estás seguro de que quieres eliminar este archivo multimedia?',
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          await deleteMediaFile(mediaId)
          toast.success('Archivo eliminado correctamente')
          loadMedia() // Recargar la lista
        } catch (error) {
          console.error('❌ Error eliminando medio:', error)
          toast.error('Error al eliminar el archivo')
        }
      })
    }

    // Inicialización
    onMounted(async () => {
      console.log('🚀 MediaManager mounted')
      $q.dark.set(isDarkMode.value)
      await loadMedia()
    })

    return {
      // Estados
      mediaFiles,
      mediaLoading,
      editDialog,
      selectedMedia,
      backendBaseUrl,
      $route,
      
      // Métodos
      loadMedia,
      handleUploadComplete,
      handleUploadError,
      editMedia,
      handleEditSave,
      deleteMedia
    }
  }
}
</script>

<style scoped>
.media-manager {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  color: #333;
}

.body--dark .media-manager {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  color: #e2e8f0;
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

/* Header Styles */
.manager-header {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
  padding: 60px 20px 40px;
  margin-bottom: 30px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.header-info h1 {
  color: white;
  font-size: 2.5rem;
  font-weight: 600;
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-icon {
  font-size: 3rem !important;
}

.header-info p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.back-btn {
  background: rgba(255, 255, 255, 0.2) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white !important;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Content Styles */
.manager-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 40px;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.upload-section,
.gallery-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.body--dark .upload-section,
.body--dark .gallery-section {
  background: rgba(30, 30, 30, 0.95);
  border-color: #374151;
}

.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e5e7eb;
}

.body--dark .section-title {
  border-bottom-color: #374151;
}

.section-title h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.body--dark .section-title h3 {
  color: #e2e8f0;
}

.section-title .q-icon {
  color: #6366f1;
  font-size: 1.8rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-info h1 {
    font-size: 2rem;
  }
  
  .manager-content {
    padding: 0 15px 40px;
  }
  
  .upload-section,
  .gallery-section {
    padding: 20px;
  }
  
  .section-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
