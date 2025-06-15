import { ref, reactive } from 'vue'
import { playlistAPI, mediaAPI } from '../services/api'
import { useToast } from 'vue-toastification'

export function usePlaylists() {
  const playlists = ref([])
  const stats = reactive({
    totalPlaylists: 0,
    totalScheduledItems: 0,
    totalMedia: 0
  })
  const toast = useToast()

  const loadPlaylists = async () => {
    try {
      const { data } = await playlistAPI.list()
      playlists.value = data
    } catch (error) {
      toast.error('Error cargando playlists')
    }
  }

  const loadStats = async () => {
    try {
      const [playlistStatsResponse, mediaResponse] = await Promise.all([
        playlistAPI.getStats(),
        mediaAPI.list()
      ])
      
      stats.totalPlaylists = playlistStatsResponse.data.total_playlists
      stats.totalScheduledItems = playlistStatsResponse.data.total_scheduled_items
      stats.totalMedia = mediaResponse.data.length
    } catch (error) {
      toast.error('Error cargando estadísticas')
    }
  }

  const createPlaylist = async (payload) => {
    await playlistAPI.create(payload)
    await loadPlaylists()
    await loadStats()
  }

  const updatePlaylist = async (id, payload) => {
    await playlistAPI.update(id, payload)
    await loadPlaylists()
    await loadStats()
  }

  const removePlaylist = async (id) => {
    await playlistAPI.delete(id)
    await loadPlaylists()
    await loadStats()
  }

  return {
    playlists,
    stats,
    loadPlaylists,
    loadStats,
    createPlaylist,
    updatePlaylist,
    removePlaylist
  }
}
