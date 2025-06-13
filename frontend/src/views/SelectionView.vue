<template>
  <div class="selection-container">
    <!-- Theme Toggle -->
    <ThemeToggle class="theme-toggle" />
    
    <!-- Main Selection Card -->
    <div class="selection-card">
      <div class="card-header">
        <div class="logo-section">
          <q-icon name="favorite" size="4rem" class="pride-icon" />
          <h2 class="welcome-title">Bienvenido</h2>
          <h3 class="system-title">Pochtecayotl Signance System</h3>
        </div>
        <p class="subtitle">Seleccione una opción para continuar</p>
      </div>

      <div class="options-section">
        <div class="option-card player-option" @click="goPlayer">
          <div class="option-icon">
            <q-icon name="play_circle_filled" size="3rem" />
          </div>
          <div class="option-content">
            <h4>Reproductor</h4>
            <p>Acceder al reproductor de contenido multimedia</p>
          </div>
          <q-icon name="arrow_forward" size="1.5rem" class="arrow-icon" />
        </div>

        <div class="option-card admin-option" @click="goAdmin">
          <div class="option-icon">
            <q-icon name="dashboard" size="3rem" />
          </div>
          <div class="option-content">
            <h4>Admin Dashboard</h4>
            <p>Gestionar contenido y configuración del sistema</p>
          </div>
          <q-icon name="arrow_forward" size="1.5rem" class="arrow-icon" />
        </div>
      </div>

      <div class="footer-section">
        <p class="footer-text">Sistema diseñado por un gei 🏳️‍🌈</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import ThemeToggle from '../components/ThemeToggle.vue'
import { useTheme } from '../composables/useTheme'

export default {
  name: 'SelectionView',
  components: {
    ThemeToggle
  },
  setup() {
    const router = useRouter()
    const { isDarkMode } = useTheme()
    
    const goPlayer = () => router.push('/player')
    const goAdmin = () => router.push('/login')
    
    return { 
      goPlayer, 
      goAdmin,
      isDarkMode
    }
  }
}
</script>

<style scoped>
.selection-container {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.selection-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 20%, rgba(240, 144, 123, 0.2) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(123, 197, 240, 0.2) 0%, transparent 50%);
  pointer-events: none;
}

[data-theme="dark"] .selection-container::before {
  background: radial-gradient(circle at 30% 20%, rgba(255, 170, 147, 0.2) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(90, 157, 203, 0.2) 0%, transparent 50%);
}

.theme-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}

.selection-card {
  background: var(--surface);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border);
  padding: 60px 40px;
  max-width: 600px;
  width: 100%;
  text-align: center;
  position: relative;
  z-index: 2;
  transition: all 0.3s ease;
}

.card-header {
  margin-bottom: 40px;
}

.logo-section {
  margin-bottom: 20px;
}

.pride-icon {
  color: var(--primary);
  margin-bottom: 16px;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 8px 0;
  background: linear-gradient(45deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.system-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: var(--text-primary);
}

.subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin: 0;
}

.options-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}

.option-card {
  display: flex;
  align-items: center;
  padding: 24px;
  border-radius: 16px;
  background: var(--background);
  border: 2px solid var(--border);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.option-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.player-option:hover {
  background: var(--hover-secondary);
}

.admin-option:hover {
  background: var(--hover-primary);
}

.option-icon {
  margin-right: 20px;
  color: var(--primary);
  transition: all 0.3s ease;
}

.option-card:hover .option-icon {
  transform: scale(1.1);
  color: var(--primary-dark);
}

.option-content {
  flex: 1;
}

.option-content h4 {
  margin: 0 0 8px 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
}

.option-content p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.arrow-icon {
  color: var(--secondary);
  transition: all 0.3s ease;
}

.option-card:hover .arrow-icon {
  transform: translateX(4px);
  color: var(--primary);
}

.footer-section {
  border-top: 1px solid var(--border);
  padding-top: 20px;
}

.footer-text {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

@media (max-width: 768px) {
  .selection-container {
    padding: 20px 10px;
  }
  
  .selection-card {
    padding: 40px 20px;
  }
  
  .welcome-title {
    font-size: 2rem;
  }
  
  .system-title {
    font-size: 1.3rem;
  }
  
  .option-card {
    padding: 20px;
  }
  
  .option-icon {
    margin-right: 16px;
  }
  
  .theme-toggle {
    top: 10px;
    right: 10px;
  }
}
</style>
