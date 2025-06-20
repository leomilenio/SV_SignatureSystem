/**
 * Backend Auto-Detection Service
 * Detecta automáticamente en qué puerto está corriendo el backend FastAPI
 * Soporta detección completamente dinámica sin hardcodear IPs
 */

import { NETWORK_CONFIG, generateCandidateIPs } from '@/config/network'

class BackendDetector {
  constructor() {
    this.detectedPort = null
    this.detectedBaseUrl = null
    this.portRange = NETWORK_CONFIG.PORT_RANGE
    this.testEndpoint = NETWORK_CONFIG.HEALTH_ENDPOINT
    this.preferredPort = NETWORK_CONFIG.BACKEND_PREFERRED_PORT
    this.connectionTimeout = NETWORK_CONFIG.CONNECTION_TIMEOUT
  }

  /**
   * Obtiene el host actual basado en la URL del navegador
   * @returns {string}
   */
  getCurrentHost() {
    // Si estamos accediendo por IP, usar esa IP para el backend
    // Si estamos en localhost, usar localhost
    const hostname = window.location.hostname
    
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return '127.0.0.1'
    }
    
    // Si accedemos por IP de red local, usar esa misma IP para el backend
    return hostname
  }

  /**
   * Obtiene una lista de hosts candidatos para probar
   * @returns {string[]}
   */
  getCandidateHosts() {
    // Usar la función centralizada para obtener IPs dinámicamente
    return generateCandidateIPs()
  }

  /**
   * Detecta automáticamente el puerto del backend
   * @returns {Promise<{port: number, baseUrl: string}>}
   */
  async detectBackend() {
    console.log('🔍 Iniciando detección automática del backend...')
    console.log(`🎯 Puerto preferido: ${this.preferredPort}`)
    console.log(`📊 Rango de puertos: ${this.portRange.start}-${this.portRange.end}`)
    
    // Si ya detectamos un puerto previamente, intentar usarlo primero
    if (this.detectedPort && this.detectedBaseUrl) {
      console.log(`⚡ Probando configuración previa: ${this.detectedBaseUrl}`)
      const host = new URL(this.detectedBaseUrl).hostname
      if (await this.testSpecificHostPort(host, this.detectedPort)) {
        console.log(`✅ Backend confirmado en configuración previa: ${this.detectedBaseUrl}`)
        return {
          port: this.detectedPort,
          baseUrl: this.detectedBaseUrl
        }
      } else {
        console.log(`❌ Configuración previa no responde, buscando nuevamente...`)
        this.detectedPort = null
        this.detectedBaseUrl = null
      }
    }

    // Obtener lista de hosts candidatos
    const candidateHosts = this.getCandidateHosts()
    console.log(`🎯 ${candidateHosts.length} hosts candidatos detectados`)

    // ESTRATEGIA DE BÚSQUEDA INTELIGENTE:
    // 1. Primero probar el puerto preferido en todas las IPs
    console.log(`🚀 FASE 1: Probando puerto preferido ${this.preferredPort} en todas las IPs...`)
    for (const host of candidateHosts) {
      console.log(`🔍 Probando ${host}:${this.preferredPort}`)
      if (await this.testSpecificHostPort(host, this.preferredPort)) {
        this.detectedPort = this.preferredPort
        this.detectedBaseUrl = `http://${host}:${this.preferredPort}`
        console.log(`✅ ¡Backend encontrado en puerto preferido! ${this.detectedBaseUrl}`)
        
        // Guardar en localStorage
        this.saveToLocalStorage(host, this.preferredPort)
        
        return {
          port: this.detectedPort,
          baseUrl: this.detectedBaseUrl
        }
      }
    }

    // 2. Si no se encuentra en el puerto preferido, buscar en todo el rango
    console.log(`🔍 FASE 2: Buscando en rango completo ${this.portRange.start}-${this.portRange.end}...`)
    for (const host of candidateHosts) {
      console.log(`🔍 Probando host: ${host}`)
      
      for (let port = this.portRange.start; port <= this.portRange.end; port++) {
        // Saltar el puerto preferido ya que ya lo probamos
        if (port === this.preferredPort) continue
        
        console.log(`🔍 Probando puerto ${port} en ${host}...`)
        
        if (await this.testSpecificHostPort(host, port)) {
          this.detectedPort = port
          this.detectedBaseUrl = `http://${host}:${port}`
          
          console.log(`✅ ¡Backend encontrado en ${this.detectedBaseUrl}!`)
          
          // Guardar en localStorage
          this.saveToLocalStorage(host, port)
          
          return {
            port: this.detectedPort,
            baseUrl: this.detectedBaseUrl
          }
        }
      }
    }

    throw new Error(`❌ No se pudo encontrar el backend en ningún host candidato (${candidateHosts.join(', ')}) en puertos ${this.portRange.start}-${this.portRange.end}`)
  }

  /**
   * Prueba si un puerto específico tiene el backend corriendo
   * @param {number} port 
   * @returns {Promise<boolean>}
   */
  async testPort(port) {
    // Si tenemos una URL detectada, usar ese host
    if (this.detectedBaseUrl) {
      const host = new URL(this.detectedBaseUrl).hostname
      return await this.testSpecificHostPort(host, port)
    }
    
    // Si no, usar el host actual del navegador
    const currentHost = window.location.hostname
    return await this.testSpecificHostPort(currentHost, port)
  }

  /**
   * Prueba un host y puerto específicos
   * @param {string} host 
   * @param {number} port 
   * @returns {Promise<boolean>}
   */
  async testSpecificHostPort(host, port) {
    const baseUrl = `http://${host}:${port}`
    
    try {
      // Crear un AbortController para el timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 3000) // 3 segundos
      
      // Intentar conectar al endpoint de health
      const response = await fetch(`${baseUrl}${this.testEndpoint}`, {
        method: 'GET',
        signal: controller.signal,
        mode: 'cors', // Importante para CORS
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })

      clearTimeout(timeoutId)

      if (response.ok) {
        const data = await response.json()
        // Verificar que sea realmente nuestro backend FastAPI
        if (data.status === 'healthy' || data.module === 'auth' || response.status === 200) {
          console.log(`✅ Puerto ${port} en ${host}: Backend FastAPI confirmado - ${JSON.stringify(data)}`)
          return true
        }
      }
    } catch (error) {
      // Puerto no disponible o error de conexión
      if (error.name === 'AbortError') {
        console.log(`⏱️ Puerto ${port} en ${host}: Timeout (3s)`)
      } else {
        console.log(`❌ Puerto ${port} en ${host}: ${error.message}`)
      }
    }

    return false
  }

  /**
   * Obtiene la configuración del backend desde localStorage
   * @returns {{port: number, baseUrl: string} | null}
   */
  getCachedBackend() {
    const port = localStorage.getItem('signance_backend_port')
    const baseUrl = localStorage.getItem('signance_backend_url')
    const cachedHost = localStorage.getItem('signance_backend_host')
    const currentHost = window.location.hostname
    
    // Verificar si el host cambió (acceso desde diferente IP)
    if (cachedHost && cachedHost !== currentHost) {
      console.log(`🔄 Host cambió de ${cachedHost} a ${currentHost}, limpiando caché...`)
      this.clearCache()
      return null
    }
    
    if (port && baseUrl) {
      return {
        port: parseInt(port),
        baseUrl
      }
    }
    
    return null
  }

  /**
   * Limpia la caché de detección
   */
  clearCache() {
    localStorage.removeItem('signance_backend_port')
    localStorage.removeItem('signance_backend_url')
    localStorage.removeItem('signance_backend_host')
    this.detectedPort = null
    this.detectedBaseUrl = null
  }

  /**
   * Verifica periódicamente que el backend siga disponible
   * @param {Function} onConnectionLost - Callback cuando se pierde la conexión
   */
  startHealthCheck(onConnectionLost) {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval)
    }

    this.healthCheckInterval = setInterval(async () => {
      if (this.detectedPort) {
        const isOnline = await this.testPort(this.detectedPort)
        if (!isOnline && onConnectionLost) {
          console.log('❌ Conexión con backend perdida')
          onConnectionLost()
        }
      }
    }, 30000) // Verificar cada 30 segundos
  }

  /**
   * Detiene el health check
   */
  stopHealthCheck() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval)
      this.healthCheckInterval = null
    }
  }

  /**
   * Guarda la configuración detectada en localStorage
   * @param {string} host 
   * @param {number} port 
   */
  saveToLocalStorage(host, port) {
    const baseUrl = `http://${host}:${port}`
    localStorage.setItem('signance_backend_port', port.toString())
    localStorage.setItem('signance_backend_url', baseUrl)
    localStorage.setItem('signance_backend_host', host)
    console.log(`💾 Configuración guardada: ${baseUrl}`)
  }
}

// Instancia singleton
const backendDetector = new BackendDetector()

export default backendDetector
