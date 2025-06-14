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
                    :src="`${backendBaseUrl}${media.file_url || `/uploads/${media.served_filename || media.filename}`}`"
                    :alt="media.filename"
                    @error="handleImageError"
                    class="preview-img"
                  />
                </div>
                <!-- Previsualización de video -->
                <div 
                  v-else-if="(media.file_type || media.media_type) === 'video'"
                  class="video-preview"
                >
                  <video 
                    :src="`${backendBaseUrl}${media.file_url || `/uploads/${media.served_filename || media.filename}`}`"
                    class="preview-video"
                    muted
                    preload="metadata"
                    @error="handleVideoError"
                    @loadedmetadata="setVideoTime"
                    @click="toggleVideoPreview"
                  >
                    Su navegador no soporta la reproducción de video.
                  </video>
                  <div class="video-overlay">
                    <q-icon name="play_circle_filled" size="2.5rem" class="play-icon" />
                    <div class="video-duration" v-if="media.duration">
                      {{ formatDuration(media.duration) }}
                    </div>
                  </div>
                </div>
                <!-- Icono para otros tipos de archivos o error de carga -->
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
      <q-card style="min-width: 400px;" :class="{ 'bg-dark text-white': isDarkMode }">
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
      <q-card style="min-width: 800px; max-width: 1000px;" :class="{ 'bg-dark text-white': isDarkMode }">
        <q-card-section>
          <div class="text-h6">Gestionar Medio - {{ editingMedia?.filename }}</div>
          <div class="text-subtitle2" :class="isDarkMode ? 'text-grey-4' : 'text-grey-6'">
            Configurar playlists y programación para este medio
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-tabs v-model="editMediaTab" dense class="text-grey" active-color="primary" indicator-color="primary">
            <q-tab name="basic" label="Información Básica" />
            <q-tab name="playlists" label="Playlists" />
            <q-tab name="schedule" label="Programación" />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="editMediaTab" animated>
            <!-- Información básica -->
            <q-tab-panel name="basic" class="q-pa-md">
              <div class="basic-info-management">
                <div class="section-header">
                  <h6 class="text-h6 q-mb-none">Información del Medio</h6>
                  <p class="text-body2 q-mt-xs q-mb-lg" :class="isDarkMode ? 'text-grey-4' : 'text-grey-6'">
                    Configura las propiedades básicas y metadatos de este archivo multimedia
                  </p>
                </div>

                <q-card class="info-form-card" flat bordered :class="{ 'bg-grey-9 text-white': isDarkMode }">
                  <q-card-section class="q-pa-lg">
                    <div class="form-grid">
                      <!-- Nombre del archivo -->
                      <div class="form-field">
                        <label class="field-label">
                          <q-icon name="file_present" class="q-mr-sm" />
                          Nombre del archivo
                        </label>
                        <q-input
                          v-model="editMediaForm.filename"
                          outlined
                          placeholder="Ingresa el nombre del archivo..."
                          :rules="[val => !!val || 'El nombre es requerido']"
                          class="styled-input"
                        />
                      </div>
                      
                      <!-- Descripción -->
                      <div class="form-field">
                        <label class="field-label">
                          <q-icon name="description" class="q-mr-sm" />
                          Descripción (opcional)
                        </label>
                        <q-input
                          v-model="editMediaForm.description"
                          type="textarea"
                          outlined
                          rows="3"
                          placeholder="Describe el contenido de este medio..."
                          class="styled-input"
                        />
                      </div>
                      
                      <!-- Etiquetas -->
                      <div class="form-field">
                        <label class="field-label">
                          <q-icon name="local_offer" class="q-mr-sm" />
                          Etiquetas (separadas por comas)
                        </label>
                        <q-input
                          v-model="editMediaForm.tags"
                          outlined
                          placeholder="Ej: promocional, evento, informativo"
                          class="styled-input"
                        />
                        <small class="field-hint">Las etiquetas ayudan a organizar y filtrar los medios</small>
                      </div>

                      <!-- Duración y Prioridad -->
                      <div class="form-row">
                        <div class="form-field">
                          <label class="field-label">
                            <q-icon name="timer" class="q-mr-sm" />
                            Duración por defecto (segundos)
                          </label>
                          <q-input
                            v-model.number="editMediaForm.duration"
                            type="number"
                            outlined
                            min="1"
                            max="3600"
                            class="styled-input"
                          />
                          <small class="field-hint">Tiempo que se mostrará este medio por defecto</small>
                        </div>

                        <div class="form-field">
                          <label class="field-label">
                            <q-icon name="priority_high" class="q-mr-sm" />
                            Prioridad del medio
                          </label>
                          <q-select
                            v-model="editMediaForm.priority"
                            :options="[
                              { label: 'Baja (1)', value: 1 },
                              { label: 'Normal (5)', value: 5 },
                              { label: 'Alta (8)', value: 8 },
                              { label: 'Crítica (10)', value: 10 }
                            ]"
                            outlined
                            emit-value
                            map-options
                            class="styled-input"
                          />
                          <small class="field-hint">Prioridad cuando se reproduce individualmente</small>
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </q-tab-panel>

            <!-- Gestión de playlists -->
            <q-tab-panel name="playlists" class="q-pa-md">
              <div class="playlists-management">
                <div class="section-header">
                  <h6 class="text-h6 q-mb-none">Gestión de Playlists</h6>
                  <p class="text-body2 q-mt-xs q-mb-lg" :class="isDarkMode ? 'text-grey-4' : 'text-grey-6'">
                    Administra en qué playlists aparece este medio y personaliza su duración
                  </p>
                </div>

                <!-- Playlists actuales -->
                <div v-if="mediaPlaylists.length > 0" class="current-playlists q-mb-xl">
                  <div class="subsection-title">
                    <q-icon name="playlist_play" class="q-mr-sm" />
                    <span>Playlists Actuales ({{ mediaPlaylists.length }})</span>
                  </div>
                  
                  <div class="playlists-cards">
                    <q-card 
                      v-for="playlist in mediaPlaylists" 
                      :key="playlist.id"
                      class="playlist-card"
                      flat
                      bordered
                      :class="{ 'bg-grey-9 text-white': isDarkMode }"
                    >
                      <q-card-section class="q-pa-md">
                        <div class="playlist-card-header">
                          <div class="playlist-info">
                            <h6 class="playlist-name">{{ playlist.name }}</h6>
                            <p class="playlist-description">{{ playlist.description || 'Sin descripción' }}</p>
                          </div>
                          <q-btn
                            flat
                            round
                            icon="close"
                            color="negative"
                            size="sm"
                            @click="removeMediaFromPlaylistInEdit(playlist.id)"
                            class="remove-btn"
                          >
                            <q-tooltip>Remover de playlist</q-tooltip>
                          </q-btn>
                        </div>
                        
                        <div class="playlist-controls">
                          <div class="duration-control">
                            <label class="control-label">Duración personalizada (segundos)</label>
                            <div class="duration-input-group">
                              <q-input
                                v-model.number="playlist.duration"
                                type="number"
                                outlined
                                dense
                                :placeholder="editMediaForm.duration.toString()"
                                class="duration-input"
                                @change="updateMediaInPlaylist(playlist)"
                                min="1"
                                max="3600"
                              />
                              <span class="default-hint">Por defecto: {{ editMediaForm.duration }}s</span>
                            </div>
                          </div>
                          
                          <div class="position-info">
                            <q-chip 
                              :label="`Posición: ${playlist.order_index + 1}`"
                              color="primary"
                              text-color="white"
                              size="sm"
                            />
                          </div>
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>
                </div>

                <!-- Estado vacío -->
                <div v-else class="empty-playlists q-mb-xl">
                  <div class="empty-state-card">
                    <q-icon name="playlist_add_circle" size="3rem" class="empty-icon" />
                    <h6 class="empty-title">Sin playlists asignadas</h6>
                    <p class="empty-description">Este medio no pertenece a ninguna playlist aún</p>
                  </div>
                </div>

                <!-- Agregar a nueva playlist -->
                <div class="add-to-playlist">
                  <div class="subsection-title">
                    <q-icon name="add_circle" class="q-mr-sm" />
                    <span>Agregar a Playlist</span>
                  </div>
                  
                  <q-card class="add-playlist-card" flat bordered :class="{ 'bg-grey-9 text-white': isDarkMode }">
                    <q-card-section class="q-pa-lg">
                      <div class="add-form">
                        <div class="form-row">
                          <div class="playlist-selector">
                            <label class="control-label">Seleccionar playlist</label>
                            <q-select
                              v-model="selectedPlaylistToAdd"
                              :options="availablePlaylistsForMedia"
                              option-label="name"
                              option-value="id"
                              outlined
                              clearable
                              placeholder="Elige una playlist..."
                              class="playlist-select"
                            >
                              <template v-slot:no-option>
                                <q-item>
                                  <q-item-section class="text-grey">
                                    No hay playlists disponibles
                                  </q-item-section>
                                </q-item>
                              </template>
                            </q-select>
                          </div>
                          
                          <div class="duration-selector">
                            <label class="control-label">Duración (opcional)</label>
                            <q-input
                              v-model.number="newPlaylistDuration"
                              type="number"
                              outlined
                              :placeholder="editMediaForm.duration.toString()"
                              suffix="segundos"
                              class="duration-input"
                              min="1"
                              max="3600"
                            />
                            <small class="input-hint">Dejar vacío para usar duración original ({{ editMediaForm.duration }}s)</small>
                          </div>
                        </div>
                        
                        <div class="form-actions">
                          <q-btn
                            label="Agregar a Playlist"
                            icon="add"
                            color="primary"
                            @click="addMediaToPlaylistInEdit"
                            :disable="!selectedPlaylistToAdd"
                            :loading="savingMedia"
                            class="add-btn"
                          />
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>
                </div>
              </div>
            </q-tab-panel>

            <!-- Programación avanzada -->
            <q-tab-panel name="schedule" class="q-pa-md">
              <div class="schedule-management">
                <div class="section-header">
                  <h6 class="text-h6 q-mb-none">Programación Avanzada</h6>
                  <p class="text-body2 q-mt-xs q-mb-lg" :class="isDarkMode ? 'text-grey-4' : 'text-grey-6'">
                    Configura cuándo este medio debe reproducirse, sobrescribiendo temporalmente el contenido de las playlists
                  </p>
                </div>

                <!-- Schedules existentes -->
                <div v-if="mediaSchedules.length > 0" class="current-schedules q-mb-xl">
                  <div class="subsection-title">
                    <q-icon name="schedule" class="q-mr-sm" />
                    <span>Programaciones Activas ({{ mediaSchedules.length }})</span>
                  </div>
                  
                  <div class="schedules-cards">
                    <q-card 
                      v-for="schedule in mediaSchedules" 
                      :key="schedule.id"
                      class="schedule-card"
                      flat
                      bordered
                    >
                      <q-card-section class="q-pa-md">
                        <div class="schedule-card-header">
                          <div class="schedule-info">
                            <div class="schedule-type">
                              <q-icon 
                                :name="schedule.schedule_type === 'simple' ? 'event_repeat' : 'event'" 
                                :color="schedule.is_active ? 'positive' : 'grey'"
                                size="1.25rem"
                                class="q-mr-sm"
                              />
                              <h6 class="schedule-title">
                                {{ schedule.schedule_type === 'simple' ? 'Programación Semanal' : 'Programación Específica' }}
                              </h6>
                            </div>
                            
                            <div class="schedule-details">
                              <div v-if="schedule.schedule_type === 'simple'" class="schedule-time">
                                <p class="schedule-days">{{ formatWeekdays(schedule.weekdays) }}</p>
                                <p class="schedule-hours">
                                  {{ schedule.is_all_day ? 'Todo el día' : `${schedule.daily_start} - ${schedule.daily_end}` }}
                                </p>
                              </div>
                              <div v-else class="schedule-time">
                                <p class="schedule-dates">{{ formatDateRange(schedule.start_date, schedule.end_date) }}</p>
                              </div>
                            </div>
                          </div>
                          
                          <div class="schedule-actions">
                            <q-btn
                              flat
                              round
                              icon="edit"
                              color="primary"
                              size="sm"
                              @click="editScheduleInMedia(schedule)"
                            >
                              <q-tooltip>Editar programación</q-tooltip>
                            </q-btn>
                            <q-btn
                              flat
                              round
                              icon="delete"
                              color="negative"
                              size="sm"
                              @click="deleteScheduleInMedia(schedule.id)"
                            >
                              <q-tooltip>Eliminar programación</q-tooltip>
                            </q-btn>
                          </div>
                        </div>
                        
                        <div class="schedule-meta">
                          <q-chip 
                            :label="`Prioridad: ${schedule.priority}`"
                            color="orange"
                            text-color="white"
                            size="sm"
                          />
                          <q-chip 
                            :label="schedule.is_active ? 'Activo' : 'Inactivo'"
                            :color="schedule.is_active ? 'positive' : 'grey'"
                            text-color="white"
                            size="sm"
                          />
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>
                </div>

                <!-- Estado vacío -->
                <div v-else class="empty-schedules q-mb-xl">
                  <div class="empty-state-card">
                    <q-icon name="schedule" size="3rem" class="empty-icon" />
                    <h6 class="empty-title">Sin programaciones configuradas</h6>
                    <p class="empty-description">Este medio no tiene programaciones avanzadas configuradas</p>
                  </div>
                </div>

                <!-- Crear nueva programación -->
                <div class="add-schedule">
                  <div class="subsection-title">
                    <q-icon name="add_circle" class="q-mr-sm" />
                    <span>Nueva Programación</span>
                  </div>
                  
                  <q-card class="add-schedule-card" flat bordered>
                    <q-card-section class="q-pa-lg text-center">
                      <q-btn
                        color="primary"
                        icon="add"
                        label="Crear Nueva Programación"
                        @click="createNewScheduleForMedia"
                        size="lg"
                        class="create-schedule-btn"
                      />
                      <p class="create-hint">
                        Configura horarios específicos para que este medio se reproduzca automáticamente
                      </p>
                    </q-card-section>
                  </q-card>
                </div>
              </div>
            </q-tab-panel>
          </q-tab-panels>
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
      <q-card style="min-width: 700px; max-width: 900px;" :class="{ 'bg-dark text-white': isDarkMode }">
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
              <q-list bordered class="available-media-list" :class="{ 'bg-grey-9': isDarkMode }">
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
              <q-list bordered class="playlist-media-list" :class="{ 'bg-grey-9': isDarkMode }">
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
      <q-card style="min-width: 600px;" :class="{ 'bg-dark text-white': isDarkMode }">
        <q-card-section>
          <div class="text-h6">
            Programar {{ scheduleForm.contentType === 'media' ? 'Medio' : 'Playlist' }}
          </div>
          <div class="text-subtitle2" :class="isDarkMode ? 'text-grey-4' : 'text-grey-6'">
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
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useToast } from 'vue-toastification'
import { authAPI, mediaAPI, playlistAPI, businessAPI } from '../services/api'
import backendDetector from '../services/backendDetector'
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

    // URL base del backend (dinámico)
    const backendBaseUrl = ref('http://127.0.0.1:8000')

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
      tags: '',
      duration: 5,
      priority: 5
    })

    // Nuevas variables para la gestión avanzada de medios
    const editMediaTab = ref('basic')
    const mediaPlaylists = ref([])
    const mediaSchedules = ref([])
    const availablePlaylistsForMedia = ref([])
    const selectedPlaylistToAdd = ref(null)
    const newPlaylistDuration = ref(5)

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
      is_active: true,
      editingScheduleId: null
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
    const initializeBackend = async () => {
      try {
        const backendInfo = await backendDetector.detectBackend()
        backendBaseUrl.value = backendInfo.baseUrl
        console.log(`📡 AdminView: Backend detectado en ${backendInfo.baseUrl}`)
      } catch (error) {
        console.error('❌ AdminView: Error detectando backend:', error)
        toast.error('No se pudo conectar al backend')
      }
    }

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
      scheduleForm.editingScheduleId = null
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

        // Determinar si es edición o creación
        const isEditing = scheduleForm.editingScheduleId
        const url = isEditing 
          ? `${backendBaseUrl.value}/api/schedules/${scheduleForm.editingScheduleId}`
          : `${backendBaseUrl.value}/api/schedules/`
        const method = isEditing ? 'PUT' : 'POST'

        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('signance_token')}`
          },
          body: JSON.stringify(scheduleData)
        })

        if (response.ok) {
          toast.success(`Programación ${isEditing ? 'actualizada' : 'creada'} exitosamente`)
          closeScheduleDialog()
          await loadStats() // Recargar estadísticas
          
          // Si estamos editando un medio, recargar sus schedules
          if (editingMedia.value && scheduleForm.contentType === 'media') {
            await loadMediaSchedules(editingMedia.value.id)
          }
        } else {
          throw new Error('Error en la respuesta del servidor')
        }
        
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
        const playlistResponse = await fetch(`${backendBaseUrl.value}/api/playlists/${playlist.id}`, {
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
        const response = await fetch(`${backendBaseUrl.value}/api/playlists/${selectedPlaylist.value.id}/media`, {
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
        const response = await fetch(`${backendBaseUrl.value}/api/playlists/${selectedPlaylist.value.id}/media/${mediaId}`, {
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

        const response = await fetch(`${backendBaseUrl.value}/api/playlists/${selectedPlaylist.value.id}/reorder`, {
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
    const editMedia = async (media) => {
      editingMedia.value = media
      editMediaForm.filename = media.filename
      editMediaForm.description = media.description || ''
      editMediaForm.tags = media.tags || ''
      editMediaForm.duration = media.duration || 5
      editMediaForm.priority = media.priority || 5
      
      // Resetear tab
      editMediaTab.value = 'basic'
      
      // Cargar playlists donde aparece este medio
      await loadMediaPlaylists(media.id)
      
      // Cargar schedules de este medio
      await loadMediaSchedules(media.id)
      
      // Cargar playlists disponibles para agregar
      await loadAvailablePlaylistsForMedia(media.id)
      
      editMediaDialog.value = true
    }

    const closeEditMediaDialog = () => {
      editMediaDialog.value = false
      editingMedia.value = null
      editMediaForm.filename = ''
      editMediaForm.description = ''
      editMediaForm.tags = ''
      editMediaForm.duration = 5
      editMediaForm.priority = 5
      mediaPlaylists.value = []
      mediaSchedules.value = []
      availablePlaylistsForMedia.value = []
      selectedPlaylistToAdd.value = null
      newPlaylistDuration.value = 5
    }

    const saveMediaChanges = async () => {
      if (!editingMedia.value) {
        toast.error('No hay medio seleccionado para editar')
        return
      }

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

    const handleVideoError = (event) => {
      const video = event.target
      const container = video.closest('.video-preview')
      if (container) {
        container.innerHTML = `
          <div class="media-icon">
            <q-icon name="videocam_off" size="2rem" color="grey" />
          </div>
        `
      }
    }

    const setVideoTime = (event) => {
      // Establecer el tiempo del video a 1 segundo para mostrar un frame más representativo
      const video = event.target
      if (video.duration > 1) {
        video.currentTime = 1
      }
    }

    const formatDuration = (seconds) => {
      if (!seconds) return '0:00'
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = Math.floor(seconds % 60)
      
      if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`
      }
    }

    const toggleVideoPreview = (event) => {
      const video = event.target
      if (video.paused) {
        video.play()
        video.muted = false
      } else {
        video.pause()
        video.currentTime = video.duration > 1 ? 1 : 0
        video.muted = true
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

    // Funciones para gestión de playlists en medios
    const loadMediaPlaylists = async (mediaId) => {
      try {
        const response = await fetch(`${backendBaseUrl.value}/api/media/${mediaId}/playlists`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('signance_token')}`
          }
        })
        const data = await response.json()
        mediaPlaylists.value = data
      } catch (error) {
        console.error('Error loading media playlists:', error)
        mediaPlaylists.value = []
      }
    }

    const loadMediaSchedules = async (mediaId) => {
      try {
        const response = await fetch(`${backendBaseUrl.value}/api/schedules/?media_id=${mediaId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('signance_token')}`
          }
        })
        const data = await response.json()
        mediaSchedules.value = data
      } catch (error) {
        console.error('Error loading media schedules:', error)
        mediaSchedules.value = []
      }
    }

    const loadAvailablePlaylistsForMedia = async (mediaId) => {
      try {
        // Cargar todas las playlists
        const allPlaylists = playlists.value
        
        // Filtrar las que ya contienen este medio
        const playlistsWithMedia = new Set(mediaPlaylists.value.map(p => p.id))
        availablePlaylistsForMedia.value = allPlaylists.filter(p => !playlistsWithMedia.has(p.id))
      } catch (error) {
        console.error('Error loading available playlists:', error)
        availablePlaylistsForMedia.value = []
      }
    }

    const addMediaToPlaylistInEdit = async () => {
      if (!selectedPlaylistToAdd.value || !editingMedia.value) return

      try {
        savingMedia.value = true
        
        // Usar la función de API en lugar de fetch directo
        await playlistAPI.addSingleMedia(selectedPlaylistToAdd.value.id, {
          media_id: editingMedia.value.id,
          duration: newPlaylistDuration.value || null
        })

        // Actualizar las listas
        await loadMediaPlaylists(editingMedia.value.id)
        await loadAvailablePlaylistsForMedia(editingMedia.value.id)
        
        selectedPlaylistToAdd.value = null
        newPlaylistDuration.value = editMediaForm.duration
        
        toast.success('Medio agregado a la playlist exitosamente')
      } catch (error) {
        console.error('Error adding media to playlist:', error)
        toast.error('Error al agregar el medio a la playlist')
      } finally {
        savingMedia.value = false
      }
    }

    const removeMediaFromPlaylistInEdit = async (playlistId) => {
      if (!editingMedia.value) return

      try {
        // Usar la función de API en lugar de fetch directo
        await playlistAPI.removeMedia(playlistId, editingMedia.value.id)

        // Actualizar las listas
        await loadMediaPlaylists(editingMedia.value.id)
        await loadAvailablePlaylistsForMedia(editingMedia.value.id)
        
        toast.success('Medio removido de la playlist exitosamente')
      } catch (error) {
        console.error('Error removing media from playlist:', error)
        toast.error('Error al remover el medio de la playlist')
      }
    }

    const updateMediaInPlaylist = async (playlist) => {
      if (!editingMedia.value) return

      try {
        // Usar la función de API en lugar de fetch directo
        await playlistAPI.updateMedia(playlist.id, editingMedia.value.id, {
          duration: playlist.duration
        })
        
        toast.success('Duración actualizada exitosamente')
      } catch (error) {
        console.error('Error updating media in playlist:', error)
        toast.error('Error al actualizar la duración')
      }
    }

    // Funciones para gestión de schedules en medios
    const createNewScheduleForMedia = () => {
      if (!editingMedia.value) return

      scheduleForm.contentType = 'media'
      scheduleForm.contentId = editingMedia.value.id
      scheduleForm.contentName = editingMedia.value.filename
      resetScheduleForm()
      scheduleDialog.value = true
    }

    const editScheduleInMedia = (schedule) => {
      if (!editingMedia.value) return

      // Cargar datos del schedule para editar
      Object.assign(scheduleForm, {
        contentType: 'media',
        contentId: editingMedia.value.id,
        contentName: editingMedia.value.filename,
        schedule_type: schedule.schedule_type,
        is_all_day: schedule.is_all_day,
        daily_start: schedule.daily_start,
        daily_end: schedule.daily_end,
        weekdays: schedule.weekdays || [],
        start_date: schedule.start_date,
        end_date: schedule.end_date,
        specific_times_text: (schedule.specific_times || []).join('\n'),
        priority: schedule.priority,
        is_active: schedule.is_active,
        editingScheduleId: schedule.id
      })
      scheduleDialog.value = true
    }

    const deleteScheduleInMedia = async (scheduleId) => {
      $q.dialog({
        title: 'Confirmar eliminación',
        message: '¿Estás seguro de que quieres eliminar esta programación?',
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          const response = await fetch(`${backendBaseUrl.value}/api/schedules/${scheduleId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('signance_token')}`
            }
          })

          if (response.ok) {
            await loadMediaSchedules(editingMedia.value.id)
            toast.success('Programación eliminada exitosamente')
          } else {
            throw new Error('Error en la respuesta del servidor')
          }
        } catch (error) {
          toast.error('Error eliminando programación')
          console.error('Error:', error)
        }
      })
    }

    // Funciones auxiliares
    const formatWeekdays = (weekdays) => {
      if (!weekdays || weekdays.length === 0) return 'Ninguno'
      const dayNames = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
      return weekdays.map(day => dayNames[day]).join(', ')
    }

    const formatDateRange = (startDate, endDate) => {
      if (!startDate && !endDate) return 'Sin fechas definidas'
      if (startDate && endDate) {
        return `${startDate} al ${endDate}`
      }
      return startDate || endDate || 'Sin definir'
    }
    // Lifecycle
    onMounted(async () => {
      await initializeBackend()
      refreshData()
      // Configurar tema inicial de Quasar
      $q.dark.set(isDarkMode.value)
    })

    // Watcher para sincronizar el tema de Quasar con el tema global
    watch(isDarkMode, (newValue) => {
      $q.dark.set(newValue)
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
      backendBaseUrl,
      playlists,
      mediaFiles,
      availableMedia,
      playlistMedias,
      playlistForm,
      editMediaForm,
      scheduleForm,
      weekdayOptions,
      
      // Nuevas variables para gestión avanzada de medios
      editMediaTab,
      mediaPlaylists,
      mediaSchedules,
      availablePlaylistsForMedia,
      selectedPlaylistToAdd,
      newPlaylistDuration,
      
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
      handleVideoError,
      setVideoTime,
      formatDuration,
      toggleVideoPreview,
      getMediaIcon,
      onMediaUploaded,
      onMediaUploadError,
      formatDate,
      logout,
      loadMedia,
      isDarkMode,
      
      // Nuevas funciones para gestión avanzada de medios
      loadMediaPlaylists,
      loadMediaSchedules,
      loadAvailablePlaylistsForMedia,
      addMediaToPlaylistInEdit,
      removeMediaFromPlaylistInEdit,
      updateMediaInPlaylist,
      createNewScheduleForMedia,
      editScheduleInMedia,
      deleteScheduleInMedia,
      formatWeekdays,
      formatDateRange
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

.video-preview {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.preview-video {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  transition: opacity 0.3s ease;
}

.video-preview:hover .video-overlay {
  opacity: 0.8;
}

.play-icon {
  color: white;
  opacity: 0.9;
}

.video-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
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

/* Estilos para el nuevo diseño de gestión de playlists */
.playlists-management {
  max-width: 100%;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h6 {
  color: var(--text-primary);
  font-weight: 600;
  margin: 0;
}

.section-header p {
  margin: 0;
  opacity: 0.8;
}

.subsection-title {
  display: flex;
  align-items: center;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.subsection-title .q-icon {
  color: var(--primary);
}

/* Cards de playlists actuales */
.playlists-cards {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

.playlist-card {
  background: var(--bg-primary);
  border: 1px solid rgba(var(--primary-rgb), 0.2);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.playlist-card:hover {
  border-color: var(--primary);
  box-shadow: 0 4px 12px rgba(var(--primary-rgb), 0.15);
}

.playlist-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.playlist-info {
  flex: 1;
}

.playlist-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.25rem 0;
}

.playlist-description {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
  opacity: 0.8;
}

.remove-btn {
  margin-left: 1rem;
}

.playlist-controls {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
}

.duration-control {
  flex: 1;
  max-width: 200px;
}

.control-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.duration-input-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.duration-input {
  width: 100%;
}

.default-hint {
  font-size: 0.75rem;
  color: var(--text-secondary);
  opacity: 0.7;
}

.position-info {
  flex-shrink: 0;
}

/* Estado vacío */
.empty-playlists {
  text-align: center;
}

.empty-state-card {
  background: var(--bg-secondary);
  border: 2px dashed rgba(var(--primary-rgb), 0.3);
  border-radius: 16px;
  padding: 3rem 2rem;
}

.empty-icon {
  color: var(--primary);
  opacity: 0.6;
  margin-bottom: 1rem;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.empty-description {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
  opacity: 0.8;
}

/* Formulario para agregar a playlist */
.add-playlist-card {
  background: var(--bg-primary);
  border: 1px solid rgba(var(--primary-rgb), 0.2);
  border-radius: 12px;
}

.add-form {
  width: 100%;
}

.form-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.playlist-selector,
.duration-selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.playlist-select,
.duration-input {
  width: 100%;
}

.input-hint {
  font-size: 0.75rem;
  color: var(--text-secondary);
  opacity: 0.7;
  margin-top: 0.25rem;
}

.form-actions {
  text-align: left;
}

.add-btn {
  padding: 12px 24px;
  font-weight: 600;
}

/* Responsive design */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .playlist-controls {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .duration-control {
    max-width: none;
  }
}

/* Dark mode específico */
.body--dark .playlist-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.body--dark .playlist-card:hover {
  border-color: var(--primary);
  box-shadow: 0 4px 12px rgba(var(--primary-rgb), 0.25);
}

.body--dark .empty-state-card {
  background: rgba(255, 255, 255, 0.02);
  border-color: rgba(255, 255, 255, 0.1);
}

.body--dark .add-playlist-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Estilos para programación avanzada */
.schedule-management {
  max-width: 100%;
}

.schedules-cards {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

.schedule-card {
  background: var(--bg-primary);
  border: 1px solid rgba(var(--primary-rgb), 0.2);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.schedule-card:hover {
  border-color: var(--primary);
  box-shadow: 0 4px 12px rgba(var(--primary-rgb), 0.15);
}

.schedule-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.schedule-info {
  flex: 1;
}

.schedule-type {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.schedule-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.schedule-details {
  margin-left: 2rem;
}

.schedule-time p {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.schedule-days {
  font-weight: 500;
  color: var(--text-primary);
}

.schedule-hours,
.schedule-dates {
  opacity: 0.8;
}

.schedule-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.schedule-meta {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.empty-schedules {
  text-align: center;
}

.add-schedule-card {
  background: var(--bg-primary);
  border: 1px solid rgba(var(--primary-rgb), 0.2);
  border-radius: 12px;
}

.create-schedule-btn {
  padding: 16px 32px;
  font-weight: 600;
  margin-bottom: 1rem;
}

.create-hint {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
  opacity: 0.8;
}

/* Dark mode para programación */
.body--dark .schedule-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.body--dark .schedule-card:hover {
  border-color: var(--primary);
  box-shadow: 0 4px 12px rgba(var(--primary-rgb), 0.25);
}

.body--dark .add-schedule-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Estilos para información básica */
.basic-info-management {
  max-width: 100%;
}

.info-form-card {
  background: var(--bg-primary);
  border: 1px solid rgba(var(--primary-rgb), 0.2);
  border-radius: 12px;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field-label {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.field-label .q-icon {
  color: var(--primary);
  font-size: 1rem;
}

.styled-input {
  width: 100%;
}

.field-hint {
  font-size: 0.75rem;
  color: var(--text-secondary);
  opacity: 0.8;
  margin-top: 0.25rem;
}

/* Responsive para información básica */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

/* Dark mode para información básica */
.body--dark .info-form-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Dark mode para previsualizaciones de video */
.body--dark .video-overlay {
  background: rgba(0, 0, 0, 0.5);
}

.body--dark .play-icon {
  color: var(--primary);
}
</style>
