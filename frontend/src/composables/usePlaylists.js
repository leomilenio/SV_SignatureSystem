import { ref, reactive } from 'vue'
import { playlistAPI } from '../services/api'
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
      const { data } = await playlistAPI.getStats()
      stats.totalPlaylists = data.total_playlists
      stats.totalScheduledItems = data.total_scheduled_items
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
