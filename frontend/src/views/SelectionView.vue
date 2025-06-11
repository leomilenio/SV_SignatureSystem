<template>
  <div class="selection-container signance-container">
    <q-card class="q-pa-xl text-center">
      <q-card-section>
        <h5>Bienvenido a Pochtecayotl Signance System</h5>
        <p>Seleccione una opción para continuar</p>
      </q-card-section>
      <q-card-actions align="center" class="q-gutter-md">
        <q-btn color="primary" label="Reproductor" @click="goPlayer" />
        <q-btn color="secondary" label="Admin Dashboard" @click="goAdmin" />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'SelectionView',
  setup() {
    const router = useRouter()
    const goPlayer = () => router.push('/player')
    const goAdmin = () => router.push('/login')
    return { goPlayer, goAdmin }
  }
}
</script>

<style scoped>
.selection-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
</style>
