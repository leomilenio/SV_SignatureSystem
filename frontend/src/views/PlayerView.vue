<template>
  <div class="signance-container">
    <h5 class="q-mb-md">Seleccionar Playlist</h5>
    <div v-if="loading" class="text-center q-my-xl">
      <q-spinner color="primary" size="2em" />
    </div>
    <div v-else>
      <div v-if="playlists.length">
        <q-list bordered separator>
          <q-item v-for="pl in playlists" :key="pl.id" clickable @click="select(pl)">
            <q-item-section>Playlist {{ pl.id }}</q-item-section>
          </q-item>
        </q-list>
      </div>
      <div v-else class="text-grey">No hay ninguna playlist</div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { scheduleAPI } from '../services/api'
import { useToast } from 'vue-toastification'

export default {
  name: 'PlayerView',
  setup() {
    const playlists = ref([])
    const loading = ref(false)
    const toast = useToast()

    const fetchPlaylists = async () => {
      loading.value = true
      try {
        const res = await scheduleAPI.list(0, 50)
        playlists.value = res.data
      } catch (e) {
        toast.error('Error obteniendo playlists')
      } finally {
        loading.value = false
      }
    }

    const select = (pl) => {
      toast.info(`Reproductor aún no implementado (playlist ${pl.id})`)
    }

    onMounted(fetchPlaylists)

    return { playlists, loading, select }
  }
}
</script>

<style scoped>
.signance-container {
  padding-top: 40px;
}
</style>
