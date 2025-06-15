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

<style scoped>
/* CSS Variables */
:root {
  --primary: #1976d2;
  --primary-light: #42a5f5;
  --primary-rgb: 25, 118, 210;
  --secondary: #dc004e;
  --accent: #9c27b0;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Dark mode for stat items */
.body--dark .stat-item {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  border-color: rgba(255, 255, 255, 0.1);
}

.stat-item:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* Specific stat item colors */
.media-stat .stat-icon {
  color: #ff9800;
  background: rgba(255, 152, 0, 0.1);
  padding: 12px;
  border-radius: 10px;
}

.playlist-stat .stat-icon {
  color: #2196f3;
  background: rgba(33, 150, 243, 0.1);
  padding: 12px;
  border-radius: 10px;
}

.schedule-stat .stat-icon {
  color: #4caf50;
  background: rgba(76, 175, 80, 0.1);
  padding: 12px;
  border-radius: 10px;
}

.business-stat .stat-icon {
  color: #9c27b0;
  background: rgba(156, 39, 176, 0.1);
  padding: 12px;
  border-radius: 10px;
}

.stat-info {
  flex: 1;
}

.stat-info h4 {
  margin: 0 0 5px 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--primary);
}

.body--dark .stat-info h4 {
  color: var(--primary-light, #42a5f5);
}

.stat-info p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.body--dark .stat-info p {
  color: #ccc;
}

/* Media queries for responsive design */
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
  }
  
  .stat-item {
    padding: 15px;
    gap: 12px;
  }
  
  .stat-info h4 {
    font-size: 1.5rem;
  }
  
  .stat-info p {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .stat-item {
    padding: 12px;
  }
  
  .stat-info h4 {
    font-size: 1.4rem;
  }
}
</style>
