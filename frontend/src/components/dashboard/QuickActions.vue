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
defineEmits(['logout'])
</script>
