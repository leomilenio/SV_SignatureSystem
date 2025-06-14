<template>
  <div class="info-card stats-card">
    <div class="card-title">
      <h3>Estadísticas del Sistema</h3>
    </div>
    <div class="stats-grid">
      <div class="stat-item media-stat">
        <div class="stat-icon"><q-icon name="video_library" size="2rem" /></div>
        <div class="stat-info">
          <h4>{{ stats.totalMedia }}</h4>
          <p>Archivos Multimedia</p>
        </div>
      </div>
      <div class="stat-item playlist-stat">
        <div class="stat-icon"><q-icon name="playlist_play" size="2rem" /></div>
        <div class="stat-info">
          <h4>{{ stats.totalPlaylists }}</h4>
          <p>Playlists Creadas</p>
        </div>
      </div>
      <div class="stat-item schedule-stat">
        <div class="stat-icon"><q-icon name="schedule" size="2rem" /></div>
        <div class="stat-info">
          <h4>{{ stats.totalScheduledItems }}</h4>
          <p>Elementos Programados</p>
        </div>
      </div>
      <div class="stat-item business-stat">
        <div class="stat-icon"><q-icon name="business" size="2rem" /></div>
        <div class="stat-info">
          <h4>{{ businessInfo.name || 'N/A' }}</h4>
          <p>Negocio Configurado</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: Object,
  businessInfo: Object
})
</script>
