/**
 * Backend Auto-Detection Service
 * Detecta automáticamente en qué puerto está corriendo el backend FastAPI
 * Soporta detección tanto en localhost como en la IP de red local
 */

class BackendDetector {
  constructor() {
    this.detectedPort = null
    this.detectedBaseUrl = null
    this.portRange = { start: 8000, end: 8010 }
    this.testEndpoint = '/health' // Endpoint simple para verificar conectividad
    this.currentHost = this.getCurrentHost()
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
    const currentHost = window.location.hostname
    const hosts = []
    
    // Siempre probar la IP fija del servidor backend primero
    hosts.push('10.0.1.76') // IP del servidor donde siempre estará el backend
    
    // Luego probar el host actual
    if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
      hosts.push('127.0.0.1', 'localhost')
    } else {
      hosts.push(currentHost)
    }
    
    // Si estamos accediendo desde una IP de red, también probar localhost
    // por si el backend está corriendo en la misma máquina
    if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
      // Intentar obtener las IPs comunes de la misma red
      const ipParts = currentHost.split('.')
      if (ipParts.length === 4) {
        // Probar algunas IPs comunes de la misma red (servidor típico)
        const baseNetwork = `${ipParts[0]}.${ipParts[1]}.${ipParts[2]}`
        hosts.push(`${baseNetwork}.1`) // Gateway común
        hosts.push(`${baseNetwork}.100`) // IP común para servidores
        hosts.push(`${baseNetwork}.10`) // IP común para servidores
      }
    }
    
    return [...new Set(hosts)] // Eliminar duplicados
  }

  /**
   * Detecta automáticamente el puerto del backend
   * @returns {Promise<{port: number, baseUrl: string}>}
   */
  async detectBackend() {
    console.log('🔍 Iniciando detección automática del backend...')
    
    // Si ya detectamos un puerto previamente, intentar usarlo primero
    if (this.detectedPort && this.detectedBaseUrl) {
      console.log(`⚡ Probando configuración previa: ${this.detectedBaseUrl}`)
      const host = new URL(this.detectedBaseUrl).hostname
      if (await this.testSpecificHostPort(host, this.detectedPort)) {
        console.log(`✅ Backend confirmado en ${this.detectedBaseUrl}`)
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
    console.log(`🎯 Hosts candidatos: ${candidateHosts.join(', ')}`)

    // Buscar en el rango de puertos para cada host
    for (const host of candidateHosts) {
      console.log(`🔍 Probando host: ${host}`)
      
      for (let port = this.portRange.start; port <= this.portRange.end; port++) {
        console.log(`🔍 Probando puerto ${port} en ${host}...`)
        
        if (await this.testSpecificHostPort(host, port)) {
          this.detectedPort = port
          this.detectedBaseUrl = `http://${host}:${port}`
          this.currentHost = host
          
          console.log(`✅ ¡Backend encontrado en ${this.detectedBaseUrl}!`)
          
          // Guardar en localStorage para próximas sesiones
          localStorage.setItem('signance_backend_port', port.toString())
          localStorage.setItem('signance_backend_url', this.detectedBaseUrl)
          localStorage.setItem('signance_backend_host', host)
          
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
    return await this.testSpecificHostPort(this.currentHost, port)
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
    
    // Verificar si el host cambió (acceso desde diferente IP)
    if (cachedHost && cachedHost !== this.currentHost) {
      console.log(`🔄 Host cambió de ${cachedHost} a ${this.currentHost}, limpiando caché...`)
      this.clearCache()
      return null
    }
    
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
}

// Instancia singleton
const backendDetector = new BackendDetector()

export default backendDetector
