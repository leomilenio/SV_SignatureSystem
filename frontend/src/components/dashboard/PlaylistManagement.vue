<template>
  <div class="info-card playlists-card">
    <div class="card-header">
      <q-icon name="playlist_play" size="2rem" />
      <div class="header-text">
        <h3>Gestión de Playlists</h3>
        <p>Crear y administrar listas de reproducción</p>
      </div>
      <q-btn color="primary" icon="add" label="Nueva Playlist" @click="$emit('create')" rounded no-caps />
    </div>

    <div class="playlists-content">
      <div v-if="playlists.length === 0" class="empty-state">
        <q-icon name="playlist_add" size="3rem" />
        <p>No hay playlists creadas</p>
        <q-btn flat color="primary" label="Crear primera playlist" @click="$emit('create')" />
      </div>

      <div v-else class="playlists-grid">
        <div v-for="playlist in playlists" :key="playlist.id" class="playlist-item">
          <div class="playlist-icon"><q-icon name="queue_music" size="1.5rem" /></div>
          <div class="playlist-info">
            <h4>{{ playlist.name }}</h4>
            <p>{{ playlist.description || 'Sin descripción' }}</p>
          </div>
          <div class="playlist-actions">
            <q-btn flat round icon="video_library" size="sm" color="secondary" title="Gestionar medios" @click="$emit('manage', playlist)" />
            <q-btn flat round icon="schedule" size="sm" color="orange" title="Programar playlist" @click="$emit('schedule', playlist)" />
            <q-btn flat round icon="edit" size="sm" color="primary" title="Editar" @click="$emit('edit', playlist)" />
            <q-btn flat round icon="delete" size="sm" color="negative" title="Eliminar" @click="$emit('delete', playlist.id)" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  playlists: Array
})
</script>
