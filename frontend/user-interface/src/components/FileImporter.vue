<script setup lang="ts">
  import {ref, onMounted} from 'vue'
  import { apiService, type PersonResponse } from '../services/apiService'
  import WebcamCapture from './WebcamCapture.vue'

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
  const editFormData = ref({ first_name: '', last_name: '' })
  const editPhotoPreview = ref<string>('')
  const editPhotoFile = ref<File | undefined>(undefined)
  const editPhotoInput = ref<HTMLInputElement | null>(null)
  const webcamMode = ref<'register' | 'edit'>('register')

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
      
      window.alert('Person updated successfully!')
      editingPerson.value = null
      editFormData.value = { first_name: '', last_name: '' }
      editPhotoPreview.value = ''
      editPhotoFile.value = undefined
      await loadPersons()
    } catch (err: any) {
      window.alert(`Error: ${err.message}`)
    }
  }

  async function deletePerson(person: PersonResponse) {
    if (!window.confirm(`Delete ${person.full_name}? This cannot be undone.`)) {
      return
    }

    try {
      await apiService.deletePerson(person.id)
      window.alert('Person deleted successfully!')
      await loadPersons()
    } catch (err: any) {
      window.alert(`Error: ${err.message}`)
    }
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
      if (!firstNameInput.value) {
        window.alert("You must input the first name!")
        return
      }
      if (!lastNameInput.value) {
        window.alert("You must input the last name!")
        return
      }

      if (!fileToBeUploaded) {
        window.alert("You must select an Image first!")
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
        window.alert(`Success! ${response.message}`)
        clearInput()
        await loadPersons() // Reload persons list
        
      } catch (error: any) {
        uploadMessage.value = `Error: ${error.message}`
        window.alert(`Error: ${error.message}`)
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
          style="display:none"
        />

        <div class="button-group-horizontal">
          <button class="btn-select" @click="triggerFileUpload">📁 Select Image</button>
          <button class="btn-camera" @click="openWebcam">📷 Capture Photo</button>
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
          <div class="empty-icon">📸</div>
          <p>Select an image or capture a photo to begin registration</p>
        </div>
      </div>
    </section>

    <!-- Registered Persons Section -->
    <section class="persons-section">
      <div class="section-header">
        <h2>👥 Registered Persons ({{ persons.length }})</h2>
        <div class="header-actions">
          <button @click="expandAll" class="btn-toggle">Show All</button>
          <button @click="collapseAll" class="btn-toggle">Hide All</button>
        </div>
      </div>

      <div v-if="isLoadingPersons" class="loading">Loading persons...</div>

      <div v-else-if="persons.length === 0" class="empty-state">
        No persons registered yet. Upload a photo above to get started!
      </div>

      <div v-else-if="isPersonsListVisible" class="persons-list">
        <div v-for="person in persons" :key="person.id" class="person-item">
          <!-- Person Header (Always Visible) -->
          <div class="person-header" @click="togglePerson(person.id)">
            <div class="person-header-left">
              <div class="person-avatar">
                <img 
                  v-if="personImages.get(person.id)" 
                  :src="personImages.get(person.id)" 
                  :alt="person.full_name"
                />
                <span v-else class="avatar-placeholder">👤</span>
              </div>
              <div class="person-info">
                <h3>{{ person.full_name }}</h3>
                <p class="person-date">Registered {{ new Date(person.date_created).toLocaleDateString() }}</p>
              </div>
            </div>
            <button class="expand-btn" :class="{ expanded: expandedPersons.has(person.id) }">
              {{ expandedPersons.has(person.id) ? '▼' : '▶' }}
            </button>
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
                  <span>👤</span>
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
                <button @click="startEdit(person)" class="btn-edit">✏️ Edit</button>
                <button @click="deletePerson(person)" class="btn-delete">🗑️ Delete</button>
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
                    <button type="button" class="btn-camera" @click="openWebcamForEdit">📷 Capture New Photo</button>
                  </div>
                  
                  <div v-if="editPhotoPreview" class="edit-photo-preview">
                    <p class="preview-label">New Photo Preview:</p>
                    <img :src="editPhotoPreview" alt="New photo preview" />
                  </div>
                </div>
                
                <div class="edit-actions">
                  <button @click="updatePerson" class="btn-save">💾 Save Changes</button>
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
  </div>
</template>

<style scoped>
.person-registration {
  max-width: 1200px;
  margin: 0 auto;
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
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-select {
  background: #4CAF50;
  color: white;
}

.btn-select:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.btn-camera {
  background: #2196F3;
  color: white;
}

.btn-camera:hover {
  background: #0b7dda;
  transform: translateY(-2px);
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

.section-header h2 {
  font-size: 1.75rem;
  color: var(--text-primary);
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-toggle {
  padding: 0.5rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-toggle:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

.loading, .empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  background: white;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.persons-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.person-item {
  background: white;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
}

.person-item:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.person-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  cursor: pointer;
  transition: background 0.2s;
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
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.person-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 2rem;
  color: white;
}

.person-info h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  color: var(--text-primary);
}

.person-date {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.expand-btn {
  background: transparent;
  border: none;
  font-size: 1.25rem;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem 1rem;
  transition: all 0.2s;
}

.expand-btn:hover {
  color: var(--primary-color);
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
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit {
  background: #2196F3;
  color: white;
}

.btn-edit:hover {
  background: #0b7dda;
  transform: translateY(-2px);
}

.btn-delete {
  background: #f44336;
  color: white;
}

.btn-delete:hover {
  background: #da190b;
  transform: translateY(-2px);
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
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save {
  background: #4CAF50;
  color: white;
  flex: 1;
}

.btn-save:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.btn-cancel {
  background: var(--gray-200);
  color: var(--text-primary);
}

.btn-cancel:hover {
  background: var(--gray-300);
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