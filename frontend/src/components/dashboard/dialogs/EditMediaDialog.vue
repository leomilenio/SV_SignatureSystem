<template>
  <q-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" persistent>
    <q-card style="min-width: 800px; max-width: 1000px;" :class="{ 'bg-dark text-white': isDark }">
      <q-card-section>
        <div class="text-h6">Gestionar Medio - {{ media?.filename }}</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input v-model="form.filename" label="Nombre del archivo" outlined class="q-mb-md" />
        <q-input v-model="form.description" label="Descripción" type="textarea" outlined rows="3" />
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
  media: Object,
  form: Object,
  loading: Boolean,
  isDark: Boolean
})

defineEmits(['update:modelValue', 'save', 'close'])
</script>
