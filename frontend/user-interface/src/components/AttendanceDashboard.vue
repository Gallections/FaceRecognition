<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService, type AttendanceMarkResponse, type AttendanceRecord, type PersonResponse } from '../services/apiService'
import WebcamCapture from './WebcamCapture.vue'

const imagePreview = ref<string>('')
const imageInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const isMarking = ref(false)
const markResult = ref<AttendanceMarkResponse | null>(null)
const showWebcam = ref(false)
const webcamMode = ref<'capture' | 'realtime'>('capture')
const notification = ref<{ message: string; type: 'success' | 'error' | 'info' } | null>(null)

// Today's attendance
const todayAttendance = ref<AttendanceRecord[]>([])
const isLoadingAttendance = ref(false)

// Manual marking
const persons = ref<PersonResponse[]>([])
const selectedPersonId = ref<string>('')
const showManualForm = ref(false)

function showNotification(message: string, type: 'success' | 'error' | 'info' = 'info') {
  notification.value = { message, type }
  setTimeout(() => {
    notification.value = null
  }, 5000)
}

onMounted(async () => {
  await loadTodayAttendance()
  await loadPersons()
})

async function loadTodayAttendance() {
  isLoadingAttendance.value = true
  try {
    todayAttendance.value = await apiService.getTodayAttendance()
  } catch (error: any) {
    console.error('Failed to load attendance:', error)
  } finally {
    isLoadingAttendance.value = false
  }
}

async function loadPersons() {
  try {
    persons.value = await apiService.getAllPersons()
  } catch (error: any) {
    console.error('Failed to load persons:', error)
  }
}

function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]

  if (file) {
    selectedFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
    markResult.value = null
  }
}

function triggerFileUpload() {
  imageInput.value?.click()
}

async function markAttendanceByFace() {
  if (!selectedFile.value) {
    showNotification('Please select an image first!', 'error')
    return
  }

  isMarking.value = true
  markResult.value = null

  try {
    const result = await apiService.markAttendanceByFace(selectedFile.value)
    markResult.value = result

    if (result.success) {
      showNotification(`✅ Attendance marked for ${result.full_name}!`, 'success')
      clearInput()
      await loadTodayAttendance() // Refresh the list
    } else {
      showNotification(result.message, 'error')
    }
  } catch (error: any) {
    showNotification(`Error: ${error.message}`, 'error')
  } finally {
    isMarking.value = false
  }
}

async function markAttendanceManual() {
  if (!selectedPersonId.value) {
    showNotification('Please select a person!', 'error')
    return
  }

  try {
    const result = await apiService.markAttendanceManual(selectedPersonId.value)
    
    if (result.success) {
      showNotification(`✅ Attendance marked for ${result.full_name}!`, 'success')
      selectedPersonId.value = ''
      showManualForm.value = false
      await loadTodayAttendance()
    } else {
      showNotification(result.message, 'error')
    }
  } catch (error: any) {
    showNotification(`Error: ${error.message}`, 'error')
  }
}

function clearInput() {
  imagePreview.value = ''
  selectedFile.value = null
  markResult.value = null
  if (imageInput.value) {
    imageInput.value.value = ''
  }
}

function openWebcam() {
  webcamMode.value = 'capture'
  showWebcam.value = true
}

function openRealtimeDetection() {
  webcamMode.value = 'realtime'
  showWebcam.value = true
}

function closeWebcam() {
  showWebcam.value = false
}

async function handleRealtimeDetection(blob: Blob): Promise<any> {
  try {
    const file = new File([blob], 'detection-frame.jpg', { type: 'image/jpeg' })
    const result = await apiService.markAttendanceByFace(file)
    
    // If attendance marked successfully, refresh the list
    if (result.success) {
      await loadTodayAttendance()
    }
    
    return result
  } catch (error: any) {
    console.error('Real-time attendance error:', error)
    return { success: false, message: error.message }
  }
}

function handleDetectionResult(result: AttendanceMarkResponse) {
  markResult.value = result
  
  if (result.success && result.full_name) {
    // Show brief success notification - attendance already marked
    console.log(`Attendance marked for: ${result.full_name}`)
  }
}

async function handleWebcamCapture(blob: Blob) {
  // Convert blob to File
  const file = new File([blob], 'webcam-capture.jpg', { type: 'image/jpeg' })
  selectedFile.value = file
  
  // Create preview
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
  
  showWebcam.value = false
  
  // Auto-mark attendance
  await markAttendanceByFace()
}
</script>

<template>
  <div class="attendance-dashboard">
    <!-- Notification Toast -->
    <div v-if="notification" :class="['notification-toast', `notification-${notification.type}`]">
      <span class="notification-icon">
        {{ notification.type === 'success' ? '✓' : notification.type === 'error' ? '✕' : 'ℹ' }}
      </span>
      <span class="notification-message">{{ notification.message }}</span>
      <button @click="notification = null" class="notification-close">×</button>
    </div>

    <h2>✅ Attendance Dashboard</h2>
    <p class="page-subtitle">Mark attendance using face recognition or manual entry</p>

    <div class="dashboard-grid">
      <!-- Mark Attendance by Face -->
      <div class="card">
        <h3>📸 Mark Attendance by Face</h3>
        <input
          type="file"
          ref="imageInput"
          @change="handleFileUpload"
          accept="image/*"
          aria-label="Upload image for face recognition"
          style="display: none"
        />

        <div class="button-group-vertical">
          <button @click="triggerFileUpload" class="btn-select" aria-label="Select image from device">
            📁 Select Image
          </button>
          <button @click="openWebcam" class="btn-camera" aria-label="Capture photo using webcam">
            📷 Capture Photo
          </button>
          <button @click="openRealtimeDetection" class="btn-realtime" aria-label="Start real-time face detection">
            🎥 Real-time Detection
          </button>
        </div>

        <div v-if="imagePreview" class="preview-section">
          <img :src="imagePreview" alt="Preview" class="image-preview" />
          <div class="action-buttons">
            <button @click="markAttendanceByFace" :disabled="isMarking" class="btn-mark">
              {{ isMarking ? 'Marking...' : '✓ Mark Attendance' }}
            </button>
            <button @click="clearInput" class="btn-clear-small">Clear</button>
          </div>
        </div>
      </div>

      <!-- Manual Attendance Marking -->
      <div class="card">
        <h3>✋ Manual Attendance</h3>
        <button @click="showManualForm = !showManualForm" class="btn-toggle">
          {{ showManualForm ? 'Hide Form' : 'Show Form' }}
        </button>

        <div v-if="showManualForm" class="manual-form">
          <label for="person-select" class="sr-only">Select person</label>
          <select 
            id="person-select"
            v-model="selectedPersonId" 
            class="person-select"
            aria-label="Select person to mark attendance"
          >
            <option value="">-- Select Person --</option>
            <option v-for="person in persons" :key="person.id" :value="person.id">
              {{ person.full_name }}
            </option>
          </select>
          <button 
            @click="markAttendanceManual" 
            class="btn-mark"
            :disabled="!selectedPersonId"
            aria-label="Mark selected person as present"
          >
            Mark Present
          </button>
        </div>
      </div>
    </div>

    <!-- Today's Attendance List -->
    <div class="attendance-list">
      <h3>📊 Today's Attendance ({{ todayAttendance.length }} present)</h3>
      
      <div v-if="isLoadingAttendance" class="loading">Loading...</div>

      <div v-else-if="todayAttendance.length === 0" class="empty-state">
        No attendance records for today yet.
      </div>

      <table v-else class="attendance-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Time</th>
            <th>Person ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in todayAttendance" :key="record.id">
            <td>{{ record.full_name }}</td>
            <td>{{ new Date(record.timestamp).toLocaleTimeString() }}</td>
            <td>{{ record.person_id }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Webcam Modal -->
    <WebcamCapture 
      v-if="showWebcam" 
      :mode="webcamMode"
      :on-detect="webcamMode === 'realtime' ? handleRealtimeDetection : undefined"
      @capture="handleWebcamCapture"
      @detected="handleDetectionResult"
      @close="closeWebcam"
    />
  </div>
</template>

<style scoped>
.attendance-dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  margin-bottom: 0.5rem;
  color: #333;
}

.page-subtitle {
  color: #666;
  margin-bottom: 2rem;
  font-size: 1rem;
}

/* Notification Toast */
.notification-toast {
  position: fixed;
  top: 2rem;
  right: 2rem;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  z-index: 9999;
  animation: slideIn 0.3s ease-out;
  max-width: 400px;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification-success {
  background: #d1fae5;
  border: 2px solid #059669;
  color: #065f46;
}

.notification-error {
  background: #fee2e2;
  border: 2px solid #dc2626;
  color: #991b1b;
}

.notification-info {
  background: #dbeafe;
  border: 2px solid #3b82f6;
  color: #1e40af;
}

.notification-icon {
  font-size: 1.25rem;
  font-weight: bold;
}

.notification-message {
  flex: 1;
  font-size: 0.95rem;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: inherit;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.notification-close:hover {
  opacity: 1;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card h3 {
  margin-bottom: 1rem;
  color: #333;
}

.btn-select {
  background: #4CAF50;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
}

.btn-select:hover {
  background: #45a049;
}

.btn-camera {
  background: #2196F3;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
}

.btn-camera:hover {
  background: #0b7dda;
}

.btn-realtime {
  background: #10b981;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
}

.btn-realtime:hover {
  background: #059669;
}

.button-group-vertical {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.btn-toggle {
  background: #2196F3;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
  margin-bottom: 1rem;
}

.btn-toggle:hover {
  background: #0b7dda;
}

.preview-section {
  margin-top: 1rem;
}

.image-preview {
  max-width: 100%;
  max-height: 250px;
  display: block;
  margin: 0 auto 1rem;
  border-radius: 6px;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-mark {
  background: #FF9800;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  flex: 1;
}

.btn-mark:hover:not(:disabled) {
  background: #F57C00;
}

.btn-mark:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-clear-small {
  background: #f44336;
  color: white;
  padding: 0.8rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-clear-small:hover {
  background: #da190b;
}

.manual-form {
  margin-top: 1rem;
}

.person-select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.person-select:focus {
  outline: none;
  border-color: #2196F3;
}

.attendance-list {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 2rem;
}

.attendance-list h3 {
  margin-bottom: 1.5rem;
  color: #333;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.attendance-table {
  width: 100%;
  border-collapse: collapse;
}

.attendance-table th {
  background: #f5f5f5;
  padding: 1rem;
  text-align: left;
  border-bottom: 2px solid #ddd;
  font-weight: bold;
  color: #555;
}

.attendance-table td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.attendance-table tr:hover {
  background: #f9f9f9;
}
</style>
