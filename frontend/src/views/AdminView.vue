<template>
  <div class="admin-dashboard-container">
    <!-- Theme Toggle -->
    <ThemeToggle class="theme-toggle" />
    
    <div class="signance-container">
      <!-- Header principal -->
      <div class="dashboard-header">
        <div class="header-icon">
          <q-icon name="dashboard" size="4rem" />
        </div>
        <h2>Dashboard Administrativo</h2>
        <p>Pochtecayotl Signance System - Panel de Control</p>
      </div>

      <!-- KPI Cards -->
      <div class="info-card stats-card">
        <div class="card-title">
          <h3>Estadísticas del Sistema</h3>
        </div>
        
        <div class="stats-grid">
          <div class="stat-item media-stat">
            <div class="stat-icon">
              <q-icon name="video_library" size="2rem" />
            </div>
            <div class="stat-info">
              <h4>{{ stats.totalMedia }}</h4>
              <p>Archivos Multimedia</p>
            </div>
          </div>
          
          <div class="stat-item playlist-stat">
            <div class="stat-icon">
              <q-icon name="playlist_play" size="2rem" />
            </div>
            <div class="stat-info">
              <h4>{{ stats.totalPlaylists }}</h4>
              <p>Playlists Creadas</p>
            </div>
          </div>
          
          <div class="stat-item schedule-stat">
            <div class="stat-icon">
              <q-icon name="schedule" size="2rem" />
            </div>
            <div class="stat-info">
              <h4>{{ stats.totalScheduledItems }}</h4>
              <p>Elementos Programados</p>
            </div>
          </div>
          
          <div class="stat-item business-stat">
            <div class="stat-icon">
              <q-icon name="business" size="2rem" />
            </div>
            <div class="stat-info">
              <h4>{{ businessInfo.name || 'N/A' }}</h4>
              <p>Negocio Configurado</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Gestión de Playlists -->
      <div class="info-card playlists-card">
        <div class="card-header">
          <q-icon name="playlist_play" size="2rem" />
          <div class="header-text">
            <h3>Gestión de Playlists</h3>
            <p>Crear y administrar listas de reproducción</p>
          </div>
          <q-btn 
            color="primary" 
            icon="add" 
            label="Nueva Playlist"
            @click="showCreatePlaylistDialog"
            rounded
            no-caps
          />
        </div>
        
        <div class="playlists-content">
          <div v-if="playlists.length === 0" class="empty-state">
            <q-icon name="playlist_add" size="3rem" />
            <p>No hay playlists creadas</p>
            <q-btn 
              flat 
              color="primary" 
              label="Crear primera playlist"
              @click="showCreatePlaylistDialog"
            />
          </div>
          
          <div v-else class="playlists-grid">
            <div 
              v-for="playlist in playlists" 
              :key="playlist.id"
              class="playlist-item"
            >
              <div class="playlist-icon">
                <q-icon name="queue_music" size="1.5rem" />
              </div>
              
              <div class="playlist-info">
                <h4>{{ playlist.name }}</h4>
                <p>{{ playlist.description || 'Sin descripción' }}</p>
                <div class="playlist-meta">
                  <q-chip size="sm" color="primary" text-color="white">
                    {{ playlist.media_count || 0 }} medios
                  </q-chip>
                  <span class="playlist-date">{{ formatDate(playlist.created_at) }}</span>
                </div>
              </div>
              
              <div class="playlist-actions">
                <q-btn 
                  flat 
                  round 
                  icon="video_library"
                  @click="managePlaylistMedia(playlist)"
                  size="sm"
                  color="secondary"
                  title="Gestionar medios"
                />
                <q-btn 
                  flat 
                  round 
                  icon="schedule"
                  @click="schedulePlaylist(playlist)"
                  size="sm"
                  color="orange"
                  title="Programar playlist"
                />
                <q-btn 
                  flat 
                  round 
                  icon="edit"
                  @click="editPlaylist(playlist)"
                  size="sm"
                  color="primary"
                  title="Editar"
                />
                <q-btn 
                  flat 
                  round 
                  icon="delete"
                  @click="deletePlaylist(playlist.id)"
                  size="sm"
                  color="negative"
                  title="Eliminar"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Subida de Archivos -->
      <div class="info-card upload-card">
        <div class="card-header">
          <q-icon name="cloud_upload" size="2rem" />
          <div class="header-text">
            <h3>Subir Multimedia</h3>
            <p>Agregar nuevos archivos al sistema</p>
          </div>
        </div>
        
        <div class="upload-content">
          <MediaUploader 
            @uploaded="onMediaUploaded"
            @error="onMediaUploadError"
          />
        </div>
      </div>

      <!-- Galería de Archivos -->
      <div class="info-card media-card">
        <div class="card-header">
          <q-icon name="video_library" size="2rem" />
          <div class="header-text">
            <h3>Archivos Multimedia</h3>
            <p>Gestionar contenido subido</p>
          </div>
          <q-btn 
            flat 
            icon="refresh" 
            @click="loadMedia"
            :loading="mediaLoading"
            round
          />
        </div>
        
        <div class="media-content">
          <div v-if="mediaFiles.length === 0" class="empty-state">
            <q-icon name="video_library" size="3rem" />
            <p>No hay archivos multimedia</p>
          </div>
          
          <div v-else class="media-grid">
            <div 
              v-for="media in mediaFiles" 
              :key="media.id"
              class="media-item"
            >
              <div class="media-preview">
                <!-- Previsualización de imagen -->
                <div 
                  v-if="(media.file_type || media.media_type) === 'image'"
                  class="image-preview"
                >
                  <img 
                    :src="`http://127.0.0.1:8002${media.file_url || `/uploads/${media.served_filename || media.filename}`}`"
                    :alt="media.filename"
                    @error="handleImageError"
                    class="preview-img"
                  />
                </div>
                <!-- Icono para archivos no imagen o error de carga -->
                <div v-else class="media-icon">
                  <q-icon 
                    :name="getMediaIcon(media.file_type || media.media_type)"
                    size="2rem"
                    :class="`media-type-${(media.file_type || media.media_type || 'unknown')}`"
                  />
                </div>
              </div>
              
              <div class="media-info">
                <h4>{{ media.filename }}</h4>
                <p>
                  <q-chip 
                    :color="(media.file_type || media.media_type) === 'image' ? 'orange' : 'blue'"
                    text-color="white"
                    size="sm"
                  >
                    {{ String(media.file_type || media.media_type || 'unknown').toUpperCase() }}
                  </q-chip>
                </p>
                <span class="media-date">{{ formatDate(media.uploaded_at) }}</span>
              </div>
              
              <div class="media-actions">
                <q-btn 
                  flat 
                  round 
                  icon="edit"
                  @click="editMedia(media)"
                  size="sm"
                  color="primary"
                  class="q-mr-xs"
                />
                <q-btn 
                  flat 
                  round 
                  icon="schedule"
                  @click="scheduleMedia(media)"
                  size="sm"
                  color="secondary"
                  class="q-mr-xs"
                />
                <q-btn 
                  flat 
                  round 
                  icon="delete"
                  @click="deleteMedia(media.id)"
                  size="sm"
                  color="negative"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Acciones rápidas -->
      <div class="info-card actions-card">
        <div class="card-title">
          <h3>Acciones Rápidas</h3>
        </div>
        
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
          
          <div class="action-button warning-action" @click="logout">
            <q-icon name="logout" size="2rem" />
            <span>Cerrar Sesión</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Dialog para crear/editar playlist -->
    <q-dialog v-model="playlistDialog" persistent>
      <q-card style="min-width: 400px;">
        <q-card-section>
          <div class="text-h6">
            {{ editingPlaylist ? 'Editar Playlist' : 'Nueva Playlist' }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            v-model="playlistForm.name"
            label="Nombre de la playlist"
            outlined
            class="q-mb-md"
          />
          <q-input
            v-model="playlistForm.description"
            label="Descripción (opcional)"
            type="textarea"
            outlined
            rows="3"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" @click="closePlaylistDialog" />
          <q-btn 
            color="primary" 
            label="Guardar" 
            @click="savePlaylist"
            :loading="savingPlaylist"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog para editar media -->
    <q-dialog v-model="editMediaDialog" persistent>
      <q-card style="min-width: 500px;">
        <q-card-section>
          <div class="text-h6">Editar Archivo</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="row q-gutter-md">
            <div class="col-12">
              <q-input
                v-model="editMediaForm.filename"
                label="Nombre del archivo"
                outlined
                :rules="[val => !!val || 'El nombre es requerido']"
              />
            </div>
            
            <div class="col-12" v-if="editMediaForm.description !== undefined">
              <q-input
                v-model="editMediaForm.description"
                label="Descripción (opcional)"
                type="textarea"
                outlined
                rows="3"
              />
            </div>
            
            <div class="col-12" v-if="editMediaForm.tags !== undefined">
              <q-input
                v-model="editMediaForm.tags"
                label="Etiquetas (separadas por comas)"
                outlined
                hint="Ej: promocional, evento, informativo"
              />
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" @click="closeEditMediaDialog" />
          <q-btn 
            color="primary" 
            label="Guardar Cambios" 
            @click="saveMediaChanges"
            :loading="savingMedia"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog para gestionar medios en playlist -->
    <q-dialog v-model="playlistMediaDialog" persistent>
      <q-card style="min-width: 700px; max-width: 900px;">
        <q-card-section>
          <div class="text-h6">
            Gestionar Medios - {{ selectedPlaylist?.name }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="row q-gutter-md">
            <!-- Medios disponibles -->
            <div class="col-5">
              <div class="text-subtitle2 q-mb-md">Medios Disponibles</div>
              <q-list bordered class="available-media-list">
                <q-item 
                  v-for="media in availableMedia" 
                  :key="media.id"
                  clickable
                  @click="addMediaToPlaylist(media)"
                >
                  <q-item-section avatar>
                    <q-icon :name="getMediaIcon(media.media_type)" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ media.filename }}</q-item-label>
                    <q-item-label caption>{{ media.media_type }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-btn flat round icon="add" size="sm" />
                  </q-item-section>
                </q-item>
              </q-list>
            </div>

            <!-- Medios en playlist -->
            <div class="col-6">
              <div class="text-subtitle2 q-mb-md">Medios en Playlist</div>
              <q-list bordered class="playlist-media-list">
                <draggable 
                  v-model="playlistMedias" 
                  @end="reorderPlaylistMedia"
                  item-key="id"
                >
                  <template #item="{ element: media, index }">
                    <q-item>
                      <q-item-section avatar>
                        <q-icon name="drag_handle" />
                      </q-item-section>
                      <q-item-section avatar>
                        <q-icon :name="getMediaIcon(media.media_type)" />
                      </q-item-section>
                      <q-item-section>
                        <q-item-label>{{ media.filename }}</q-item-label>
                        <q-item-label caption>{{ media.media_type }} - Orden: {{ index + 1 }}</q-item-label>
                      </q-item-section>
                      <q-item-section side>
                        <q-btn 
                          flat 
                          round 
                          icon="remove" 
                          size="sm"
                          @click="removeMediaFromPlaylist(media.id)"
                        />
                      </q-item-section>
                    </q-item>
                  </template>
                </draggable>
              </q-list>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cerrar" @click="closePlaylistMediaDialog" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog para programar media o playlist -->
    <q-dialog v-model="scheduleDialog" persistent>
      <q-card style="min-width: 600px;">
        <q-card-section>
          <div class="text-h6">
            Programar {{ scheduleForm.contentType === 'media' ? 'Medio' : 'Playlist' }}
          </div>
          <div class="text-subtitle2 text-grey-6">
            {{ scheduleForm.contentName }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="row q-gutter-md">
            <!-- Tipo de programación -->
            <div class="col-12">
              <q-select
                v-model="scheduleForm.schedule_type"
                :options="[
                  { label: 'Programación Simple (Semanal)', value: 'simple' },
                  { label: 'Programación Avanzada (Fechas específicas)', value: 'advanced' }
                ]"
                option-label="label"
                option-value="value"
                emit-value
                map-options
                outlined
                label="Tipo de Programación"
                @update:model-value="onScheduleTypeChange"
              />
            </div>

            <!-- Programación Simple -->
            <template v-if="scheduleForm.schedule_type === 'simple'">
              <div class="col-12">
                <div class="text-subtitle2 q-mb-sm">Días de la semana</div>
                <q-option-group
                  v-model="scheduleForm.weekdays"
                  :options="weekdayOptions"
                  type="checkbox"
                  inline
                />
              </div>

              <div class="col-12">
                <q-checkbox 
                  v-model="scheduleForm.is_all_day" 
                  label="Todo el día"
                  @update:model-value="onAllDayChange"
                />
              </div>

              <template v-if="!scheduleForm.is_all_day">
                <div class="col-6">
                  <q-input
                    v-model="scheduleForm.daily_start"
                    type="time"
                    outlined
                    label="Hora de inicio"
                  />
                </div>
                <div class="col-6">
                  <q-input
                    v-model="scheduleForm.daily_end"
                    type="time"
                    outlined
                    label="Hora de fin"
                  />
                </div>
              </template>
            </template>

            <!-- Programación Avanzada -->
            <template v-if="scheduleForm.schedule_type === 'advanced'">
              <div class="col-6">
                <q-input
                  v-model="scheduleForm.start_date"
                  type="date"
                  outlined
                  label="Fecha de inicio"
                />
              </div>
              <div class="col-6">
                <q-input
                  v-model="scheduleForm.end_date"
                  type="date"
                  outlined
                  label="Fecha de fin"
                />
              </div>
              
              <div class="col-12">
                <q-input
                  v-model="scheduleForm.specific_times_text"
                  type="textarea"
                  outlined
                  label="Fechas específicas (una por línea, formato: YYYY-MM-DD)"
                  rows="3"
                  hint="Ejemplo: 2024-10-31 para Halloween"
                />
              </div>
            </template>

            <!-- Configuración común -->
            <div class="col-6">
              <q-input
                v-model.number="scheduleForm.priority"
                type="number"
                outlined
                label="Prioridad"
                min="1"
                max="10"
                hint="1 = Baja, 10 = Alta"
              />
            </div>
            <div class="col-6">
              <q-checkbox 
                v-model="scheduleForm.is_active" 
                label="Activar programación"
              />
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" @click="closeScheduleDialog" />
          <q-btn 
            color="primary" 
            label="Guardar Programación" 
            @click="saveSchedule"
            :loading="savingSchedule"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useToast } from 'vue-toastification'
import { authAPI, mediaAPI, playlistAPI, businessAPI } from '../services/api'
import MediaUploader from '../components/MediaUploader.vue'
import ThemeToggle from '../components/ThemeToggle.vue'
import { useTheme } from '../composables/useTheme'
import draggable from 'vuedraggable'

export default {
  name: 'AdminView',
  components: {
    MediaUploader,
    ThemeToggle,
    draggable
  },
  setup() {
    const router = useRouter()
    const $q = useQuasar()
    const toast = useToast()
    const { isDarkMode } = useTheme()

    // Estados reactivos
    const isLoading = ref(false)
    const mediaLoading = ref(false)
    const savingPlaylist = ref(false)
    const savingMedia = ref(false)
    const savingSchedule = ref(false)
    const playlistDialog = ref(false)
    const editMediaDialog = ref(false)
    const playlistMediaDialog = ref(false)
    const scheduleDialog = ref(false)
    const editingPlaylist = ref(null)
    const editingMedia = ref(null)
    const selectedPlaylist = ref(null)

    const stats = reactive({
      totalMedia: 0,
      totalPlaylists: 0,
      totalScheduledItems: 0
    })

    const businessInfo = reactive({
      name: '',
      logo: null
    })

    const playlists = ref([])
    const mediaFiles = ref([])
    const availableMedia = ref([])
    const playlistMedias = ref([])

    const playlistForm = reactive({
      name: '',
      description: ''
    })

    const editMediaForm = reactive({
      filename: '',
      description: '',
      tags: ''
    })

    const scheduleForm = reactive({
      contentType: 'media', // 'media' or 'playlist'
      contentId: null,
      contentName: '',
      schedule_type: 'simple',
      // Simple scheduling
      is_all_day: false,
      daily_start: '09:00',
      daily_end: '18:00',
      weekdays: [],
      // Advanced scheduling
      start_date: '',
      end_date: '',
      specific_times_text: '',
      // Common
      priority: 1,
      is_active: true
    })

    const weekdayOptions = [
      { label: 'Lun', value: 0 },
      { label: 'Mar', value: 1 },
      { label: 'Mié', value: 2 },
      { label: 'Jue', value: 3 },
      { label: 'Vie', value: 4 },
      { label: 'Sáb', value: 5 },
      { label: 'Dom', value: 6 }
    ]

    // Métodos
    const refreshData = async () => {
      isLoading.value = true
      try {
        await Promise.all([
          loadStats(),
          loadPlaylists(),
          loadMedia(),
          loadBusinessInfo()
        ])
      } finally {
        isLoading.value = false
      }
    }

    const loadStats = async () => {
      try {
        const [mediaResponse, playlistResponse] = await Promise.all([
          mediaAPI.list(),
          playlistAPI.getStats()
        ])
        
        stats.totalMedia = mediaResponse.data.length
        stats.totalPlaylists = playlistResponse.data.total_playlists
        stats.totalScheduledItems = playlistResponse.data.total_scheduled_items
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    }

    const loadPlaylists = async () => {
      try {
        const response = await playlistAPI.list()
        playlists.value = response.data
      } catch (error) {
        toast.error('Error cargando playlists')
        console.error('Error loading playlists:', error)
      }
    }

    const loadMedia = async () => {
      mediaLoading.value = true
      try {
        const response = await mediaAPI.list()
        mediaFiles.value = response.data
      } catch (error) {
        toast.error('Error cargando archivos multimedia')
        console.error('Error loading media:', error)
      } finally {
        mediaLoading.value = false
      }
    }

    const loadBusinessInfo = async () => {
      try {
        const response = await businessAPI.get()
        Object.assign(businessInfo, response.data)
      } catch (error) {
        console.error('Error loading business info:', error)
      }
    }

    const showCreatePlaylistDialog = () => {
      editingPlaylist.value = null
      playlistForm.name = ''
      playlistForm.description = ''
      playlistDialog.value = true
    }

    const editPlaylist = (playlist) => {
      editingPlaylist.value = playlist
      playlistForm.name = playlist.name
      playlistForm.description = playlist.description || ''
      playlistDialog.value = true
    }

    const closePlaylistDialog = () => {
      playlistDialog.value = false
      editingPlaylist.value = null
    }

    const savePlaylist = async () => {
      if (!playlistForm.name.trim()) {
        toast.warning('El nombre de la playlist es requerido')
        return
      }

      savingPlaylist.value = true
      try {
        if (editingPlaylist.value) {
          await playlistAPI.update(editingPlaylist.value.id, playlistForm)
          toast.success('Playlist actualizada exitosamente')
        } else {
          await playlistAPI.create(playlistForm)
          toast.success('Playlist creada exitosamente')
        }
        
        await loadPlaylists()
        await loadStats()
        closePlaylistDialog()
      } catch (error) {
        toast.error('Error guardando playlist')
        console.error('Error saving playlist:', error)
      } finally {
        savingPlaylist.value = false
      }
    }

    const deletePlaylist = async (playlistId) => {
      $q.dialog({
        title: 'Confirmar eliminación',
        message: '¿Estás seguro de que quieres eliminar esta playlist?',
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          await playlistAPI.delete(playlistId)
          toast.success('Playlist eliminada exitosamente')
          await loadPlaylists()
          await loadStats()
        } catch (error) {
          toast.error('Error eliminando playlist')
          console.error('Error deleting playlist:', error)
        }
      })
    }

    const deleteMedia = async (mediaId) => {
      $q.dialog({
        title: 'Confirmar eliminación',
        message: '¿Estás seguro de que quieres eliminar este archivo?',
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          await mediaAPI.delete(mediaId)
          toast.success('Archivo eliminado exitosamente')
          await loadMedia()
          await loadStats()
        } catch (error) {
          toast.error('Error eliminando archivo')
          console.error('Error deleting media:', error)
        }
      })
    }

    const scheduleMedia = (media) => {
      scheduleForm.contentType = 'media'
      scheduleForm.contentId = media.id
      scheduleForm.contentName = media.filename
      resetScheduleForm()
      scheduleDialog.value = true
    }

    const schedulePlaylist = (playlist) => {
      scheduleForm.contentType = 'playlist'
      scheduleForm.contentId = playlist.id
      scheduleForm.contentName = playlist.name
      resetScheduleForm()
      scheduleDialog.value = true
    }

    const resetScheduleForm = () => {
      scheduleForm.schedule_type = 'simple'
      scheduleForm.is_all_day = false
      scheduleForm.daily_start = '09:00'
      scheduleForm.daily_end = '18:00'
      scheduleForm.weekdays = []
      scheduleForm.start_date = ''
      scheduleForm.end_date = ''
      scheduleForm.specific_times_text = ''
      scheduleForm.priority = 1
      scheduleForm.is_active = true
    }

    const onScheduleTypeChange = (type) => {
      if (type === 'simple') {
        scheduleForm.start_date = ''
        scheduleForm.end_date = ''
        scheduleForm.specific_times_text = ''
      } else {
        scheduleForm.weekdays = []
        scheduleForm.is_all_day = false
        scheduleForm.daily_start = ''
        scheduleForm.daily_end = ''
      }
    }

    const onAllDayChange = (isAllDay) => {
      if (isAllDay) {
        scheduleForm.daily_start = ''
        scheduleForm.daily_end = ''
      } else {
        scheduleForm.daily_start = '09:00'
        scheduleForm.daily_end = '18:00'
      }
    }

    const closeScheduleDialog = () => {
      scheduleDialog.value = false
      resetScheduleForm()
    }

    const saveSchedule = async () => {
      savingSchedule.value = true
      try {
        const scheduleData = {
          schedule_type: scheduleForm.schedule_type,
          priority: scheduleForm.priority,
          is_active: scheduleForm.is_active
        }

        // Añadir campo específico según el tipo de contenido
        if (scheduleForm.contentType === 'media') {
          scheduleData.media_id = scheduleForm.contentId
        } else {
          scheduleData.playlist_id = scheduleForm.contentId
        }

        // Añadir campos según el tipo de programación
        if (scheduleForm.schedule_type === 'simple') {
          scheduleData.is_all_day = scheduleForm.is_all_day
          scheduleData.weekdays = scheduleForm.weekdays
          if (!scheduleForm.is_all_day) {
            scheduleData.daily_start = scheduleForm.daily_start
            scheduleData.daily_end = scheduleForm.daily_end
          }
        } else {
          scheduleData.start_date = scheduleForm.start_date
          scheduleData.end_date = scheduleForm.end_date
          if (scheduleForm.specific_times_text.trim()) {
            // Convertir texto a array de fechas
            const specificTimes = scheduleForm.specific_times_text
              .split('\n')
              .map(line => line.trim())
              .filter(line => line.length > 0)
            scheduleData.specific_times = specificTimes
          }
        }

        // Usar la API de schedules existente
        await fetch('http://127.0.0.1:8002/api/schedules/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(scheduleData)
        })

        toast.success('Programación guardada exitosamente')
        closeScheduleDialog()
        await loadStats() // Recargar estadísticas
        
      } catch (error) {
        toast.error('Error guardando programación')
        console.error('Error saving schedule:', error)
      } finally {
        savingSchedule.value = false
      }
    }

    // Gestión de medios en playlists
    const managePlaylistMedia = async (playlist) => {
      selectedPlaylist.value = playlist
      try {
        // Cargar medios de la playlist
        const playlistResponse = await fetch(`http://127.0.0.1:8002/api/playlists/${playlist.id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        const playlistData = await playlistResponse.json()
        playlistMedias.value = playlistData.medias || []

        // Cargar todos los medios disponibles
        const mediaResponse = await mediaAPI.list()
        // Filtrar medios que no están en la playlist
        const mediaInPlaylist = new Set(playlistMedias.value.map(m => m.id))
        availableMedia.value = mediaResponse.data.filter(m => !mediaInPlaylist.has(m.id))

        playlistMediaDialog.value = true
      } catch (error) {
        toast.error('Error cargando datos de playlist')
        console.error('Error loading playlist media:', error)
      }
    }

    const closePlaylistMediaDialog = () => {
      playlistMediaDialog.value = false
      selectedPlaylist.value = null
      availableMedia.value = []
      playlistMedias.value = []
    }

    const addMediaToPlaylist = async (media) => {
      try {
        const response = await fetch(`http://127.0.0.1:8002/api/playlists/${selectedPlaylist.value.id}/media`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            media_id: media.id
          })
        })

        if (response.ok) {
          // Mover el media de disponible a playlist
          availableMedia.value = availableMedia.value.filter(m => m.id !== media.id)
          playlistMedias.value.push({
            ...media,
            order_index: playlistMedias.value.length
          })
          toast.success(`"${media.filename}" añadido a la playlist`)
        } else {
          throw new Error('Error en la respuesta del servidor')
        }
      } catch (error) {
        toast.error('Error añadiendo medio a la playlist')
        console.error('Error adding media to playlist:', error)
      }
    }

    const removeMediaFromPlaylist = async (mediaId) => {
      try {
        const response = await fetch(`http://127.0.0.1:8002/api/playlists/${selectedPlaylist.value.id}/media/${mediaId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })

        if (response.ok) {
          // Mover el media de playlist a disponible
          const mediaToRemove = playlistMedias.value.find(m => m.id === mediaId)
          if (mediaToRemove) {
            playlistMedias.value = playlistMedias.value.filter(m => m.id !== mediaId)
            availableMedia.value.push(mediaToRemove)
            toast.success(`"${mediaToRemove.filename}" removido de la playlist`)
          }
        } else {
          throw new Error('Error en la respuesta del servidor')
        }
      } catch (error) {
        toast.error('Error removiendo medio de la playlist')
        console.error('Error removing media from playlist:', error)
      }
    }

    const reorderPlaylistMedia = async () => {
      try {
        const mediaOrder = playlistMedias.value.map((media, index) => ({
          media_id: media.id,
          order_index: index
        }))

        const response = await fetch(`http://127.0.0.1:8002/api/playlists/${selectedPlaylist.value.id}/reorder`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            media_order: mediaOrder
          })
        })

        if (response.ok) {
          toast.success('Orden actualizado')
        } else {
          throw new Error('Error en la respuesta del servidor')
        }
      } catch (error) {
        toast.error('Error reordenando medios')
        console.error('Error reordering media:', error)
      }
    }

    // Funciones para editar media
    const editMedia = (media) => {
      editingMedia.value = media
      editMediaForm.filename = media.filename
      editMediaForm.description = media.description || ''
      editMediaForm.tags = media.tags || ''
      editMediaDialog.value = true
    }

    const closeEditMediaDialog = () => {
      editMediaDialog.value = false
      editingMedia.value = null
      editMediaForm.filename = ''
      editMediaForm.description = ''
      editMediaForm.tags = ''
    }

    const saveMediaChanges = async () => {
      if (!editMediaForm.filename.trim()) {
        toast.error('El nombre del archivo es requerido')
        return
      }

      savingMedia.value = true
      try {
        const updateData = {
          filename: editMediaForm.filename.trim(),
          description: editMediaForm.description?.trim() || null,
          tags: editMediaForm.tags?.trim() || null
        }

        await mediaAPI.update(editingMedia.value.id, updateData)
        toast.success('Archivo actualizado exitosamente')
        
        closeEditMediaDialog()
        await loadMedia()
        
      } catch (error) {
        toast.error('Error actualizando archivo')
        console.error('Error updating media:', error)
      } finally {
        savingMedia.value = false
      }
    }

    // Función para manejar errores de carga de imagen
    const handleImageError = (event) => {
      const img = event.target
      const container = img.closest('.image-preview')
      if (container) {
        container.innerHTML = `
          <div class="media-icon">
            <q-icon name="broken_image" size="2rem" color="grey" />
          </div>
        `
      }
    }

    // Función para obtener el icono apropiado según el tipo de archivo
    const getMediaIcon = (fileType) => {
      if (!fileType) return 'description'
      
      const type = fileType.toLowerCase()
      if (type.includes('image')) return 'image'
      if (type.includes('video')) return 'videocam'
      if (type.includes('audio')) return 'audiotrack'
      if (type.includes('pdf')) return 'picture_as_pdf'
      return 'description'
    }

    const onMediaUploaded = (mediaData) => {
      toast.success(`Archivo "${mediaData.filename}" subido exitosamente`)
      loadMedia()
      loadStats()
    }

    const onMediaUploadError = (error) => {
      console.error('Upload error:', error)
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Fecha no disponible'
      return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const logout = async () => {
      try {
        await authAPI.logout()
      } catch (error) {
        console.error('Error en logout:', error)
      } finally {
        localStorage.removeItem('signance_token')
        toast.success('Sesión cerrada exitosamente')
        router.push('/login')
      }
    }

    // Lifecycle
    onMounted(() => {
      refreshData()
    })

    return {
      // Estados reactivos
      isLoading,
      mediaLoading,
      savingPlaylist,
      savingMedia,
      savingSchedule,
      playlistDialog,
      editMediaDialog,
      playlistMediaDialog,
      scheduleDialog,
      editingPlaylist,
      editingMedia,
      selectedPlaylist,
      stats,
      businessInfo,
      playlists,
      mediaFiles,
      availableMedia,
      playlistMedias,
      playlistForm,
      editMediaForm,
      scheduleForm,
      weekdayOptions,
      
      // Funciones
      refreshData,
      showCreatePlaylistDialog,
      editPlaylist,
      closePlaylistDialog,
      savePlaylist,
      deletePlaylist,
      deleteMedia,
      scheduleMedia,
      schedulePlaylist,
      closeScheduleDialog,
      saveSchedule,
      onScheduleTypeChange,
      onAllDayChange,
      managePlaylistMedia,
      closePlaylistMediaDialog,
      addMediaToPlaylist,
      removeMediaFromPlaylist,
      reorderPlaylistMedia,
      editMedia,
      closeEditMediaDialog,
      saveMediaChanges,
      handleImageError,
      getMediaIcon,
      onMediaUploaded,
      onMediaUploadError,
      formatDate,
      logout,
      loadMedia,
      isDarkMode
    }
  }
}
</script>

<style scoped>
.admin-dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
  padding: 20px 0;
  position: relative;
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.signance-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.dashboard-header {
  text-align: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 40px 20px;
  margin-bottom: 30px;
  box-shadow: var(--shadow-xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

[data-theme="dark"] .dashboard-header {
  background: rgba(30, 30, 30, 0.95);
  color: var(--text-primary);
}

.header-icon {
  color: var(--primary);
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.dashboard-header h2 {
  margin: 0 0 12px 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.dashboard-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.info-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  border-bottom: 1px solid var(--border);
}

.card-header q-icon {
  color: var(--primary);
}

.header-text h3 {
  margin: 0 0 4px 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
}

.header-text p {
  margin: 0;
  color: var(--text-secondary);
}

.card-title {
  padding: 24px 24px 16px;
  border-bottom: 1px solid var(--border);
}

.card-title h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* Stats Grid */
.stats-grid {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.media-stat {
  border-color: var(--primary);
}

.playlist-stat {
  border-color: var(--secondary);
}

.schedule-stat {
  border-color: var(--accent);
}

.business-stat {
  border-color: var(--success);
}

.stat-icon {
  color: var(--text-secondary);
}

.media-stat .stat-icon {
  color: var(--primary);
}

.playlist-stat .stat-icon {
  color: var(--secondary);
}

.schedule-stat .stat-icon {
  color: var(--accent);
}

.business-stat .stat-icon {
  color: var(--success);
}

.stat-info h4 {
  margin: 0 0 4px 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-info p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

/* Playlists Content */
.playlists-content {
  padding: 20px;
}

.playlists-grid {
  display: grid;
  gap: 16px;
}

.playlist-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.playlist-item:hover {
  box-shadow: var(--shadow-md);
}

.playlist-icon {
  color: var(--secondary);
}

.playlist-info {
  flex: 1;
}

.playlist-info h4 {
  margin: 0 0 4px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.playlist-info p {
  margin: 0 0 4px 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.playlist-date {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.playlist-actions {
  display: flex;
  gap: 8px;
}

/* Upload Content */
.upload-content {
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

/* Media Content */
.media-content {
  padding: 20px;
}

.media-grid {
  display: grid;
  gap: 16px;
}

.media-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.media-item:hover {
  box-shadow: var(--shadow-md);
}

/* Media Preview */
.media-preview {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  overflow: hidden;
  background: var(--surface);
  border: 1px solid var(--border);
}

.image-preview {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.media-icon {
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.media-type-image {
  color: var(--warning);
}

.media-type-video {
  color: var(--info);
}

.media-info {
  flex: 1;
}

.media-info h4 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.media-info p {
  margin: 0 0 4px 0;
}

.media-date {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.media-actions {
  display: flex;
  gap: 4px;
  align-items: center;
}

.media-actions .q-btn {
  transition: all 0.2s ease;
}

.media-actions .q-btn:hover {
  transform: scale(1.1);
}

/* Actions Grid */
.actions-grid {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.primary-action {
  background: var(--hover-primary);
  border: 2px solid var(--primary);
  color: var(--primary);
}

.secondary-action {
  background: var(--hover-secondary);
  border: 2px solid var(--secondary);
  color: var(--secondary);
}

.accent-action {
  background: rgba(240, 210, 123, 0.1);
  border: 2px solid var(--accent);
  color: var(--accent);
}

[data-theme="dark"] .accent-action {
  background: rgba(209, 176, 95, 0.1);
}

.warning-action {
  background: rgba(251, 140, 0, 0.1);
  border: 2px solid var(--warning);
  color: var(--warning);
}

[data-theme="dark"] .warning-action {
  background: rgba(255, 167, 38, 0.1);
}

.action-button span {
  font-weight: 500;
  font-size: 0.95rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);
}

.empty-state q-icon {
  color: var(--text-secondary);
  opacity: 0.5;
  margin-bottom: 16px;
}

.empty-state p {
  margin: 0 0 16px 0;
  font-size: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .admin-dashboard-container {
    padding: 10px;
  }
  
  .dashboard-header {
    padding: 30px 15px;
  }
  
  .dashboard-header h2 {
    font-size: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
  
  .actions-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .action-button {
    padding: 20px 12px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .theme-toggle {
    top: 10px;
    right: 10px;
  }
}

/* Nuevos estilos para gestión de playlists y programación */
.playlist-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.playlist-meta .q-chip {
  font-size: 0.75rem;
}

.available-media-list,
.playlist-media-list {
  max-height: 300px;
  overflow-y: auto;
  border-radius: 8px;
}

.available-media-list .q-item:hover,
.playlist-media-list .q-item:hover {
  background: rgba(var(--primary-rgb), 0.1);
}

.schedule-form-section {
  margin-bottom: 16px;
}

.schedule-form-section .text-subtitle2 {
  margin-bottom: 8px;
  color: var(--text-primary);
  font-weight: 600;
}

.weekday-options {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.sortable-ghost {
  opacity: 0.5;
}

.sortable-chosen {
  background: rgba(var(--primary-rgb), 0.1);
}

.drag-handle {
  cursor: grab;
}

.drag-handle:active {
  cursor: grabbing;
}

/* Dark mode específico para los nuevos elementos */
.body--dark .available-media-list,
.body--dark .playlist-media-list {
  border-color: rgba(255, 255, 255, 0.12);
}

.body--dark .available-media-list .q-item:hover,
.body--dark .playlist-media-list .q-item:hover {
  background: rgba(255, 255, 255, 0.05);
}
</style>
