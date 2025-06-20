import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import Ok_TestView from '../views/Ok_TestView.vue'
import Error_View from '../views/Error_View.vue'
import SelectionView from '../views/SelectionView.vue'
import PlayerView from '../views/PlayerView.vue'
import ConfigView from '../views/ConfigView.vue'
import AdminView from '../views/AdminView.vue'

const routes = [
  {
    path: '/',
    name: 'Selection',
    component: SelectionView,
    meta: {
      requiresAuth: false,
      title: 'Pochtecayotl Signance System'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: {
      requiresAuth: false,
      title: 'Iniciar Sesión - Pochtecayotl Signance System'
    }
  },
  {
    path: '/config',
    name: 'Config',
    component: ConfigView,
    meta: {
      requiresAuth: false,
      title: 'Configuración - Pochtecayotl Signance System'
    }
  },
  {
    path: '/test-ok',
    name: 'TestOk',
    component: Ok_TestView,
    meta: { 
      requiresAuth: true,
      title: 'Prueba Exitosa - Pochtecayotl Signance System'
    }
  },
  {
    path: '/error',
    name: 'Error',
    component: Error_View,
    meta: {
      requiresAuth: false,
      title: 'Error - Pochtecayotl Signance System'
    }
  },
  {
    path: '/player',
    name: 'Player',
    component: PlayerView,
    meta: {
      requiresAuth: false,
      title: 'Reproductor - Pochtecayotl Signance System'
    }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
    meta: { 
      requiresAuth: true, 
      role: 'admin',
      title: 'Dashboard Admin - Pochtecayotl Signance System'
    }
  },
  // Rutas administrativas adicionales:
  {
    path: '/config-admin',
    name: 'ConfigAdmin',
    component: () => import('../views/ConfigView.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/media',
    name: 'MediaManager',
    component: () => import('../views/MediaManager.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/player-admin',
    name: 'PlayerAdmin',
    component: () => import('../views/PlayerView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation Guards
router.beforeEach((to, from, next) => {
  
  // Actualizar título de la página
  document.title = to.meta.title || 'Pochtecayotl Signance System'
  
  // Verificar autenticación
  const token = localStorage.getItem('signance_token')
  const isAuthenticated = !!token
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      // Redirigir al login si no está autenticado
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      // TODO: Verificar si el token es válido
      // TODO: Verificar roles de usuario
      next()
    }
  } else {
    // Ruta pública
    next()
  }
})

export default router
