<template>
  <div class="media-card" :class="{ 'compact-card': compact }">
    <!-- Previsualización -->
    <div class="media-preview">
      <!-- Imagen -->
      <div v-if="isImage" class="image-preview">
        <img 
          :src="mediaUrl" 
          :alt="media.filename" 
          @error="handleImageError"
          class="preview-img" 
        />
      </div>
      
      <!-- Video -->
      <div v-else-if="isVideo" class="video-preview">
        <video 
          :src="mediaUrl" 
          class="preview-video" 
          muted 
          preload="metadata"
          @error="handleVideoError"
        />
        <div class="video-overlay">
          <q-icon name="play_circle_filled" size="2.5rem" class="play-icon" />
          <div class="video-duration" v-if="media.duration">
            {{ formatDuration(media.duration) }}
          </div>
        </div>
      </div>
      
      <!-- Otros archivos -->
      <div v-else class="file-preview">
        <q-icon :name="getFileIcon()" size="3rem" color="grey-6" />
      </div>
    </div>

    <!-- Información -->
    <div class="media-info">
      <h4 class="media-title" :title="media.filename">{{ media.filename }}</h4>
      <p class="media-meta">
        <span class="file-size">{{ formatFileSize(media.file_size || media.size) }}</span>
        <span v-if="media.created_at" class="upload-date">{{ formatDate(media.created_at) }}</span>
      </p>
    </div>

    <!-- Acciones -->
    <div class="media-actions">
      <q-btn 
        flat 
        round 
        icon="edit"
        @click="$emit('edit')"
        size="sm"
        color="primary"
      >
        <q-tooltip>Editar</q-tooltip>
      </q-btn>
      <q-btn 
        flat 
        round 
        icon="delete"
        @click="$emit('delete')"
        size="sm"
        color="negative"
      >
        <q-tooltip>Eliminar</q-tooltip>
      </q-btn>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  media: {
    type: Object,
    required: true
  },
  backendBaseUrl: {
    type: String,
    default: ''
  },
  compact: {
    type: Boolean,
    default: false
  }
})

defineEmits(['edit', 'delete'])

// Computed properties
const mediaUrl = computed(() => {
  const baseUrl = props.backendBaseUrl || ''
  const fileUrl = props.media.file_url || `/uploads/${props.media.served_filename || props.media.filename}`
  return `${baseUrl}${fileUrl}`
})

const isImage = computed(() => {
  const type = props.media.file_type || props.media.media_type || ''
  return type === 'image' || /\.(jpg|jpeg|png|gif|webp|bmp)$/i.test(props.media.filename)
})

const isVideo = computed(() => {
  const type = props.media.file_type || props.media.media_type || ''
  return type === 'video' || /\.(mp4|avi|mov|mkv|webm)$/i.test(props.media.filename)
})

// Utility functions
const getFileIcon = () => {
  const filename = props.media.filename || ''
  const ext = filename.split('.').pop()?.toLowerCase()
  
  switch (ext) {
    case 'pdf': return 'picture_as_pdf'
    case 'doc':
    case 'docx': return 'description'
    case 'mp3':
    case 'wav':
    case 'aac': return 'audiotrack'
    default: return 'insert_drive_file'
  }
}

const formatFileSize = (bytes) => {
  if (!bytes) return 'N/A'
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
}

const formatDuration = (seconds) => {
  if (!seconds) return ''
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { 
    day: '2-digit', 
    month: 'short',
    year: 'numeric'
  })
}

const handleImageError = (event) => {
  const img = event.target
  const container = img.closest('.image-preview')
  if (container) {
    container.innerHTML = `
      <div class="file-preview">
        <q-icon name="broken_image" size="3rem" color="grey-6" />
      </div>
    `
  }
}

const handleVideoError = (event) => {
  const video = event.target
  const container = video.closest('.video-preview')
  if (container) {
    container.innerHTML = `
      <div class="file-preview">
        <q-icon name="error" size="3rem" color="grey-6" />
      </div>
    `
  }
}
</script>

<style scoped>
.media-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.media-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.body--dark .media-card {
  background: #1f2937;
  border-color: #374151;
}

.compact-card {
  border-radius: 8px;
}

.compact-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

/* Preview */
.media-preview {
  aspect-ratio: 16/9;
  position: relative;
  overflow: hidden;
  background: #f9fafb;
}

.body--dark .media-preview {
  background: #111827;
}

.image-preview,
.video-preview,
.file-preview {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-img,
.preview-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
}

.play-icon {
  color: white;
  opacity: 0.9;
}

.video-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
}

/* Info */
.media-info {
  padding: 12px 16px;
}

.compact-card .media-info {
  padding: 8px 12px;
}

.media-title {
  margin: 0 0 4px 0;
  font-size: 0.9rem;
  font-weight: 500;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.body--dark .media-title {
  color: #e5e7eb;
}

.compact-card .media-title {
  font-size: 0.8rem;
}

.media-meta {
  margin: 0;
  font-size: 0.75rem;
  color: #6b7280;
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.body--dark .media-meta {
  color: #9ca3af;
}

/* Actions */
.media-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s ease;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 4px;
}

.body--dark .media-actions {
  background: rgba(0, 0, 0, 0.7);
}

.media-card:hover .media-actions {
  opacity: 1;
}

.compact-card .media-actions {
  top: 6px;
  right: 6px;
  padding: 2px;
}
</style>
