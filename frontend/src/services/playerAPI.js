/**
 * Player API - Endpoints públicos para el reproductor
 * Usa los endpoints públicos existentes en playlists.py
 */
import axios from 'axios'
import backendDetector from './backendDetector'
import { createProductionBackendDetector } from './productionDetector'

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
      
      // NUEVO: Verificar si estamos en modo producción
      const productionConfig = createProductionBackendDetector()
      
      if (productionConfig) {
        console.log('🎯 Player API en modo producción, usando mismo origen')
        playerApi.defaults.baseURL = `${productionConfig.baseUrl}/api`
        
        // Verificar conectividad
        await playerApi.get('/health', { timeout: 5000 })
        
        isPlayerAPIInitialized = true
        console.log(`✅ Player API inicializada en modo producción: ${productionConfig.baseUrl}`)
        return playerApi
      }
      
      // Modo desarrollo: usar detección automática
      console.log('🔧 Player API en modo desarrollo, detectando backend...')
      
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
    return api.get(`/player/playlists?skip=${skip}&limit=${limit}`)
  },
  
  // Alias para compatibilidad con PlayerView
  listPlaylists: async (skip = 0, limit = 100) => {
    const api = await ensurePlayerAPIInitialized()
    return api.get(`/player/playlists?skip=${skip}&limit=${limit}`)
  },
  
  // Obtener playlist específica para reproductor (con medias completas)
  getPlaylist: async (playlistId) => {
    const api = await ensurePlayerAPIInitialized()
    return api.get(`/player/playlists/${playlistId}/complete`)
  },
  
  // Obtener información básica de una playlist
  getPlaylistInfo: async (playlistId) => {
    const api = await ensurePlayerAPIInitialized()
    return api.get(`/player/playlists/${playlistId}`)
  }
}

// Función para obtener URL de media
export const getMediaUrl = async (media) => {
  if (!media) return ''
  
  console.log('🐛 getMediaUrl - Entrada:', media)
  
  try {
    // Verificar si estamos en modo producción primero
    const productionConfig = createProductionBackendDetector()
    let baseUrl
    
    if (productionConfig) {
      baseUrl = productionConfig.baseUrl
      console.log('🐛 getMediaUrl - Usando producción:', baseUrl)
    } else {
      const detected = await backendDetector.detectBackend()
      baseUrl = detected.baseUrl
      console.log('🐛 getMediaUrl - Backend detectado:', detected)
    }
    
    // Usar file_url si está disponible (debería empezar con /uploads/)
    if (media.file_url) {
      // file_url ya incluye /uploads/, así que solo agregamos el baseUrl
      const finalUrl = `${baseUrl}${media.file_url}`
      console.log('🐛 getMediaUrl - URL final con file_url:', finalUrl)
      return finalUrl
    }
    
    // Fallback: construir URL desde filepath o filename
    let filepath = media.filepath || media.served_filename || media.filename
    console.log('🐛 getMediaUrl - Filepath fallback:', filepath)
    
    // Asegurar que empiece con /uploads/
    if (!filepath.startsWith('/uploads/')) {
      filepath = `/uploads/${filepath}`
    }
    
    const finalUrl = `${baseUrl}${filepath}`
    console.log('🐛 getMediaUrl - URL final con fallback:', finalUrl)
    return finalUrl
  } catch (error) {
    console.error('🐛 getMediaUrl - Error construyendo URL de media:', error)
    
    // Fallback URL con mejor manejo
    let fallbackPath
    if (media.file_url) {
      fallbackPath = media.file_url
    } else {
      const filename = media.served_filename || media.filename
      fallbackPath = `/uploads/${filename}`
    }
    
    const fallbackUrl = `http://127.0.0.1:8000${fallbackPath}`
    console.log('🐛 getMediaUrl - URL de fallback:', fallbackUrl)
    return fallbackUrl
  }
}

export { initializePlayerAPI, ensurePlayerAPIInitialized }
