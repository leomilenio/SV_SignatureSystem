<template>
  <div class="media-uploader">
    <q-card>
      <q-card-section>
        <div class="text-h6 q-mb-md">
          <q-icon name="cloud_upload" class="q-mr-sm" />
          Subir Archivo Multimedia
        </div>
        
        <!-- Zona de arrastrar y soltar -->
        <q-file
          v-model="selectedFile"
          outlined
          multiple
          accept="image/*,video/*"
          max-file-size="104857600"
          @input="handleFileSelect"
          class="q-mb-md"
        >
          <template v-slot:prepend>
            <q-icon name="attach_file" />
          </template>
          
          <template v-slot:hint>
            Formatos soportados: JPG, PNG, GIF, MP4, AVI, MOV (máximo 100MB)
          </template>
        </q-file>

        <!-- Información del archivo seleccionado -->
        <div v-if="selectedFile" class="file-info q-mb-md">
          <q-item>
            <q-item-section avatar>
              <q-icon :name="getFileIcon(selectedFile.type)" size="2rem" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ selectedFile.name }}</q-item-label>
              <q-item-label caption>
                {{ formatFileSize(selectedFile.size) }} • {{ selectedFile.type }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </div>

        <!-- Formulario de metadatos -->
        <q-form v-if="selectedFile" @submit="uploadFile" class="q-gutter-md">
          <q-input
            v-model="metadata.filename"
            label="Nombre del archivo"
            outlined
            :rules="[val => !!val || 'Requerido']"
          />
          
          <q-select
            v-model="metadata.media_type"
            :options="mediaTypeOptions"
            label="Tipo de media"
            outlined
            :rules="[val => !!val || 'Requerido']"
          />
          
          <q-input
            v-model.number="metadata.duration"
            label="Duración (segundos)"
            type="number"
            outlined
            hint="Para imágenes usar 0, para videos será detectado automáticamente"
          />
          
          <div class="row q-gutter-md">
            <q-btn
              type="submit"
              label="Subir Archivo"
              color="primary"
              icon="cloud_upload"
              :loading="isUploading"
              :disable="!selectedFile"
              class="col"
            />
            
            <q-btn
              label="Cancelar"
              color="grey"
              icon="cancel"
              @click="resetForm"
              :disable="isUploading"
              class="col"
            />
          </div>
        </q-form>

        <!-- Progreso de subida -->
        <div v-if="uploadProgress.show" class="q-mt-md">
          <q-linear-progress
            :value="uploadProgress.percent / 100"
            color="primary"
            size="20px"
            class="q-mb-sm"
          />
          <div class="text-center">
            {{ uploadProgress.message }} ({{ uploadProgress.percent }}%)
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { mediaAPI, handleFileError } from '../services/api'

export default {
  name: 'MediaUploader',
  emits: ['upload-complete', 'upload-error'],
  setup(props, { emit }) {
    const toast = useToast()

    // Estados reactivos
    const selectedFile = ref(null)
    const isUploading = ref(false)
    
    const metadata = reactive({
      filename: '',
      media_type: '',
      duration: 0
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

    // Manejar selección de archivo
    const handleFileSelect = (file) => {
      if (file) {
        metadata.filename = file.name
        
        // Detectar tipo automáticamente
        if (file.type.startsWith('image/')) {
          metadata.media_type = 'image'
          metadata.duration = 0
        } else if (file.type.startsWith('video/')) {
          metadata.media_type = 'video'
          metadata.duration = 30 // Valor temporal, será detectado por FFmpeg
        }
      }
    }

    // Obtener icono según tipo de archivo
    const getFileIcon = (mimeType) => {
      if (mimeType.startsWith('image/')) {
        return 'image'
      } else if (mimeType.startsWith('video/')) {
        return 'movie'
      }
      return 'description'
    }

    // Formatear tamaño de archivo
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    // Subir archivo
    const uploadFile = async () => {
      if (!selectedFile.value) {
        toast.warning('Selecciona un archivo')
        return
      }

      isUploading.value = true
      uploadProgress.show = true
      uploadProgress.percent = 0
      uploadProgress.message = 'Preparando subida...'

      try {
        // Simular progreso
        const progressInterval = setInterval(() => {
          if (uploadProgress.percent < 90) {
            uploadProgress.percent += Math.random() * 10
            uploadProgress.message = `Subiendo ${metadata.filename}...`
          }
        }, 200)

        const fileData = {
          file: selectedFile.value,
          filename: metadata.filename,
          media_type: metadata.media_type,
          duration: metadata.duration
        }

        const response = await mediaAPI.upload(fileData)

        clearInterval(progressInterval)
        uploadProgress.percent = 100
        uploadProgress.message = 'Archivo subido exitosamente'

        toast.success(`✅ ${metadata.filename} subido correctamente`)
        
        emit('upload-complete', response.data)
        
        // Reset después de un momento
        setTimeout(resetForm, 2000)

      } catch (error) {
        console.error('Error subiendo archivo:', error)
        handleFileError(error, toast)
        emit('upload-error', error)
        
      } finally {
        isUploading.value = false
        setTimeout(() => {
          uploadProgress.show = false
        }, 3000)
      }
    }

    // Resetear formulario
    const resetForm = () => {
      selectedFile.value = null
      metadata.filename = ''
      metadata.media_type = ''
      metadata.duration = 0
      uploadProgress.show = false
      uploadProgress.percent = 0
    }

    return {
      selectedFile,
      metadata,
      isUploading,
      uploadProgress,
      mediaTypeOptions,
      handleFileSelect,
      getFileIcon,
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

.file-info {
  background: rgba(25, 118, 210, 0.1);
  border-radius: 8px;
  padding: 8px;
}

@media (max-width: 600px) {
  .row.q-gutter-md {
    flex-direction: column;
  }
  
  .row.q-gutter-md .col {
    width: 100%;
  }
}
</style>
