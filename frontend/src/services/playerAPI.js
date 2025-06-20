/**
 * Player API - Endpoints públicos para el reproductor
 * Usa los endpoints públicos existentes en playlists.py
 */
import axios from 'axios'
import backendDetector from './backendDetector'

// Configuración inicial de Axios para el reproductor
let playerApi = axios.create({
  baseURL: '', // Se configurará dinámicamente
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Flag para controlar la inicialización
let isPlayerAPIInitialized = false
let initializationPromise = null

// Función para inicializar la API del reproductor
const initializePlayerAPI = async () => {
  if (isPlayerAPIInitialized) return playerApi
  if (initializationPromise) return initializationPromise

  initializationPromise = (async () => {
    try {
      console.log('🎬 Inicializando API del reproductor...')
      
      // Detectar backend automáticamente
      const { baseUrl } = await backendDetector.detectBackend()
      playerApi.defaults.baseURL = `${baseUrl}/api`
      
      // Hacer una prueba rápida de conectividad
      await playerApi.get('/health', { timeout: 5000 })
      
      isPlayerAPIInitialized = true
      console.log(`✅ API del reproductor inicializada: ${baseUrl}`)
      
      return playerApi
    } catch (error) {
      console.error('❌ Error inicializando API del reproductor:', error)
      // Fallback a localhost:8000
      playerApi.defaults.baseURL = 'http://127.0.0.1:8000/api'
      
      try {
        await playerApi.get('/health', { timeout: 3000 })
        console.log('✅ API del reproductor inicializada con fallback localhost:8000')
        isPlayerAPIInitialized = true
        return playerApi
      } catch (fallbackError) {
        console.error('❌ Fallback también falló:', fallbackError)
        throw new Error('No se pudo conectar con el backend para el reproductor.')
      }
    }
  })()

  return initializationPromise
}

// Función helper para asegurar inicialización
const ensurePlayerAPIInitialized = async () => {
  if (!isPlayerAPIInitialized) {
    await initializePlayerAPI()
  }
  return playerApi
}

// API del reproductor (endpoints públicos)
export const playerAPI = {
  // Listar playlists públicas
  list: async (skip = 0, limit = 100) => {
    const api = await ensurePlayerAPIInitialized()
    return api.get(`/playlists/public?skip=${skip}&limit=${limit}`)
  },
  
  // Alias para compatibilidad con PlayerView
  listPlaylists: async (skip = 0, limit = 100) => {
    const api = await ensurePlayerAPIInitialized()
    return api.get(`/playlists/public?skip=${skip}&limit=${limit}`)
  },
  
  // Obtener playlist específica para reproductor (con medias y schedules)
  getPlaylist: async (playlistId) => {
    const api = await ensurePlayerAPIInitialized()
    return api.get(`/playlists/${playlistId}/player`)
  },
  
  // Obtener información básica de una playlist
  getPlaylistInfo: async (playlistId) => {
    const api = await ensurePlayerAPIInitialized()
    return api.get(`/playlists/${playlistId}`)
  }
}

// Función para obtener URL de media
export const getMediaUrl = async (media) => {
  if (!media) return ''
  
  try {
    const { baseUrl } = await backendDetector.detectBackend()
    
    // Usar file_url si está disponible, si no construir desde filepath
    if (media.file_url) {
      return `${baseUrl}${media.file_url}`
    }
    
    // Fallback: construir URL desde filepath o filename
    let filepath = media.filepath || media.served_filename || media.filename
    if (!filepath.startsWith('/uploads/')) {
      filepath = `/uploads/${filepath}`
    }
    
    return `${baseUrl}${filepath}`
  } catch (error) {
    console.error('Error construyendo URL de media:', error)
    // Fallback URL
    const filepath = media.file_url || `/uploads/${media.served_filename || media.filename}`
    return `http://127.0.0.1:8000${filepath}`
  }
}

export { initializePlayerAPI, ensurePlayerAPIInitialized }
