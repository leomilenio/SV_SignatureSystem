import { ref } from 'vue'
import { scheduleAPI } from '../services/api'
import { useToast } from 'vue-toastification'

export function useSchedules() {
  const schedules = ref([])
  const toast = useToast()

  const loadSchedules = async () => {
    try {
      const { data } = await scheduleAPI.list()
      schedules.value = data
    } catch (error) {
      toast.error('Error cargando programaciones')
    }
  }

  const createSchedule = async (payload) => {
    await scheduleAPI.create(payload)
    await loadSchedules()
  }

  return {
    schedules,
    loadSchedules,
    createSchedule
  }
}
