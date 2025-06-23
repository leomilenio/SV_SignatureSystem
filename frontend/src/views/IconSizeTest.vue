<template>
  <div class="q-pa-md">
    <div class="text-h4 q-mb-md">🎯 Prueba de Tamaños de Iconos</div>
    
    <div class="q-mb-lg">
      <div class="text-h6 q-mb-sm">Tamaños por Props de Quasar:</div>
      <div class="row q-gutter-md items-center">
        <q-icon name="home" size="xs" />
        <span>xs</span>
        <q-icon name="home" size="sm" />
        <span>sm</span>
        <q-icon name="home" size="md" />
        <span>md</span>
        <q-icon name="home" size="lg" />
        <span>lg</span>
        <q-icon name="home" size="xl" />
        <span>xl</span>
      </div>
    </div>

    <div class="q-mb-lg">
      <div class="text-h6 q-mb-sm">Tamaños por Clases CSS:</div>
      <div class="row q-gutter-md items-center">
        <q-icon name="star" class="text-xs" />
        <span>text-xs</span>
        <q-icon name="star" class="text-sm" />
        <span>text-sm</span>
        <q-icon name="star" class="text-base" />
        <span>text-base</span>
        <q-icon name="star" class="text-lg" />
        <span>text-lg</span>
        <q-icon name="star" class="text-xl" />
        <span>text-xl</span>
      </div>
    </div>

    <div class="q-mb-lg">
      <div class="text-h6 q-mb-sm">Tamaños Específicos con Style:</div>
      <div class="row q-gutter-md items-center">
        <q-icon name="settings" style="font-size: 16px" />
        <span>16px</span>
        <q-icon name="settings" style="font-size: 24px" />
        <span>24px</span>
        <q-icon name="settings" style="font-size: 32px" />
        <span>32px</span>
        <q-icon name="settings" style="font-size: 48px" />
        <span>48px</span>
      </div>
    </div>

    <div class="q-mb-lg">
      <div class="text-h6 q-mb-sm">Iconos en Botones:</div>
      <div class="row q-gutter-md">
        <q-btn icon="play_circle_filled" label="Play" size="sm" />
        <q-btn icon="dashboard" label="Dashboard" size="md" />
        <q-btn icon="arrow_forward" label="Forward" size="lg" />
      </div>
    </div>

    <div class="q-mb-lg">
      <div class="text-h6 q-mb-sm">Iconos Problemáticos Originales:</div>
      <div class="row q-gutter-md items-center">
        <q-icon name="play_circle_filled" size="lg" color="primary" />
        <span>play_circle_filled</span>
        <q-icon name="arrow_forward" size="lg" color="secondary" />
        <span>arrow_forward</span>
        <q-icon name="dashboard" size="lg" color="accent" />
        <span>dashboard</span>
      </div>
    </div>

    <div class="q-mb-lg">
      <div class="text-h6 q-mb-sm">Controles de Diagnóstico:</div>
      <div class="row q-gutter-md">
        <q-btn @click="verifyIconSizes" label="Verificar Tamaños" color="primary" />
        <q-btn @click="resetIconSizes" label="Resetear Tamaños" color="secondary" />
        <q-btn @click="fixIconSizes" label="Corregir Iconos" color="positive" />
        <q-btn @click="applyIconSizeFixes" label="Aplicar CSS Fix" color="warning" />
        <q-btn @click="testIconSizes" label="Test Visual" color="info" />
      </div>
    </div>

    <div class="q-mb-lg">
      <div class="text-h6 q-mb-sm">Información del Sistema:</div>
      <div class="q-pa-md bg-grey-1 rounded-borders">
        <pre>{{ systemInfo }}</pre>
      </div>
    </div>

    <div class="q-mb-lg">
      <div class="text-h6 q-mb-sm">Log de Diagnóstico:</div>
      <div class="q-pa-md bg-grey-1 rounded-borders" style="max-height: 200px; overflow-y: auto;">
        <div v-for="(log, index) in logs" :key="index" class="q-mb-xs">
          <small>{{ log.time }}</small> - {{ log.message }}
        </div>
      </div>
    </div>

    <div class="q-mt-lg">
      <q-btn @click="$router.push('/')" label="Volver al Inicio" icon="home" color="primary" outline />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { verifyIconSizes, resetIconSizes, fixIconSizes, applyIconSizeFixes, testIconSizes } from '../utils/iconSizeUtils'

export default {
  name: 'IconSizeTest',
  setup() {
    const systemInfo = ref('')
    const logs = ref([])

    const addLog = (message) => {
      logs.value.unshift({
        time: new Date().toLocaleTimeString(),
        message
      })
      if (logs.value.length > 20) {
        logs.value = logs.value.slice(0, 20)
      }
    }

    const updateSystemInfo = () => {
      const sample = document.querySelector('.q-icon')
      if (sample) {
        const computedStyle = window.getComputedStyle(sample)
        systemInfo.value = JSON.stringify({
          'Fuente de Iconos': computedStyle.fontFamily,
          'Tamaño Base': computedStyle.fontSize,
          'User Agent': navigator.userAgent.substring(0, 100) + '...',
          'Viewport': `${window.innerWidth}x${window.innerHeight}`,
          'Timestamp': new Date().toLocaleString()
        }, null, 2)
      }
    }

    const handleVerifyIconSizes = () => {
      addLog('Verificando tamaños de iconos...')
      verifyIconSizes()
      updateSystemInfo()
    }

    const handleResetIconSizes = () => {
      addLog('Reseteando tamaños de iconos...')
      resetIconSizes()
      updateSystemInfo()
    }

    const handleFixIconSizes = () => {
      addLog('Aplicando correcciones de iconos...')
      fixIconSizes()
      updateSystemInfo()
    }

    const handleApplyIconSizeFixes = () => {
      addLog('Aplicando CSS de corrección de tamaños...')
      applyIconSizeFixes()
      updateSystemInfo()
    }

    const handleTestIconSizes = () => {
      addLog('Iniciando test visual de tamaños...')
      testIconSizes()
    }

    onMounted(() => {
      addLog('Página de prueba de tamaños cargada')
      updateSystemInfo()
    })

    return {
      systemInfo,
      logs,
      verifyIconSizes: handleVerifyIconSizes,
      resetIconSizes: handleResetIconSizes,
      fixIconSizes: handleFixIconSizes,
      applyIconSizeFixes: handleApplyIconSizeFixes,
      testIconSizes: handleTestIconSizes
    }
  }
}
</script>

<style scoped>
.row {
  align-items: center;
}
</style>
