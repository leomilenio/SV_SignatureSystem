<template>
  <div class="media-list-item">
    <!-- Thumbnail -->
    <div class="media-thumbnail">
      <div v-if="isImage" class="image-thumb">
        <img 
          :src="mediaUrl" 
          :alt="media.filename" 
          @error="handleImageError"
        />
      </div>
      <div v-else-if="isVideo" class="video-thumb">
        <video 
          :src="mediaUrl" 
          muted 
          preload="metadata"
          @error="handleVideoError"
        />
        <q-icon name="play_circle_filled" class="play-overlay" />
      </div>
      <div v-else class="file-thumb">
        <q-icon :name="getFileIcon()" size="2rem" />
      </div>
    </div>

    <!-- Información -->
    <div class="media-details">
      <div class="media-name">
        <h4>{{ media.filename }}</h4>
        <p v-if="media.description">{{ media.description }}</p>
      </div>
      
      <div class="media-metadata">
        <div class="meta-item">
          <q-icon name="folder" size="sm" />
          <span>{{ getFileType() }}</span>
        </div>
        <div class="meta-item">
          <q-icon name="data_usage" size="sm" />
          <span>{{ formatFileSize(media.file_size || media.size) }}</span>
        </div>
        <div v-if="media.duration" class="meta-item">
          <q-icon name="schedule" size="sm" />
          <span>{{ formatDuration(media.duration) }}</span>
        </div>
        <div v-if="media.created_at" class="meta-item">
          <q-icon name="event" size="sm" />
          <span>{{ formatDate(media.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- Acciones -->
    <div class="media-list-actions">
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

const getFileType = () => {
  const type = props.media.file_type || props.media.media_type
  if (type) return type.charAt(0).toUpperCase() + type.slice(1)
  
  const filename = props.media.filename || ''
  const ext = filename.split('.').pop()?.toLowerCase()
  return ext ? ext.toUpperCase() : 'Archivo'
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
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleImageError = (event) => {
  const img = event.target
  const container = img.closest('.image-thumb')
  if (container) {
    container.innerHTML = `
      <div class="file-thumb">
        <q-icon name="broken_image" size="2rem" color="grey-6" />
      </div>
    `
  }
}

const handleVideoError = (event) => {
  const video = event.target
  const container = video.closest('.video-thumb')
  if (container) {
    container.innerHTML = `
      <div class="file-thumb">
        <q-icon name="error" size="2rem" color="grey-6" />
      </div>
    `
  }
}
</script>

<style scoped>
.media-list-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.media-list-item:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.body--dark .media-list-item {
  background: #1f2937;
  border-color: #374151;
}

.body--dark .media-list-item:hover {
  border-color: #4b5563;
}

/* Thumbnail */
.media-thumbnail {
  flex-shrink: 0;
  width: 80px;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  background: #f9fafb;
  position: relative;
}

.body--dark .media-thumbnail {
  background: #111827;
}

.image-thumb,
.video-thumb,
.file-thumb {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-thumb img,
.video-thumb video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 1.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.file-thumb {
  color: #6b7280;
}

/* Details */
.media-details {
  flex: 1;
  min-width: 0;
}

.media-name h4 {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 500;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.body--dark .media-name h4 {
  color: #e5e7eb;
}

.media-name p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.body--dark .media-name p {
  color: #9ca3af;
}

.media-metadata {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  color: #6b7280;
}

.body--dark .meta-item {
  color: #9ca3af;
}

.meta-item .q-icon {
  color: #9ca3af;
}

/* Actions */
.media-list-actions {
  flex-shrink: 0;
  display: flex;
  gap: 8px;
}

/* Responsive */
@media (max-width: 768px) {
  .media-list-item {
    gap: 12px;
    padding: 12px;
  }
  
  .media-thumbnail {
    width: 60px;
    height: 45px;
  }
  
  .media-metadata {
    gap: 12px;
  }
  
  .meta-item {
    font-size: 0.7rem;
  }
}
</style>
