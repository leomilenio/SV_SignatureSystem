<template>
  <div class="admin-dashboard-container">
    <ThemeToggle class="theme-toggle" />
    <div class="signance-container">
      <div class="dashboard-header">
        <div class="header-icon">
          <q-icon name="dashboard" size="4rem" />
        </div>
        <h2>Dashboard Administrativo</h2>
        <p>Pochtecayotl Signance System - Panel de Control</p>
      </div>

      <StatisticsCard :stats="stats" :business-info="businessInfo" />

      <PlaylistManagement
        :playlists="playlists"
        @create="showCreatePlaylistDialog"
        @edit="editPlaylist"
        @manage="managePlaylistMedia"
        @schedule="schedulePlaylist"
        @delete="deletePlaylist"
      />

      <div class="info-card upload-card">
        <div class="card-header">
          <q-icon name="cloud_upload" size="2rem" />
          <div class="header-text">
            <h3>Subir Multimedia</h3>
            <p>Agregar nuevos archivos al sistema</p>
          </div>
        </div>
        <div class="upload-content">
          <MediaUploader @uploaded="onMediaUploaded" @error="onMediaUploadError" />
        </div>
      </div>

      <MediaGallery
        :media-files="mediaFiles"
        :backend-base-url="backendBaseUrl"
        :loading="mediaLoading"
        mode="compact"
        title="Archivos Multimedia"
        subtitle="Archivos recientes"
        :max-items="8"
        @refresh="loadMedia"
        @edit="editMedia"
        @delete="deleteMedia"
        @show-all="navigateToMediaManager"
        class="section-spacing"
      />

      <QuickActions @logout="logout" class="section-spacing" />
    </div>

    <PlaylistDialog
      v-model="playlistDialog"
      :playlist="editingPlaylist"
      :form="playlistForm"
      :loading="savingPlaylist"
      :is-dark="isDarkMode"
      @save="savePlaylist"
      @close="closePlaylistDialog"
    />

    <EditMediaDialog
      v-model="editMediaDialog"
      :media="editingMedia"
      :form="editMediaForm"
      :loading="savingMedia"
      :is-dark="isDarkMode"
      @save="saveMediaChanges"
      @close="closeEditMediaDialog"
    />

    <ScheduleDialog
      v-model="scheduleDialog"
      :form="scheduleForm"
      :loading="savingSchedule"
      :weekday-options="weekdayOptions"
      :is-dark="isDarkMode"
      @save="saveSchedule"
      @close="closeScheduleDialog"
    />

    <!-- Dialog para gestionar medios en playlist -->
    <q-dialog v-model="playlistMediaDialog" persistent>
      <q-card style="min-width: 700px; max-width: 900px;" :class="{ 'bg-dark text-white': isDarkMode }">
        <q-card-section>
          <div class="text-h6">
            Gestionar Medios - {{ selectedPlaylist?.name }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="row q-gutter-md">
            <!-- Medios disponibles -->
            <div class="col-5">
              <div class="text-subtitle2 q-mb-md">Medios Disponibles</div>
              <q-list bordered class="available-media-list" :class="{ 'bg-grey-9': isDarkMode }">
                <q-item 
                  v-for="media in availableMedia" 
                  :key="media.id"
                  clickable
                  @click="addMediaToPlaylist(media)"
                >
                  <q-item-section avatar>
                    <q-icon :name="getMediaIcon(media.media_type || media.file_type)" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ media.filename }}</q-item-label>
                    <q-item-label caption>{{ media.media_type || media.file_type }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-btn flat round icon="add" size="sm" />
                  </q-item-section>
                </q-item>
                <q-item v-if="availableMedia.length === 0">
                  <q-item-section>
                    <q-item-label class="text-center text-grey">No hay medios disponibles</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>

            <!-- Medios en playlist -->
            <div class="col-6">
              <div class="text-subtitle2 q-mb-md">Medios en Playlist</div>
              <q-list bordered class="playlist-media-list" :class="{ 'bg-grey-9': isDarkMode }">
                <draggable 
                  v-model="playlistMedias" 
                  @end="reorderPlaylistMedia"
                  item-key="id"
                >
                  <template #item="{ element: media, index }">
                    <q-item>
                      <q-item-section avatar>
                        <q-icon name="drag_handle" />
                      </q-item-section>
                      <q-item-section avatar>
                        <q-icon :name="getMediaIcon(media.media_type || media.file_type)" />
                      </q-item-section>
                      <q-item-section>
                        <q-item-label>{{ media.filename }}</q-item-label>
                        <q-item-label caption>{{ media.media_type || media.file_type }} - Orden: {{ index + 1 }}</q-item-label>
                      </q-item-section>
                      <q-item-section side>
                        <q-btn 
                          flat 
                          round 
                          icon="remove" 
                          size="sm"
                          @click="removeMediaFromPlaylist(media.id)"
                        />
                      </q-item-section>
                    </q-item>
                  </template>
                </draggable>
                <q-item v-if="playlistMedias.length === 0">
                  <q-item-section>
                    <q-item-label class="text-center text-grey">No hay medios en esta playlist</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cerrar" @click="closePlaylistMediaDialog" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useToast } from 'vue-toastification'
import { businessAPI } from '../services/api'
import MediaUploader from '../components/MediaUploader.vue'
import ThemeToggle from '../components/ThemeToggle.vue'
import StatisticsCard from '../components/dashboard/StatisticsCard.vue'
import PlaylistManagement from '../components/dashboard/PlaylistManagement.vue'
import MediaGallery from '../components/dashboard/MediaGallery.vue'
import QuickActions from '../components/dashboard/QuickActions.vue'
import PlaylistDialog from '../components/dashboard/dialogs/PlaylistDialog.vue'
import EditMediaDialog from '../components/dashboard/dialogs/EditMediaDialog.vue'
import ScheduleDialog from '../components/dashboard/dialogs/ScheduleDialog.vue'
import { useTheme } from '../composables/useTheme'
import { usePlaylists } from '../composables/usePlaylists'
import { useMedia } from '../composables/useMedia'
import { useSchedules } from '../composables/useSchedules'
import { useMediaUrl } from '../composables/useMediaUrl'
import backendDetector from '../services/backendDetector'
import draggable from 'vuedraggable'

export default {
  name: 'AdminView',
  components: {
    MediaUploader,
    ThemeToggle,
    StatisticsCard,
    PlaylistManagement,
    MediaGallery,
    QuickActions,
    PlaylistDialog,
    EditMediaDialog,
    ScheduleDialog,
    draggable
  },
  setup () {
    const router = useRouter()
    const $q = useQuasar()
    const toast = useToast()
    const { isDarkMode } = useTheme()
    const { backendBaseUrl } = useMediaUrl()

    const playlistDialog = ref(false)
    const editMediaDialog = ref(false)
    const scheduleDialog = ref(false)
    const playlistMediaDialog = ref(false)

    const playlistForm = reactive({ name: '', description: '' })
    const editMediaForm = reactive({ filename: '', description: '' })
    const scheduleForm = reactive({ contentName: '' })

    const savingPlaylist = ref(false)
    const savingMedia = ref(false)
    const savingSchedule = ref(false)
    const mediaLoading = ref(false)

    const { playlists, stats, loadPlaylists, loadStats, createPlaylist, updatePlaylist, removePlaylist } = usePlaylists()
    const { mediaFiles, loadMedia, removeMedia } = useMedia()
    const { loadSchedules } = useSchedules()

    const businessInfo = reactive({ name: '', logo: null })
    const editingPlaylist = ref(null)
    const editingMedia = ref(null)
    const selectedPlaylist = ref(null)
    const availableMedia = ref([])
    const playlistMedias = ref([])

    const weekdayOptions = [
      { label: 'Lun', value: 0 },
      { label: 'Mar', value: 1 },
      { label: 'Mié', value: 2 },
      { label: 'Jue', value: 3 },
      { label: 'Vie', value: 4 },
      { label: 'Sáb', value: 5 },
      { label: 'Dom', value: 6 }
    ]

    const refreshData = async () => {
      await Promise.all([loadPlaylists(), loadMedia(), loadStats(), loadSchedules(), loadBusinessInfo()])
    }

    const loadBusinessInfo = async () => {
      try {
        const response = await businessAPI.get()
        Object.assign(businessInfo, response.data)
      } catch (error) {
        console.error('Error loading business info:', error)
        // Set default values if error
        businessInfo.name = 'Signance System'
        businessInfo.logo = null
      }
    }

    const showCreatePlaylistDialog = () => {
      editingPlaylist.value = null
      playlistForm.name = ''
      playlistForm.description = ''
      playlistDialog.value = true
    }

    const editPlaylist = (playlist) => {
      editingPlaylist.value = playlist
      playlistForm.name = playlist.name
      playlistForm.description = playlist.description || ''
      playlistDialog.value = true
    }

    const savePlaylist = async () => {
      savingPlaylist.value = true
      try {
        if (editingPlaylist.value) {
          await updatePlaylist(editingPlaylist.value.id, playlistForm)
        } else {
          await createPlaylist(playlistForm)
        }
        playlistDialog.value = false
      } finally {
        savingPlaylist.value = false
      }
    }

    const deletePlaylist = async (playlistId) => {
      await removePlaylist(playlistId)
    }

    const onMediaUploaded = () => {
      loadMedia()
      loadStats()
    }

    const onMediaUploadError = () => {
      toast.error('Error subiendo archivo')
    }

    const editMedia = (media) => {
      editingMedia.value = media
      editMediaForm.filename = media.filename
      editMediaForm.description = media.description
      editMediaDialog.value = true
    }

    const saveMediaChanges = async () => {
      // Placeholder for update logic
      editMediaDialog.value = false
    }

    const deleteMedia = async (mediaId) => {
      await removeMedia(mediaId)
      loadStats()
    }

    const schedulePlaylist = (playlist) => {
      scheduleForm.contentName = playlist.name
      scheduleDialog.value = true
    }

    const managePlaylistMedia = async (playlist) => {
      selectedPlaylist.value = playlist
      try {
        // Cargar medios de la playlist
        const playlistResponse = await fetch(`${backendBaseUrl.value}/api/playlists/${playlist.id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('signance_token')}`
          }
        })
        const playlistData = await playlistResponse.json()
        playlistMedias.value = playlistData.medias || []

        // Cargar todos los medios disponibles
        // Filtrar medios que no están en la playlist
        const mediaInPlaylist = new Set(playlistMedias.value.map(m => m.id))
        availableMedia.value = mediaFiles.value.filter(m => !mediaInPlaylist.has(m.id))

        playlistMediaDialog.value = true
      } catch (error) {
        toast.error('Error cargando datos de playlist')
        console.error('Error loading playlist media:', error)
      }
    }

    const closePlaylistMediaDialog = () => {
      playlistMediaDialog.value = false
      selectedPlaylist.value = null
      availableMedia.value = []
      playlistMedias.value = []
    }

    const closePlaylistDialog = () => { playlistDialog.value = false }
    const closeEditMediaDialog = () => { editMediaDialog.value = false }
    const closeScheduleDialog = () => { scheduleDialog.value = false }

    const saveSchedule = async () => {
      savingSchedule.value = false
      scheduleDialog.value = false
    }

    const logout = () => {
      localStorage.removeItem('signance_token')
      router.push('/login')
    }

    const addMediaToPlaylist = async (media) => {
      try {
        const response = await fetch(`${backendBaseUrl.value}/api/playlists/${selectedPlaylist.value.id}/media`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('signance_token')}`
          },
          body: JSON.stringify({
            media_id: media.id
          })
        })

        if (response.ok) {
          // Mover el media de disponible a playlist
          availableMedia.value = availableMedia.value.filter(m => m.id !== media.id)
          playlistMedias.value.push({
            ...media,
            order_index: playlistMedias.value.length
          })
          toast.success(`"${media.filename}" añadido a la playlist`)
        } else {
          throw new Error('Error en la respuesta del servidor')
        }
      } catch (error) {
        toast.error('Error añadiendo medio a la playlist')
        console.error('Error adding media to playlist:', error)
      }
    }

    const removeMediaFromPlaylist = async (mediaId) => {
      try {
        const response = await fetch(`${backendBaseUrl.value}/api/playlists/${selectedPlaylist.value.id}/media/${mediaId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('signance_token')}`
          }
        })

        if (response.ok) {
          // Mover el media de playlist a disponible
          const mediaToRemove = playlistMedias.value.find(m => m.id === mediaId)
          if (mediaToRemove) {
            playlistMedias.value = playlistMedias.value.filter(m => m.id !== mediaId)
            availableMedia.value.push(mediaToRemove)
            toast.success(`"${mediaToRemove.filename}" removido de la playlist`)
          }
        } else {
          throw new Error('Error en la respuesta del servidor')
        }
      } catch (error) {
        toast.error('Error removiendo medio de la playlist')
        console.error('Error removing media from playlist:', error)
      }
    }

    const reorderPlaylistMedia = async () => {
      try {
        const mediaOrder = playlistMedias.value.map((media, index) => ({
          media_id: media.id,
          order_index: index
        }))

        const response = await fetch(`${backendBaseUrl.value}/api/playlists/${selectedPlaylist.value.id}/reorder`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('signance_token')}`
          },
          body: JSON.stringify({
            media_order: mediaOrder
          })
        })

        if (response.ok) {
          toast.success('Orden actualizado')
        } else {
          throw new Error('Error en la respuesta del servidor')
        }
      } catch (error) {
        toast.error('Error reordenando medios')
        console.error('Error reordering media:', error)
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

    const navigateToMediaManager = () => {
      router.push('/media')
    }

    onMounted(async () => {
      refreshData()
      $q.dark.set(isDarkMode.value)
    })

    watch(isDarkMode, (val) => {
      $q.dark.set(val)
    })

    return {
      backendBaseUrl,
      playlistDialog,
      editMediaDialog,
      scheduleDialog,
      playlistMediaDialog,
      playlistForm,
      editMediaForm,
      scheduleForm,
      savingPlaylist,
      savingMedia,
      savingSchedule,
      mediaLoading,
      playlists,
      stats,
      mediaFiles,
      businessInfo,
      editingPlaylist,
      editingMedia,
      selectedPlaylist,
      availableMedia,
      playlistMedias,
      weekdayOptions,
      isDarkMode,
      loadMedia,
      showCreatePlaylistDialog,
      editPlaylist,
      savePlaylist,
      deletePlaylist,
      managePlaylistMedia,
      closePlaylistMediaDialog,
      schedulePlaylist,
      onMediaUploaded,
      onMediaUploadError,
      editMedia,
      saveMediaChanges,
      deleteMedia,
      saveSchedule,
      closePlaylistDialog,
      closeEditMediaDialog,
      closeScheduleDialog,
      logout,
      addMediaToPlaylist,
      removeMediaFromPlaylist,
      reorderPlaylistMedia,
      getMediaIcon
    }
  }
}
</script>

<style scoped>
/* CSS Variables */
:root {
  --primary: #1976d2;
  --primary-light: #42a5f5;
  --primary-rgb: 25, 118, 210;
  --secondary: #dc004e;
  --accent: #9c27b0;
}

.admin-dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
  padding: 20px 0;
  position: relative;
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.signance-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.dashboard-header {
  text-align: center;
  color: white;
  margin-bottom: 40px;
  padding: 40px 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.header-icon {
  margin-bottom: 20px;
  opacity: 0.9;
}

.dashboard-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 10px 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.dashboard-header p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
  font-weight: 300;
}

/* Card Styles */
.info-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* Dark mode card styles */
.body--dark .info-card {
  background: rgba(30, 30, 30, 0.95);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
}

.body--dark .card-header {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

.header-text h3 {
  margin: 0 0 5px 0;
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--primary);
}

.body--dark .header-text h3 {
  color: var(--primary-light, #42a5f5);
}

.header-text p {
  margin: 0;
  color: #666;
  font-size: 1rem;
}

.body--dark .header-text p {
  color: #ccc;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.card-title h3 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--primary);
}

.body--dark .card-title h3 {
  color: var(--primary-light, #42a5f5);
}

/* Upload Card Specific Styles */
.upload-card .upload-content {
  padding: 20px 0;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  transition: all 0.3s ease;
}

.body--dark .stat-item {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
}

.stat-item:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  color: var(--primary);
  opacity: 0.8;
}

.stat-info h4 {
  margin: 0 0 5px 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--primary);
}

.body--dark .stat-info h4 {
  color: var(--primary-light, #42a5f5);
}

.stat-info p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.body--dark .stat-info p {
  color: #ccc;
}

/* Responsive Design */
@media (max-width: 768px) {
  .signance-container {
    padding: 0 10px;
  }
  
  .info-card {
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .dashboard-header {
    padding: 30px 15px;
  }
  
  .dashboard-header h2 {
    font-size: 2rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .card-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .theme-toggle {
    top: 10px;
    right: 10px;
  }
  
  .dashboard-header h2 {
    font-size: 1.8rem;
  }
  
  .dashboard-header p {
    font-size: 1rem;
  }
  
  .info-card {
    padding: 15px;
  }
  
  .header-text h3 {
    font-size: 1.5rem;
  }
}

/* Playlist Media Management Dialog Styles */
.available-media-list,
.playlist-media-list {
  max-height: 400px;
  overflow-y: auto;
  border-radius: 8px;
}

.body--dark .available-media-list,
.body--dark .playlist-media-list {
  background-color: #1e1e1e;
  border-color: rgba(255, 255, 255, 0.1);
}

/* Custom scrollbar for lists */
.available-media-list::-webkit-scrollbar,
.playlist-media-list::-webkit-scrollbar {
  width: 6px;
}

.available-media-list::-webkit-scrollbar-track,
.playlist-media-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.available-media-list::-webkit-scrollbar-thumb,
.playlist-media-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.available-media-list::-webkit-scrollbar-thumb:hover,
.playlist-media-list::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.body--dark .available-media-list::-webkit-scrollbar-track,
.body--dark .playlist-media-list::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.body--dark .available-media-list::-webkit-scrollbar-thumb,
.body--dark .playlist-media-list::-webkit-scrollbar-thumb {
  background: #555;
}

.body--dark .available-media-list::-webkit-scrollbar-thumb:hover,
.body--dark .playlist-media-list::-webkit-scrollbar-thumb:hover {
  background: #777;
}

/* Separación entre secciones */
.section-spacing {
  margin-bottom: 32px;
}

/* Espaciado especial para MediaGallery */
.section-spacing + .section-spacing {
  margin-top: 24px;
}

/* Responsive spacing */
@media (max-width: 768px) {
  .section-spacing {
    margin-bottom: 24px;
  }
  
  .section-spacing + .section-spacing {
    margin-top: 16px;
  }
}
</style>

