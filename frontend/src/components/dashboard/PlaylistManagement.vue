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
            <div class="playlist-meta">
              <q-chip size="sm" color="primary" text-color="white">
                {{ playlist.media_count || 0 }} medios
              </q-chip>
              <span class="playlist-date">{{ formatDate(playlist.created_at) }}</span>
            </div>
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

const formatDate = (dateString) => {
  if (!dateString) return 'Fecha no disponible'
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>

<style scoped>
.playlists-content {
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

.playlists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.playlist-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.body--dark .playlist-item {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  border-color: rgba(255, 255, 255, 0.1);
}

.playlist-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.playlist-icon {
  color: var(--primary);
  padding: 10px;
  border-radius: 8px;
  background: rgba(var(--primary-rgb), 0.1);
}

.playlist-info {
  flex: 1;
}

.playlist-info h4 {
  margin: 0 0 5px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--primary);
}

.body--dark .playlist-info h4 {
  color: var(--primary-light, #42a5f5);
}

.playlist-info p {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.body--dark .playlist-info p {
  color: #ccc;
}

.playlist-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.playlist-date {
  font-size: 0.8rem;
  color: #999;
}

.body--dark .playlist-date {
  color: #aaa;
}

.playlist-actions {
  display: flex;
  gap: 5px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .playlists-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .playlist-item {
    padding: 15px;
    gap: 12px;
  }
  
  .playlist-info h4 {
    font-size: 1rem;
  }
  
  .playlist-actions {
    flex-direction: column;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .empty-state {
    padding: 40px 15px;
  }
  
  .playlist-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .playlist-actions {
    flex-direction: row;
    width: 100%;
    justify-content: space-around;
  }
}
</style>
