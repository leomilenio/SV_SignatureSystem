<template>
  <div class="player-container">
    <!-- Theme Toggle -->
    <ThemeToggle class="theme-toggle" />
    
    <!-- Header -->
    <div class="player-header">
      <div class="header-content">
        <div class="header-icon">
          <q-icon name="play_circle_filled" size="3rem" />
        </div>
        <div class="header-text">
          <h2>Reproductor de Contenido</h2>
          <p>Seleccione una playlist para comenzar la reproducción</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="content-card">
        <!-- Loading State -->
        <div v-if="loading" class="loading-section">
          <q-spinner color="primary" size="3rem" />
          <p class="loading-text">Cargando playlists...</p>
        </div>

        <!-- Playlist Selection -->
        <div v-else-if="playlists.length" class="playlists-section">
          <div class="section-header">
            <h3>Playlists Disponibles</h3>
            <div class="playlist-count">
              {{ playlists.length }} playlist{{ playlists.length !== 1 ? 's' : '' }} disponible{{ playlists.length !== 1 ? 's' : '' }}
            </div>
          </div>

          <div class="playlists-grid">
            <div 
              v-for="playlist in playlists" 
              :key="playlist.id"
              class="playlist-card"
              @click="select(playlist)"
            >
              <div class="playlist-icon">
                <q-icon name="queue_music" size="2.5rem" />
              </div>
              <div class="playlist-info">
                <h4>Playlist {{ playlist.id }}</h4>
                <p>{{ playlist.description || 'Lista de reproducción de contenido multimedia' }}</p>
                <div class="playlist-meta">
                  <span class="meta-item">
                    <q-icon name="schedule" size="1rem" />
                    {{ playlist.duration || 'Duración no especificada' }}
                  </span>
                  <span class="meta-item">
                    <q-icon name="playlist_play" size="1rem" />
                    {{ playlist.itemCount || 0 }} elementos
                  </span>
                </div>
              </div>
              <div class="playlist-action">
                <q-icon name="play_arrow" size="1.5rem" />
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">
            <q-icon name="playlist_remove" size="4rem" />
          </div>
          <h3>No hay playlists disponibles</h3>
          <p>Actualmente no hay ninguna playlist configurada en el sistema.</p>
          <div class="empty-actions">
            <q-btn
              color="primary"
              icon="add"
              label="Crear Playlist"
              @click="goToAdmin"
              rounded
              unelevated
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Actions -->
    <div class="footer-actions">
      <q-btn
        color="secondary"
        icon="arrow_back"
        label="Volver"
        @click="goBack"
        outline
        rounded
      />
      <q-btn
        color="accent"
        icon="refresh"
        label="Actualizar"
        @click="fetchPlaylists"
        rounded
        unelevated
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { scheduleAPI } from '../services/api'
import { useToast } from 'vue-toastification'
import ThemeToggle from '../components/ThemeToggle.vue'
import { useTheme } from '../composables/useTheme'

export default {
  name: 'PlayerView',
  components: {
    ThemeToggle
  },
  setup() {
    const router = useRouter()
    const playlists = ref([])
    const loading = ref(false)
    const toast = useToast()
    const { isDarkMode } = useTheme()

    const fetchPlaylists = async () => {
      loading.value = true
      try {
        const res = await scheduleAPI.list(0, 50)
        playlists.value = res.data.map(playlist => ({
          ...playlist,
          description: `Lista de reproducción ${playlist.id}`,
          duration: '00:00:00',
          itemCount: Math.floor(Math.random() * 20) + 1
        }))
      } catch (e) {
        toast.error('Error obteniendo playlists')
        console.error('Error:', e)
      } finally {
        loading.value = false
      }
    }

    const select = (playlist) => {
      toast.info(`Reproductor aún no implementado - Playlist ${playlist.id} seleccionada`, {
        timeout: 3000
      })
      // Aquí se implementaría la lógica del reproductor
      console.log('Playlist seleccionada:', playlist)
    }

    const goToAdmin = () => {
      router.push('/admin')
    }

    const goBack = () => {
      router.push('/')
    }

    onMounted(fetchPlaylists)

    return { 
      playlists, 
      loading, 
      select, 
      fetchPlaylists,
      goToAdmin,
      goBack,
      isDarkMode
    }
  }
}
</script>

<style scoped>
.player-container {
  min-height: 100vh;
  background: var(--background);
  color: var(--text-primary);
  position: relative;
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.player-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  padding: 60px 20px 40px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.player-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.header-icon {
  color: var(--on-primary);
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.header-text h2 {
  color: var(--on-primary);
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 12px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.header-text p {
  color: var(--on-primary);
  font-size: 1.2rem;
  margin: 0;
  opacity: 0.9;
}

.main-content {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.content-card {
  background: var(--surface);
  border-radius: 20px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border);
  overflow: hidden;
}

.loading-section {
  padding: 80px 20px;
  text-align: center;
}

.loading-text {
  margin-top: 20px;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.section-header {
  padding: 30px 30px 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.playlist-count {
  color: var(--text-secondary);
  background: var(--background);
  padding: 8px 16px;
  border-radius: 12px;
  font-size: 0.9rem;
  border: 1px solid var(--border);
}

.playlists-grid {
  padding: 20px;
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
}

.playlist-card {
  display: flex;
  align-items: center;
  padding: 24px;
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.playlist-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.playlist-icon {
  color: var(--primary);
  margin-right: 20px;
  transition: all 0.3s ease;
}

.playlist-card:hover .playlist-icon {
  transform: scale(1.1);
  color: var(--primary-dark);
}

.playlist-info {
  flex: 1;
}

.playlist-info h4 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.playlist-info p {
  margin: 0 0 12px 0;
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.4;
}

.playlist-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.playlist-action {
  color: var(--secondary);
  transition: all 0.3s ease;
}

.playlist-card:hover .playlist-action {
  transform: translateX(4px);
  color: var(--primary);
}

.empty-state {
  padding: 80px 40px;
  text-align: center;
}

.empty-icon {
  color: var(--text-secondary);
  margin-bottom: 24px;
  opacity: 0.6;
}

.empty-state h3 {
  margin: 0 0 12px 0;
  font-size: 1.5rem;
  color: var(--text-primary);
}

.empty-state p {
  margin: 0 0 32px 0;
  color: var(--text-secondary);
  font-size: 1.1rem;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.empty-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.footer-actions {
  padding: 20px;
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .player-header {
    padding: 40px 15px 30px;
  }
  
  .header-text h2 {
    font-size: 2rem;
  }
  
  .main-content {
    padding: 20px 10px;
  }
  
  .section-header {
    padding: 20px 20px 15px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .playlists-grid {
    grid-template-columns: 1fr;
    padding: 15px;
  }
  
  .playlist-card {
    padding: 20px;
  }
  
  .empty-state {
    padding: 60px 20px;
  }
  
  .footer-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .theme-toggle {
    top: 10px;
    right: 10px;
  }
}
</style>
