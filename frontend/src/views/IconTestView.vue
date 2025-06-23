<template>
  <div class="icon-test-container">
    <div class="test-header">
      <h1>🧪 Prueba de Iconos - Diagnóstico</h1>
      <p>Esta página prueba diferentes métodos de renderizado de iconos</p>
    </div>

    <div class="test-sections">
      <!-- Test 1: Quasar Icons -->
      <div class="test-section">
        <h2>1. Iconos Quasar (q-icon)</h2>
        <div class="icon-grid">
          <div class="icon-item">
            <q-icon name="play_circle_filled" size="2rem" />
            <span>play_circle_filled</span>
          </div>
          <div class="icon-item">
            <q-icon name="arrow_forward" size="2rem" />
            <span>arrow_forward</span>
          </div>
          <div class="icon-item">
            <q-icon name="dashboard" size="2rem" />
            <span>dashboard</span>
          </div>
          <div class="icon-item">
            <q-icon name="settings" size="2rem" />
            <span>settings</span>
          </div>
          <div class="icon-item">
            <q-icon name="video_library" size="2rem" />
            <span>video_library</span>
          </div>
        </div>
      </div>

      <!-- Test 2: Material Icons directos -->
      <div class="test-section">
        <h2>2. Material Icons directos (CSS class)</h2>
        <div class="icon-grid">
          <div class="icon-item">
            <i class="material-icons">play_circle_filled</i>
            <span>play_circle_filled</span>
          </div>
          <div class="icon-item">
            <i class="material-icons">arrow_forward</i>
            <span>arrow_forward</span>
          </div>
          <div class="icon-item">
            <i class="material-icons">dashboard</i>
            <span>dashboard</span>
          </div>
          <div class="icon-item">
            <i class="material-icons">settings</i>
            <span>settings</span>
          </div>
          <div class="icon-item">
            <i class="material-icons">video_library</i>
            <span>video_library</span>
          </div>
        </div>
      </div>

      <!-- Test 3: Font Information -->
      <div class="test-section">
        <h2>3. Información de Fuentes</h2>
        <div class="font-info">
          <p><strong>Font Face Test:</strong></p>
          <div class="font-test">
            <span style="font-family: 'Material Icons';">play_circle_filled</span>
            <span class="font-name">Font Family: Material Icons</span>
          </div>
        </div>
      </div>

      <!-- Test 4: Debug Info -->
      <div class="test-section">
        <h2>4. Información de Debug</h2>
        <div class="debug-info">
          <pre>{{ debugInfo }}</pre>
        </div>
      </div>
    </div>

    <div class="actions">
      <q-btn 
        @click="$router.go(-1)" 
        label="Volver" 
        icon="arrow_back"
        color="primary"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'IconTestView',
  setup() {
    const debugInfo = ref({})

    onMounted(() => {
      // Obtener información de debug
      debugInfo.value = {
        userAgent: navigator.userAgent,
        fonts: {
          available: document.fonts ? document.fonts.size : 'API no disponible',
          materialIcons: checkFontLoaded('Material Icons')
        },
        documentFonts: Array.from(document.styleSheets).map(sheet => {
          try {
            return Array.from(sheet.cssRules || sheet.rules || [])
              .filter(rule => rule.type === CSSRule.FONT_FACE_RULE)
              .map(rule => rule.cssText)
          } catch (e) {
            return 'No accesible (CORS): ' + sheet.href
          }
        }).flat(),
        computedStyles: {
          materialIconsClass: getComputedStyle(document.createElement('i')).fontFamily,
          qIconClass: window.getComputedStyle ? 'Disponible' : 'No disponible'
        }
      }
    })

    const checkFontLoaded = (fontName) => {
      if (!document.fonts) return 'API no disponible'
      
      const fontFace = new FontFace(fontName, 'url(about:blank)')
      return document.fonts.check('1em ' + fontName) ? 'Cargada' : 'No cargada'
    }

    return {
      debugInfo
    }
  }
}
</script>

<style scoped>
.icon-test-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.test-header {
  text-align: center;
  margin-bottom: 40px;
}

.test-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #1976d2;
}

.test-sections {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.test-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.test-section h2 {
  margin: 0 0 20px 0;
  color: #333;
  border-bottom: 2px solid #1976d2;
  padding-bottom: 10px;
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.icon-item span {
  font-size: 0.9rem;
  color: #666;
  text-align: center;
  font-family: monospace;
}

.font-info {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #1976d2;
}

.font-test {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-top: 10px;
}

.font-test span:first-child {
  font-size: 2rem;
  background: white;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.font-name {
  font-family: monospace;
  color: #666;
}

.debug-info {
  background: #f0f0f0;
  padding: 15px;
  border-radius: 8px;
  overflow: auto;
}

.debug-info pre {
  margin: 0;
  font-size: 0.8rem;
  white-space: pre-wrap;
  word-break: break-all;
}

.actions {
  margin-top: 40px;
  text-align: center;
}

/* Material Icons específicos */
.material-icons {
  font-family: 'Material Icons' !important;
  font-weight: normal !important;
  font-style: normal !important;
  font-size: 24px !important;
  line-height: 1 !important;
  letter-spacing: normal !important;
  text-transform: none !important;
  display: inline-block !important;
  white-space: nowrap !important;
  word-wrap: normal !important;
  direction: ltr !important;
  font-feature-settings: 'liga' !important;
  -webkit-font-feature-settings: 'liga' !important;
  -webkit-font-smoothing: antialiased !important;
}

/* Modo oscuro */
.body--dark .test-section {
  background: #1e1e1e;
  border-color: #333;
}

.body--dark .test-section h2 {
  color: #e0e0e0;
}

.body--dark .icon-item {
  background: #2a2a2a;
  border-color: #444;
}

.body--dark .font-info {
  background: #2a2a2a;
}

.body--dark .debug-info {
  background: #2a2a2a;
}
</style>
