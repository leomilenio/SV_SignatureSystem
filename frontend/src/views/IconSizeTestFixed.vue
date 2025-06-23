<template>
  <q-page padding>
    <div class="q-pa-lg">
      <h4>Test de Tamaños de Iconos - Versión Corregida</h4>
      
      <!-- Test básico con diferentes tamaños usando size prop -->
      <div class="q-mb-lg">
        <h5>Usando prop 'size' de Quasar:</h5>
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

      <!-- Test con tamaños específicos -->
      <div class="q-mb-lg">
        <h5>Usando tamaños específicos:</h5>
        <div class="row q-gutter-md items-center">
          <q-icon name="dashboard" size="1rem" />
          <span>1rem</span>
          <q-icon name="dashboard" size="1.5rem" />
          <span>1.5rem</span>
          <q-icon name="dashboard" size="2rem" />
          <span>2rem</span>
          <q-icon name="dashboard" size="3rem" />
          <span>3rem</span>
          <q-icon name="dashboard" size="4rem" />
          <span>4rem</span>
        </div>
      </div>

      <!-- Test con clases de texto -->
      <div class="q-mb-lg">
        <h5>Usando clases de texto de Quasar:</h5>
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
          <q-icon name="star" class="text-2xl" />
          <span>text-2xl</span>
          <q-icon name="star" class="text-3xl" />
          <span>text-3xl</span>
        </div>
      </div>

      <!-- Test en botones -->
      <div class="q-mb-lg">
        <h5>Iconos en botones:</h5>
        <div class="row q-gutter-md">
          <q-btn color="primary" icon="add" label="Pequeño" size="sm" />
          <q-btn color="primary" icon="add" label="Mediano" size="md" />
          <q-btn color="primary" icon="add" label="Grande" size="lg" />
        </div>
      </div>

      <!-- Test manual con Material Icons -->
      <div class="q-mb-lg">
        <h5>Material Icons directo (para comparación):</h5>
        <div class="row q-gutter-md items-center">
          <i class="material-icons" style="font-size: 16px;">home</i>
          <span>16px</span>
          <i class="material-icons" style="font-size: 24px;">home</i>
          <span>24px</span>
          <i class="material-icons" style="font-size: 32px;">home</i>
          <span>32px</span>
          <i class="material-icons" style="font-size: 48px;">home</i>
          <span>48px</span>
        </div>
      </div>

      <!-- Debug info -->
      <div class="q-mt-xl">
        <h5>Información de Debug:</h5>
        <div class="q-pa-md bg-grey-2 rounded-borders">
          <p><strong>Fonts disponibles:</strong> {{ fontsInfo.available ? 'Sí' : 'No' }}</p>
          <p><strong>Material Icons cargado:</strong> {{ fontsInfo.materialIconsCheck ? 'Sí' : 'No' }}</p>
          <p><strong>Enlaces de fonts encontrados:</strong> {{ materialIconsLinks.length }}</p>
        </div>
        
        <q-btn 
          color="primary" 
          label="Verificar tamaños" 
          @click="checkIconSizes"
          class="q-mt-md"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'IconSizeTestFixed',
  data() {
    return {
      fontsInfo: {
        available: false,
        materialIconsCheck: false
      },
      materialIconsLinks: []
    }
  },
  mounted() {
    this.checkFontsInfo()
  },
  methods: {
    checkFontsInfo() {
      if (document.fonts) {
        this.fontsInfo.available = true
        this.fontsInfo.materialIconsCheck = document.fonts.check('1rem "Material Icons"')
      }
      
      this.materialIconsLinks = Array.from(
        document.querySelectorAll('link[href*="material-icons"], link[href*="Material+Icons"]')
      ).map(link => link.href)
    },
    
    checkIconSizes() {
      const icons = document.querySelectorAll('.q-icon')
      console.log('🔍 Verificando tamaños de iconos:')
      
      icons.forEach((icon, index) => {
        const computedStyle = window.getComputedStyle(icon)
        const rect = icon.getBoundingClientRect()
        
        console.log(`Icono ${index + 1}:`, {
          fontSize: computedStyle.fontSize,
          width: computedStyle.width,
          height: computedStyle.height,
          actualWidth: rect.width,
          actualHeight: rect.height,
          fontFamily: computedStyle.fontFamily.substring(0, 50) + '...',
          classes: icon.className
        })
      })
      
      this.$q.notify({
        type: 'info',
        message: 'Información de tamaños en la consola',
        caption: 'Abre las herramientas de desarrollador para ver los detalles'
      })
    }
  }
}
</script>

<style scoped>
h5 {
  margin: 16px 0 8px 0;
}
</style>
