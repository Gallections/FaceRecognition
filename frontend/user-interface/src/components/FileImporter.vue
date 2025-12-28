<script setup lang="ts">
  import {ref, onMounted, computed} from 'vue'
  import { apiService, type PersonResponse } from '../services/apiService'
  import WebcamCapture from './WebcamCapture.vue'
  import ConfirmDialog from './ConfirmDialog.vue'

  const filteredPersons = computed(() => {
    if (!searchQuery.value.trim()) {
      return persons.value
    }
    const query = searchQuery.value.toLowerCase()
    return persons.value.filter(p => 
      p.full_name.toLowerCase().includes(query) ||
      p.first_name.toLowerCase().includes(query) ||
      p.last_name.toLowerCase().includes(query)
    )
  })

  function showNotification(message: string, type: 'success' | 'error' | 'info' = 'info') {
    notification.value = { message, type }
    setTimeout(() => {
      notification.value = null
    }, 5000)
  }

  const imagePreview = ref<string>('');
  const imageInput = ref<HTMLInputElement | null>(null);
  let firstNameInput = ref<string>("")
  let lastNameInput = ref<string>("")
  let fileToBeUploaded: undefined | File = undefined;
  let uploadMessage = ref<string>("")
  let isUploading = ref<boolean>(false)
  const showWebcam = ref(false)

  // Person management
  const persons = ref<PersonResponse[]>([])
  const personImages = ref<Map<string, string>>(new Map())
  const isLoadingPersons = ref(false)
  const isPersonsListVisible = ref(true)
  const expandedPersons = ref<Set<string>>(new Set())
  const editingPerson = ref<PersonResponse | null>(null)
  const searchQuery = ref<string>('')
  const notification = ref<{ message: string; type: 'success' | 'error' | 'info' } | null>(null)
  const editFormData = ref({ first_name: '', last_name: '' })
  const editPhotoPreview = ref<string>('')
  const editPhotoFile = ref<File | undefined>(undefined)
  const editPhotoInput = ref<HTMLInputElement | null>(null)
  const webcamMode = ref<'register' | 'edit'>('register')
  const showDeleteConfirm = ref(false)
  const personToDelete = ref<PersonResponse | null>(null)

  onMounted(async () => {
    await loadPersons()
  })

  async function loadPersons() {
    isLoadingPersons.value = true
    try {
      persons.value = await apiService.getAllPersons()
      await loadPersonImages()
    } catch (err: any) {
      console.error('Failed to load persons:', err)
    } finally {
      isLoadingPersons.value = false
    }
  }

  async function loadPersonImages() {
    const imageMap = new Map<string, string>()
    
    for (const person of persons.value) {
      try {
        const imageUrl = await apiService.getPersonImage(person.id)
        if (imageUrl) {
          imageMap.set(person.id, imageUrl)
        }
      } catch (err) {
        console.error(`Failed to load image for person ${person.id}:`, err)
      }
    }
    
    personImages.value = imageMap
  }

  function togglePerson(personId: string) {
    if (expandedPersons.value.has(personId)) {
      expandedPersons.value.delete(personId)
    } else {
      expandedPersons.value.add(personId)
    }
  }

  function collapseAll() {
    isPersonsListVisible.value = false
  }

  function expandAll() {
    isPersonsListVisible.value = true
  }

  function startEdit(person: PersonResponse) {
    editingPerson.value = person
    editFormData.value = {
      first_name: person.first_name,
      last_name: person.last_name
    }
    editPhotoPreview.value = ''
    editPhotoFile.value = undefined
  }

  function cancelEdit() {
    editingPerson.value = null
    editFormData.value = { first_name: '', last_name: '' }
    editPhotoPreview.value = ''
    editPhotoFile.value = undefined
  }

  async function updatePerson() {
    if (!editingPerson.value) return

    try {
      // Update name fields
      await apiService.updatePerson(editingPerson.value.id, editFormData.value)
      
      // Update photo if changed
      if (editPhotoFile.value) {
        await apiService.updatePersonImage(editingPerson.value.id, editPhotoFile.value)
      }
      
      showNotification('Person updated successfully!', 'success')
      editingPerson.value = null
      editFormData.value = { first_name: '', last_name: '' }
      editPhotoPreview.value = ''
      editPhotoFile.value = undefined
      await loadPersons()
    } catch (err: any) {
      showNotification(`Error: ${err.message}`, 'error')
    }
  }

  function confirmDelete(person: PersonResponse) {
    personToDelete.value = person
    showDeleteConfirm.value = true
  }

  async function deletePerson() {
    if (!personToDelete.value) return

    try {
      await apiService.deletePerson(personToDelete.value.id)
      showNotification('Person deleted successfully!', 'success')
      await loadPersons()
    } catch (err: any) {
      showNotification(`Error: ${err.message}`, 'error')
    } finally {
      showDeleteConfirm.value = false
      personToDelete.value = null
    }
  }

  function cancelDelete() {
    showDeleteConfirm.value = false
    personToDelete.value = null
  }


  function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (file) {
      fileToBeUploaded = file;
      const reader = new FileReader();
      reader.onload = (e) => {  // registers the callback
        imagePreview.value = e.target?.result as string;
      };
      reader.readAsDataURL(file);  // this function actually triggers the onload, it's asynchronous
    }
  }

  function triggerFileUpload() {
    imageInput.value?.click();
  }

  async function triggerBackendUpload() {
      if (!firstNameInput.value.trim()) {
        showNotification("First name is required", 'error')
        return
      }
      if (!lastNameInput.value.trim()) {
        showNotification("Last name is required", 'error')
        return
      }

      if (!fileToBeUploaded) {
        showNotification("Please select an image first", 'error')
        return;
      }

      isUploading.value = true
      uploadMessage.value = ""

      try {
        // Use the new API service
        const response = await apiService.uploadPersonImage(
          fileToBeUploaded,
          firstNameInput.value,
          lastNameInput.value
        )
        
        uploadMessage.value = response.message
        showNotification(`✅ ${response.message}`, 'success')
        clearInput()
        await loadPersons() // Reload persons list
        
      } catch (error: any) {
        uploadMessage.value = `Error: ${error.message}`
        showNotification(`Error: ${error.message}`, 'error')
      } finally {
        isUploading.value = false
      }
  }

  function openWebcam() {
    webcamMode.value = 'register'
    showWebcam.value = true
  }

  function openWebcamForEdit() {
    webcamMode.value = 'edit'
    showWebcam.value = true
  }

  function closeWebcam() {
    showWebcam.value = false
  }

  async function handleWebcamCapture(blob: Blob) {
    const file = new File([blob], 'webcam-capture.jpg', { type: 'image/jpeg' })
    
    if (webcamMode.value === 'edit') {
      editPhotoFile.value = file
      const reader = new FileReader()
      reader.onload = (e) => {
        editPhotoPreview.value = e.target?.result as string
      }
      reader.readAsDataURL(file)
    } else {
      fileToBeUploaded = file
      const reader = new FileReader()
      reader.onload = (e) => {
        imagePreview.value = e.target?.result as string
      }
      reader.readAsDataURL(file)
    }
    
    showWebcam.value = false
  }

  function triggerEditPhotoUpload() {
    editPhotoInput.value?.click()
  }

  function handleEditPhotoUpload(event: Event) {
    const input = event.target as HTMLInputElement
    const file = input.files?.[0]

    if (file) {
      editPhotoFile.value = file
      const reader = new FileReader()
      reader.onload = (e) => {
        editPhotoPreview.value = e.target?.result as string
      }
      reader.readAsDataURL(file)
    }
  }

  function clearInput() {
    imageInput.value = null;
    imagePreview.value ='';
    fileToBeUploaded = undefined;
    firstNameInput.value = '';
    lastNameInput.value ='';
  }

</script>

<template>
  <div class="person-registration">
    <!-- Notification Toast -->
    <div v-if="notification" :class="['notification-toast', `notification-${notification.type}`]">
      <span class="notification-icon">
        {{ notification.type === 'success' ? '✓' : notification.type === 'error' ? '✕' : 'ℹ' }}
      </span>
      <span class="notification-message">{{ notification.message }}</span>
      <button @click="notification = null" class="notification-close">×</button>
    </div>

    <!-- Upload Section -->
    <section class="upload-section">
      <h2>📤 Register New Person</h2>
      <p class="section-subtitle">Upload a photo or capture from camera to register a new person</p>

      <div class="upload-card">
        <input
          type= "file"
          ref = "imageInput"
          @change ="handleFileUpload"
          accept = "image/*"
          aria-label="Upload person image"
          style="display:none"
        />

        <div class="button-group-horizontal">
          <button class="btn-select" @click="triggerFileUpload">📁 Select Image</button>
          <button class="btn-camera" @click="openWebcam">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/>
              <circle cx="12" cy="13" r="4"/>
            </svg>
            Capture Photo
          </button>
        </div>

        <div v-if="imagePreview" class="upload-preview-container">
          <h3>Preview & Details</h3>
          <img id="image-previewer" :src="imagePreview" alt="preview-image" />

          <div class="input-row">
            <div class="input-container">
              <label>First Name:</label>
              <input
                  v-model="firstNameInput"
                  type="text"
                  placeholder="Enter first name"
                  required
              />
            </div>

            <div class="input-container">
              <label>Last Name:</label>
              <input
                  v-model="lastNameInput"
                  type="text"
                  placeholder="Enter last name"
                  required
                />
            </div>
          </div>

          <div class="action-buttons">
            <button class="btn-upload" @click="triggerBackendUpload" :disabled="isUploading">
              {{ isUploading ? 'Uploading...' : '✓ Register Person' }}
            </button>
            <button class="btn-clear" @click="clearInput">Clear</button>
          </div>

          <div v-if="uploadMessage" class="upload-message">
            {{ uploadMessage }}
          </div>
        </div>

        <div v-else class="upload-empty">
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/>
              <circle cx="12" cy="13" r="4"/>
            </svg>
          </div>
          <p>Select an image or capture a photo to begin registration</p>
        </div>
      </div>
    </section>

    <!-- Registered Persons Section -->
    <section class="persons-section">
      <div class="section-header">
        <div class="section-header-left">
          <h2>👥 Registered Persons ({{ filteredPersons.length }}{{ searchQuery ? ` of ${persons.length}` : '' }})</h2>
        </div>
        <div class="header-actions">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="🔍 Search persons..." 
            class="search-input"
          />
          <button @click="expandAll" class="btn-toggle">Show All</button>
          <button @click="collapseAll" class="btn-toggle">Hide All</button>
        </div>
      </div>

      <div v-if="isLoadingPersons" class="loading">
        <div class="spinner"></div>
        <p>Loading persons...</p>
      </div>

      <div v-else-if="filteredPersons.length === 0 && searchQuery" class="empty-state">
        No persons found matching "{{ searchQuery }}"
      </div>

      <div v-else-if="persons.length === 0" class="empty-state">
        No persons registered yet. Upload a photo above to get started!
      </div>

      <div v-else-if="isPersonsListVisible" class="persons-list">
        <div v-for="person in filteredPersons" :key="person.id" class="person-item">
          <!-- Person Header (Always Visible) -->
          <div class="person-header" @click="togglePerson(person.id)">
            <div class="person-header-left">
              <div class="person-avatar">
                <img 
                  v-if="personImages.get(person.id)" 
                  :src="personImages.get(person.id)" 
                  :alt="person.full_name"
                />
                <svg v-else class="avatar-placeholder" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2M12 11a4 4 0 100-8 4 4 0 000 8z"/>
                </svg>
              </div>
              <div class="person-info">
                <h3>{{ person.full_name }}</h3>
                <p class="person-date">Registered {{ new Date(person.date_created).toLocaleDateString() }}</p>
              </div>
            </div>
            <div class="person-header-actions">
              <button 
                class="delete-icon-btn" 
                @click.stop="confirmDelete(person)"
                title="Delete person"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2M10 11v6M14 11v6"/>
                </svg>
              </button>
              <button class="expand-btn" :class="{ expanded: expandedPersons.has(person.id) }">
                {{ expandedPersons.has(person.id) ? '▼' : '▶' }}
              </button>
            </div>
          </div>

          <!-- Person Details (Collapsible) -->
          <div v-if="expandedPersons.has(person.id)" class="person-details">
            <!-- View Mode -->
            <div v-if="editingPerson?.id !== person.id" class="person-view">
              <div class="person-image-large">
                <img 
                  v-if="personImages.get(person.id)" 
                  :src="personImages.get(person.id)" 
                  :alt="person.full_name"
                />
                <div v-else class="image-placeholder">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2M12 11a4 4 0 100-8 4 4 0 000 8z"/>
                  </svg>
                </div>
              </div>

              <div class="person-data">
                <div class="data-row">
                  <span class="data-label">ID:</span>
                  <span class="data-value">{{ person.id }}</span>
                </div>
                <div class="data-row">
                  <span class="data-label">First Name:</span>
                  <span class="data-value">{{ person.first_name }}</span>
                </div>
                <div class="data-row">
                  <span class="data-label">Last Name:</span>
                  <span class="data-value">{{ person.last_name }}</span>
                </div>
                <div class="data-row">
                  <span class="data-label">Created:</span>
                  <span class="data-value">{{ new Date(person.date_created).toLocaleString() }}</span>
                </div>
              </div>

              <div class="person-actions">
                <button @click="startEdit(person)" class="btn-edit">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                  Edit
                </button>
                <button @click="confirmDelete(person)" class="btn-delete">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2M10 11v6M14 11v6"/>
                  </svg>
                  Delete
                </button>
              </div>
            </div>

            <!-- Edit Mode -->
            <div v-else class="person-edit">
              <h4>Edit Person Details</h4>
              <div class="edit-form">
                <div class="input-container">
                  <label>First Name:</label>
                  <input v-model="editFormData.first_name" type="text" />
                </div>
                <div class="input-container">
                  <label>Last Name:</label>
                  <input v-model="editFormData.last_name" type="text" />
                </div>
                
                <!-- Photo Change Section -->
                <div class="photo-change-section">
                  <h5>Change Photo (Optional)</h5>
                  <input
                    type="file"
                    ref="editPhotoInput"
                    @change="handleEditPhotoUpload"
                    accept="image/*"
                    style="display:none"
                  />
                  <div class="button-group-horizontal">
                    <button type="button" class="btn-select" @click="triggerEditPhotoUpload">📁 Select New Image</button>
                    <button type="button" class="btn-camera" @click="openWebcamForEdit">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/>
                        <circle cx="12" cy="13" r="4"/>
                      </svg>
                      Capture New Photo
                    </button>
                  </div>
                  
                  <div v-if="editPhotoPreview" class="edit-photo-preview">
                    <p class="preview-label">New Photo Preview:</p>
                    <img :src="editPhotoPreview" alt="New photo preview" />
                  </div>
                </div>
                
                <div class="edit-actions">
                  <button @click="updatePerson" class="btn-save">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/>
                      <polyline points="17 21 17 13 7 13 7 21"/>
                      <polyline points="7 3 7 8 15 8"/>
                    </svg>
                    Save Changes
                  </button>
                  <button @click="cancelEdit" class="btn-cancel">Cancel</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Webcam Modal -->
    <WebcamCapture 
      v-if="showWebcam" 
      mode="capture"
      @capture="handleWebcamCapture"
      @close="closeWebcam"
    />

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      :show="showDeleteConfirm"
      :title="'Confirm Deletion'"
      :message="`Are you sure you want to delete ${personToDelete?.full_name}? This action cannot be undone.`"
      confirmText="Delete"
      cancelText="Cancel"
      variant="danger"
      @confirm="deletePerson"
      @cancel="cancelDelete"
    />
  </div>
</template>

<style scoped>
.person-registration {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

/* Notification Toast */
.notification-toast {
  position: fixed;
  top: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  animation: slideIn 0.3s ease;
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
  background: #10b981;
  color: white;
}

.notification-error {
  background: #ef4444;
  color: white;
}

.notification-info {
  background: #3b82f6;
  color: white;
}

.notification-icon {
  font-size: 1.25rem;
  font-weight: bold;
}

.notification-message {
  flex: 1;
  font-weight: 500;
}

.notification-close {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  line-height: 1;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.notification-close:hover {
  opacity: 1;
}

/* Upload Section */
.upload-section {
  margin-bottom: 3rem;
}

.upload-section h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.section-subtitle {
  color: var(--text-secondary);
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.upload-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 2px solid var(--border-color);
}

.button-group-horizontal {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.btn-select, .btn-camera {
  flex: 1;
  min-width: 200px;
  padding: 0.875rem 1.75rem;
  font-size: 1rem;
  font-weight: 500;
  border: 1px solid var(--border-dark);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-select {
  background: var(--bg-dark);
  color: white;
  border-color: var(--bg-dark);
}

.btn-select:hover {
  background: #0a1120;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}

.btn-camera {
  background: white;
  color: var(--text-primary);
}

.btn-camera:hover {
  background: var(--bg-secondary);
  border-color: var(--text-primary);
}

.upload-preview-container {
  margin-top: 2rem;
}

.upload-preview-container h3 {
  margin-bottom: 1rem;
  color: var(--text-primary);
}

#image-previewer {
  width: 100%;
  max-width: 600px;
  max-height: 400px;
  object-fit: contain;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.input-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-container label {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.input-container input {
  padding: 0.75rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.input-container input:focus {
  border-color: var(--primary-color);
  outline: none;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.btn-upload, .btn-clear {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-upload {
  flex: 1;
  background: #FF9800;
  color: white;
}

.btn-upload:hover:not(:disabled) {
  background: #F57C00;
  transform: translateY(-2px);
}

.btn-upload:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-clear {
  background: var(--gray-200);
  color: var(--text-primary);
}

.btn-clear:hover {
  background: var(--gray-300);
}

.upload-message {
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: 8px;
  color: var(--text-primary);
  text-align: center;
}

.upload-empty {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 2px dashed var(--border-color);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.upload-empty p {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

/* Persons Section */
.persons-section {
  margin-top: 3rem;
}

.section-header {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header-left {
  flex: 1;
}

.section-header h2 {
  font-size: 1.75rem;
  color: var(--text-primary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-input {
  padding: 0.65rem 1rem;
  border: 2px solid var(--border-color);
  border-radius: 6px;
  font-size: 0.95rem;
  min-width: 200px;
  transition: all 0.2s;
}

.search-input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.btn-toggle {
  padding: 0.65rem 1.25rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-toggle:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  background: white;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  background: white;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  font-size: 1.05rem;
}

.persons-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.person-item {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.person-item:hover {
  border-color: var(--border-dark);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.person-item:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.person-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  cursor: pointer;
  transition: background 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

.person-header:hover {
  background: var(--bg-secondary);
}

.person-header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
}

.person-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 2px solid rgba(102, 126, 234, 0.2);
}

.person-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  color: var(--gray-400);
}

.person-info h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.person-date {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

.person-header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.delete-icon-btn {
  background: rgba(220, 38, 38, 0.1);
  border: 1px solid rgba(220, 38, 38, 0.2);
  color: #dc2626;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-icon-btn:hover {
  background: #dc2626;
  border-color: #dc2626;
  color: white;
  transform: scale(1.05);
}

.delete-icon-btn svg {
  stroke-width: 2;
}

.expand-btn {
  background: transparent;
  border: none;
  font-size: 1rem;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 0.375rem 0.75rem;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 8px;
}

.expand-btn:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.expand-btn.expanded {
  transform: rotate(0deg);
}

.person-details {
  padding: 0 1.5rem 1.5rem 1.5rem;
  border-top: 1px solid var(--border-color);
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 1000px;
  }
}

.person-view {
  padding-top: 1.5rem;
}

.person-image-large {
  width: 100%;
  max-width: 400px;
  height: 300px;
  margin-bottom: 1.5rem;
  border-radius: 12px;
  overflow: hidden;
  background: var(--bg-secondary);
}

.person-image-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-size: 6rem;
  color: white;
}

.person-data {
  margin-bottom: 1.5rem;
}

.data-row {
  display: flex;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-color);
}

.data-row:last-child {
  border-bottom: none;
}

.data-label {
  font-weight: 600;
  color: var(--text-secondary);
  min-width: 120px;
}

.data-value {
  color: var(--text-primary);
  word-break: break-all;
}

.person-actions {
  display: flex;
  gap: 1rem;
}

.btn-edit, .btn-delete {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  font-size: 0.9375rem;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-edit {
  background: var(--gray-100);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-edit:hover {
  background: var(--gray-200);
  border-color: var(--border-dark);
}

.btn-delete {
  background: white;
  color: #dc2626;
  border: 2px solid #dc2626;
}

.btn-delete:hover {
  background: #dc2626;
  color: white;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
  transform: translateY(-1px);
}

.person-edit {
  padding-top: 1.5rem;
}

.person-edit h4 {
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.photo-change-section {
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.photo-change-section h5 {
  margin: 0 0 1rem 0;
  color: var(--text-primary);
  font-size: 1.1rem;
}

.edit-photo-preview {
  margin-top: 1.5rem;
}

.preview-label {
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.edit-photo-preview img {
  width: 100%;
  max-width: 300px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid var(--border-color);
}

.edit-actions {
  display: flex;
  gap: 1rem;
}

.btn-save, .btn-cancel {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  font-size: 0.9375rem;
  font-weight: 500;
  border: 1px solid var(--border-dark);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-save {
  background: var(--bg-dark);
  color: white;
  border-color: var(--bg-dark);
  flex: 1;
}

.btn-save:hover {
  background: #0a1120;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}

.btn-cancel {
  background: white;
  color: var(--text-primary);
}

.btn-cancel:hover {
  background: var(--bg-secondary);
  border-color: var(--text-primary);
}

@media (max-width: 768px) {
  .button-group-horizontal {
    flex-direction: column;
  }

  .btn-select, .btn-camera {
    min-width: 100%;
  }

  .input-row {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .person-header-left {
    gap: 1rem;
  }

  .person-avatar {
    width: 50px;
    height: 50px;
  }
}
</style>