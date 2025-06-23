// Composable para manejar URLs de media de manera reactiva
import { ref, watch } from 'vue'
import backendDetector from '../services/backendDetector'

export function useMediaUrl() {
  const backendBaseUrl = ref('')
  
  // Detectar backend una vez
  const detectBackend = async () => {
    try {
      const { baseUrl } = await backendDetector.detectBackend()
      backendBaseUrl.value = baseUrl
    } catch (error) {
      console.error('Error detectando backend:', error)
      backendBaseUrl.value = 'http://127.0.0.1:8000' // Fallback
    }
  }
  
  // Función para construir URL de media
  const buildMediaUrl = (media) => {
    if (!media || !backendBaseUrl.value) return ''
    
    // Priorizar file_url si está disponible (ya incluye la ruta correcta /uploads/)
    if (media.file_url) {
      return `${backendBaseUrl.value}${media.file_url}`
    }
    
    // Fallback: usar served_filename o filename
    const filename = media.served_filename || media.filename
    if (!filename) {
      console.error('No se puede construir URL: falta file_url, served_filename y filename')
      return ''
    }
    
    // Construir URL con /uploads/
    return `${backendBaseUrl.value}/uploads/${filename}`
  }
  
  // Inicializar detección al usar el composable
  detectBackend()
  
  return {
    backendBaseUrl,
    buildMediaUrl,
    detectBackend
  }
}
