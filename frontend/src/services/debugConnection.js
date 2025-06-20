// Función utilitaria para debugging de conectividad
export const debugConnection = async () => {
  console.log('🔧 DEBUGGING CONECTIVIDAD DEL BACKEND')
  console.log('=====================================')
  
  const currentHost = window.location.hostname
  console.log(`📍 Host actual del frontend: ${currentHost}`)
  
  // Probar detección
  console.log('🔍 Iniciando detección...')
  try {
    const detector = (await import('./backendDetector')).default
    const result = await detector.detectBackend()
    console.log(`✅ Backend detectado: ${result.baseUrl}`)
    
    // Probar conectividad directa
    console.log('🧪 Probando conectividad directa...')
    const response = await fetch(`${result.baseUrl}/health`, {
      method: 'GET',
      timeout: 5000
    })
    
    if (response.ok) {
      const data = await response.json()
      console.log('✅ Respuesta del backend:', data)
    } else {
      console.log('❌ Respuesta no OK:', response.status, response.statusText)
    }
    
  } catch (error) {
    console.error('❌ Error en detección:', error)
  }
  
  // Probar URLs comunes
  const commonURLs = [
    `http://127.0.0.1:8000`,
    `http://${currentHost}:8000`,
    `http://127.0.0.1:8002`,
    `http://${currentHost}:8002`
  ]
  
  console.log('🔍 Probando URLs comunes...')
  for (const url of commonURLs) {
    try {
      const response = await fetch(`${url}/health`, {
        method: 'GET',
        timeout: 3000
      })
      console.log(`✅ ${url}: ${response.status}`)
    } catch (error) {
      console.log(`❌ ${url}: ${error.message}`)
    }
  }
  
  console.log('=====================================')
}

// Exportar para uso global en consola
if (typeof window !== 'undefined') {
  window.debugSignanceConnection = debugConnection
}
