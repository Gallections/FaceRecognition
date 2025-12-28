<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService, type AttendanceRecord, type PersonResponse } from '../services/apiService'

// Date filtering
const selectedDate = ref<string>(new Date().toISOString().split('T')[0])
const attendanceRecords = ref<AttendanceRecord[]>([])
const isLoading = ref(false)

// Person attendance filtering
const persons = ref<PersonResponse[]>([])
const selectedPersonId = ref<string>('')
const startDate = ref<string>('')
const endDate = ref<string>('')
const personAttendance = ref<AttendanceRecord[]>([])
const isLoadingPersonAttendance = ref(false)
const notification = ref<{ message: string; type: 'success' | 'error' | 'info' } | null>(null)

function showNotification(message: string, type: 'success' | 'error' | 'info' = 'info') {
  notification.value = { message, type }
  setTimeout(() => {
    notification.value = null
  }, 4000)
}

onMounted(async () => {
  await loadPersons()
  await loadAttendanceByDate()
})

async function loadPersons() {
  try {
    persons.value = await apiService.getAllPersons()
  } catch (error: any) {
    console.error('Failed to load persons:', error)
  }
}

async function loadAttendanceByDate() {
  isLoading.value = true
  try {
    attendanceRecords.value = await apiService.getAttendanceByDate(selectedDate.value)
  } catch (error: any) {
    showNotification(`Error: ${error.message}`, 'error')
  } finally {
    isLoading.value = false
  }
}

async function loadPersonAttendance() {
  if (!selectedPersonId.value) {
    showNotification('Please select a person', 'error')
    return
  }

  isLoadingPersonAttendance.value = true
  try {
    personAttendance.value = await apiService.getPersonAttendance(
      selectedPersonId.value,
      startDate.value || undefined,
      endDate.value || undefined
    )
  } catch (error: any) {
    showNotification(`Error: ${error.message}`, 'error')
  } finally {
    isLoadingPersonAttendance.value = false
  }
}

async function exportTodayCSV() {
  try {
    const blob = await apiService.exportTodayAttendanceCSV()
    downloadBlob(blob, `attendance_today_${new Date().toISOString().split('T')[0]}.csv`)
    showNotification('CSV exported successfully!', 'success')
  } catch (error: any) {
    showNotification(`Error: ${error.message}`, 'error')
  }
}

async function exportDateCSV() {
  try {
    const blob = await apiService.exportAttendanceCSVByDate(selectedDate.value)
    downloadBlob(blob, `attendance_${selectedDate.value}.csv`)
    showNotification('CSV exported successfully!', 'success')
  } catch (error: any) {
    showNotification(`Error: ${error.message}`, 'error')
  }
}

function downloadBlob(blob: Blob, filename: string) {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}

function getSelectedPersonName(): string {
  const person = persons.value.find(p => p.id === selectedPersonId.value)
  return person?.full_name || 'Unknown'
}
</script>

<template>
  <div class="attendance-reports">
    <!-- Notification Toast -->
    <div v-if="notification" :class="['notification-toast', `notification-${notification.type}`]">
      <span class="notification-icon">
        {{ notification.type === 'success' ? '✓' : notification.type === 'error' ? '✕' : 'ℹ' }}
      </span>
      <span class="notification-message">{{ notification.message }}</span>
      <button @click="notification = null" class="notification-close">×</button>
    </div>

    <h2>📊 Attendance Reports & Analytics</h2>
    <p class="page-subtitle">View, filter, and export attendance records</p>

    <div class="reports-grid">
      <!-- Export Today's Attendance -->
      <div class="card">
        <h3>📅 Today's Attendance Export</h3>
        <p class="card-description">Download today's attendance records as CSV</p>
        <button @click="exportTodayCSV" class="btn-export">
          📥 Export Today's Attendance
        </button>
      </div>

      <!-- View/Export by Date -->
      <div class="card">
        <h3>📆 Attendance by Date</h3>
        <div class="form-group">
          <label>Select Date:</label>
          <input 
            v-model="selectedDate" 
            type="date" 
            class="date-input"
            @change="loadAttendanceByDate"
          />
        </div>

        <div class="button-group">
          <button @click="loadAttendanceByDate" class="btn-load">
            🔍 View Records
          </button>
          <button @click="exportDateCSV" class="btn-export-small">
            📥 Export CSV
          </button>
        </div>

        <div v-if="isLoading" class="loading">Loading...</div>

        <div v-else-if="attendanceRecords.length > 0" class="records-summary">
          <p><strong>Total Present:</strong> {{ attendanceRecords.length }}</p>
          <div class="records-list">
            <div v-for="record in attendanceRecords" :key="record.id" class="record-item">
              <span>{{ record.full_name }}</span>
              <span class="time">{{ new Date(record.timestamp).toLocaleTimeString() }}</span>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          No records for {{ selectedDate }}
        </div>
      </div>

      <!-- Person Attendance History -->
      <div class="card full-width">
        <h3>👤 Individual Attendance History</h3>
        
        <div class="filter-section">
          <div class="form-group">
            <label>Select Person:</label>
            <select v-model="selectedPersonId" class="person-select">
              <option value="">-- Select Person --</option>
              <option v-for="person in persons" :key="person.id" :value="person.id">
                {{ person.full_name }}
              </option>
            </select>
          </div>

          <div class="date-range">
            <div class="form-group">
              <label>Start Date:</label>
              <input v-model="startDate" type="date" class="date-input" />
            </div>

            <div class="form-group">
              <label>End Date:</label>
              <input v-model="endDate" type="date" class="date-input" />
            </div>
          </div>

          <button @click="loadPersonAttendance" class="btn-load">
            🔍 Load Attendance History
          </button>
        </div>

        <div v-if="isLoadingPersonAttendance" class="loading">Loading...</div>

        <div v-else-if="personAttendance.length > 0" class="person-history">
          <h4>📊 {{ getSelectedPersonName() }} - {{ personAttendance.length }} records</h4>
          
          <table class="attendance-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in personAttendance" :key="record.id">
                <td>{{ new Date(record.timestamp).toLocaleDateString() }}</td>
                <td>{{ new Date(record.timestamp).toLocaleTimeString() }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else-if="selectedPersonId" class="empty-state">
          No attendance records found for the selected criteria.
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.attendance-reports {
  padding: 2rem;
  max-width: 1400px;
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

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card.full-width {
  grid-column: 1 / -1;
}

.card h3 {
  margin-bottom: 1rem;
  color: #333;
}

.card-description {
  color: #666;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555;
}

.date-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.date-input:focus {
  outline: none;
  border-color: #2196F3;
}

.person-select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.person-select:focus {
  outline: none;
  border-color: #2196F3;
}

.button-group {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-export {
  background: #4CAF50;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
}

.btn-export:hover {
  background: #45a049;
}

.btn-load {
  background: #2196F3;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  flex: 1;
}

.btn-load:hover {
  background: #0b7dda;
}

.btn-export-small {
  background: #4CAF50;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-export-small:hover {
  background: #45a049;
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
  background: #f9f9f9;
  border-radius: 6px;
  margin-top: 1rem;
}

.records-summary {
  margin-top: 1.5rem;
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 6px;
}

.records-summary p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: #333;
}

.records-list {
  max-height: 300px;
  overflow-y: auto;
}

.record-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: white;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.record-item .time {
  color: #666;
  font-size: 0.9rem;
}

.filter-section {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.date-range {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.person-history h4 {
  margin-bottom: 1rem;
  color: #333;
  padding: 1rem;
  background: #e3f2fd;
  border-radius: 6px;
}

.attendance-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
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

/* Responsive Design */
@media (max-width: 768px) {
  .reports-grid {
    grid-template-columns: 1fr;
  }
  
  .date-range {
    grid-template-columns: 1fr;
  }
  
  .notification-toast {
    left: 1rem;
    right: 1rem;
    top: 1rem;
    z-index: 9999;
  }
  
  .attendance-table {
    font-size: 0.9rem;
  }
  
  .attendance-table th,
  .attendance-table td {
    padding: 0.5rem;
  }
}
</style>
