import axios from 'axios'
import { useToast } from 'vue-toastification'

// Configuración base de Axios
const api = axios.create({
  baseURL: 'http://127.0.0.1:8002/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

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

// Funciones de API específicas del sistema
export const authAPI = {
  // Verificar estado de configuración inicial
  checkSetup: () => api.get('/auth/check-setup'),
  
  // Configurar usuario administrador inicial
  setupAdmin: (userData) => api.post('/auth/setup-admin', userData),
  
  // Iniciar sesión
  login: (credentials) => {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },
  
  // Cerrar sesión
  logout: () => api.post('/auth/logout'),
  
  // Obtener información del usuario actual
  getCurrentUser: () => api.get('/auth/me'),
  
  // Verificar ruta protegida (para testing)
  testProtected: () => api.get('/auth/protected')
}

export const mediaAPI = {
  // Listar archivos multimedia
  list: (skip = 0, limit = 100) => api.get(`/media/?skip=${skip}&limit=${limit}`),
  
  // Obtener archivo específico
  get: (mediaId) => api.get(`/media/${mediaId}`),
  
  // Subir nuevo archivo multimedia
  upload: (fileData) => {
    const formData = new FormData()
    formData.append('file', fileData.file)
    formData.append('filename', fileData.filename)
    formData.append('media_type', fileData.media_type)
    formData.append('duration', fileData.duration)
    
    return api.post('/media/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // Actualizar archivo multimedia
  update: (mediaId, updateData) => api.put(`/media/${mediaId}`, updateData),
  
  // Eliminar archivo multimedia
  delete: (mediaId) => api.delete(`/media/${mediaId}`)
}

export const businessAPI = {
  // Obtener información del negocio
  get: () => api.get('/business/'),

  // Verificar si requiere configuración
  checkSetup: () => api.get('/business/check-setup'),
  
  // Crear información del negocio
  create: (businessData) => {
    const formData = new FormData()
    formData.append('name', businessData.name)
    if (businessData.logo) {
      formData.append('logo', businessData.logo)
    }
    
    return api.post('/business/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // Actualizar información del negocio
  update: (businessData) => {
    const formData = new FormData()
    if (businessData.name) {
      formData.append('name', businessData.name)
    }
    if (businessData.logo) {
      formData.append('logo', businessData.logo)
    }
    
    return api.put('/business/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // Obtener logo del negocio
  getLogo: () => api.get('/business/logo'),
  
  // Eliminar información del negocio
  delete: () => api.delete('/business/')
}

export const scheduleAPI = {
  // Listar todas las programaciones
  list: (skip = 0, limit = 100) => api.get(`/schedules/?skip=${skip}&limit=${limit}`),
  
  // Obtener programación específica
  get: (scheduleId) => api.get(`/schedules/${scheduleId}`),
  
  // Obtener programaciones de un medio específico
  getByMedia: (mediaId) => api.get(`/schedules/media/${mediaId}`),
  
  // Crear nueva programación
  create: (scheduleData) => api.post('/schedules/', scheduleData),
  
  // Actualizar programación
  update: (scheduleId, updateData) => api.put(`/schedules/${scheduleId}`, updateData),
  
  // Eliminar programación
  delete: (scheduleId) => api.delete(`/schedules/${scheduleId}`)
}

export const playlistAPI = {
  // Listar todas las playlists
  list: (skip = 0, limit = 100) => api.get(`/schedules/playlist-list?skip=${skip}&limit=${limit}`),
  
  // Obtener playlist específica
  get: (playlistId) => api.get(`/schedules/playlist-get/${playlistId}`),
  
  // Obtener estadísticas de playlists
  getStats: () => api.get('/schedules/playlist-stats'),
  
  // Crear nueva playlist
  create: (playlistData) => api.post('/schedules/playlist-create', playlistData),
  
  // Actualizar playlist
  update: (playlistId, updateData) => api.put(`/schedules/playlist-update/${playlistId}`, updateData),
  
  // Eliminar playlist
  delete: (playlistId) => api.delete(`/schedules/playlist-delete/${playlistId}`)
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

export default api

