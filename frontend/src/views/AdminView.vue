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
        @refresh="loadMedia"
        @edit="editMedia"
        @delete="deleteMedia"
      />

      <QuickActions @logout="logout" />
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
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useToast } from 'vue-toastification'
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
import backendDetector from '../services/backendDetector'

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
    ScheduleDialog
  },
  setup () {
    const router = useRouter()
    const $q = useQuasar()
    const toast = useToast()
    const { isDarkMode } = useTheme()

    const backendBaseUrl = ref('http://127.0.0.1:8000')
    const playlistDialog = ref(false)
    const editMediaDialog = ref(false)
    const scheduleDialog = ref(false)

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

    const initializeBackend = async () => {
      const backendInfo = await backendDetector.detectBackend()
      backendBaseUrl.value = backendInfo.baseUrl
    }

    const refreshData = async () => {
      await Promise.all([loadPlaylists(), loadMedia(), loadStats(), loadSchedules()])
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

    const managePlaylistMedia = (playlist) => {
      router.push('/media')
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

    onMounted(async () => {
      await initializeBackend()
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
      isDarkMode,
      loadMedia,
      showCreatePlaylistDialog,
      editPlaylist,
      savePlaylist,
      deletePlaylist,
      managePlaylistMedia,
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
      logout
    }
  }
}
</script>

