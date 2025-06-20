<template>
  <div class="media-gallery" :class="{ 'full-view': mode === 'full', 'compact-view': mode === 'compact' }">
    <!-- Header con controles -->
    <div class="gallery-header">
      <div class="header-info">
        <q-icon name="video_library" size="2rem" />
        <div class="header-text">
          <h3>{{ title || 'Archivos Multimedia' }}</h3>
          <p>{{ subtitle || (mode === 'full' ? 'Gestiona tu biblioteca completa' : 'Archivos recientes') }}</p>
        </div>
      </div>
      
      <div class="header-controls">
        <!-- Búsqueda (solo en modo full) -->
        <q-input
          v-if="mode === 'full'"
          v-model="searchQuery"
          placeholder="Buscar archivos..."
          outlined
          dense
          class="search-input"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
          <template v-slot:append>
            <q-icon 
              v-if="searchQuery" 
              name="clear" 
              @click="searchQuery = ''" 
              class="cursor-pointer" 
            />
          </template>
        </q-input>
        
        <!-- Controles de vista (solo en modo full) -->
        <div v-if="mode === 'full'" class="view-controls">
          <q-btn-toggle
            v-model="viewMode"
            :options="[
              { label: 'Tarjetas', value: 'grid', icon: 'grid_view' },
              { label: 'Lista', value: 'list', icon: 'view_list' }
            ]"
            flat
            color="primary"
            toggle-color="primary"
            no-caps
          />
        </div>
        
        <!-- Botón refresh -->
        <q-btn 
          flat 
          icon="refresh" 
          @click="$emit('refresh')" 
          :loading="loading" 
          round 
          color="primary"
        >
          <q-tooltip>Actualizar</q-tooltip>
        </q-btn>
      </div>
    </div>

    <!-- Contenido -->
    <div class="gallery-content">
      <!-- Estado vacío -->
      <div v-if="filteredMedia.length === 0 && !loading" class="empty-state">
        <q-icon name="video_library" size="4rem" color="grey-5" />
        <h4>{{ searchQuery ? 'No se encontraron archivos' : 'No hay archivos multimedia' }}</h4>
        <p>{{ searchQuery ? 'Intenta con otros términos de búsqueda' : 'Sube tus primeros archivos multimedia' }}</p>
      </div>

      <!-- Loading state -->
      <div v-else-if="loading" class="loading-state">
        <q-skeleton height="150px" class="q-mb-md" v-for="n in 6" :key="n" />
      </div>

      <!-- Vista de tarjetas -->
      <div v-else-if="viewMode === 'grid'" class="media-grid" :class="{ 'compact-grid': mode === 'compact' }">
        <MediaCard
          v-for="media in displayedMedia"
          :key="media.id"
          :media="media"
          :backend-base-url="backendBaseUrl"
          :compact="mode === 'compact'"
          @edit="$emit('edit', media)"
          @delete="$emit('delete', media.id)"
        />
      </div>

      <!-- Vista de lista (solo modo full) -->
      <div v-else-if="viewMode === 'list' && mode === 'full'" class="media-list">
        <MediaListItem
          v-for="media in displayedMedia"
          :key="media.id"
          :media="media"
          :backend-base-url="backendBaseUrl"
          @edit="$emit('edit', media)"
          @delete="$emit('delete', media.id)"
        />
      </div>
    </div>

    <!-- Mostrar más en modo compact -->
    <div v-if="mode === 'compact' && mediaFiles.length > maxItems" class="show-more">
      <q-btn 
        flat 
        color="primary" 
        :label="`Ver todos (${mediaFiles.length} archivos)`"
        icon="arrow_forward"
        @click="$emit('show-all')"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import MediaCard from './MediaCard.vue'
import MediaListItem from './MediaListItem.vue'

const props = defineProps({
  mediaFiles: {
    type: Array,
    default: () => []
  },
  backendBaseUrl: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'compact', // 'compact' o 'full'
    validator: (value) => ['compact', 'full'].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  maxItems: {
    type: Number,
    default: 6
  }
})

defineEmits(['refresh', 'edit', 'delete', 'show-all'])

// Estados reactivos
const searchQuery = ref('')
const viewMode = ref('grid')

// Computed para filtrar y ordenar medios
const filteredMedia = computed(() => {
  if (!props.mediaFiles) return []
  
  let filtered = [...props.mediaFiles]
  
  // Filtrar por búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(media => 
      media.filename?.toLowerCase().includes(query) ||
      media.description?.toLowerCase().includes(query)
    )
  }
  
  // Ordenar por fecha de creación (más recientes primero)
  filtered.sort((a, b) => {
    const dateA = new Date(a.created_at || a.upload_date || 0)
    const dateB = new Date(b.created_at || b.upload_date || 0)
    return dateB - dateA
  })
  
  return filtered
})

// Computed para limitar elementos en modo compact
const displayedMedia = computed(() => {
  if (props.mode === 'compact') {
    return filteredMedia.value.slice(0, props.maxItems)
  }
  return filteredMedia.value
})
</script>

<style scoped>
.media-gallery {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.body--dark .media-gallery {
  background: rgba(30, 30, 30, 0.95);
  border-color: #374151;
}

/* Header */
.gallery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.body--dark .gallery-header {
  border-bottom-color: #374151;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-info .q-icon {
  color: #6366f1;
}

.header-text h3 {
  margin: 0 0 4px 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.body--dark .header-text h3 {
  color: #e2e8f0;
}

.header-text p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.body--dark .header-text p {
  color: #9ca3af;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-input {
  min-width: 250px;
}

.view-controls {
  display: flex;
  align-items: center;
}

/* Content */
.gallery-content {
  padding: 24px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state h4 {
  margin: 16px 0 8px 0;
  font-size: 1.2rem;
  color: #374151;
}

.body--dark .empty-state h4 {
  color: #d1d5db;
}

.empty-state p {
  margin: 0;
  color: #6b7280;
}

.loading-state {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

/* Media Grid */
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.compact-grid {
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

/* Media List */
.media-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Show More */
.show-more {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.body--dark .show-more {
  border-top-color: #374151;
}

/* Responsive */
@media (max-width: 768px) {
  .gallery-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-controls {
    justify-content: space-between;
  }
  
  .search-input {
    min-width: auto;
    flex: 1;
  }
  
  .media-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 12px;
  }
  
  .compact-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Modo Full vs Compact */
.full-view {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.compact-view {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.compact-view .gallery-header {
  padding: 16px 20px;
}

.compact-view .gallery-content {
  padding: 20px;
}
</style>
