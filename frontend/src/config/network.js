// Configuración de red para Signance System
// Detección completamente dinámica - NO hardcodear IPs

export const NETWORK_CONFIG = {
  // Puerto preferido del backend
  BACKEND_PREFERRED_PORT: 8000,
  
  // Rango de puertos a probar
  PORT_RANGE: {
    start: 8000,
    end: 8010
  },
  
  // Endpoint para verificar que el backend está funcionando
  HEALTH_ENDPOINT: '/health',
  
  // Timeout para las pruebas de conectividad
  CONNECTION_TIMEOUT: 3000
}

// Detectar automáticamente todas las IPs posibles donde puede estar el backend
export function generateCandidateIPs() {
  const currentHost = window.location.hostname
  const ips = []
  
  console.log(`🔍 Detectando IPs candidatas desde: ${currentHost}`)
  
  // 1. PRIORIDAD: La IP desde donde se accede al frontend (muy probable que el backend esté aquí)
  if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
    ips.push(currentHost)
    console.log(`✅ Agregando IP actual del frontend: ${currentHost}`)
  }
  
  // 2. Localhost (por si el backend está en la misma máquina)
  ips.push('127.0.0.1', 'localhost')
  
  // 3. Si tenemos una IP de red, generar IPs comunes de la misma red
  if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
    const ipParts = currentHost.split('.')
    if (ipParts.length === 4 && ipParts.every(part => !isNaN(part))) {
      const baseNetwork = `${ipParts[0]}.${ipParts[1]}.${ipParts[2]}`
      console.log(`🌐 Generando IPs de la red: ${baseNetwork}.x`)
      
      // IPs comunes de servidores en la red
      const commonServerIPs = [1, 10, 50, 100, 150, 200, 254]
      for (const ip of commonServerIPs) {
        ips.push(`${baseNetwork}.${ip}`)
      }
    }
  }
  
  // 4. Redes comunes de routers/modems
  const commonNetworks = [
    '192.168.1', '192.168.0', '192.168.100', '192.168.10',
    '10.0.0', '10.0.1', '10.1.1',
    '172.16.0', '172.16.1'
  ]
  
  for (const network of commonNetworks) {
    // Solo agregar si no es la red actual para evitar duplicados
    if (!currentHost.startsWith(network)) {
      ips.push(`${network}.1`, `${network}.100`, `${network}.10`)
    }
  }
  
  // Eliminar duplicados y retornar
  const uniqueIPs = [...new Set(ips)]
  console.log(`🎯 ${uniqueIPs.length} IPs candidatas generadas:`, uniqueIPs)
  return uniqueIPs
}
