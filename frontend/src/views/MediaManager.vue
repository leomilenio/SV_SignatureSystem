<template>
  <div class="media-manager-container">
    <!-- Theme Toggle -->
    <ThemeToggle class="theme-toggle" />
    
    <!-- Header -->
    <div class="media-header">
      <div class="header-content">
        <div class="header-icon">
          <q-icon name="perm_media" size="3rem" />
        </div>
        <div class="header-text">
          <h2>Gestión de Contenido Multimedia</h2>
          <p>Administra y organiza tu biblioteca de archivos multimedia</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Stats Section -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <q-icon name="image" size="2rem" />
          </div>
          <div class="stat-info">
            <h3>{{ mediaStats.images }}</h3>
            <p>Imágenes</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <q-icon name="videocam" size="2rem" />
          </div>
          <div class="stat-info">
            <h3>{{ mediaStats.videos }}</h3>
            <p>Videos</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <q-icon name="music_note" size="2rem" />
          </div>
          <div class="stat-info">
            <h3>{{ mediaStats.audio }}</h3>
            <p>Audio</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <q-icon name="folder" size="2rem" />
          </div>
          <div class="stat-info">
            <h3>{{ mediaStats.total }}</h3>
            <p>Total</p>
          </div>
        </div>
      </div>

      <!-- Actions Section -->
      <div class="actions-section">
        <div class="section-header">
          <h3>Acciones Disponibles</h3>
        </div>
        
        <div class="actions-grid">
          <div class="action-card" @click="uploadMedia">
            <div class="action-icon">
              <q-icon name="cloud_upload" size="3rem" />
            </div>
            <div class="action-content">
              <h4>Subir Archivos</h4>
              <p>Agregar nuevos archivos multimedia al sistema</p>
            </div>
            <q-icon name="arrow_forward" class="action-arrow" />
          </div>

          <div class="action-card" @click="browseMedia">
            <div class="action-icon">
              <q-icon name="folder_open" size="3rem" />
            </div>
            <div class="action-content">
              <h4>Explorar Biblioteca</h4>
              <p>Navegar y gestionar archivos existentes</p>
            </div>
            <q-icon name="arrow_forward" class="action-arrow" />
          </div>

          <div class="action-card" @click="createPlaylist">
            <div class="action-icon">
              <q-icon name="playlist_add" size="3rem" />
            </div>
            <div class="action-content">
              <h4>Crear Playlist</h4>
              <p>Organizar contenido en listas de reproducción</p>
            </div>
            <q-icon name="arrow_forward" class="action-arrow" />
          </div>

          <div class="action-card" @click="manageSchedules">
            <div class="action-icon">
              <q-icon name="schedule" size="3rem" />
            </div>
            <div class="action-content">
              <h4>Programar Horarios</h4>
              <p>Configurar horarios de reproducción automática</p>
            </div>
            <q-icon name="arrow_forward" class="action-arrow" />
          </div>
        </div>
      </div>

      <!-- Quick Access Section -->
      <div class="quick-access-section">
        <div class="section-header">
          <h3>Acceso Rápido</h3>
        </div>
        
        <div class="quick-access-grid">
          <div class="quick-access-card">
            <q-icon name="dashboard" size="2rem" />
            <span>Dashboard</span>
            <q-btn
              flat
              round
              icon="launch"
              @click="goToDashboard"
              size="sm"
            />
          </div>
          
          <div class="quick-access-card">
            <q-icon name="settings" size="2rem" />
            <span>Configuración</span>
            <q-btn
              flat
              round
              icon="launch"
              @click="goToConfig"
              size="sm"
            />
          </div>
          
          <div class="quick-access-card">
            <q-icon name="play_circle" size="2rem" />
            <span>Reproductor</span>
            <q-btn
              flat
              round
              icon="launch"
              @click="goToPlayer"
              size="sm"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Development Notice -->
    <div class="dev-notice">
      <q-icon name="construction" size="1.5rem" />
      <span>Módulo en desarrollo - Funcionalidad completa próximamente</span>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import ThemeToggle from '../components/ThemeToggle.vue'
import { useTheme } from '../composables/useTheme'

export default {
  name: 'MediaManager',
  components: {
    ThemeToggle
  },
  setup() {
    const router = useRouter()
    const toast = useToast()
    const { isDarkMode } = useTheme()

    // Media statistics (mock data for now)
    const mediaStats = ref({
      images: 42,
      videos: 18,
      audio: 27,
      total: 87
    })

    // Action handlers
    const uploadMedia = () => {
      toast.info('Función de subida de archivos en desarrollo')
    }

    const browseMedia = () => {
      toast.info('Explorador de archivos en desarrollo')
    }

    const createPlaylist = () => {
      toast.info('Creador de playlists en desarrollo')
    }

    const manageSchedules = () => {
      toast.info('Gestor de horarios en desarrollo')
    }

    // Navigation
    const goToDashboard = () => {
      router.push('/admin')
    }

    const goToConfig = () => {
      router.push('/config')
    }

    const goToPlayer = () => {
      router.push('/player')
    }

    // Load media statistics
    const loadMediaStats = async () => {
      try {
        // Here you would load real statistics from API
        // For now using mock data
        console.log('Loading media statistics...')
      } catch (error) {
        console.error('Error loading media stats:', error)
        toast.error('Error cargando estadísticas de multimedia')
      }
    }

    onMounted(() => {
      loadMediaStats()
    })

    return {
      mediaStats,
      uploadMedia,
      browseMedia,
      createPlaylist,
      manageSchedules,
      goToDashboard,
      goToConfig,
      goToPlayer,
      isDarkMode
    }
  }
}
</script>

<style scoped>
.media-manager-container {
  min-height: 100vh;
  background: var(--background);
  color: var(--text-primary);
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.media-header {
  background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%);
  padding: 60px 20px 40px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.media-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 70% 30%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.stat-icon {
  color: var(--primary);
  background: var(--hover-primary);
  padding: 12px;
  border-radius: 12px;
}

.stat-info h3 {
  margin: 0 0 4px 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-info p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.actions-section,
.quick-access-section {
  margin-bottom: 40px;
}

.section-header {
  margin-bottom: 24px;
}

.section-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.action-card {
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.action-icon {
  color: var(--secondary);
  transition: all 0.3s ease;
}

.action-card:hover .action-icon {
  transform: scale(1.1);
  color: var(--primary);
}

.action-content {
  flex: 1;
}

.action-content h4 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.action-content p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.4;
}

.action-arrow {
  color: var(--accent);
  transition: all 0.3s ease;
}

.action-card:hover .action-arrow {
  transform: translateX(4px);
  color: var(--primary);
}

.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.quick-access-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
}

.quick-access-card:hover {
  background: var(--hover-color);
  border-color: var(--primary);
}

.quick-access-card q-icon:first-child {
  color: var(--primary);
}

.quick-access-card span {
  flex: 1;
  font-weight: 500;
  color: var(--text-primary);
}

.dev-notice {
  background: var(--warning);
  color: var(--on-primary);
  padding: 16px 20px;
  margin: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  box-shadow: var(--shadow-md);
}

@media (max-width: 768px) {
  .media-header {
    padding: 40px 15px 30px;
  }
  
  .header-text h2 {
    font-size: 2rem;
  }
  
  .main-content {
    padding: 20px 10px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .action-card {
    padding: 20px;
  }
  
  .quick-access-grid {
    grid-template-columns: 1fr;
  }
  
  .theme-toggle {
    top: 10px;
    right: 10px;
  }
}
</style>
