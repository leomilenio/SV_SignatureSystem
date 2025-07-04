import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Inicializar API con auto-detección del backend
import { initializeAPI } from './services/api'

// Quasar Framework
import { 
  Quasar, 
  Notify, 
  Dialog, 
  Loading,
  QCard,
  QCardSection,
  QCardActions,
  QBtn,
  QInput,
  QForm,
  QPage,
  QPageContainer,
  QLayout,
  QHeader,
  QToolbar,
  QToolbarTitle,
  QDrawer,
  QList,
  QItem,
  QItemSection,
  QItemLabel,
  QSeparator,
  QIcon,
  QSpinner,
  QLinearProgress,
  QFile,
  QUploader,
  QTable,
  QTh,
  QTr,
  QTd,
  QSelect,
  QDate,
  QTime,
  QToggle,
  QDialog,
  QExpansionItem,
  QTooltip,
  QBanner,
  QBtnToggle,
  QSkeleton
} from 'quasar'
import quasarLang from 'quasar/lang/es'
import quasarIconSet from 'quasar/icon-set/material-icons'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'

// Import Quasar css
import 'quasar/dist/quasar.css'

// Import icon fixes
import './assets/icon-fixes.css'

// Toast notifications
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

// Utilidades para iconos
import { initializeMaterialIcons } from './utils/iconUtils'
import { applyIconSizeFixes } from './utils/iconSizeUtils'

const app = createApp(App)

console.log('🎬 Pochtecayotl Signance System - Frontend iniciado')
// Verificar que el iconset se esté cargando correctamente
console.log('🎨 Icon set cargado:', quasarIconSet)

// Inicializar correcciones de iconos
initializeMaterialIcons()

// Aplicar correcciones de tamaños después de un breve delay (sin interferir)
setTimeout(() => {
  applyIconSizeFixes()
}, 500)

// Configure Quasar with components
app.use(Quasar, {
  plugins: {
    Notify,
    Dialog,
    Loading
  },
  components: {
    QCard,
    QCardSection,
    QCardActions,
    QBtn,
    QInput,
    QForm,
    QPage,
    QPageContainer,
    QLayout,
    QHeader,
    QToolbar,
    QToolbarTitle,
    QDrawer,
    QList,
    QItem,
    QItemSection,
    QItemLabel,
    QSeparator,
    QIcon,
    QSpinner,
    QLinearProgress,
    QFile,
    QUploader,
    QTable,
    QTh,
    QTr,
    QTd,
    QSelect,
    QDate,
    QTime,
    QToggle,
    QDialog,
    QExpansionItem,
    QTooltip,
    QBanner,
    QBtnToggle,
    QSkeleton
  },
  lang: quasarLang,
  iconSet: quasarIconSet,
  config: {
    notify: {
      position: 'top-right',
      timeout: 3000
    }
  }
})

// Configure Toast
const toastOptions = {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
}

app.use(Toast, toastOptions)
app.use(router)

// Inicializar la detección del backend en segundo plano
initializeAPI().catch(error => {
  console.warn('⚠️ No se pudo conectar al backend al iniciar:', error.message)
  console.log('🔄 La detección se reintentará automáticamente en las próximas peticiones')
})

app.mount('#app')
