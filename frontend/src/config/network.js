// Configuración de red para Signance System
// Actualiza estas variables según tu configuración de red

export const NETWORK_CONFIG = {
  // IP del servidor donde se ejecuta el backend (siempre la misma)
  BACKEND_SERVER_IP: '10.0.1.76',
  
  // Puerto preferido del backend
  BACKEND_PORT: 8002,
  
  // Rango de puertos a probar si el puerto principal no está disponible
  PORT_RANGE: {
    start: 8000,
    end: 8010
  },
  
  // IPs alternativas a probar (por si el servidor cambia de IP)
  FALLBACK_IPS: [
    '127.0.0.1',
    'localhost'
  ]
}

// Auto-detectar IP de red local si es necesario
export function getLocalNetworkIPs() {
  const currentHost = window.location.hostname
  const ips = [NETWORK_CONFIG.BACKEND_SERVER_IP]
  
  if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
    ips.push(currentHost)
    
    // Generar IPs comunes de la misma red
    const ipParts = currentHost.split('.')
    if (ipParts.length === 4) {
      const baseNetwork = `${ipParts[0]}.${ipParts[1]}.${ipParts[2]}`
      ips.push(
        `${baseNetwork}.1`,   // Gateway
        `${baseNetwork}.100`, // Servidor común
        `${baseNetwork}.10`   // Servidor común
      )
    }
  }
  
  ips.push(...NETWORK_CONFIG.FALLBACK_IPS)
  
  // Eliminar duplicados y retornar
  return [...new Set(ips)]
}
