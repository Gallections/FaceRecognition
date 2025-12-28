<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{
  mode?: 'capture' | 'realtime'
  onDetect?: (imageBlob: Blob) => Promise<any>
}>()

const emit = defineEmits<{
  (e: 'capture', imageBlob: Blob): void
  (e: 'detected', result: any): void
  (e: 'close'): void
}>()

const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const stream = ref<MediaStream | null>(null)
const isActive = ref(false)
const error = ref<string>('')
const isDetecting = ref(false)
const detectionResult = ref<any>(null)
const detectionInterval = ref<number | null>(null)

onMounted(async () => {
  await startCamera()
})

onBeforeUnmount(() => {
  stopCamera()
  stopDetection()
})

async function startCamera() {
  try {
    stream.value = await navigator.mediaDevices.getUserMedia({ 
      video: { 
        width: { ideal: 1280 },
        height: { ideal: 720 },
        facingMode: 'user'
      } 
    })
    
    if (videoRef.value) {
      videoRef.value.srcObject = stream.value
      isActive.value = true
      
      // Auto-start real-time detection if in realtime mode
      if (props.mode === 'realtime') {
        await videoRef.value.play()
        startRealtimeDetection()
      }
    }
  } catch (err: any) {
    error.value = 'Failed to access camera. Please ensure camera permissions are granted.'
    console.error('Camera error:', err)
  }
}

function stopCamera() {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
    isActive.value = false
  }
}

function startRealtimeDetection() {
  if (detectionInterval.value) return
  
  isDetecting.value = true
  // Detect every 2 seconds to avoid overwhelming the API
  detectionInterval.value = window.setInterval(async () => {
    await detectFrame()
  }, 2000)
}

function stopDetection() {
  if (detectionInterval.value) {
    clearInterval(detectionInterval.value)
    detectionInterval.value = null
  }
  isDetecting.value = false
  detectionResult.value = null
}

async function detectFrame() {
  if (!videoRef.value || !canvasRef.value || !props.onDetect) return

  const video = videoRef.value
  const canvas = canvasRef.value
  
  // Set canvas dimensions to match video
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  
  // Draw current video frame to canvas
  const ctx = canvas.getContext('2d')
  if (ctx) {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    // Convert canvas to blob
    canvas.toBlob(async (blob) => {
      if (blob) {
        try {
          const result = await props.onDetect!(blob)
          detectionResult.value = result
          emit('detected', result)
        } catch (err) {
          console.error('Detection error:', err)
        }
      }
    }, 'image/jpeg', 0.85)
  }
}

async function capturePhoto() {
  if (!videoRef.value || !canvasRef.value) return

  const video = videoRef.value
  const canvas = canvasRef.value
  
  // Set canvas dimensions to match video
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  
  // Draw current video frame to canvas
  const ctx = canvas.getContext('2d')
  if (ctx) {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    // Convert canvas to blob
    canvas.toBlob((blob) => {
      if (blob) {
        emit('capture', blob)
        stopCamera()
        stopDetection()
      }
    }, 'image/jpeg', 0.95)
  }
}

function close() {
  stopCamera()
  stopDetection()
  emit('close')
}
</script>

<template>
  <div class="webcam-modal">
    <div class="webcam-overlay" @click="close"></div>
    
    <div class="webcam-container">
      <div class="webcam-header">
        <h3 id="webcam-title">{{ mode === 'realtime' ? '🎥 Real-time Detection' : '📷 Camera Capture' }}</h3>
        <button 
          @click="close" 
          class="btn-close"
          aria-label="Close camera"
        >✕</button>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-else class="webcam-content">
        <div class="video-container">
          <video 
            ref="videoRef" 
            autoplay 
            playsinline
            class="webcam-video"
            aria-label="Live camera feed"
          ></video>
          
          <!-- Real-time Detection Overlay -->
          <div v-if="mode === 'realtime' && detectionResult" class="detection-overlay">
            <div v-if="detectionResult.success" class="detection-success">
              <div class="detection-badge">
                <span class="badge-icon">✓</span>
                <div class="badge-info">
                  <strong>{{ detectionResult.full_name || detectionResult.person?.full_name }}</strong>
                  <span v-if="detectionResult.confidence" class="confidence">
                    {{ Math.round(detectionResult.confidence * 100) }}% confidence
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="detection-fail">
              <div class="detection-badge fail">
                <span class="badge-icon">✗</span>
                <span>{{ detectionResult.message || 'No face detected' }}</span>
              </div>
            </div>
          </div>

          <!-- Real-time Status Indicator -->
          <div v-if="mode === 'realtime'" class="status-indicator">
            <span class="status-dot" :class="{ active: isDetecting }"></span>
            <span class="status-text">{{ isDetecting ? 'Detecting...' : 'Paused' }}</span>
          </div>
        </div>
        
        <canvas ref="canvasRef" style="display: none;"></canvas>

        <div class="webcam-controls">
          <button 
            v-if="mode === 'capture'" 
            @click="capturePhoto" 
            :disabled="!isActive" 
            class="btn-capture"
            aria-label="Capture photo from camera"
          >
            📸 Capture Photo
          </button>
          <button 
            v-else-if="isDetecting" 
            @click="stopDetection" 
            class="btn-pause"
            aria-label="Pause real-time detection"
          >
            ⏸ Pause Detection
          </button>
          <button 
            v-else 
            @click="startRealtimeDetection" 
            class="btn-resume"
            aria-label="Resume real-time detection"
          >
            ▶ Resume Detection
          </button>
          <button 
            @click="close" 
            class="btn-cancel"
            aria-label="Close camera and cancel"
          >
            Close
          </button>
        </div>

        <p class="webcam-hint">
          {{ mode === 'realtime' 
            ? 'Detection runs automatically every 2 seconds' 
            : 'Position your face in the center and click Capture' 
          }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.webcam-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.webcam-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
}

.webcam-container {
  position: relative;
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.webcam-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 2px solid var(--border-color);
  background: var(--bg-secondary);
}

.webcam-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-primary);
}

.btn-close {
  background: transparent;
  color: var(--text-secondary);
  font-size: 1.5rem;
  padding: 0.25rem 0.5rem;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-close:hover {
  color: var(--danger-color);
}

.error-message {
  padding: 2rem;
  text-align: center;
  color: var(--danger-color);
  background: #ffebee;
  margin: 1rem;
  border-radius: 8px;
}

.webcam-content {
  padding: 1.5rem;
}

.video-container {
  position: relative;
  margin-bottom: 1.5rem;
}

.webcam-video {
  width: 100%;
  max-height: 500px;
  border-radius: 12px;
  background: #000;
  display: block;
}

.detection-overlay {
  position: absolute;
  top: 1rem;
  left: 1rem;
  right: 1rem;
  pointer-events: none;
}

.detection-badge {
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  padding: 1rem 1.5rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: slideIn 0.3s ease;
}

.detection-badge.fail {
  background: rgba(239, 68, 68, 0.9);
}

.detection-success .detection-badge {
  background: rgba(16, 185, 129, 0.9);
}

.badge-icon {
  font-size: 2rem;
  color: white;
}

.badge-info {
  display: flex;
  flex-direction: column;
  color: white;
}

.badge-info strong {
  font-size: 1.25rem;
  margin-bottom: 0.25rem;
}

.confidence {
  font-size: 0.9rem;
  opacity: 0.9;
}

.status-indicator {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  font-size: 0.9rem;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--gray-400);
  animation: pulse 2s infinite;
}

.status-dot.active {
  background: #10b981;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.webcam-controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 1rem;
}

.btn-capture {
  background: var(--primary-color);
  color: white;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-capture:hover:not(:disabled) {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-pause {
  background: #f59e0b;
  color: white;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-pause:hover {
  background: #d97706;
  transform: translateY(-2px);
}

.btn-resume {
  background: #10b981;
  color: white;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-resume:hover {
  background: #059669;
  transform: translateY(-2px);
}

.btn-capture:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancel {
  background: var(--gray-200);
  color: var(--text-primary);
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: var(--gray-300);
}

.webcam-hint {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin: 0;
}

@media (max-width: 640px) {
  .webcam-container {
    width: 100%;
    max-height: 100vh;
    border-radius: 0;
  }

  .webcam-video {
    max-height: 400px;
  }

  .webcam-controls {
    flex-direction: column;
  }

  .btn-capture, .btn-cancel {
    width: 100%;
  }
}
</style>
