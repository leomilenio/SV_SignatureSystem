<template>
  <div class="info-card media-card">
    <div class="card-header">
      <q-icon name="video_library" size="2rem" />
      <div class="header-text">
        <h3>Archivos Multimedia</h3>
        <p>Gestionar contenido subido</p>
      </div>
      <q-btn flat icon="refresh" @click="$emit('refresh')" :loading="loading" round />
    </div>

    <div class="media-content">
      <div v-if="mediaFiles.length === 0" class="empty-state">
        <q-icon name="video_library" size="3rem" />
        <p>No hay archivos multimedia</p>
      </div>

      <div v-else class="media-grid">
        <div v-for="media in mediaFiles" :key="media.id" class="media-item">
          <div class="media-preview">
            <!-- Previsualización de imagen -->
            <div v-if="(media.file_type || media.media_type) === 'image'" class="image-preview">
              <img 
                :src="`${backendBaseUrl}${media.file_url || `/uploads/${media.served_filename || media.filename}`}`" 
                :alt="media.filename" 
                @error="handleImageError"
                class="preview-img" 
              />
            </div>
            <!-- Previsualización de video -->
            <div v-else-if="(media.file_type || media.media_type) === 'video'" class="video-preview">
              <video 
                :src="`${backendBaseUrl}${media.file_url || `/uploads/${media.served_filename || media.filename}`}`" 
                class="preview-video" 
                muted 
                preload="metadata"
                @error="handleVideoError"
                @loadedmetadata="setVideoTime"
                @click="toggleVideoPreview"
              >
                Su navegador no soporta la reproducción de video.
              </video>
              <div class="video-overlay">
                <q-icon name="play_circle_filled" size="2.5rem" class="play-icon" />
                <div class="video-duration" v-if="media.duration">
                  {{ formatDuration(media.duration) }}
                </div>
              </div>
            </div>
            <!-- Icono para otros tipos de archivos -->
            <div v-else class="media-icon">
              <q-icon 
                :name="getMediaIcon(media.file_type || media.media_type)"
                size="2rem"
                :class="`media-type-${(media.file_type || media.media_type || 'unknown')}`"
              />
            </div>
          </div>
          
          <div class="media-info">
            <h4>{{ media.filename }}</h4>
            <p>
              <q-chip 
                :color="(media.file_type || media.media_type) === 'image' ? 'orange' : 'blue'"
                text-color="white"
                size="sm"
              >
                {{ String(media.file_type || media.media_type || 'unknown').toUpperCase() }}
              </q-chip>
            </p>
            <span class="media-date">{{ formatDate(media.uploaded_at) }}</span>
          </div>
          
          <div class="media-actions">
            <q-btn 
              flat 
              round 
              icon="edit"
              @click="$emit('edit', media)"
              size="sm"
              color="primary"
              class="q-mr-xs"
            />
            <q-btn 
              flat 
              round 
              icon="schedule"
              @click="$emit('schedule', media)"
              size="sm"
              color="secondary"
              class="q-mr-xs"
            />
            <q-btn 
              flat 
              round 
              icon="delete"
              @click="$emit('delete', media.id)"
              size="sm"
              color="negative"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  mediaFiles: Array,
  backendBaseUrl: String,
  loading: Boolean
})

const handleImageError = (event) => {
  const img = event.target
  const container = img.closest('.image-preview')
  if (container) {
    container.innerHTML = `
      <div class="media-icon">
        <q-icon name="broken_image" size="2rem" color="grey" />
      </div>
    `
  }
}

const handleVideoError = (event) => {
  const video = event.target
  const container = video.closest('.video-preview')
  if (container) {
    container.innerHTML = `
      <div class="media-icon">
        <q-icon name="videocam_off" size="2rem" color="grey" />
      </div>
    `
  }
}

const setVideoTime = (event) => {
  const video = event.target
  if (video.duration > 1) {
    video.currentTime = 1
  }
}

const formatDuration = (seconds) => {
  if (!seconds) return '0:00'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  } else {
    return `${minutes}:${secs.toString().padStart(2, '0')}`
  }
}

const toggleVideoPreview = (event) => {
  const video = event.target
  if (video.paused) {
    video.play()
    video.muted = false
  } else {
    video.pause()
    video.currentTime = video.duration > 1 ? 1 : 0
    video.muted = true
  }
}

const getMediaIcon = (fileType) => {
  if (!fileType) return 'description'
  
  const type = fileType.toLowerCase()
  if (type.includes('image')) return 'image'
  if (type.includes('video')) return 'videocam'
  if (type.includes('audio')) return 'audiotrack'
  if (type.includes('pdf')) return 'picture_as_pdf'
  return 'description'
}

const formatDate = (dateString) => {
  if (!dateString) return 'Fecha no disponible'
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.media-content {
  padding-top: 10px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.body--dark .empty-state {
  color: #ccc;
}

.empty-state q-icon {
  margin-bottom: 20px;
  opacity: 0.6;
}

.empty-state p {
  font-size: 1.1rem;
  margin-bottom: 20px;
  font-weight: 500;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.media-item {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  padding: 15px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  overflow: hidden;
}

.body--dark .media-item {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  border-color: rgba(255, 255, 255, 0.1);
}

.media-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.media-preview {
  width: 100%;
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 15px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.body--dark .media-preview {
  background: #1a1a1a;
}

.image-preview,
.video-preview {
  width: 100%;
  height: 100%;
  position: relative;
}

.preview-img,
.preview-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.video-overlay:hover {
  background: rgba(0, 0, 0, 0.5);
}

.play-icon {
  color: white;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.5));
}

.video-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.media-icon {
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.media-type-image {
  color: #ff9800;
}

.media-type-video {
  color: #2196f3;
}

.media-type-audio {
  color: #9c27b0;
}

.media-info {
  margin-bottom: 12px;
}

.media-info h4 {
  margin: 0 0 8px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.body--dark .media-info h4 {
  color: var(--primary-light, #42a5f5);
}

.media-info p {
  margin: 0 0 8px 0;
}

.media-date {
  font-size: 0.8rem;
  color: #999;
}

.body--dark .media-date {
  color: #aaa;
}

.media-actions {
  display: flex;
  justify-content: center;
  gap: 5px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .media-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 15px;
  }
  
  .media-item {
    padding: 12px;
  }
  
  .media-preview {
    height: 140px;
    margin-bottom: 12px;
  }
}

@media (max-width: 480px) {
  .media-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .media-preview {
    height: 120px;
  }
  
  .empty-state {
    padding: 40px 15px;
  }
  
  .media-actions {
    flex-wrap: wrap;
  }
}
</style>
