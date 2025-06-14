<template>
  <q-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" persistent>
    <q-card style="min-width: 400px;" :class="{ 'bg-dark text-white': isDark }">
      <q-card-section>
        <div class="text-h6">Programar Contenido</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input v-model="form.contentName" label="Nombre" outlined class="q-mb-md" />
        <!-- Campos adicionales para programación -->
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Cancelar" @click="$emit('close')" />
        <q-btn color="primary" label="Guardar" :loading="loading" @click="$emit('save')" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
defineProps({
  modelValue: Boolean,
  form: Object,
  loading: Boolean,
  isDark: Boolean,
  weekdayOptions: Array
})

defineEmits(['update:modelValue', 'save', 'close'])
</script>
