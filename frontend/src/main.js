import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Quasar Framework
import { Quasar, Notify, Dialog, Loading } from 'quasar'
import quasarLang from 'quasar/lang/es'
import quasarIconSet from 'quasar/icon-set/material-icons'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'

// Import Quasar css
import 'quasar/src/css/index.sass'

// Toast notifications
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)

// Configure Quasar
app.use(Quasar, {
  plugins: {
    Notify,
    Dialog,
    Loading
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

app.mount('#app')
