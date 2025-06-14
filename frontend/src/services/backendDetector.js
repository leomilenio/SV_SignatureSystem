/**
 * Backend Auto-Detection Service
 * Detecta automáticamente en qué puerto está corriendo el backend FastAPI
 */

class BackendDetector {
  constructor() {
    this.detectedPort = null
    this.detectedBaseUrl = null
    this.portRange = { start: 8000, end: 8010 }
    this.testEndpoint = '/health' // Endpoint simple para verificar conectividad
  }

  /**
   * Detecta automáticamente el puerto del backend
   * @returns {Promise<{port: number, baseUrl: string}>}
   */
  async detectBackend() {
    console.log('🔍 Iniciando detección automática del backend...')
    
    // Si ya detectamos un puerto previamente, intentar usarlo primero
    if (this.detectedPort) {
      console.log(`⚡ Probando puerto previamente detectado: ${this.detectedPort}`)
      if (await this.testPort(this.detectedPort)) {
        console.log(`✅ Backend confirmado en puerto ${this.detectedPort}`)
        return {
          port: this.detectedPort,
          baseUrl: this.detectedBaseUrl
        }
      } else {
        console.log(`❌ Puerto ${this.detectedPort} ya no responde, buscando nuevamente...`)
        this.detectedPort = null
        this.detectedBaseUrl = null
      }
    }

    // Buscar en el rango de puertos
    for (let port = this.portRange.start; port <= this.portRange.end; port++) {
      console.log(`🔍 Probando puerto ${port}...`)
      
      if (await this.testPort(port)) {
        this.detectedPort = port
        this.detectedBaseUrl = `http://127.0.0.1:${port}`
        
        console.log(`✅ ¡Backend encontrado en puerto ${port}!`)
        
        // Guardar en localStorage para próximas sesiones
        localStorage.setItem('signance_backend_port', port.toString())
        localStorage.setItem('signance_backend_url', this.detectedBaseUrl)
        
        return {
          port: this.detectedPort,
          baseUrl: this.detectedBaseUrl
        }
      }
    }

    throw new Error(`❌ No se pudo encontrar el backend en el rango de puertos ${this.portRange.start}-${this.portRange.end}`)
  }

  /**
   * Prueba si un puerto específico tiene el backend corriendo
   * @param {number} port 
   * @returns {Promise<boolean>}
   */
  async testPort(port) {
    const baseUrl = `http://127.0.0.1:${port}`
    
    try {
      // Intentar conectar al endpoint de health
      const response = await fetch(`${baseUrl}${this.testEndpoint}`, {
        method: 'GET',
        timeout: 2000, // 2 segundos de timeout
        signal: AbortSignal.timeout(2000)
      })

      if (response.ok) {
        const data = await response.json()
        // Verificar que sea realmente nuestro backend FastAPI
        if (data.status === 'healthy' || data.module === 'auth' || response.status === 200) {
          console.log(`✅ Puerto ${port}: Backend FastAPI confirmado - ${JSON.stringify(data)}`)
          return true
        }
      }
    } catch (error) {
      // Puerto no disponible o error de conexión
      console.log(`❌ Puerto ${port}: ${error.message}`)
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
    
    if (port && baseUrl) {
      return {
        port: parseInt(port),
        baseUrl: baseUrl
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
}

// Instancia singleton
const backendDetector = new BackendDetector()

export default backendDetector
