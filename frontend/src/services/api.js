import axios from 'axios'
import { useToast } from 'vue-toastification'
import backendDetector from './backendDetector'

// Configuración inicial de Axios (se actualizará dinámicamente)
let api = axios.create({
  baseURL: '', // Iniciar vacío, se configurará automáticamente
  timeout: 15000, // Aumentar timeout para detección
  headers: {
    'Content-Type': 'application/json'
  }
})

// Función para inicializar la API con auto-detección
let isInitialized = false
let initializationPromise = null

const initializeAPI = async () => {
  if (isInitialized) return api
  if (initializationPromise) return initializationPromise

  initializationPromise = (async () => {
    try {
      console.log('🚀 Inicializando API con auto-detección del backend...')
      
      // Intentar usar caché primero
      const cached = backendDetector.getCachedBackend()
      if (cached) {
        console.log(`📦 Usando backend desde caché: ${cached.baseUrl}`)
        api.defaults.baseURL = `${cached.baseUrl}/api`
        
        // Verificar que el backend cached siga funcionando
        try {
          const isWorking = await backendDetector.testPort(cached.port)
          if (isWorking) {
            isInitialized = true
            console.log('✅ API inicializada correctamente con backend desde caché')
            return api
          } else {
            console.log('❌ Backend cached no responde, detectando nuevamente...')
            backendDetector.clearCache()
          }
        } catch (error) {
          console.log('❌ Error probando backend cached:', error.message)
          backendDetector.clearCache()
        }
      }
      
      // Detectar backend automáticamente
      console.log('🔍 Detectando backend automáticamente...')
      const { baseUrl } = await backendDetector.detectBackend()
      api.defaults.baseURL = `${baseUrl}/api`
      
      // Hacer una prueba rápida de conectividad
      console.log('🧪 Probando conectividad con el backend...')
      await api.get('/health', { timeout: 5000 })
      
      isInitialized = true
      console.log(`✅ API inicializada correctamente con backend: ${baseUrl}`)
      
      // Iniciar health check
      backendDetector.startHealthCheck(() => {
        console.log('⚠️ Conexión con backend perdida, reintentando...')
        isInitialized = false
        initializationPromise = null
      })
      
      return api
    } catch (error) {
      console.error('❌ Error inicializando API:', error)
      // Fallback: intentar con localhost en puerto 8000
      console.log('🔄 Intentando fallback con localhost:8000...')
      api.defaults.baseURL = 'http://127.0.0.1:8000/api'
      
      try {
        await api.get('/health', { timeout: 3000 })
        console.log('✅ API inicializada con fallback localhost:8000')
        isInitialized = true
        return api
      } catch (fallbackError) {
        console.error('❌ Fallback también falló:', fallbackError)
        throw new Error('No se pudo conectar con el backend. Verifica que el servidor esté ejecutándose.')
      }
    }
  })()

  return initializationPromise
}

// Función helper para asegurar que la API esté inicializada
const ensureAPIInitialized = async () => {
  if (!isInitialized) {
    await initializeAPI()
  }
  return api
}

// Interceptor de request para añadir token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('signance_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor de response para manejar errores
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const toast = useToast()
    
    if (error.response) {
      // El servidor respondió con un código de error
      const status = error.response.status
      const message = error.response.data?.detail || 'Error del servidor'
      
      switch (status) {
        case 401:
          // Token inválido o expirado
          localStorage.removeItem('signance_token')
          toast.error('Sesión expirada. Por favor inicia sesión nuevamente.')
          window.location.href = '/login'
          break
        case 403:
          toast.error('No tienes permisos para realizar esta acción')
          break
        case 404:
          toast.error('Recurso no encontrado')
          break
        case 500:
          toast.error('Error interno del servidor')
          break
        default:
          toast.error(message)
      }
    } else if (error.request) {
      // No se recibió respuesta del servidor
      toast.error('No se puede conectar con el servidor')
    } else {
      // Error en la configuración de la request
      toast.error('Error en la solicitud')
    }
    
    return Promise.reject(error)
  }
)

// Wrapper para métodos HTTP que asegura la inicialización
const createAPIMethod = (method) => {
  return async (...args) => {
    const apiInstance = await ensureAPIInitialized()
    return apiInstance[method](...args)
  }
}

// Crear métodos HTTP wrappeados
const httpMethods = {
  get: createAPIMethod('get'),
  post: createAPIMethod('post'),
  put: createAPIMethod('put'),
  delete: createAPIMethod('delete'),
  patch: createAPIMethod('patch')
}

// Funciones de API específicas del sistema
export const authAPI = {
  // Verificar estado de configuración inicial
  checkSetup: () => httpMethods.get('/auth/check-setup'),
  
  // Configurar usuario administrador inicial
  setupAdmin: (userData) => httpMethods.post('/auth/setup-admin', userData),
  
  // Iniciar sesión
  login: async (credentials) => {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    
    const apiInstance = await ensureAPIInitialized()
    return apiInstance.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },
  
  // Cerrar sesión
  logout: () => httpMethods.post('/auth/logout'),
  
  // Obtener información del usuario actual
  getCurrentUser: () => httpMethods.get('/auth/me'),
  
  // Verificar ruta protegida (para testing)
  testProtected: () => httpMethods.get('/auth/protected')
}

export const mediaAPI = {
  // Listar archivos multimedia
  list: (skip = 0, limit = 100) => httpMethods.get(`/media/?skip=${skip}&limit=${limit}`),
  
  // Obtener archivo específico
  get: (mediaId) => httpMethods.get(`/media/${mediaId}`),
  
  // Subir nuevo archivo multimedia
  upload: async (fileData) => {
    const formData = new FormData()
    formData.append('file', fileData.file)
    formData.append('filename', fileData.filename)
    formData.append('media_type', fileData.media_type)
    formData.append('duration', fileData.duration)
    
    const apiInstance = await ensureAPIInitialized()
    return apiInstance.post('/media/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // Actualizar archivo multimedia
  update: (mediaId, updateData) => httpMethods.put(`/media/${mediaId}`, updateData),
  
  // Eliminar archivo multimedia
  delete: (mediaId) => httpMethods.delete(`/media/${mediaId}`),
  
  // Nueva función: obtener playlists de un medio
  getPlaylists: (mediaId) => httpMethods.get(`/media/${mediaId}/playlists`)
}

export const businessAPI = {
  // Obtener información del negocio
  get: () => httpMethods.get('/business/'),

  // Verificar si requiere configuración
  checkSetup: () => httpMethods.get('/business/check-setup'),
  
  // Crear información del negocio
  create: async (businessData) => {
    const formData = new FormData()
    formData.append('name', businessData.name)
    if (businessData.logo) {
      formData.append('logo', businessData.logo)
    }
    
    const apiInstance = await ensureAPIInitialized()
    return apiInstance.post('/business/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // Actualizar información del negocio
  update: async (businessData) => {
    const formData = new FormData()
    if (businessData.name) {
      formData.append('name', businessData.name)
    }
    if (businessData.logo) {
      formData.append('logo', businessData.logo)
    }
    
    const apiInstance = await ensureAPIInitialized()
    return apiInstance.put('/business/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // Obtener logo del negocio
  getLogo: () => httpMethods.get('/business/logo'),
  
  // Eliminar información del negocio
  delete: () => httpMethods.delete('/business/')
}

export const scheduleAPI = {
  // Listar todas las programaciones
  list: (skip = 0, limit = 100) => httpMethods.get(`/schedules/?skip=${skip}&limit=${limit}`),
  
  // Obtener programación específica
  get: (scheduleId) => httpMethods.get(`/schedules/${scheduleId}`),
  
  // Obtener programaciones de un medio específico
  getByMedia: (mediaId) => httpMethods.get(`/schedules/media/${mediaId}`),
  
  // Obtener programaciones activas
  getActive: (scheduleType = null) => {
    const url = scheduleType ? `/schedules/schedules/active?schedule_type=${scheduleType}` : '/schedules/schedules/active'
    return httpMethods.get(url)
  },
  
  // Crear nueva programación
  create: (scheduleData) => httpMethods.post('/schedules/', scheduleData),
  
  // Actualizar programación
  update: (scheduleId, updateData) => httpMethods.put(`/schedules/${scheduleId}`, updateData),
  
  // Eliminar programación
  delete: (scheduleId) => httpMethods.delete(`/schedules/${scheduleId}`)
}

export const playlistAPI = {
  // Listar todas las playlists
  list: (skip = 0, limit = 100) => httpMethods.get(`/playlists/?skip=${skip}&limit=${limit}`),
  
  // Obtener playlist específica
  get: (playlistId) => httpMethods.get(`/playlists/${playlistId}`),
  
  // Obtener estadísticas de playlists
  getStats: () => httpMethods.get('/playlists/stats'),
  
  // Crear nueva playlist
  create: (playlistData) => httpMethods.post('/playlists/', playlistData),
  
  // Actualizar playlist
  update: (playlistId, updateData) => httpMethods.put(`/playlists/${playlistId}`, updateData),
  
  // Eliminar playlist
  delete: (playlistId) => httpMethods.delete(`/playlists/${playlistId}`),
  
  // Agregar medios a playlist (múltiples)
  addMedia: (playlistId, mediaIds) => httpMethods.post(`/playlists/${playlistId}/media`, { media_ids: mediaIds }),
  
  // Agregar un solo medio a playlist
  addSingleMedia: (playlistId, mediaData) => httpMethods.post(`/playlists/${playlistId}/media`, mediaData),
  
  // Quitar medio de playlist
  removeMedia: (playlistId, mediaId) => httpMethods.delete(`/playlists/${playlistId}/media/${mediaId}`),
  
  // Actualizar medio en playlist (duración, orden, etc.)
  updateMedia: (playlistId, mediaId, updateData) => httpMethods.put(`/playlists/${playlistId}/media/${mediaId}`, updateData),
  
  // Reordenar medios en playlist
  reorder: (playlistId, mediaOrders) => httpMethods.put(`/playlists/${playlistId}/reorder`, { media_orders: mediaOrders }),
  
  // Obtener medios de una playlist
  getMedia: (playlistId) => httpMethods.get(`/playlists/${playlistId}`)
}

// Función utilitaria para manejar errores de archivo
export const handleFileError = (error, toast) => {
  if (error.response?.status === 413) {
    toast.error('El archivo es demasiado grande')
  } else if (error.response?.status === 415) {
    toast.error('Tipo de archivo no soportado')
  } else {
    toast.error('Error al procesar el archivo')
  }
}

// Exportar funciones de inicialización
export { initializeAPI, ensureAPIInitialized }

// Exportar la instancia de API y el detector
export { backendDetector }
export default httpMethods

