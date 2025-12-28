<script setup lang="ts">
import { ref } from 'vue'
import { apiService, type FaceRecognitionResponse } from '../services/apiService'
import WebcamCapture from './WebcamCapture.vue'

const imagePreview = ref<string>('')
const imageInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const isRecognizing = ref(false)
const recognitionResult = ref<FaceRecognitionResponse | null>(null)
const showWebcam = ref(false)
const webcamMode = ref<'capture' | 'realtime'>('capture')

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
    recognitionResult.value = null // Clear previous result
  }
}

function triggerFileUpload() {
  imageInput.value?.click()
}

async function recognizeFace() {
  if (!selectedFile.value) {
    window.alert('Please select an image first!')
    return
  }

  isRecognizing.value = true
  recognitionResult.value = null

  try {
    const result = await apiService.recognizeFace(selectedFile.value)
    recognitionResult.value = result

    if (result.success && result.full_name) {
      window.alert(`✅ Recognized: ${result.full_name}\nConfidence: ${(result.confidence! * 100).toFixed(1)}%`)
    } else {
      window.alert(`❌ ${result.message}`)
    }
  } catch (error: any) {
    window.alert(`Error: ${error.message}`)
  } finally {
    isRecognizing.value = false
  }
}

function clearInput() {
  imagePreview.value = ''
  selectedFile.value = null
  recognitionResult.value = null
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
    const result = await apiService.recognizeFace(file)
    return result
  } catch (error: any) {
    console.error('Real-time detection error:', error)
    return { success: false, message: error.message }
  }
}

function handleDetectionResult(result: FaceRecognitionResponse) {
  recognitionResult.value = result
  
  if (result.success && result.full_name) {
    // Show brief notification
    console.log(`Detected: ${result.full_name}`)
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
  
  // Auto-recognize
  await recognizeFace()
}
</script>

<template>
  <div class="face-recognition">
    <h2>Face Recognition</h2>
    <p class="subtitle">Upload a photo or use your camera to identify who it is</p>

    <input
      type="file"
      ref="imageInput"
      @change="handleFileUpload"
      accept="image/*"
      style="display: none"
    />

    <div class="button-group">
      <button @click="triggerFileUpload" class="btn-select">
        📁 Select Image
      </button>
      <button @click="openWebcam" class="btn-camera">
        📷 Capture Photo
      </button>
      <button @click="openRealtimeDetection" class="btn-realtime">
        🎥 Real-time Detection
      </button>
    </div>

    <div v-if="imagePreview" class="preview-container">
      <h3>Image Preview</h3>
      <img :src="imagePreview" alt="Preview" class="image-preview" />

      <div class="action-buttons">
        <button @click="recognizeFace" :disabled="isRecognizing" class="btn-recognize">
          {{ isRecognizing ? '🔍 Recognizing...' : '🔍 Recognize Face' }}
        </button>
        <button @click="clearInput" class="btn-clear">Clear</button>
      </div>

      <!-- Recognition Result -->
      <div v-if="recognitionResult" class="result-card">
        <div v-if="recognitionResult.success" class="result-success">
          <h3>✅ Recognition Successful!</h3>
          <div class="result-details">
            <p><strong>Person:</strong> {{ recognitionResult.full_name }}</p>
            <p><strong>Person ID:</strong> {{ recognitionResult.person_id }}</p>
            <p><strong>Confidence:</strong> {{ (recognitionResult.confidence! * 100).toFixed(2) }}%</p>
          </div>
        </div>
        <div v-else class="result-failure">
          <h3>❌ Recognition Failed</h3>
          <p>{{ recognitionResult.message }}</p>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>👆 Click "Select Image" to upload a photo or "Use Camera" to capture live</p>
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
.face-recognition {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

h2 {
  margin-bottom: 0.5rem;
  color: #333;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.btn-select {
  background: #4CAF50;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1rem;
  flex: 1;
  min-width: 200px;
}

.btn-select:hover {
  background: #45a049;
}

.btn-camera {
  background: #2196F3;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1rem;
  flex: 1;
  min-width: 200px;
}

.btn-camera:hover {
  background: #0b7dda;
}

.btn-realtime {
  background: #10b981;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1rem;
  flex: 1;
  min-width: 200px;
}

.btn-realtime:hover {
  background: #059669;
}

.preview-container {
  background: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
}

h3 {
  margin-bottom: 1rem;
  color: #333;
}

.image-preview {
  max-width: 100%;
  max-height: 500px;
  display: block;
  margin: 0 auto 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.btn-recognize {
  background: #2196F3;
  color: white;
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
}

.btn-recognize:hover:not(:disabled) {
  background: #0b7dda;
}

.btn-recognize:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-clear {
  background: #f44336;
  color: white;
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-clear:hover {
  background: #da190b;
}

.result-card {
  margin-top: 2rem;
  padding: 1.5rem;
  border-radius: 8px;
}

.result-success {
  background: #e8f5e9;
  border: 2px solid #4CAF50;
  padding: 1rem;
  border-radius: 8px;
}

.result-success h3 {
  color: #2e7d32;
  margin-bottom: 1rem;
}

.result-details p {
  margin: 0.5rem 0;
  font-size: 1.1rem;
  color: #333;
}

.result-failure {
  background: #ffebee;
  border: 2px solid #f44336;
  padding: 1rem;
  border-radius: 8px;
}

.result-failure h3 {
  color: #c62828;
  margin-bottom: 1rem;
}

.result-failure p {
  color: #666;
  font-size: 1rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #999;
  font-size: 1.2rem;
  background: #f9f9f9;
  border-radius: 8px;
  border: 2px dashed #ddd;
}
</style>
