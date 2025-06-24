import { ref, computed, watch } from 'vue'

// Estado global del tema
const isDarkMode = ref(false)

// Cargar el tema guardado al inicializar
const savedTheme = localStorage.getItem('signance-theme')
if (savedTheme) {
  isDarkMode.value = savedTheme === 'dark'
} else {
  // Detectar preferencia del sistema
  isDarkMode.value = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
}

// Definir las variables CSS del tema
const setCSSVariables = (dark) => {
  const root = document.documentElement
  
  if (dark) {
    // Modo Oscuro
    root.style.setProperty('--primary', '#FFAA93')
    root.style.setProperty('--primary-dark', '#CC7A66')
    root.style.setProperty('--primary-light', '#FFCCB3')
    root.style.setProperty('--secondary', '#5A9DCB')
    root.style.setProperty('--accent', '#D1B05F')
    root.style.setProperty('--background', '#121212')
    root.style.setProperty('--surface', '#1E1E1E')
    root.style.setProperty('--on-primary', '#000000')
    root.style.setProperty('--on-secondary', '#FFFFFF')
    root.style.setProperty('--text-primary', '#E0E0E0')
    root.style.setProperty('--text-secondary', '#B0B0B0')
    root.style.setProperty('--border', '#2C2C2C')
    root.style.setProperty('--error', '#FF6F6F')
    root.style.setProperty('--success', '#66BB6A')
    root.style.setProperty('--warning', '#FFA726')
    root.style.setProperty('--info', '#42A5F5')
    // Sombras adaptativas para modo oscuro
    root.style.setProperty('--shadow-sm', '0 1px 3px 0 rgba(0, 0, 0, 0.5)')
    root.style.setProperty('--shadow-md', '0 4px 6px -1px rgba(0, 0, 0, 0.4)')
    root.style.setProperty('--shadow-lg', '0 10px 15px -3px rgba(0, 0, 0, 0.4)')
    root.style.setProperty('--shadow-xl', '0 20px 25px -5px rgba(0, 0, 0, 0.5)')
  } else {
    // Modo Claro
    root.style.setProperty('--primary', '#F0907B')
    root.style.setProperty('--primary-dark', '#D66E58')
    root.style.setProperty('--primary-light', '#FAC3B8')
    root.style.setProperty('--secondary', '#7BC5F0')
    root.style.setProperty('--accent', '#F0D27B')
    root.style.setProperty('--background', '#FFFFFF')
    root.style.setProperty('--surface', '#F5F5F5')
    root.style.setProperty('--on-primary', '#FFFFFF')
    root.style.setProperty('--on-secondary', '#FFFFFF')
    root.style.setProperty('--text-primary', '#212121')
    root.style.setProperty('--text-secondary', '#424242')
    root.style.setProperty('--border', '#E0E0E0')
    root.style.setProperty('--error', '#E53935')
    root.style.setProperty('--success', '#43A047')
    root.style.setProperty('--warning', '#FB8C00')
    root.style.setProperty('--info', '#1E88E5')
    // Sombras adaptativas para modo claro
    root.style.setProperty('--shadow-sm', '0 1px 3px 0 rgba(0, 0, 0, 0.1)')
    root.style.setProperty('--shadow-md', '0 4px 6px -1px rgba(0, 0, 0, 0.1)')
    root.style.setProperty('--shadow-lg', '0 10px 15px -3px rgba(0, 0, 0, 0.1)')
    root.style.setProperty('--shadow-xl', '0 20px 25px -5px rgba(0, 0, 0, 0.1)')
  }
}

// Aplicar el tema al documento
const applyTheme = (dark) => {
  setCSSVariables(dark)
  if (dark) {
    document.documentElement.setAttribute('data-theme', 'dark')
    document.body.style.backgroundColor = '#121212'
    document.body.style.color = '#E0E0E0'
    document.body.classList.add('dark-mode')
    document.body.classList.remove('light-mode')
  } else {
    document.documentElement.removeAttribute('data-theme')
    document.body.style.backgroundColor = '#FFFFFF'
    document.body.style.color = '#212121'
    document.body.classList.add('light-mode')
    document.body.classList.remove('dark-mode')
  }
}

// Aplicar tema inicial
applyTheme(isDarkMode.value)

// Observar cambios en el tema
watch(isDarkMode, (newValue) => {
  localStorage.setItem('signance-theme', newValue ? 'dark' : 'light')
  applyTheme(newValue)
})

// Variables CSS computadas para el tema
const themeVars = computed(() => ({
  // Colores principales
  primaryColor: isDarkMode.value ? '#FFAA93' : '#F0907B',
  primaryDark: isDarkMode.value ? '#CC7A66' : '#D66E58',
  primaryLight: isDarkMode.value ? '#FFCCB3' : '#FAC3B8',
  secondaryColor: isDarkMode.value ? '#5A9DCB' : '#7BC5F0',
  accentColor: isDarkMode.value ? '#D1B05F' : '#F0D27B',
  
  // Colores de estado
  errorColor: isDarkMode.value ? '#FF6F6F' : '#E53935',
  successColor: isDarkMode.value ? '#66BB6A' : '#43A047',
  warningColor: isDarkMode.value ? '#FFA726' : '#FB8C00',
  infoColor: isDarkMode.value ? '#42A5F5' : '#1E88E5',
  
  // Colores de fondo y superficie
  backgroundColor: isDarkMode.value ? '#121212' : '#FFFFFF',
  surfaceColor: isDarkMode.value ? '#1E1E1E' : '#F5F5F5',
  cardColor: isDarkMode.value ? '#1E1E1E' : '#FFFFFF',
  
  // Colores de texto
  textPrimary: isDarkMode.value ? '#E0E0E0' : '#212121',
  textSecondary: isDarkMode.value ? '#B0B0B0' : '#424242',
  onPrimary: isDarkMode.value ? '#000000' : '#FFFFFF',
  onSecondary: isDarkMode.value ? '#FFFFFF' : '#FFFFFF',
  
  // Bordes y divisores
  borderColor: isDarkMode.value ? '#2C2C2C' : '#E0E0E0',
  
  // Gradientes elegantes
  gradientPrimary: isDarkMode.value 
    ? 'linear-gradient(135deg, #FFAA93 0%, #CC7A66 100%)'
    : 'linear-gradient(135deg, #F0907B 0%, #D66E58 100%)',
  gradientSecondary: isDarkMode.value
    ? 'linear-gradient(135deg, #5A9DCB 0%, #42A5F5 100%)'
    : 'linear-gradient(135deg, #7BC5F0 0%, #1E88E5 100%)',
  gradientAccent: isDarkMode.value
    ? 'linear-gradient(135deg, #D1B05F 0%, #FFA726 100%)'
    : 'linear-gradient(135deg, #F0D27B 0%, #FB8C00 100%)',
  
  // Sombras adaptativas
  shadowSm: isDarkMode.value 
    ? '0 1px 3px 0 rgba(0, 0, 0, 0.5)' 
    : '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
  shadowMd: isDarkMode.value 
    ? '0 4px 6px -1px rgba(0, 0, 0, 0.4)' 
    : '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  shadowLg: isDarkMode.value 
    ? '0 10px 15px -3px rgba(0, 0, 0, 0.4)' 
    : '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  shadowXl: isDarkMode.value
    ? '0 20px 25px -5px rgba(0, 0, 0, 0.5)'
    : '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
  
  // Estados hover
  hoverColor: isDarkMode.value ? '#2C2C2C' : '#F5F5F5',
  hoverPrimary: isDarkMode.value ? 'rgba(255, 170, 147, 0.1)' : 'rgba(240, 144, 123, 0.1)',
  hoverSecondary: isDarkMode.value ? 'rgba(90, 157, 203, 0.1)' : 'rgba(123, 197, 240, 0.1)'
}))

// Función para alternar tema
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
}

// Función para cargar tema (para compatibilidad)
const loadTheme = () => {
  applyTheme(isDarkMode.value)
}

export function useTheme() {
  return {
    isDarkMode,
    toggleTheme,
    loadTheme,
    themeVars
  }
}
