// Corrección para el problema de detección de backend en producción
// Cuando el frontend se sirve desde /static/, está en el mismo servidor que el backend

export function createProductionBackendDetector() {
  const currentOrigin = window.location.origin;
  const isServedFromBackend = window.location.pathname.startsWith('/') && 
                              !window.location.hostname.includes('localhost:8080');
  
  console.log('🔍 Detectando contexto del frontend...');
  console.log(`   📍 Origin: ${currentOrigin}`);
  console.log(`   🌐 Hostname: ${window.location.hostname}`);
  console.log(`   📂 Pathname: ${window.location.pathname}`);
  console.log(`   🔗 Servido desde backend: ${isServedFromBackend}`);
  
  if (isServedFromBackend) {
    // El frontend se sirve desde el backend, usar el mismo origen
    console.log('✅ Frontend servido desde backend, usando mismo origen');
    return {
      baseUrl: currentOrigin,
      port: parseInt(window.location.port) || (window.location.protocol === 'https:' ? 443 : 80),
      isProduction: true
    };
  } else {
    // Modo desarrollo, usar detección automática
    console.log('🔧 Modo desarrollo detectado, usando auto-detección');
    return null; // Usar backendDetector normal
  }
}

// Función para detectar si necesitamos usar URLs relativas o absolutas
export function getAPIBaseURL() {
  const productionConfig = createProductionBackendDetector();
  
  if (productionConfig) {
    // En producción, usar mismo origen
    return `${productionConfig.baseUrl}/api`;
  } else {
    // En desarrollo, será configurado por backendDetector
    return null;
  }
}
