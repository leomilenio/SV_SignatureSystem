<template>
  <div 
    class="player-container" 
    :class="{ 'fullscreen-mode': isFullscreen }"
    @mousemove="isFullscreen ? onMouseMoveFullscreen() : null"
  >
    <!-- Theme Toggle -->
    <ThemeToggle v-if="!isFullscreen" class="theme-toggle" />
    
    <!-- Player States -->
    
    <!-- Playlist Selection State -->
    <div v-if="!selectedPlaylist" class="selection-state">
      <div class="player-header">
        <div class="header-content">
          <div class="header-icon">
            <q-icon name="play_circle_filled" size="3rem" />
          </div>
          <div class="header-text">
            <h2>Reproductor de Contenido</h2>
            <p>Seleccione una playlist para comenzar la reproducción</p>
          </div>
        </div>
      </div>

      <div class="main-content">
        <div class="content-card">
          <!-- Loading State -->
          <div v-if="loading" class="loading-section">
            <q-spinner color="primary" size="3rem" />
            <p class="loading-text">Cargando playlists...</p>
          </div>

          <!-- Playlist Selection -->
          <div v-else-if="playlists.length" class="playlists-section">
            <div class="section-header">
              <h3>Playlists Disponibles</h3>
              <div class="playlist-count">
                {{ playlists.length }} playlist{{ playlists.length !== 1 ? 's' : '' }} disponible{{ playlists.length !== 1 ? 's' : '' }}
              </div>
            </div>

            <div class="playlists-grid">
              <div 
                v-for="playlist in playlists" 
                :key="playlist.id"
                class="playlist-card"
                @click="selectPlaylist(playlist)"
              >
                <div class="playlist-icon">
                  <q-icon name="queue_music" size="2.5rem" />
                </div>
                <div class="playlist-info">
                  <h4>{{ playlist.name }}</h4>
                  <p>{{ playlist.description || 'Lista de reproducción de contenido multimedia' }}</p>
                  <div class="playlist-meta">
                    <span class="meta-item">
                      <q-icon name="schedule" size="1rem" />
                      {{ formatTotalDuration(playlist.total_duration) }}
                    </span>
                    <span class="meta-item">
                      <q-icon name="playlist_play" size="1rem" />
                      {{ playlist.media_count || 0 }} elementos
                    </span>
                  </div>
                </div>
                <div class="playlist-action">
                  <q-icon name="play_arrow" size="1.5rem" />
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="empty-state">
            <div class="empty-icon">
              <q-icon name="playlist_remove" size="4rem" />
            </div>
            <h3>No hay playlists disponibles</h3>
            <p>Actualmente no hay ninguna playlist configurada en el sistema.</p>
            <div class="empty-actions">
              <q-btn
                color="primary"
                icon="add"
                label="Crear Playlist"
                @click="goToAdmin"
                rounded
                unelevated
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Footer Actions -->
      <div class="footer-actions">
        <q-btn
          color="secondary"
          icon="arrow_back"
          label="Volver"
          @click="goBack"
          outline
          rounded
        />
        <q-btn
          color="accent"
          icon="refresh"
          label="Actualizar"
          @click="fetchPlaylists"
          rounded
          unelevated
        />
      </div>
    </div>

    <!-- Player State -->
    <div v-else class="player-state">
      <!-- Media Display Area -->
      <div class="media-display-area">
        <div v-if="currentMedia" class="media-container">
          <!-- Image Display -->
          <div v-if="currentMedia.media_type === 'image' && currentMediaSrc" class="image-display">
            <img 
              :src="currentMediaSrc" 
              :alt="currentMedia.filename"
              class="media-image"
              @error="handleMediaError"
              @load="onMediaLoaded"
            />
          </div>
          
          <!-- Video Display -->
          <div v-else-if="currentMedia.media_type === 'video' && currentMediaSrc" class="video-display">
            <video 
              ref="videoPlayer"
              :src="currentMediaSrc"
              class="media-video"
              @ended="onMediaEnded"
              @error="handleMediaError"
              @loadeddata="onMediaLoaded"
              autoplay
              muted
            />
          </div>
          
          <!-- Loading state while URL is being constructed -->
          <div v-else-if="currentMedia && !currentMediaSrc" class="loading-media">
            <q-spinner-dots color="primary" size="3rem" />
            <p>Preparando {{ currentMedia.filename }}...</p>
          </div>
          
          <!-- Media Info Overlay -->
          <div class="media-info-overlay" v-if="showInfo">
            <div class="media-info">
              <h3>{{ currentMedia.filename }}</h3>
              <p>{{ currentMedia.description || 'Sin descripción' }}</p>
              <div class="media-details">
                <span>Duración: {{ getCurrentDuration() }}s</span>
                <span>Tipo: {{ currentMedia.media_type }}</span>
                <span>Posición: {{ currentMediaIndex + 1 }}/{{ playlistMedia.length }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Loading Next Media -->
        <div v-else class="loading-media">
          <q-spinner color="primary" size="4rem" />
          <p>Cargando próximo contenido...</p>
        </div>
      </div>
      
      <!-- Player Controls (Solo en modo normal) -->
      <div v-if="!isFullscreen" class="player-controls normal-controls">
        <div class="control-panel">
          <!-- Playlist Info -->
          <div class="playlist-info-controls">
            <h4>{{ selectedPlaylist.name }}</h4>
            <p>{{ playlistMedia.length }} elementos • Reproduciendo en bucle</p>
          </div>
          
          <!-- Media Controls -->
          <div class="media-controls">
            <q-btn
              :icon="isPlaying ? 'pause' : 'play_arrow'"
              @click="togglePlayPause"
              color="primary"
              size="lg"
              round
              class="play-pause-btn"
            />
            <q-btn
              icon="skip_next"
              @click="skipToNext"
              color="secondary"
              size="md"
              round
              class="skip-btn"
            />
            <q-btn
              icon="skip_previous"
              @click="skipToPrevious"
              color="secondary"
              size="md"
              round
              class="skip-btn"
            />
          </div>
          
          <!-- Progress and Info -->
          <div class="progress-info">
            <div class="progress-bar">
              <q-linear-progress 
                :value="progress" 
                color="primary" 
                size="4px" 
                class="media-progress"
              />
              <div class="time-info">
                <span>{{ formatTime(elapsedTime) }}</span>
                <span>{{ formatTime(getCurrentDuration()) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Additional Controls -->
          <div class="additional-controls">
            <q-btn
              :icon="showInfo ? 'info' : 'info_outline'"
              @click="toggleInfo"
              flat
              round
              class="info-btn"
            >
              <q-tooltip>{{ showInfo ? 'Ocultar' : 'Mostrar' }} información</q-tooltip>
            </q-btn>
            
            <q-btn
              icon="fullscreen"
              @click="toggleFullscreen"
              flat
              round
              size="md"
              class="fullscreen-btn"
            >
              <q-tooltip>Pantalla completa</q-tooltip>
            </q-btn>
            
            <q-btn
              icon="bug_report"
              @click="debugCurrentMedia"
              flat
              round
              color="orange"
              class="debug-btn"
            >
              <q-tooltip>Debug URLs</q-tooltip>
            </q-btn>
            
            <q-btn
              icon="stop"
              @click="stopPlayback"
              flat
              round
              color="negative"
              class="stop-btn"
            >
              <q-tooltip>Detener y volver</q-tooltip>
            </q-btn>
          </div>
        </div>
      </div>

      <!-- Fullscreen Exit Button (Solo en pantalla completa) -->
      <div 
        v-if="isFullscreen" 
        class="fullscreen-exit-overlay"
        :class="{ 'visible': showFullscreenControls }"
      >
        <q-btn
          icon="fullscreen_exit"
          @click="toggleFullscreen"
          color="white"
          text-color="black"
          size="xl"
          round
          class="exit-fullscreen-btn"
        >
          <q-tooltip>Salir de pantalla completa (ESC)</q-tooltip>
        </q-btn>
      </div>

      <!-- Business Logo (Solo en pantalla completa) -->
      <div v-if="isFullscreen && businessLogo" class="business-logo-overlay">
        <img :src="businessLogo" alt="Logo" class="business-logo" />
      </div>

      <!-- Schedule Override Notification -->
      <div v-if="scheduleOverride && !isFullscreen" class="schedule-notification">
        <q-banner class="bg-orange text-white">
          <template v-slot:avatar>
            <q-icon name="schedule" />
          </template>
          <strong>Programación Activa</strong><br>
          Reproduciendo contenido programado: "{{ scheduleOverride.media.filename }}"
          <template v-slot:action>
            <q-btn flat icon="close" @click="dismissScheduleNotification" />
          </template>
        </q-banner>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { playerAPI, getMediaUrl } from '../services/playerAPI'  // Usar API pública del reproductor
import backendDetector from '../services/backendDetector'
import { useToast } from 'vue-toastification'
import ThemeToggle from '../components/ThemeToggle.vue'
import { useTheme } from '../composables/useTheme'
import { useWebSocket } from '../services/ws'
import { useMediaUrl } from '../composables/useMediaUrl'

export default {
  name: 'PlayerView',
  components: {
    ThemeToggle
  },
  setup() {
    const router = useRouter()
    const toast = useToast()
    const { isDarkMode } = useTheme()
    const { backendBaseUrl, buildMediaUrl } = useMediaUrl()
    
    // Referencias a elementos del DOM
    const videoPlayer = ref(null)
    
    // Estado de la aplicación
    const loading = ref(false)
    const playlists = ref([])
    const selectedPlaylist = ref(null)
    const playlistMedia = ref([])
    const currentMedia = ref(null)
    const currentMediaIndex = ref(0)
    const isPlaying = ref(false)
    const showInfo = ref(false)
    const elapsedTime = ref(0)
    const scheduleOverride = ref(null)
    const currentMediaUrl = ref('') // URL actual del media
    
    // Timers
    let playbackTimer = null
    let scheduleCheckTimer = null
    let progressTimer = null
    
    // Computed properties
    const progress = computed(() => {
      if (!currentMedia.value) return 0
      const duration = getCurrentDuration()
      return duration > 0 ? elapsedTime.value / duration : 0
    })
    
    // Computed para URL del media actual
    const currentMediaSrc = computed(() => {
      return currentMediaUrl.value || ''
    })
    
    // WebSocket: desestructurar funciones necesarias
    const { connect, disconnect, on, off } = useWebSocket()
    
    // Handlers para eventos WebSocket
    const mediaCreatedHandler = async ({ id }) => {
      if (!selectedPlaylist.value) return
      await loadPlaylistMedia(selectedPlaylist.value.id)
      toast.info('Se añadió un nuevo medio a la playlist')
    }
    
    const playlistUpdatedHandler = async ({ playlist_id, action, media_id }) => {
      if (!selectedPlaylist.value || selectedPlaylist.value.id !== playlist_id) return
      
      console.log(`Playlist actualizada: ${action}`)
      
      // Recargar medios de la playlist activa
      const oldLength = playlistMedia.value.length
      await loadPlaylistMedia(playlist_id)
      const newLength = playlistMedia.value.length
      
      // Ajustar índice actual si cambió el total de medios
      if (action === 'media_removed' && newLength < oldLength) {
        if (currentMediaIndex.value >= newLength && newLength > 0) {
          currentMediaIndex.value = 0
          loadCurrentMedia()
        }
      }
      
      // Mostrar notificación según la acción
      switch (action) {
        case 'media_added':
          toast.info('Se añadió un medio a la playlist activa')
          break
        case 'media_removed':
          toast.warning('Se removió un medio de la playlist activa')
          break
        case 'playlist_modified':
          toast.info('La playlist activa fue modificada')
          break
      }
    }
    
    // Función para conectar WebSocket con manejo de errores
    const connectWebSocket = () => {
      try {
        connect()
        on('media_created', mediaCreatedHandler)
        on('playlist_updated', playlistUpdatedHandler)
        console.log('WebSocket conectado exitosamente')
      } catch (error) {
        console.warn('WebSocket no disponible, continuando sin actualizaciones automáticas:', error)
      }
    }
    
    // Función para desconectar WebSocket con manejo de errores
    const disconnectWebSocket = () => {
      try {
        off('media_created', mediaCreatedHandler)
        off('playlist_updated', playlistUpdatedHandler)
        disconnect()
        console.log('WebSocket desconectado exitosamente')
      } catch (error) {
        console.warn('Error al desconectar WebSocket:', error)
      }
    }
    
    // Funciones de utilidad
    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins}:${secs.toString().padStart(2, '0')}`
    }
    
    const formatTotalDuration = (totalSeconds) => {
      if (!totalSeconds) return '0:00'
      const hours = Math.floor(totalSeconds / 3600)
      const minutes = Math.floor((totalSeconds % 3600) / 60)
      const seconds = totalSeconds % 60
      
      if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
      }
      return `${minutes}:${seconds.toString().padStart(2, '0')}`
    }
    
    const getCurrentDuration = () => {
      if (!currentMedia.value) return 0
      // Usar la duración específica de la playlist o la duración original del media
      return currentMedia.value.effective_duration || currentMedia.value.duration || 5
    }
    
    // Usar la función importada de playerAPI
    const getMediaUrlForPlayer = getMediaUrl
    
    // Funciones de carga de datos
    const fetchPlaylists = async () => {
      loading.value = true
      try {
        console.log('Intentando cargar playlists...')
        const response = await playerAPI.listPlaylists()
        playlists.value = response.data || []
        console.log('Playlists cargadas exitosamente:', playlists.value)
      } catch (error) {
        console.error('Error fetching playlists:', error)
        
        if (error.response?.status === 401) {
          toast.error('Sesión expirada. Redirigiendo al login...')
          localStorage.removeItem('signance_token')
          router.push('/login')
        } else {
          toast.error('Error al cargar las playlists')
        }
      } finally {
        loading.value = false
      }
    }
    
    const loadPlaylistMedia = async (playlistId) => {
      try {
        console.log('Cargando medios de playlist:', playlistId)
        const response = await playerAPI.getPlaylist(playlistId)
        
        // El endpoint /playlists/{id}/player devuelve { medias: [...], ... }
        const playlistData = response.data || {}
        const medias = playlistData.medias || []
        
        if (!Array.isArray(medias)) {
          console.error('La respuesta no contiene un array de medias:', playlistData)
          playlistMedia.value = []
          toast.error('Error: formato de datos incorrecto')
          return
        }
        
        // Los medios ya vienen con toda la información necesaria
        playlistMedia.value = medias.map(media => ({
          ...media,  // Datos del media (id, filename, media_type, etc.)
          effective_duration: media.duration,  // Ya incluye la duración específica de la playlist
          url: media.file_url  // Usar directamente file_url del backend (ya es URL completa)
        }))
        
        console.log('Medios de playlist cargados:', {
          count: playlistMedia.value.length,
          playlist_name: playlistData.name,
          items: medias.map(media => ({
            id: media.id,
            filename: media.filename,
            duration: media.duration,
            file_url: media.file_url
          }))
        })
        
        if (playlistMedia.value.length > 0) {
          currentMediaIndex.value = 0
          loadCurrentMedia()
        } else {
          console.warn('No se encontraron medios en la playlist')
          toast.warning('Esta playlist no contiene medios')
        }
      } catch (error) {
        console.error('Error loading playlist media:', error)
        playlistMedia.value = [] // Asegurar que sea un array vacío
        toast.error('Error al cargar los medios de la playlist')
      }
    }
    
    const loadCurrentMedia = () => {
      if (playlistMedia.value.length > 0) {
        const media = playlistMedia.value[currentMediaIndex.value]
        currentMedia.value = media
        elapsedTime.value = 0
        
        // Usar la URL ya construida
        currentMediaUrl.value = media.url || ''
        
        console.log('Medio actual cargado:', {
          index: currentMediaIndex.value,
          filename: media.filename,
          media_type: media.media_type,
          filepath: media.filepath,
          duration: media.duration,
          effective_duration: media.effective_duration,
          url: media.url
        })
      } else {
        console.warn('No hay medios disponibles para cargar')
        currentMedia.value = null
        currentMediaUrl.value = ''
      }
    }
    
    // Funciones de control de reproducción
    const selectPlaylist = async (playlist) => {
      selectedPlaylist.value = playlist
      await loadPlaylistMedia(playlist.id)
      if (playlistMedia.value.length > 0) {
        startPlayback()
        toast.success(`Reproduciendo: ${playlist.name}`)
      } else {
        toast.warning('Esta playlist no tiene medios para reproducir')
      }
    }
    
    const startPlayback = () => {
      isPlaying.value = true
      scheduleMediaPlayback()
      startProgressTimer()
      startScheduleCheck()
    }
    
    const scheduleMediaPlayback = () => {
      if (!currentMedia.value) return
      
      const duration = getCurrentDuration()
      console.log(`Programando cambio de medio en ${duration} segundos`)
      
      clearTimeout(playbackTimer)
      playbackTimer = setTimeout(() => {
        if (isPlaying.value) {
          nextMedia()
        }
      }, duration * 1000)
    }
    
    const nextMedia = () => {
      if (playlistMedia.value.length === 0) return
      
      // Avanzar al siguiente medio (con bucle)
      currentMediaIndex.value = (currentMediaIndex.value + 1) % playlistMedia.value.length
      loadCurrentMedia()
      
      if (isPlaying.value) {
        scheduleMediaPlayback()
      }
    }
    
    const previousMedia = () => {
      if (playlistMedia.value.length === 0) return
      
      // Retroceder al medio anterior (con bucle)
      currentMediaIndex.value = currentMediaIndex.value === 0 
        ? playlistMedia.value.length - 1 
        : currentMediaIndex.value - 1
      loadCurrentMedia()
      
      if (isPlaying.value) {
        scheduleMediaPlayback()
      }
    }
    
    const togglePlayPause = () => {
      if (isPlaying.value) {
        pausePlayback()
      } else {
        resumePlayback()
      }
    }
    
    const pausePlayback = () => {
      isPlaying.value = false
      clearTimeout(playbackTimer)
      clearInterval(progressTimer)
      
      // Pausar video si es el tipo actual
      if (currentMedia.value?.media_type === 'video' && videoPlayer.value) {
        videoPlayer.value.pause()
      }
      
      toast.info('Reproducción pausada')
    }
    
    const resumePlayback = () => {
      isPlaying.value = true
      scheduleMediaPlayback()
      startProgressTimer()
      
      // Reanudar video si es el tipo actual
      if (currentMedia.value?.media_type === 'video' && videoPlayer.value) {
        videoPlayer.value.play()
      }
      
      toast.info('Reproducción reanudada')
    }
    
    const stopPlayback = () => {
      isPlaying.value = false
      clearTimeout(playbackTimer)
      clearInterval(progressTimer)
      clearInterval(scheduleCheckTimer)
      
      selectedPlaylist.value = null
      currentMedia.value = null
      playlistMedia.value = []
      scheduleOverride.value = null
      elapsedTime.value = 0
      
      toast.info('Reproducción detenida')
    }
    
    const skipToNext = () => {
      nextMedia()
      if (isPlaying.value) {
        scheduleMediaPlayback()
      }
    }
    
    const skipToPrevious = () => {
      previousMedia()
      if (isPlaying.value) {
        scheduleMediaPlayback()
      }
    }
    
    // Gestión de programación avanzada
    const startScheduleCheck = () => {
      // Temporalmente deshabilitado para debug
      console.log('Schedule check temporalmente deshabilitado')
      return
      
      // Verificar cada 10 segundos si hay programaciones activas
      scheduleCheckTimer = setInterval(checkActiveSchedules, 10000)
      // También verificar inmediatamente
      checkActiveSchedules()
    }
    
    const checkActiveSchedules = async () => {
      if (!selectedPlaylist.value) return
      
      try {
        // Obtener schedules activos
        const response = await scheduleAPI.getActive()
        const activeSchedules = response.data || []
        
        const now = new Date()
        const currentTime = now.toTimeString().slice(0, 8) // HH:MM:SS
        const currentDay = now.getDay() // 0 = Sunday, 1 = Monday, etc.
        const today = now.toISOString().split('T')[0] // YYYY-MM-DD
        
        console.log('Verificando programaciones activas...', {
          currentTime,
          currentDay,
          today,
          activeSchedules: activeSchedules.length
        })
        
        // Buscar schedules que deben ejecutarse ahora
        const applicableSchedule = findApplicableSchedule(activeSchedules, now, currentTime, currentDay, today)
        
        if (applicableSchedule) {
          console.log('Schedule aplicable encontrado:', applicableSchedule)
          handleScheduleOverride(applicableSchedule)
        } else if (scheduleOverride.value) {
          // Si había un schedule activo pero ya no aplica, volver a la playlist normal
          console.log('Schedule override terminado, volviendo a playlist normal')
          scheduleOverride.value = null
          // Continuar con la reproducción normal
        }
        
      } catch (error) {
        console.error('Error checking active schedules:', error)
      }
    }
    
    const findApplicableSchedule = (schedules, now, currentTime, currentDay, today) => {
      // Ordenar por prioridad (mayor prioridad primero)
      const sortedSchedules = [...schedules].sort((a, b) => (b.priority || 1) - (a.priority || 1))
      
      for (const schedule of sortedSchedules) {
        if (!schedule.is_active) continue
        
        // Verificar schedules de tipo "simple" (programación semanal)
        if (schedule.schedule_type === 'simple') {
          if (isSimpleScheduleActive(schedule, currentTime, currentDay)) {
            return schedule
          }
        }
        
        // Verificar schedules de tipo "advanced" (fechas específicas)
        if (schedule.schedule_type === 'advanced') {
          if (isAdvancedScheduleActive(schedule, now, today, currentTime)) {
            return schedule
          }
        }
      }
      
      return null
    }
    
    const isSimpleScheduleActive = (schedule, currentTime, currentDay) => {
      // Convertir día de la semana (JS usa 0=Sunday, pero nuestro modelo usa 0=Monday)
      const adjustedDay = currentDay === 0 ? 6 : currentDay - 1 // Convertir a 0=Monday
      
      // Verificar si el día actual está en los weekdays programados
      if (schedule.weekdays && !schedule.weekdays.includes(adjustedDay)) {
        return false
      }
      
      // Si es todo el día, aplica
      if (schedule.is_all_day) {
        return true
      }
      
      // Verificar horario
      if (schedule.daily_start && schedule.daily_end) {
        const currentMinutes = timeToMinutes(currentTime)
        const startMinutes = timeToMinutes(schedule.daily_start)
        const endMinutes = timeToMinutes(schedule.daily_end)
        
        return currentMinutes >= startMinutes && currentMinutes <= endMinutes
      }
      
      return false
    }
    
    const isAdvancedScheduleActive = (schedule, now, today, currentTime) => {
      // Verificar fechas de inicio y fin
      if (schedule.start_date && schedule.end_date) {
        const startDate = new Date(schedule.start_date)
        const endDate = new Date(schedule.end_date)
        
        if (now < startDate || now > endDate) {
          return false
        }
      }
      
      // Verificar tiempos específicos
      if (schedule.specific_times && Array.isArray(schedule.specific_times)) {
        for (const specificTime of schedule.specific_times) {
          if (isSpecificTimeActive(specificTime, today, currentTime)) {
            return true
          }
        }
        return false
      }
      
      // Si no hay tiempos específicos pero está en el rango de fechas, aplica todo el día
      return true
    }
    
    const isSpecificTimeActive = (specificTime, today, currentTime) => {
      // specificTime puede ser:
      // - { date: "2024-01-15", start_time: "10:00", end_time: "12:00" }
      // - { date: "2024-01-15", time: "10:30" } (tiempo específico)
      
      if (specificTime.date !== today) {
        return false
      }
      
      if (specificTime.time) {
        // Tiempo específico con tolerancia de ±30 segundos
        const specificMinutes = timeToMinutes(specificTime.time)
        const currentMinutes = timeToMinutes(currentTime)
        return Math.abs(currentMinutes - specificMinutes) <= 0.5 // 30 segundos
      }
      
      if (specificTime.start_time && specificTime.end_time) {
        const currentMinutes = timeToMinutes(currentTime)
        const startMinutes = timeToMinutes(specificTime.start_time)
        const endMinutes = timeToMinutes(specificTime.end_time)
        
        return currentMinutes >= startMinutes && currentMinutes <= endMinutes
      }
      
      return false
    }
    
    const timeToMinutes = (timeString) => {
      // Convertir "HH:MM" o "HH:MM:SS" a minutos desde medianoche
      const parts = timeString.split(':')
      const hours = parseInt(parts[0], 10)
      const minutes = parseInt(parts[1], 10)
      const seconds = parts[2] ? parseInt(parts[2], 10) : 0
      
      return hours * 60 + minutes + seconds / 60
    }
    
    const handleScheduleOverride = (schedule) => {
      // Si ya estamos reproduciendo este schedule, no hacer nada
      if (scheduleOverride.value && scheduleOverride.value.id === schedule.id) {
        return
      }
      
      console.log('Aplicando schedule override:', schedule)
      
      // Pausar la reproducción actual
      const wasPlaying = isPlaying.value
      pausePlayback()
      
      // Configurar el schedule override
      scheduleOverride.value = schedule
      
      // Si el schedule es para un medio específico, reproducirlo
      if (schedule.media_id && schedule.media) {
        // Crear un "medio virtual" con la información del schedule
        const scheduleMedia = {
          ...schedule.media,
          effective_duration: schedule.media.duration, // Usar duración original
          isScheduleOverride: true,
          scheduleInfo: {
            type: schedule.schedule_type,
            priority: schedule.priority,
            id: schedule.id
          }
        }
        
        // Guardar el estado actual de la playlist
        const originalIndex = currentMediaIndex.value
        const originalMedia = currentMedia.value
        
        // Reproducir el medio programado
        currentMedia.value = scheduleMedia
        elapsedTime.value = 0
        
        if (wasPlaying) {
          isPlaying.value = true
          scheduleMediaPlayback()
          startProgressTimer()
        }
        
        // Mostrar notificación
        toast.info(`Reproduciendo contenido programado: ${schedule.media.filename}`)
        
        // Programar volver a la playlist original cuando termine el medio programado
        setTimeout(() => {
          if (scheduleOverride.value && scheduleOverride.value.id === schedule.id) {
            console.log('Finalizando schedule override, volviendo a playlist')
            scheduleOverride.value = null
            
            // Volver al medio original o al siguiente
            currentMediaIndex.value = originalIndex
            loadCurrentMedia()
            
            if (isPlaying.value) {
              scheduleMediaPlayback()
            }
          }
        }, (scheduleMedia.effective_duration || 5) * 1000)
        
      } else if (schedule.playlist_id && schedule.playlist) {
        // Si el schedule es para una playlist completa, cambiar a esa playlist
        // Esta sería una funcionalidad más avanzada para implementar después
        console.log('Schedule para playlist completa - funcionalidad pendiente')
      }
    }
    
    // Gestión de progreso
    const startProgressTimer = () => {
      clearInterval(progressTimer)
      progressTimer = setInterval(() => {
        if (isPlaying.value && currentMedia.value) {
          elapsedTime.value += 0.1
          
          // Verificar si el video ha terminado naturalmente
          if (currentMedia.value.media_type === 'video' && videoPlayer.value) {
            if (videoPlayer.value.ended) {
              onMediaEnded()
            }
          }
        }
      }, 100)
    }
    
    // Event handlers
    const onMediaEnded = () => {
      console.log('Medio terminado, avanzando al siguiente')
      nextMedia()
    }
    
    const onMediaLoaded = () => {
      console.log('Medio cargado exitosamente:', currentMedia.value?.filename)
    }
    
    const handleMediaError = async (error) => {
      console.error('Error de medio:', {
        error,
        media: currentMedia.value,
        url: currentMediaUrl.value
      })
      
      // Debug: Verificar detección del backend
      try {
        const backendDetector = (await import('../services/backendDetector')).default
        const detected = await backendDetector.detectBackend()
        console.log('🔍 Backend detectado:', detected)
        
        // Debug: Verificar qué URL está construyendo getMediaUrl
        const { getMediaUrl } = await import('../services/playerAPI')
        const debugUrl = await getMediaUrl(currentMedia.value)
        console.log('🔍 URL construida por getMediaUrl:', debugUrl)
        
        // Debug: Verificar si el archivo existe en el servidor
        const testUrl = `${detected.baseUrl}/uploads/${currentMedia.value?.served_filename || currentMedia.value?.filename}`
        console.log('🔍 URL de prueba directa:', testUrl)
        
        // Probar acceso directo al archivo
        try {
          const response = await fetch(testUrl, { method: 'HEAD' })
          console.log('🔍 Respuesta del servidor para archivo:', response.status, response.statusText)
        } catch (fetchError) {
          console.error('🔍 Error al acceder al archivo:', fetchError)
        }
        
      } catch (debugError) {
        console.error('🔍 Error en debug:', debugError)
      }
      
      toast.error(`Error al cargar: ${currentMedia.value?.filename || 'medio desconocido'}`)
      
      // Intentar cargar el siguiente medio después de un breve delay
      setTimeout(() => {
        if (playlistMedia.value.length > 1) {
          console.log('Saltando al siguiente medio debido a error')
          nextMedia()
        } else {
          console.log('No hay más medios disponibles')
          toast.warning('No hay más medios disponibles en la playlist')
        }
      }, 2000)
    }
    
    const toggleInfo = () => {
      showInfo.value = !showInfo.value
    }
    
    const debugCurrentMedia = async () => {
      if (!currentMedia.value) {
        console.warn('No hay medio actual para debuggear')
        toast.warning('No hay medio actual para debuggear')
        return
      }
      
      console.log('🐛 === DEBUG INFORMACIÓN DEL MEDIO ===')
      console.log('🐛 Medio actual:', currentMedia.value)
      console.log('🐛 URL actual:', currentMediaUrl.value)
      
      try {
        // Debug: Verificar detección del backend
        const backendDetector = (await import('../services/backendDetector')).default
        const detected = await backendDetector.detectBackend()
        console.log('🐛 Backend detectado:', detected)
        
        // Debug: Verificar qué URL está construyendo getMediaUrl
        const { getMediaUrl } = await import('../services/playerAPI')
        const debugUrl = await getMediaUrl(currentMedia.value)
        console.log('🐛 URL construida por getMediaUrl:', debugUrl)
        
        // Debug: Diferentes variaciones de URL
        const variations = [
          `${detected.baseUrl}/uploads/${currentMedia.value.served_filename}`,
          `${detected.baseUrl}/uploads/${currentMedia.value.filename}`,
          `${detected.baseUrl}${currentMedia.value.file_url}`,
          `${detected.baseUrl}${currentMedia.value.filepath}`
        ]
        
        console.log('🐛 Variaciones de URL a probar:', variations)
        
        for (let i = 0; i < variations.length; i++) {
          const url = variations[i]
          if (url && !url.includes('undefined')) {
            try {
              const response = await fetch(url, { method: 'HEAD' })
              console.log(`🐛 Variación ${i + 1} (${url}):`, response.status, response.statusText)
            } catch (fetchError) {
              console.error(`🐛 Variación ${i + 1} falló:`, fetchError.message)
            }
          }
        }
        
        toast.info('Información de debug en la consola')
        
      } catch (debugError) {
        console.error('🐛 Error en debug:', debugError)
        toast.error('Error en debug - ver consola')
      }
    }
    
    const isFullscreen = ref(false)
    const showFullscreenControls = ref(false)
    const businessLogo = ref(null)
    
    // Timer para ocultar controles en pantalla completa
    let fullscreenControlsTimer = null
    
    // Asegurar que el estado inicial sea correcto
    const initializeFullscreenState = () => {
      isFullscreen.value = !!document.fullscreenElement
      console.log('Initialized fullscreen state:', isFullscreen.value)
    }
    
    const toggleFullscreen = async () => {
      try {
        if (!document.fullscreenElement) {
          // Entrar en pantalla completa
          const playerElement = document.querySelector('.player-state')
          if (playerElement) {
            await playerElement.requestFullscreen()
          } else {
            await document.documentElement.requestFullscreen()
          }
          isFullscreen.value = true
          toast.info('Modo pantalla completa activado')
        } else {
          // Salir de pantalla completa
          await document.exitFullscreen()
          isFullscreen.value = false
          toast.info('Modo pantalla completa desactivado')
        }
      } catch (error) {
        console.error('Error toggle fullscreen:', error)
        toast.error('Error al cambiar modo de pantalla')
      }
    }
    
    // Escuchar cambios de pantalla completa
    const handleFullscreenChange = () => {
      const wasFullscreen = isFullscreen.value
      isFullscreen.value = !!document.fullscreenElement
      
      console.log('Fullscreen state changed:', {
        wasFullscreen,
        nowFullscreen: isFullscreen.value,
        element: document.fullscreenElement
      })
      
      // Resetear controles al cambiar de modo
      if (!isFullscreen.value) {
        showFullscreenControls.value = false
        if (fullscreenControlsTimer) {
          clearTimeout(fullscreenControlsTimer)
          fullscreenControlsTimer = null
        }
      }
    }

    // Manejar movimiento del mouse en pantalla completa
    const onMouseMoveFullscreen = () => {
      if (!isFullscreen.value) return
      
      showFullscreenControls.value = true
      
      // Mostrar cursor
      document.body.style.cursor = 'default'
      
      // Limpiar timer anterior
      if (fullscreenControlsTimer) {
        clearTimeout(fullscreenControlsTimer)
      }
      
      // Ocultar controles después de 3 segundos de inactividad
      fullscreenControlsTimer = setTimeout(() => {
        showFullscreenControls.value = false
        // Ocultar cursor en pantalla completa
        if (isFullscreen.value) {
          document.body.style.cursor = 'none'
        }
      }, 3000)
    }
    
    const dismissScheduleNotification = () => {
      scheduleOverride.value = null
    }
    
    const goToAdmin = () => {
      router.push('/admin')
    }
    
    // Cargar logo del negocio
    const loadBusinessLogo = async () => {
      try {
        console.log('🔍 Intentando cargar logo del negocio...')
        
        // Obtener la URL base del backend usando la misma lógica que los medios
        let baseUrl
        try {
          const detected = await backendDetector.detectBackend()
          baseUrl = detected.baseUrl
          console.log('📡 Backend detectado para logo:', baseUrl)
        } catch (detectionError) {
          console.log('❌ Error detectando backend para logo:', detectionError)
          return
        }
        
        // Intentar cargar el logo directamente
        const logoUrl = `${baseUrl}/api/business/logo`
        console.log('🖼️ Intentando cargar logo desde:', logoUrl)
        
        try {
          const response = await fetch(logoUrl, {
            method: 'GET'
            // No necesitamos autenticación ahora que es público
          })
          
          console.log('📥 Respuesta del logo:', response.status, response.statusText)
          
          if (response.ok) {
            const data = await response.json()
            console.log('📄 Datos recibidos:', data.logo ? 'Logo base64 presente' : 'Sin logo')
            
            if (data.logo) {
              // Convertir base64 a data URL
              businessLogo.value = `data:image/png;base64,${data.logo}`
              console.log('✅ Logo cargado exitosamente como data URL')
            } else {
              console.log('❌ No hay datos de logo en la respuesta')
              businessLogo.value = null
            }
          } else if (response.status === 404) {
            console.log('📄 No hay logo configurado (404)')
            businessLogo.value = null
          } else {
            console.log('❌ Error cargando logo:', response.status, response.statusText)
            businessLogo.value = null
          }
        } catch (fetchError) {
          console.log('❌ Error de red cargando logo:', fetchError)
          businessLogo.value = null
        }
        
        // TEMPORAL: Para testing - ya no necesitamos esto
        // if (!businessLogo.value) {
        //   console.log('🧪 Usando logo de prueba para testing')
        //   businessLogo.value = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI0MCIgZmlsbD0iIzIxOTZGMyIgLz4KICA8dGV4dCB4PSI1MCIgeT0iNTciIGZvcnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNiIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkxPR088L3RleHQ+Cjwvc3ZnPgo='
        // }
      } catch (error) {
        console.log('❌ Error general cargando logo:', error)
        businessLogo.value = null
      }
    }

    const goBack = () => {
      stopPlayback()
      router.push('/')
    }
    
    // Lifecycle hooks
    onMounted(() => {
      console.log('PlayerView mounted, initial fullscreen state:', isFullscreen.value)
      initializeFullscreenState()
      fetchPlaylists()
      
      // Cargar logo después de un breve delay para asegurar que el backend esté detectado
      setTimeout(() => {
        loadBusinessLogo()
      }, 1000)
      
      // Agregar listener para cambios de pantalla completa
      document.addEventListener('fullscreenchange', handleFullscreenChange)
      
      // WebSocket: conectar y manejar eventos
      connectWebSocket()
    })
    
    onUnmounted(() => {
      clearTimeout(playbackTimer)
      clearInterval(progressTimer)
      clearInterval(scheduleCheckTimer)
      // Limpiar timer de controles de pantalla completa
      if (fullscreenControlsTimer) {
        clearTimeout(fullscreenControlsTimer)
      }
      // Remover listener
      document.removeEventListener('fullscreenchange', handleFullscreenChange)
      
      // WebSocket: desconectar y limpiar handlers
      disconnectWebSocket()
    })

    return { 
      // State
      loading,
      playlists,
      selectedPlaylist,
      playlistMedia,
      currentMedia,
      currentMediaIndex,
      isPlaying,
      showInfo,
      elapsedTime,
      scheduleOverride,
      progress,
      currentMediaSrc, // Nueva URL reactiva
      videoPlayer,
      isFullscreen,
      showFullscreenControls,
      businessLogo,
      
      // Methods
      fetchPlaylists,
      selectPlaylist,
      togglePlayPause,
      skipToNext,
      skipToPrevious,
      stopPlayback,
      toggleInfo,
      debugCurrentMedia,
      toggleFullscreen,
      dismissScheduleNotification,
      goToAdmin,
      goBack,
      onMediaEnded,
      onMediaLoaded,
      handleMediaError,
      formatTime,
      formatTotalDuration,
      getCurrentDuration,
      initializeFullscreenState,
      onMouseMoveFullscreen,
      
      // Theme
      isDarkMode
    }
  }
}
</script>

<style scoped>
/* Container Principal */
.player-container {
  min-height: 100vh;
  background: var(--background);
  color: var(--text-primary);
  position: relative;
  overflow: hidden;
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

/* Selection State Styles */
.selection-state {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.player-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  padding: 60px 20px 40px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header-icon {
  color: white;
  opacity: 0.9;
}

.header-text h2 {
  color: white;
  margin: 0 0 10px 0;
  font-weight: 600;
  font-size: 2.5rem;
}

.header-text p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 1.1rem;
}

.main-content {
  flex: 1;
  padding: 40px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-card {
  max-width: 1200px;
  width: 100%;
  background: var(--bg-primary);
  border-radius: 20px;
  padding: 40px;
  box-shadow: var(--shadow-xl);
  border: 1px solid rgba(var(--primary-rgb), 0.1);
}

.loading-section {
  text-align: center;
  padding: 60px 20px;
}

.loading-text {
  margin-top: 20px;
  font-size: 1.1rem;
  color: var(--text-secondary);
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-header h3 {
  font-size: 2rem;
  margin: 0 0 10px 0;
  color: var(--text-primary);
  font-weight: 600;
}

.playlist-count {
  color: var(--text-secondary);
  font-size: 1rem;
}

.playlists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.playlist-card {
  background: var(--bg-secondary);
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  display: flex;
  align-items: center;
  gap: 20px;
}

.playlist-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.playlist-icon {
  color: var(--primary);
  flex-shrink: 0;
}

.playlist-info {
  flex: 1;
}

.playlist-info h4 {
  margin: 0 0 8px 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.playlist-info p {
  margin: 0 0 12px 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
}

.playlist-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.playlist-action {
  color: var(--primary);
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.playlist-card:hover .playlist-action {
  opacity: 1;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  color: var(--text-secondary);
  opacity: 0.5;
  margin-bottom: 24px;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin: 0 0 12px 0;
  color: var(--text-primary);
}

.empty-state p {
  color: var(--text-secondary);
  margin: 0 0 24px 0;
  font-size: 1rem;
}

.footer-actions {
  padding: 20px;
  display: flex;
  justify-content: center;
  gap: 16px;
}

/* Player State Styles */
.player-state {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.media-display-area {
  flex: 1;
  position: relative;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.media-container {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-display,
.video-display {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.media-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.media-video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.media-info-overlay {
  position: absolute;
  bottom: 20px;
  left: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 20px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  animation: fadeInUp 0.3s ease;
}

.media-info h3 {
  margin: 0 0 8px 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.media-info p {
  margin: 0 0 12px 0;
  opacity: 0.9;
}

.media-details {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  opacity: 0.8;
}

.loading-media {
  text-align: center;
  color: white;
}

.loading-media p {
  margin-top: 20px;
  font-size: 1.2rem;
}

.player-controls {
  background: var(--bg-primary);
  border-top: 1px solid rgba(var(--primary-rgb), 0.1);
  padding: 20px;
}

.control-panel {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  grid-template-areas: 
    "info controls additional"
    "progress progress progress";
  gap: 20px;
  align-items: center;
}

/* Cuando NO es fullscreen, mostrar el layout normal */
.player-controls:not(.fullscreen-controls) .control-panel {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  grid-template-areas: 
    "info controls additional"
    "progress progress progress";
  gap: 20px;
}

.player-controls:not(.fullscreen-controls) .playlist-info-controls {
  grid-area: info;
}

.player-controls:not(.fullscreen-controls) .media-controls {
  grid-area: controls;
  justify-self: center;
  display: flex;
  align-items: center;
  gap: 12px;
}

.player-controls:not(.fullscreen-controls) .progress-info {
  grid-area: progress;
  grid-column: 1 / -1;
  text-align: center;
  margin-top: 10px;
}

.player-controls:not(.fullscreen-controls) .additional-controls {
  grid-area: additional;
  justify-self: end;
  display: flex;
  gap: 8px;
  align-items: center;
}

.playlist-info-controls h4 {
  margin: 0 0 4px 0;
  font-size: 1.2rem;
  color: var(--text-primary);
}

.playlist-info-controls p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.media-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.play-pause-btn {
  width: 60px;
  height: 60px;
}

.skip-btn {
  width: 48px;
  height: 48px;
}

.progress-info {
  text-align: right;
}

.progress-bar {
  min-width: 200px;
}

.media-progress {
  margin-bottom: 8px;
}

.time-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.additional-controls {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  align-items: center;
}

.schedule-notification {
  position: fixed;
  top: 80px;
  left: 20px;
  right: 20px;
  z-index: 900;
  animation: slideDown 0.3s ease;
}

/* Fullscreen Mode Styles */
.fullscreen-mode {
  background: #000 !important;
}

.fullscreen-mode .player-state {
  height: 100vh !important;
  display: flex !important;
  flex-direction: column !important;
}

.fullscreen-mode .media-display-area {
  flex: 1 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: #000 !important;
}

.fullscreen-mode .media-container {
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.fullscreen-mode .media-image,
.fullscreen-mode .media-video {
  max-width: 100% !important;
  max-height: 100% !important;
  width: auto !important;
  height: auto !important;
  object-fit: contain !important;
}

/* Estilos específicos para FULLSCREEN */
.fullscreen-mode .fullscreen-controls {
  position: absolute !important;
  bottom: 20px !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  background: rgba(0, 0, 0, 0.7) !important;
  backdrop-filter: blur(10px) !important;
  padding: 15px 25px !important;
  border-radius: 25px !important;
  z-index: 1000 !important;
}

.fullscreen-mode .fullscreen-controls .control-panel {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 20px !important;
  grid-template-columns: none !important;
  grid-template-areas: none !important;
}

.fullscreen-mode .fullscreen-controls .media-controls {
  display: flex !important;
  gap: 15px !important;
  align-items: center !important;
}

.fullscreen-mode .fullscreen-controls .additional-controls {
  display: flex !important;
  gap: 10px !important;
  align-items: center !important;
}

/* Auto-hide controls in fullscreen after 3 seconds */
.fullscreen-mode .fullscreen-controls {
  transition: opacity 0.3s ease !important;
}

.fullscreen-mode .fullscreen-controls:not(:hover) {
  animation: fadeOutAfterDelay 0.3s ease 3s forwards !important;
}

@keyframes fadeOutAfterDelay {
  to {
    opacity: 0.3;
  }
}

.fullscreen-mode .fullscreen-controls:hover {
  opacity: 1 !important;
  animation: none !important;
}

/* Estilos específicos para MODO NORMAL (no fullscreen) */
.normal-controls {
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  background: rgba(0, 0, 0, 0.9) !important;
  backdrop-filter: blur(10px) !important;
  border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
  padding: 15px 20px !important;
  z-index: 1000 !important;
}

.normal-controls .control-panel {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  grid-template-areas: 
    "info controls additional";
  gap: 20px;
  align-items: center;
}

.normal-controls .playlist-info-controls {
  grid-area: info;
  color: white;
}

.normal-controls .playlist-info-controls h4 {
  margin: 0 0 4px 0;
  font-size: 1.1rem;
  color: white;
  font-weight: 600;
}

.normal-controls .playlist-info-controls p {
  margin: 0;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
}

.normal-controls .media-controls {
  grid-area: controls;
  justify-self: center;
  display: flex;
  align-items: center;
  gap: 12px;
}

.normal-controls .progress-info {
  display: none; /* Ocultar en controles normales para simplicidad */
}

.normal-controls .additional-controls {
  grid-area: additional;
  justify-self: end;
  display: flex;
  gap: 8px;
  align-items: center;
}

/* Fullscreen Exit Overlay */
.fullscreen-exit-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2000;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.fullscreen-exit-overlay.visible {
  opacity: 1;
  pointer-events: auto;
}

.exit-fullscreen-btn {
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.exit-fullscreen-btn:hover {
  background: rgba(255, 255, 255, 1) !important;
  transform: scale(1.1);
}

/* Business Logo Overlay */
.business-logo-overlay {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1500;
  opacity: 0.8;
}

.business-logo {
  max-width: 138px;
  max-height: 92px;
  object-fit: contain;
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3));
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
  }
  to {
    transform: translateY(0);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  
  .header-text h2 {
    font-size: 2rem;
  }
  
  .playlists-grid {
    grid-template-columns: 1fr;
  }
  
  .playlist-card {
    flex-direction: column;
    text-align: center;
  }
  
  .control-panel {
    grid-template-columns: 1fr;
    gap: 15px;
    text-align: center;
  }
  
  .progress-info {
    text-align: center;
  }
  
  .media-details {
    flex-direction: column;
    gap: 8px;
  }
  
  .additional-controls {
    position: relative;
    top: auto;
    right: auto;
    justify-content: center;
    margin-top: 15px;
  }
}

/* Dark Mode Specific Adjustments */
.body--dark .content-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.body--dark .playlist-card {
  background: rgba(255, 255, 255, 0.03);
}

.body--dark .playlist-card:hover {
  background: rgba(255, 255, 255, 0.08);
}

.body--dark .player-controls {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.player-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.header-icon {
  color: var(--on-primary);
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.header-text h2 {
  color: var(--on-primary);
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 12px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.header-text p {
  color: var(--on-primary);
  font-size: 1.2rem;
  margin: 0;
  opacity: 0.9;
}

.main-content {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.content-card {
  background: var(--surface);
  border-radius: 20px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border);
  overflow: hidden;
}

.loading-section {
  padding: 80px 20px;
  text-align: center;
}

.loading-text {
  margin-top: 20px;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.section-header {
  padding: 30px 30px 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.playlist-count {
  color: var(--text-secondary);
  background: var(--background);
  padding: 8px 16px;
  border-radius: 12px;
  font-size: 0.9rem;
  border: 1px solid var(--border);
}

.playlists-grid {
  padding: 20px;
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
}

.playlist-card {
  display: flex;
  align-items: center;
  padding: 24px;
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.playlist-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.playlist-icon {
  color: var(--primary);
  margin-right: 20px;
  transition: all 0.3s ease;
}

.playlist-card:hover .playlist-icon {
  transform: scale(1.1);
  color: var(--primary-dark);
}

.playlist-info {
  flex: 1;
}

.playlist-info h4 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.playlist-info p {
  margin: 0 0 12px 0;
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.4;
}

.playlist-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.playlist-action {
  color: var(--secondary);
  transition: all 0.3s ease;
}
</style>

