<template>
  <div class="info-card actions-card">
    <div class="card-title"><h3>Acciones Rápidas</h3></div>
    <div class="actions-grid">
      <div class="action-button primary-action" @click="$router.push('/config')">
        <q-icon name="settings" size="2rem" />
        <span>Configuración</span>
      </div>
      <div class="action-button secondary-action" @click="$router.push('/player')">
        <q-icon name="play_circle" size="2rem" />
        <span>Reproductor</span>
      </div>
      <div class="action-button accent-action" @click="$router.push('/media')">
        <q-icon name="folder" size="2rem" />
        <span>Explorar Media</span>
      </div>
      <div class="action-button warning-action" @click="$emit('logout')">
        <q-icon name="logout" size="2rem" />
        <span>Cerrar Sesión</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const $router = useRouter()

defineEmits(['logout'])
</script>

<style scoped>
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 10px;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 25px 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 1rem;
  text-align: center;
  border: 2px solid transparent;
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.primary-action {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.primary-action:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

.secondary-action {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.secondary-action:hover {
  background: linear-gradient(135deg, #ee82e9 0%, #f3455a 100%);
}

.accent-action {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.accent-action:hover {
  background: linear-gradient(135deg, #3d9aec 0%, #00e0ec 100%);
}

.warning-action {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
}

.warning-action:hover {
  background: linear-gradient(135deg, #f95e88 0%, #fedd2e 100%);
}

/* Dark mode styles */
.body--dark .action-button {
  border-color: rgba(255, 255, 255, 0.1);
}

.body--dark .primary-action {
  background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
}

.body--dark .secondary-action {
  background: linear-gradient(135deg, #9f7aea 0%, #667eea 100%);
}

.body--dark .accent-action {
  background: linear-gradient(135deg, #38b2ac 0%, #319795 100%);
}

.body--dark .warning-action {
  background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
}

/* Responsive Design */
@media (max-width: 768px) {
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .action-button {
    padding: 20px 15px;
    gap: 10px;
  }
  
  .action-button q-icon {
    transform: scale(0.8);
  }
  
  .action-button span {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .actions-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .action-button {
    flex-direction: row;
    justify-content: flex-start;
    padding: 18px;
    gap: 15px;
  }
}
</style>
