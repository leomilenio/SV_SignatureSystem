<template>
  <div class="media-uploader">
    <!-- Zona de arrastrar y soltar mejorada -->
    <div 
      class="upload-zone"
      :class="{ 
        'drag-over': isDragOver, 
        'has-file': selectedFile,
        'uploading': isUploading 
      }"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave" 
      @drop.prevent="handleDrop"
      @click="triggerFileSelect"
    >
      <input 
        ref="fileInput"
        type="file"
        accept="image/*,video/*"
        @change="handleFileSelect"
        class="hidden-input"
      />
      
      <!-- Estado normal - sin archivo -->
      <div v-if="!selectedFile && !isUploading" class="upload-prompt">
        <div class="upload-icon">
          <q-icon name="cloud_upload" size="3rem" />
        </div>
        <h4>Arrastra archivos aquí</h4>
        <p>o haz clic para seleccionar</p>
        <div class="supported-formats">
          <q-chip size="sm" color="primary" text-color="white">JPG</q-chip>
          <q-chip size="sm" color="primary" text-color="white">PNG</q-chip>
          <q-chip size="sm" color="secondary" text-color="white">MP4</q-chip>
          <q-chip size="sm" color="secondary" text-color="white">WebM</q-chip>
        </div>
        <div class="size-limit">Máximo 100MB</div>
      </div>

      <!-- Archivo seleccionado -->
      <div v-else-if="selectedFile && !isUploading" class="file-selected">
        <div class="file-preview">
          <!-- Vista previa de imagen -->
          <div v-if="previewUrl && metadata.media_type === 'image'" class="image-preview">
            <img :src="previewUrl" :alt="selectedFile.name" />
          </div>
          <!-- Icono para videos y otros archivos -->
          <div v-else class="file-icon">
            <q-icon :name="getFileIcon(selectedFile.type)" size="3rem" />
          </div>
        </div>
        
        <div class="file-details">
          <h4>{{ selectedFile.name }}</h4>
          <div class="file-meta">
            <q-chip size="sm" :color="getTypeColor(metadata.media_type)" text-color="white">
              {{ metadata.media_type?.toUpperCase() || 'ARCHIVO' }}
            </q-chip>
            <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
          </div>
        </div>

        <q-btn 
          round 
          flat 
          icon="close" 
          @click.stop="resetForm"
          class="remove-file"
          size="sm"
        />
      </div>

      <!-- Estado de subida -->
      <div v-else-if="isUploading" class="upload-progress">
        <div class="progress-circle">
          <q-circular-progress
            :value="uploadProgress.percent"
            size="60px"
            :thickness="0.2"
            color="primary"
            track-color="grey-3"
            class="q-ma-md"
          />
          <div class="progress-text">
            {{ Math.round(uploadProgress.percent) }}%
          </div>
        </div>
        <h4>{{ uploadProgress.message }}</h4>
        <p>{{ selectedFile?.name }}</p>
      </div>
    </div>

    <!-- Formulario de metadatos mejorado -->
    <div v-if="selectedFile && !isUploading" class="metadata-form">
      <div class="form-section">
        <h5>Detalles del archivo</h5>
        
        <div class="form-grid">
          <q-input
            v-model="metadata.filename"
            label="Nombre del archivo"
            outlined
            class="filename-input"
            :rules="[val => !!val || 'El nombre es requerido']"
          >
            <template v-slot:prepend>
              <q-icon name="edit" />
            </template>
          </q-input>

          <q-select
            v-model="metadata.media_type"
            :options="mediaTypeOptions"
            label="Tipo de contenido"
            outlined
            emit-value
            map-options
            :rules="[val => !!val || 'Selecciona el tipo']"
          >
            <template v-slot:prepend>
              <q-icon name="category" />
            </template>
          </q-select>

          <q-input
            v-model.number="metadata.duration"
            label="Duración (segundos)"
            type="number"
            outlined
            :hint="metadata.media_type === 'image' ? 'Para imágenes: tiempo de visualización' : 'Se detectará automáticamente para videos'"
          >
            <template v-slot:prepend>
              <q-icon name="schedule" />
            </template>
          </q-input>
        </div>
      </div>

      <!-- Acciones -->
      <div class="form-actions">
        <q-btn
          label="Cancelar"
          color="grey-7"
          flat
          @click="resetForm"
          :disable="isUploading"
          class="cancel-btn"
        />
        <q-btn
          label="Subir archivo"
          color="primary"
          unelevated
          @click="uploadFile"
          :loading="isUploading"
          :disable="!isFormValid"
          class="upload-btn"
        >
          <template v-slot:loading>
            Subiendo...
          </template>
        </q-btn>
      </div>
    </div>

    <!-- Mensaje de éxito -->
    <div v-if="uploadSuccess" class="success-message">
      <q-icon name="check_circle" size="2rem" color="positive" />
      <h4>¡Archivo subido correctamente!</h4>
      <p>{{ uploadedFileName }} está listo para usar</p>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, nextTick } from 'vue'
import { useToast } from 'vue-toastification'
import { mediaAPI, handleFileError } from '../services/api'

export default {
  name: 'MediaUploader',
  emits: ['upload-complete', 'upload-error', 'uploaded'],
  setup(props, { emit }) {
    const toast = useToast()

    // Referencias del DOM
    const fileInput = ref(null)

    // Estados reactivos
    const selectedFile = ref(null)
    const isUploading = ref(false)
    const isDragOver = ref(false)
    const previewUrl = ref(null)
    const uploadSuccess = ref(false)
    const uploadedFileName = ref('')
    
    const metadata = reactive({
      filename: '',
      media_type: '',
      duration: 5
    })

    const uploadProgress = reactive({
      show: false,
      percent: 0,
      message: ''
    })

    // Opciones de tipo de media
    const mediaTypeOptions = [
      { label: 'Imagen', value: 'image' },
      { label: 'Video', value: 'video' }
    ]

    // Computed
    const isFormValid = computed(() => {
      return selectedFile.value && 
             metadata.filename.trim() && 
             metadata.media_type &&
             metadata.duration > 0
    })

    // Manejo de archivos
    const triggerFileSelect = () => {
      if (!isUploading.value) {
        fileInput.value?.click()
      }
    }

    const handleFileSelect = (event) => {
      const file = event.target.files?.[0] || event
      if (file && file instanceof File) {
        processFile(file)
      }
    }

    const processFile = (file) => {
      // Validar tamaño
      if (file.size > 104857600) { // 100MB
        toast.error('El archivo es demasiado grande. Máximo 100MB.')
        return
      }

      // Validar tipo
      if (!file.type.startsWith('image/') && !file.type.startsWith('video/')) {
        toast.error('Tipo de archivo no soportado. Solo imágenes y videos.')
        return
      }

      selectedFile.value = file
      metadata.filename = file.name.replace(/\.[^/.]+$/, "") // Remover extensión
      
      // Detectar tipo automáticamente
      if (file.type.startsWith('image/')) {
        metadata.media_type = 'image'
        metadata.duration = 5 // Duración por defecto para imágenes
        createImagePreview(file)
      } else if (file.type.startsWith('video/')) {
        metadata.media_type = 'video'
        metadata.duration = 30 // Valor temporal, será detectado por FFmpeg
        previewUrl.value = null
      }

      uploadSuccess.value = false
    }

    const createImagePreview = (file) => {
      const reader = new FileReader()
      reader.onload = (e) => {
        previewUrl.value = e.target.result
      }
      reader.readAsDataURL(file)
    }

    // Manejo de drag and drop
    const handleDragOver = (event) => {
      event.preventDefault()
      isDragOver.value = true
    }

    const handleDragLeave = (event) => {
      event.preventDefault()
      isDragOver.value = false
    }

    const handleDrop = (event) => {
      event.preventDefault()
      isDragOver.value = false
      
      const files = event.dataTransfer.files
      if (files.length > 0) {
        processFile(files[0])
      }
    }

    // Utilidades
    const getFileIcon = (mimeType) => {
      if (!mimeType) return 'description'
      if (mimeType.startsWith('image/')) return 'image'
      if (mimeType.startsWith('video/')) return 'videocam'
      return 'description'
    }

    const getTypeColor = (type) => {
      switch (type) {
        case 'image': return 'orange'
        case 'video': return 'purple'
        default: return 'grey'
      }
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    // Subir archivo
    const uploadFile = async () => {
      if (!isFormValid.value) {
        toast.warning('Completa todos los campos requeridos')
        return
      }

      isUploading.value = true
      uploadProgress.show = true
      uploadProgress.percent = 0
      uploadProgress.message = 'Preparando subida...'

      try {
        // Simular progreso inicial
        const progressInterval = setInterval(() => {
          if (uploadProgress.percent < 85) {
            uploadProgress.percent += Math.random() * 15
            if (uploadProgress.percent < 30) {
              uploadProgress.message = 'Analizando archivo...'
            } else if (uploadProgress.percent < 60) {
              uploadProgress.message = 'Subiendo archivo...'
            } else {
              uploadProgress.message = 'Procesando multimedia...'
            }
          }
        }, 300)

        const fileData = {
          file: selectedFile.value,
          filename: metadata.filename,
          media_type: metadata.media_type,
          duration: metadata.duration
        }

        const response = await mediaAPI.upload(fileData)

        clearInterval(progressInterval)
        uploadProgress.percent = 100
        uploadProgress.message = '¡Completado!'

        // Mostrar éxito
        uploadedFileName.value = metadata.filename
        uploadSuccess.value = true
        
        toast.success(`✅ ${metadata.filename} subido correctamente`)
        
        // Emitir eventos
        emit('upload-complete', response.data)
        emit('uploaded', response.data)
        
        // Reset después de mostrar éxito
        setTimeout(() => {
          resetForm()
        }, 3000)

      } catch (error) {
        console.error('Error subiendo archivo:', error)
        handleFileError(error, toast)
        emit('upload-error', error)
        uploadProgress.message = 'Error en la subida'
        
      } finally {
        isUploading.value = false
        setTimeout(() => {
          uploadProgress.show = false
        }, 2000)
      }
    }

    // Resetear formulario
    const resetForm = () => {
      selectedFile.value = null
      metadata.filename = ''
      metadata.media_type = ''
      metadata.duration = 5
      previewUrl.value = null
      uploadProgress.show = false
      uploadProgress.percent = 0
      uploadSuccess.value = false
      uploadedFileName.value = ''
      isDragOver.value = false
      
      // Limpiar input de archivo
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    return {
      // Refs
      fileInput,
      
      // Estados
      selectedFile,
      metadata,
      isUploading,
      isDragOver,
      previewUrl,
      uploadProgress,
      uploadSuccess,
      uploadedFileName,
      
      // Computed
      isFormValid,
      
      // Opciones
      mediaTypeOptions,
      
      // Métodos
      triggerFileSelect,
      handleFileSelect,
      handleDragOver,
      handleDragLeave,
      handleDrop,
      getFileIcon,
      getTypeColor,
      formatFileSize,
      uploadFile,
      resetForm
    }
  }
}
</script>
 
 <style scoped>
.media-uploader {
  width: 100%;
}

/* Zona de subida principal */
.upload-zone {
  position: relative;
  min-height: 200px;
  border: 2px dashed var(--border, #e0e0e0);
  border-radius: 16px;
  background: var(--surface, #ffffff);
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  overflow: hidden;
}

.upload-zone:hover {
  border-color: var(--primary, #1976d2);
  background: rgba(var(--primary-rgb, 25, 118, 210), 0.02);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(var(--primary-rgb, 25, 118, 210), 0.15);
}

.upload-zone.drag-over {
  border-color: var(--primary, #1976d2);
  background: rgba(var(--primary-rgb, 25, 118, 210), 0.08);
  border-style: solid;
  box-shadow: 0 0 20px rgba(var(--primary-rgb, 25, 118, 210), 0.2);
}

.upload-zone.has-file {
  border-style: solid;
  border-color: var(--positive, #21ba45);
  background: rgba(var(--positive-rgb, 33, 186, 69), 0.02);
  min-height: 160px;
}

.upload-zone.uploading {
  border-color: var(--warning, #f2c037);
  background: rgba(var(--warning-rgb, 242, 192, 55), 0.02);
  cursor: not-allowed;
}

.hidden-input {
  display: none;
}

/* Estado inicial - prompt */
.upload-prompt {
  text-align: center;
  padding: 32px 24px;
}

.upload-icon {
  margin-bottom: 16px;
  color: var(--text-secondary, #666);
}

.upload-prompt h4 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary, #333);
}

.upload-prompt p {
  margin: 0 0 20px 0;
  color: var(--text-secondary, #666);
  font-size: 0.95rem;
}

.supported-formats {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.size-limit {
  font-size: 0.85rem;
  color: var(--text-secondary, #666);
}

/* Archivo seleccionado */
.file-selected {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  width: 100%;
  position: relative;
}

.file-preview {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 12px;
  overflow: hidden;
  background: var(--background, #f5f5f5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

.file-icon {
  color: var(--text-secondary, #666);
}

.file-details {
  flex-grow: 1;
  min-width: 0;
}

.file-details h4 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary, #333);
  word-break: break-word;
}

.file-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.file-size {
  font-size: 0.9rem;
  color: var(--text-secondary, #666);
}

.remove-file {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
}

/* Progreso de subida */
.upload-progress {
  text-align: center;
  padding: 32px 24px;
  position: relative;
}

.progress-circle {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-primary, #333);
}

.upload-progress h4 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary, #333);
}

.upload-progress p {
  margin: 0;
  color: var(--text-secondary, #666);
  font-size: 0.9rem;
}

/* Formulario de metadatos */
.metadata-form {
  background: var(--surface, #ffffff);
  border: 1px solid var(--border, #e0e0e0);
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 24px;
}

.form-section {
  padding: 24px;
  border-bottom: 1px solid var(--border, #e0e0e0);
}

.form-section h5 {
  margin: 0 0 20px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary, #333);
}

.form-grid {
  display: grid;
  gap: 16px;
}

.filename-input {
  grid-column: 1 / -1;
}

.form-actions {
  padding: 20px 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  background: rgba(var(--border-rgb, 224, 224, 224), 0.1);
}

.cancel-btn {
  min-width: 100px;
}

.upload-btn {
  min-width: 140px;
  font-weight: 600;
}

/* Mensaje de éxito */
.success-message {
  text-align: center;
  padding: 32px 24px;
  background: rgba(var(--positive-rgb, 33, 186, 69), 0.05);
  border: 1px solid rgba(var(--positive-rgb, 33, 186, 69), 0.2);
  border-radius: 16px;
  margin-bottom: 24px;
}

.success-message h4 {
  margin: 16px 0 8px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--positive, #21ba45);
}

.success-message p {
  margin: 0;
  color: var(--text-secondary, #666);
  font-size: 0.95rem;
}

/* Responsive */
@media (max-width: 768px) {
  .upload-zone {
    min-height: 160px;
  }
  
  .upload-prompt {
    padding: 24px 16px;
  }
  
  .upload-prompt h4 {
    font-size: 1.1rem;
  }
  
  .file-selected {
    padding: 20px 16px;
    gap: 16px;
    flex-direction: column;
    text-align: center;
  }
  
  .file-preview {
    width: 60px;
    height: 60px;
  }
  
  .form-section {
    padding: 20px 16px;
  }
  
  .form-actions {
    padding: 16px;
    flex-direction: column;
  }
  
  .form-actions .q-btn {
    width: 100%;
  }
}

/* Dark mode */
.body--dark .upload-zone {
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.02);
}

.body--dark .upload-zone:hover {
  background: rgba(var(--primary-rgb, 25, 118, 210), 0.05);
}

.body--dark .metadata-form {
  background: rgba(255, 255, 255, 0.02);
  border-color: rgba(255, 255, 255, 0.12);
}

.body--dark .form-section {
  border-color: rgba(255, 255, 255, 0.12);
}

.body--dark .form-actions {
  background: rgba(255, 255, 255, 0.02);
}
</style>
