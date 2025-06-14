<template>
  <q-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" persistent>
    <q-card style="min-width: 400px;" :class="{ 'bg-dark text-white': isDark }">
      <q-card-section>
        <div class="text-h6">{{ playlist ? 'Editar Playlist' : 'Nueva Playlist' }}</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input v-model="form.name" label="Nombre de la playlist" outlined class="q-mb-md" />
        <q-input v-model="form.description" label="Descripción (opcional)" type="textarea" outlined rows="3" />
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
  playlist: Object,
  form: Object,
  loading: Boolean,
  isDark: Boolean
})

defineEmits(['update:modelValue', 'save', 'close'])
</script>
