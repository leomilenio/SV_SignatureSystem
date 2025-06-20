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
    
    // Obtener filepath del media
    let filepath = media.filepath || media.file_path || ''
    
    // Si no hay filepath, intentar construir uno basado en el ID o filename
    if (!filepath) {
      if (media.id) {
        filepath = `/uploads/${media.id}`
      } else {
        console.error('No se puede construir filepath sin ID')
        return ''
      }
    }
    
    // Normalizar el path
    if (filepath && !filepath.startsWith('/')) {
      filepath = '/' + filepath
    }
    
    // Si no incluye /uploads/, agregarlo
    if (filepath && !filepath.includes('/uploads/')) {
      if (filepath.startsWith('/')) {
        filepath = filepath.substring(1)
      }
      filepath = `/uploads/${filepath}`
    }
    
    return `${backendBaseUrl.value}${filepath}`
  }
  
  // Inicializar detección al usar el composable
  detectBackend()
  
  return {
    backendBaseUrl,
    buildMediaUrl,
    detectBackend
  }
}
