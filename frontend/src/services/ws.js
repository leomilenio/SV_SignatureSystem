import backendDetector from './backendDetector'

class WebSocketService {
  constructor() {
    this.socket = null
    this.connected = false
    this.listeners = new Map()
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
    this.detectedBackendUrl = null
  }

  /**
   * Obtiene la URL del WebSocket basada en la detección del backend
   * @returns {Promise<string>}
   */
  async getWebSocketUrl() {
    try {
      // Usar el backend ya detectado o detectar uno nuevo
      let backendUrl = this.detectedBackendUrl
      
      if (!backendUrl) {
        const { baseUrl } = await backendDetector.detectBackend()
        this.detectedBackendUrl = baseUrl
        backendUrl = baseUrl
      }
      
      // Convertir HTTP a WebSocket URL
      const wsUrl = backendUrl.replace('http://', 'ws://') + '/ws'
      console.log(`🎯 URL WebSocket generada: ${wsUrl}`)
      return wsUrl
    } catch (error) {
      console.error('❌ Error obteniendo URL del WebSocket:', error)
      // Fallback a localhost
      return 'ws://127.0.0.1:8002/ws'
    }
  }

  // Conectar al WebSocket del servidor
  async connect(serverUrl = null) {
    try {
      // Si no se proporciona URL, obtener automáticamente
      if (!serverUrl) {
        serverUrl = await this.getWebSocketUrl()
      }
      
      console.log(`🔌 Conectando WebSocket a: ${serverUrl}`)
      
      // Crear conexión WebSocket nativa
      this.socket = new WebSocket(serverUrl)

      // Eventos de conexión
      this.socket.onopen = () => {
        console.log('✅ WebSocket conectado')
        this.connected = true
        this.reconnectAttempts = 0
        this.emit('connection-status', { connected: true })
      }

      this.socket.onclose = (event) => {
        console.log('❌ WebSocket desconectado:', event.code, event.reason)
        this.connected = false
        this.emit('connection-status', { connected: false, reason: event.reason })
        
        // Intentar reconectar automáticamente
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++
          console.log(`🔄 Intentando reconectar (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`)
          setTimeout(() => this.connect(serverUrl), this.reconnectDelay * this.reconnectAttempts)
        }
      }

      this.socket.onerror = (error) => {
        console.error('❌ Error de conexión WebSocket:', error)
        this.emit('connection-error', error)
      }

      this.socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          if (message.event && message.data) {
            this.emit(message.event, message.data)
          }
        } catch (error) {
          console.error('Error parseando mensaje WebSocket:', error)
        }
      }

    } catch (error) {
      console.error('Error inicializando WebSocket:', error)
    }
  }

  // Desconectar WebSocket
  disconnect() {
    if (this.socket) {
      this.socket.close()
      this.socket = null
      this.connected = false
      this.listeners.clear()
      console.log('🔌 WebSocket desconectado manualmente')
    }
  }

  // Enviar mensaje al servidor
  send(event, data) {
    if (this.socket && this.connected) {
      const message = JSON.stringify({ event, data })
      this.socket.send(message)
    } else {
      console.warn('⚠️ WebSocket no conectado, no se puede enviar:', event)
    }
  }

  // Escuchar eventos
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  // Dejar de escuchar eventos
  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event)
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  // Emitir evento a los listeners locales
  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data)
        } catch (error) {
          console.error(`Error en listener para evento ${event}:`, error)
        }
      })
    }
  }

  // Métodos específicos para Pochtecayotl Signance System
  
  // Notificar inicio de upload de archivo
  notifyUploadStart(fileData) {
    this.send('media-upload-start', fileData)
  }

  // Solicitar estado actual de reproducción
  requestPlaybackStatus() {
    this.send('get-playback-status')
  }

  // Enviar comando de control de reproductor
  sendPlayerCommand(command, data = {}) {
    this.send('player-command', { command, ...data })
  }

  // Notificar cambio en programación
  notifyScheduleChange(scheduleData) {
    this.send('schedule-change', scheduleData)
  }

  // Obtener estadísticas del sistema en tiempo real
  requestSystemStats() {
    this.send('get-system-stats')
  }
}

// Singleton instance
const wsService = new WebSocketService()

// Funciones de utilidad
export const connectWebSocket = () => {
  wsService.connect()
}

export const disconnectWebSocket = () => {
  wsService.disconnect()
}

export const isWebSocketConnected = () => {
  return wsService.connected
}

// Composable para Vue 3
export const useWebSocket = () => {
  return {
    connect: connectWebSocket,
    disconnect: disconnectWebSocket,
    isConnected: isWebSocketConnected,
    on: (event, callback) => wsService.on(event, callback),
    off: (event, callback) => wsService.off(event, callback),
    send: (event, data) => wsService.send(event, data),
    
    // Métodos específicos de Signance
    notifyUploadStart: (fileData) => wsService.notifyUploadStart(fileData),
    requestPlaybackStatus: () => wsService.requestPlaybackStatus(),
    sendPlayerCommand: (command, data) => wsService.sendPlayerCommand(command, data),
    notifyScheduleChange: (scheduleData) => wsService.notifyScheduleChange(scheduleData),
    requestSystemStats: () => wsService.requestSystemStats()
  }
}

export default wsService
