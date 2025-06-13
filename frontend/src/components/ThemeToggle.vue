<template>
  <q-btn
    :icon="isDarkMode ? 'wb_sunny' : 'nights_stay'"
    @click="toggleTheme"
    :class="themeToggleClass"
    flat
    square
    size="md"
  >
  </q-btn>
</template>

<script>
import { computed } from 'vue'
import { useTheme } from '../composables/useTheme'

export default {
  name: 'ThemeToggle',
  setup() {
    const { isDarkMode, toggleTheme } = useTheme()
    
    const themeToggleClass = computed(() => ({
      'theme-toggle': true,
      'theme-toggle--dark': isDarkMode.value,
      'theme-toggle--light': !isDarkMode.value
    }))
    
    return {
      isDarkMode,
      toggleTheme,
      themeToggleClass
    }
  }
}
</script>

<style scoped>
.theme-toggle {
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text-primary);
  border-radius: 8px !important;
  width: 44px !important;
  height: 44px !important;
  min-width: 44px !important;
  min-height: 44px !important;
}

.theme-toggle:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.2);
}

.theme-toggle--dark {
  color: #fbbf24 !important;
  background: rgba(30, 30, 30, 0.8) !important;
  border: 1px solid rgba(251, 191, 36, 0.3) !important;
}

.theme-toggle--dark:hover {
  background: rgba(30, 30, 30, 0.9) !important;
  border: 1px solid rgba(251, 191, 36, 0.5) !important;
}

.theme-toggle--light {
  color: #374151 !important;
  background: rgba(255, 255, 255, 0.8) !important;
  border: 1px solid rgba(55, 65, 81, 0.2) !important;
}

.theme-toggle--light:hover {
  background: rgba(255, 255, 255, 0.9) !important;
  border: 1px solid rgba(55, 65, 81, 0.3) !important;
}
</style>
