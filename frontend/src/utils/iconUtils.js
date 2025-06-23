// Utilidad para forzar la carga correcta de Material Icons

export function initializeMaterialIcons() {
  console.log('🎨 Inicializando Material Icons...')
  
  // 1. Asegurar que Google Fonts esté cargado
  loadGoogleFonts()
  
  // 2. Aplicar CSS correctivo
  applyCorrectiveCSS()
  
  // 3. Verificar carga después de un delay
  setTimeout(verifyIconsLoaded, 1000)
}

function loadGoogleFonts() {
  // Verificar si ya existe un link a Google Fonts
  const existingLink = document.querySelector('link[href*="fonts.googleapis.com"][href*="Material+Icons"]')
  
  if (!existingLink) {
    console.log('📥 Cargando Material Icons desde Google Fonts...')
    
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://fonts.googleapis.com/icon?family=Material+Icons&display=swap'
    link.onload = () => {
      console.log('✅ Material Icons cargado desde Google Fonts')
    }
    link.onerror = () => {
      console.error('❌ Error al cargar Material Icons desde Google Fonts')
    }
    
    document.head.appendChild(link)
  }
}

function applyCorrectiveCSS() {
  console.log('🎨 Aplicando CSS correctivo para iconos...')
  
  const css = `
    /* Corrección global para Material Icons sin interferir con tamaños */
    .material-icons {
      font-family: 'Material Icons' !important;
      font-weight: normal !important;
      font-style: normal !important;
      line-height: 1 !important;
      letter-spacing: normal !important;
      text-transform: none !important;
      display: inline-block !important;
      white-space: nowrap !important;
      word-wrap: normal !important;
      direction: ltr !important;
      font-feature-settings: 'liga' !important;
      -webkit-font-feature-settings: 'liga' !important;
      -webkit-font-smoothing: antialiased !important;
      -moz-osx-font-smoothing: grayscale !important;
    }
    
    /* Corrección específica para Quasar Icons - mantener tamaños */
    .q-icon {
      font-family: 'Material Icons' !important;
      font-feature-settings: 'liga' !important;
      -webkit-font-feature-settings: 'liga' !important;
      /* NO sobrescribir font-size, width, height - dejar que Quasar los maneje */
    }
    
    /* Corrección para iconos que aparecen como texto */
    .q-icon:not(.q-icon--svg) {
      font-family: 'Material Icons' !important;
    }
  `
  
  const style = document.createElement('style')
  style.id = 'material-icons-fix'
  style.textContent = css
  document.head.appendChild(style)
}

function verifyIconsLoaded() {
  console.log('🔍 Verificando carga de iconos...')
  
  // Crear elemento de prueba
  const testElement = document.createElement('i')
  testElement.className = 'material-icons'
  testElement.textContent = 'home'
  testElement.style.position = 'absolute'
  testElement.style.left = '-9999px'
  testElement.style.fontSize = '24px'
  
  document.body.appendChild(testElement)
  
  setTimeout(() => {
    const rect = testElement.getBoundingClientRect()
    const computedStyle = window.getComputedStyle(testElement)
    
    console.log('📊 Resultados de verificación:', {
      width: rect.width,
      height: rect.height,
      fontFamily: computedStyle.fontFamily,
      fontSize: computedStyle.fontSize,
      rendered: rect.width > 0 && rect.height > 0
    })
    
    if (rect.width > 0 && rect.height > 0) {
      console.log('✅ Material Icons cargado correctamente')
    } else {
      console.warn('⚠️ Material Icons puede no estar cargando correctamente')
      // Intentar una segunda corrección
      forceIconCorrection()
    }
    
    document.body.removeChild(testElement)
  }, 100)
}

function forceIconCorrection() {
  console.log('🔧 Aplicando corrección forzada de iconos...')
  
  // Forzar recarga de todos los iconos
  const iconElements = document.querySelectorAll('.q-icon')
  iconElements.forEach((element, index) => {
    element.style.fontFamily = '"Material Icons" !important'
    
    // Si el elemento contiene texto (nombre del icono), puede ser que no se esté renderizando
    if (element.textContent && element.textContent.length > 0) {
      console.warn('Icono ' + index + ' contiene texto: "' + element.textContent + '"')
      // Crear un elemento i con la clase material-icons
      const iconText = element.textContent
      element.innerHTML = '<i class="material-icons">' + iconText + '</i>'
    }
  })
}

// Función para verificar si un icono específico está disponible
export function checkIconAvailability(iconName) {
  const testElement = document.createElement('i')
  testElement.className = 'material-icons'
  testElement.textContent = iconName
  testElement.style.position = 'absolute'
  testElement.style.left = '-9999px'
  
  document.body.appendChild(testElement)
  
  return new Promise((resolve) => {
    setTimeout(() => {
      const rect = testElement.getBoundingClientRect()
      const isAvailable = rect.width > 0 && rect.height > 0
      document.body.removeChild(testElement)
      resolve(isAvailable)
    }, 100)
  })
}

// Función para obtener información de debug
export function getIconDebugInfo() {
  return {
    fontsAPI: {
      available: !!document.fonts,
      size: document.fonts ? document.fonts.size : 'N/A',
      materialIconsCheck: document.fonts ? document.fonts.check('1rem "Material Icons"') : 'N/A'
    },
    stylesheets: Array.from(document.styleSheets).map(sheet => {
      try {
        return {
          href: sheet.href,
          rules: sheet.cssRules ? sheet.cssRules.length : 'N/A'
        }
      } catch (e) {
        return {
          href: sheet.href,
          error: 'CORS restriction'
        }
      }
    }),
    materialIconsLinks: Array.from(document.querySelectorAll('link[href*="material-icons"], link[href*="Material+Icons"]')).map(link => link.href)
  }
}

// Función para corregir tamaños de iconos
export function fixIconSizes() {
  console.log('🔧 Corrigiendo tamaños de iconos...')
  
  // No aplicamos tamaños fijos, dejamos que Quasar maneje los tamaños
  const icons = document.querySelectorAll('.q-icon')
  
  icons.forEach(icon => {
    // Solo nos aseguramos de que tengan la fuente correcta
    if (!icon.style.fontFamily || !icon.style.fontFamily.includes('Material Icons')) {
      icon.style.fontFamily = 'Material Icons, Material Icons Outlined, Material Icons Round, Material Icons Sharp, Material Icons Two Tone'
    }
    
    // Removemos cualquier tamaño fijo que hayamos aplicado anteriormente
    if (icon.style.fontSize && (icon.style.fontSize === '16px' || icon.style.fontSize === '14px' || icon.style.fontSize === '24px')) {
      icon.style.removeProperty('font-size')
    }
    if (icon.style.width && (icon.style.width === '16px' || icon.style.width === '14px' || icon.style.width === '24px')) {
      icon.style.removeProperty('width')
    }
    if (icon.style.height && (icon.style.height === '16px' || icon.style.height === '14px' || icon.style.height === '24px')) {
      icon.style.removeProperty('height')
    }
  })
  
  console.log('✅ Tamaños corregidos para ' + icons.length + ' iconos')
}

export function verifyIconSizes() {
  const icons = document.querySelectorAll('.q-icon')
  console.log('🔍 Verificando tamaños de iconos:')
  
  icons.forEach((icon, index) => {
    const computedStyle = window.getComputedStyle(icon)
    console.log('Icono ' + (index + 1) + ':', {
      fontSize: computedStyle.fontSize,
      width: computedStyle.width,
      height: computedStyle.height,
      fontFamily: computedStyle.fontFamily,
      classes: icon.className
    })
  })
}

export function resetIconSizes() {
  console.log('🔄 Reseteando tamaños de iconos a valores por defecto de Quasar...')
  
  const icons = document.querySelectorAll('.q-icon')
  
  icons.forEach(icon => {
    // Removemos estilos inline que puedan estar interfiriendo
    icon.style.removeProperty('font-size')
    icon.style.removeProperty('width') 
    icon.style.removeProperty('height')
    
    // Mantenemos solo la fuente
    icon.style.fontFamily = 'Material Icons, Material Icons Outlined, Material Icons Round, Material Icons Sharp, Material Icons Two Tone'
  })
  
  console.log('✅ Tamaños reseteados para ' + icons.length + ' iconos')
}
