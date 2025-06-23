// Utilidades específicas para manejar tamaños de iconos

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

// Función para aplicar correcciones CSS específicas de tamaños
export function applyIconSizeFixes() {
  // Verificar si ya existe el estilo
  const existingStyle = document.querySelector('#icon-size-fixes')
  if (existingStyle) {
    existingStyle.remove()
  }
  
  const css = `
    /* Corrección específica para mantener el sistema de tamaños de Quasar */
    .q-icon {
      font-family: 'Material Icons' !important;
      /* Permitir que Quasar maneje todos los tamaños automáticamente */
    }
    
    /* Asegurar que las clases de tamaño de Quasar NO sean sobrescritas */
    .q-icon.text-xs,
    .q-icon.text-sm,
    .q-icon.text-base,
    .q-icon.text-lg,
    .q-icon.text-xl,
    .q-icon.text-2xl,
    .q-icon.text-3xl,
    .q-icon.text-4xl,
    .q-icon.text-5xl,
    .q-icon.text-6xl {
      /* Dejar que Quasar maneje estos tamaños naturalmente */
    }
  `
  
  const style = document.createElement('style')
  style.id = 'icon-size-fixes'
  style.textContent = css
  document.head.appendChild(style)
  
  console.log('✅ CSS de corrección de tamaños aplicado (sin sobreescribir)')
}

// Función para testear diferentes tamaños
export function testIconSizes() {
  const testContainer = document.createElement('div')
  testContainer.id = 'icon-size-test'
  testContainer.style.position = 'fixed'
  testContainer.style.top = '10px'
  testContainer.style.right = '10px'
  testContainer.style.background = 'white'
  testContainer.style.padding = '10px'
  testContainer.style.border = '1px solid black'
  testContainer.style.zIndex = '9999'
  
  const sizes = ['xs', 'sm', 'md', 'lg', 'xl']
  sizes.forEach(size => {
    const icon = document.createElement('i')
    icon.className = 'q-icon material-icons'
    icon.style.fontSize = size === 'xs' ? '12px' : 
                         size === 'sm' ? '16px' :
                         size === 'md' ? '20px' :
                         size === 'lg' ? '24px' : '32px'
    icon.textContent = 'home'
    
    const label = document.createElement('span')
    label.textContent = ' ' + size + ' '
    
    testContainer.appendChild(icon)
    testContainer.appendChild(label)
  })
  
  const closeBtn = document.createElement('button')
  closeBtn.textContent = 'X'
  closeBtn.onclick = () => document.body.removeChild(testContainer)
  testContainer.appendChild(closeBtn)
  
  document.body.appendChild(testContainer)
  
  console.log('✅ Test de tamaños de iconos agregado a la página')
}
