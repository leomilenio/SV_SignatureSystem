import { io } from 'socket.io-client'

class WebSocketService {
  constructor() {
    this.socket = null
    this.connected = false
    this.listeners = new Map()
  }

  // Conectar al WebSocket del servidor
  connect(serverUrl = 'http://127.0.0.1:8002') {
    try {
      // Configurar socket con autenticación
      const token = localStorage.getItem('signance_token')
      
      this.socket = io(serverUrl, {
        auth: {
          token: token
        },
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: 5,
        timeout: 20000
      })

      // Eventos de conexión
      this.socket.on('connect', () => {
        console.log('✅ WebSocket conectado')
        this.connected = true
        this.emit('connection-status', { connected: true })
      })

      this.socket.on('disconnect', (reason) => {
        console.log('❌ WebSocket desconectado:', reason)
        this.connected = false
        this.emit('connection-status', { connected: false, reason })
      })

      this.socket.on('connect_error', (error) => {
        console.error('❌ Error de conexión WebSocket:', error)
        this.emit('connection-error', error)
      })

      // Eventos específicos del sistema
      this.setupSignanceEvents()

    } catch (error) {
      console.error('Error inicializando WebSocket:', error)
    }
  }

  // Configurar eventos específicos de Signance
  setupSignanceEvents() {
    if (!this.socket) return

    // Eventos de media/multimedia
    this.socket.on('media-upload-progress', (data) => {
      this.emit('media-upload-progress', data)
    })

    this.socket.on('media-processing-complete', (data) => {
      this.emit('media-processing-complete', data)
    })

    this.socket.on('media-processing-error', (data) => {
      this.emit('media-processing-error', data)
    })

    // Eventos de programación/scheduling
    this.socket.on('schedule-updated', (data) => {
      this.emit('schedule-updated', data)
    })

    this.socket.on('playback-status', (data) => {
      this.emit('playback-status', data)
    })

    // Eventos del sistema
    this.socket.on('system-notification', (data) => {
      this.emit('system-notification', data)
    })

    // Eventos de configuración de negocio
    this.socket.on('business-config-updated', (data) => {
      this.emit('business-config-updated', data)
    })
  }

  // Desconectar WebSocket
  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
      this.connected = false
      this.listeners.clear()
      console.log('🔌 WebSocket desconectado manualmente')
    }
  }

  // Enviar mensaje al servidor
  send(event, data) {
    if (this.socket && this.connected) {
      this.socket.emit(event, data)
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
