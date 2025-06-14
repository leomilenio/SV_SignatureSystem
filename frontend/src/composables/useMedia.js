import { ref } from 'vue'
import { mediaAPI } from '../services/api'
import { useToast } from 'vue-toastification'

export function useMedia() {
  const mediaFiles = ref([])
  const toast = useToast()

  const loadMedia = async () => {
    try {
      const { data } = await mediaAPI.list()
      mediaFiles.value = data
    } catch (error) {
      toast.error('Error cargando medios')
    }
  }

  const removeMedia = async (id) => {
    await mediaAPI.delete(id)
    await loadMedia()
  }

  return {
    mediaFiles,
    loadMedia,
    removeMedia
  }
}
