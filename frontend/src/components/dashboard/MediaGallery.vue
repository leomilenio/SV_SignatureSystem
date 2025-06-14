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
            <div v-if="(media.file_type || media.media_type) === 'image'" class="image-preview">
              <img :src="`${backendBaseUrl}${media.file_url || `/uploads/${media.served_filename || media.filename}`}`" :alt="media.filename" class="preview-img" />
            </div>
            <div v-else-if="(media.file_type || media.media_type) === 'video'" class="video-preview">
              <video :src="`${backendBaseUrl}${media.file_url || `/uploads/${media.served_filename || media.filename}`}`" class="preview-video" muted preload="metadata" />
            </div>
          </div>
          <div class="media-actions">
            <q-btn flat round icon="edit" size="sm" color="primary" @click="$emit('edit', media)" />
            <q-btn flat round icon="delete" size="sm" color="negative" @click="$emit('delete', media.id)" />
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
</script>
