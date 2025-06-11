import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import Ok_TestView from '../views/Ok_TestView.vue'
import Error_View from '../views/Error_View.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { 
      requiresAuth: false,
      title: 'Iniciar Sesión - Signance System'
    }
  },
  {
    path: '/test-ok',
    name: 'TestOk',
    component: Ok_TestView,
    meta: { 
      requiresAuth: true,
      title: 'Prueba Exitosa - Signance System'
    }
  },
  {
    path: '/error',
    name: 'Error',
    component: Error_View,
    meta: { 
      requiresAuth: false,
      title: 'Error - Signance System'
    }
  }
  // Futuras rutas para el sistema completo:
  /*
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/AdminView.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/config',
    name: 'Config',
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
    path: '/player',
    name: 'Player',
    component: () => import('../views/PlayerView.vue'),
    meta: { requiresAuth: true }
  }
  */
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation Guards
router.beforeEach((to, from, next) => {
  // Actualizar título de la página
  document.title = to.meta.title || 'Signance System'
  
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
