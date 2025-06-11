<template>
  <div class="signance-container q-pa-md">
    <q-card class="q-pa-lg" style="max-width:400px;margin:auto;">
      <q-card-section>
        <h5 class="text-center">Configuración del Negocio</h5>
      </q-card-section>
      <q-card-section>
        <q-form @submit.prevent="save" class="q-gutter-md">
          <q-input v-model="form.name" label="Nombre del negocio" required />
          <q-file v-model="form.logo" label="Logo (PNG)" accept="image/png" />
          <q-btn type="submit" color="primary" label="Guardar" :loading="loading" />
        </q-form>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { businessAPI } from '../services/api'
import { useToast } from 'vue-toastification'

export default {
  name: 'ConfigView',
  setup() {
    const router = useRouter()
    const toast = useToast()
    const loading = ref(false)
    const form = ref({ name: '', logo: null })

    const save = async () => {
      if (!form.value.name) {
        toast.warning('Ingresa el nombre del negocio')
        return
      }
      loading.value = true
      try {
        await businessAPI.create(form.value)
        toast.success('Negocio configurado')
        router.push('/login')
      } catch (err) {
        toast.error('Error guardando negocio')
      } finally {
        loading.value = false
      }
    }

    return { form, save, loading }
  }
}
</script>

<style scoped>
.signance-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
</style>

