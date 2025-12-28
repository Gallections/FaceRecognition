<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  show: boolean
  title?: string
  message: string
  confirmText?: string
  cancelText?: string
  variant?: 'danger' | 'warning' | 'info'
}>()

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()

const isVisible = ref(props.show)

watch(() => props.show, (newVal) => {
  isVisible.value = newVal
})

function handleConfirm() {
  emit('confirm')
}

function handleCancel() {
  emit('cancel')
}
</script>

<template>
  <div v-if="isVisible" class="modal-overlay" @click="handleCancel" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3 id="dialog-title" class="modal-title">{{ title || 'Confirm Action' }}</h3>
      </div>
      <div class="modal-body">
        <p>{{ message }}</p>
      </div>
      <div class="modal-footer">
        <button 
          @click="handleCancel" 
          class="btn-outline"
          aria-label="Cancel action"
        >
          {{ cancelText || 'Cancel' }}
        </button>
        <button 
          @click="handleConfirm" 
          :class="variant === 'danger' ? 'btn-danger' : 'btn-primary'"
          aria-label="Confirm action"
        >
          {{ confirmText || 'Confirm' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn-outline {
  background: transparent;
  color: var(--text-primary);
  border: 2px solid var(--border-color);
  padding: 0.625rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline:hover {
  border-color: #2563eb;
  color: #2563eb;
  background: rgba(37, 99, 235, 0.05);
  transform: translateY(-1px);
}

.btn-primary, .btn-danger {
  padding: 0.625rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  border: none;
  color: white;
  transition: all 0.2s;
}

.btn-primary {
  background: #2563eb;
  color: white;
  border: none;
}

.btn-primary:hover {
  background: #1d4ed8;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
  transform: translateY(-1px);
}

.btn-danger {
  background: #dc2626;
  color: white;
  border: none;
}

.btn-danger:hover {
  background: #b91c1c;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
  transform: translateY(-1px);
}
</style>
