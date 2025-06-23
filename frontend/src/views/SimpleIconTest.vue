<template>
  <div class="simple-test">
    <h1>Prueba Simple de Iconos</h1>
    
    <div class="test-section">
      <h2>1. Test Quasar Icon Component</h2>
      <div class="icon-test">
        <q-icon name="home" size="2rem" color="primary" />
        <span>home (debería mostrar ícono de casa)</span>
      </div>
      <div class="icon-test">
        <q-icon name="star" size="2rem" color="amber" />
        <span>star (debería mostrar estrella)</span>
      </div>
      <div class="icon-test">
        <q-icon name="favorite" size="2rem" color="red" />
        <span>favorite (debería mostrar corazón)</span>
      </div>
    </div>

    <div class="test-section">
      <h2>2. Test HTML + CSS directo</h2>
      <div class="icon-test">
        <i class="material-icons" style="font-size: 2rem; color: blue;">home</i>
        <span>home (HTML directo)</span>
      </div>
      <div class="icon-test">
        <i class="material-icons" style="font-size: 2rem; color: orange;">star</i>
        <span>star (HTML directo)</span>
      </div>
      <div class="icon-test">
        <i class="material-icons" style="font-size: 2rem; color: red;">favorite</i>
        <span>favorite (HTML directo)</span>
      </div>
    </div>

    <div class="test-section">
      <h2>3. Font Check</h2>
      <p><strong>Fuente computada:</strong> {{ computedFont }}</p>
      <p><strong>Fonts API:</strong> {{ fontsApiStatus }}</p>
      <button @click="runTests" class="test-btn">Ejecutar Pruebas</button>
    </div>

    <div class="test-section">
      <h2>4. Debug Info</h2>
      <pre>{{ debugInfo }}</pre>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'SimpleIconTest',
  setup() {
    const computedFont = ref('')
    const fontsApiStatus = ref('')
    const debugInfo = ref({})

    const runTests = () => {
      // Test 1: Crear elemento de prueba
      const testEl = document.createElement('i')
      testEl.className = 'material-icons'
      testEl.textContent = 'home'
      testEl.style.position = 'absolute'
      testEl.style.left = '-9999px'
      document.body.appendChild(testEl)

      computedFont.value = window.getComputedStyle(testEl).fontFamily
      
      // Test 2: Verificar si el icono se renderiza
      setTimeout(() => {
        const rect = testEl.getBoundingClientRect()
        debugInfo.value = {
          width: rect.width,
          height: rect.height,
          fontFamily: window.getComputedStyle(testEl).fontFamily,
          fontSize: window.getComputedStyle(testEl).fontSize,
          textContent: testEl.textContent,
          offsetWidth: testEl.offsetWidth,
          offsetHeight: testEl.offsetHeight
        }
        document.body.removeChild(testEl)
      }, 100)

      // Test 3: Fonts API
      if (document.fonts) {
        fontsApiStatus.value = `${document.fonts.size} fuentes cargadas. Material Icons: ${document.fonts.check('1rem "Material Icons"') ? 'OK' : 'NO'}`
      } else {
        fontsApiStatus.value = 'Fonts API no disponible'
      }
    }

    onMounted(() => {
      setTimeout(runTests, 1000)
    })

    return {
      computedFont,
      fontsApiStatus,
      debugInfo,
      runTests
    }
  }
}
</script>

<style scoped>
.simple-test {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
}

.icon-test {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
  padding: 10px;
  background: white;
  border-radius: 4px;
}

.test-btn {
  background: #1976d2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.test-btn:hover {
  background: #1565c0;
}

pre {
  background: #f0f0f0;
  padding: 10px;
  border-radius: 4px;
  overflow: auto;
  font-size: 12px;
}

/* Forzar Material Icons */
.material-icons {
  font-family: 'Material Icons' !important;
  font-weight: normal !important;
  font-style: normal !important;
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
</style>
