<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '../services/apiService'

const router = useRouter()
const stats = ref({
  totalPersons: 0,
  todayAttendance: 0,
  isLoading: true
})

onMounted(async () => {
  try {
    const [persons, attendance] = await Promise.all([
      apiService.getAllPersons(),
      apiService.getTodayAttendance()
    ])
    stats.value = {
      totalPersons: persons.length,
      todayAttendance: attendance.length,
      isLoading: false
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
    stats.value.isLoading = false
  }
})

function navigateTo(path: string) {
  router.push(path)
}
</script>

<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">Welcome to FaceRecognition Attendance</h1>
        <p class="hero-subtitle">
          Streamline your attendance tracking with cutting-edge facial recognition technology.
          Fast, accurate, and secure.
        </p>
        <div class="hero-actions">
          <button 
            @click="navigateTo('/attendance')" 
            class="btn-primary"
            aria-label="Go to attendance marking page"
          >
            <span>✓</span>
            Mark Attendance
          </button>
          <button 
            @click="navigateTo('/file_import')" 
            class="btn-secondary"
            aria-label="Go to person registration page"
          >
            <span>📤</span>
            Register New Person
          </button>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <p class="stat-label">Total Registered</p>
          <h2 class="stat-value">{{ stats.isLoading ? '...' : stats.totalPersons }}</h2>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✓</div>
        <div class="stat-info">
          <p class="stat-label">Present Today</p>
          <h2 class="stat-value">{{ stats.isLoading ? '...' : stats.todayAttendance }}</h2>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <p class="stat-label">Attendance Rate</p>
          <h2 class="stat-value">
            {{ stats.isLoading ? '...' : stats.totalPersons > 0 ? Math.round((stats.todayAttendance / stats.totalPersons) * 100) : 0 }}%
          </h2>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <h2 class="section-title">Key Features</h2>
      <div class="features-grid">
        <div 
          class="feature-card" 
          @click="navigateTo('/recognize')"
          @keypress.enter="navigateTo('/recognize')"
          @keypress.space="navigateTo('/recognize')"
          tabindex="0"
          role="button"
          aria-label="Go to face recognition page"
        >
          <div class="feature-icon">🔍</div>
          <h3>Face Recognition</h3>
          <p>Instantly identify individuals from photos with high accuracy</p>
        </div>
        
        <div 
          class="feature-card" 
          @click="navigateTo('/attendance')"
          @keypress.enter="navigateTo('/attendance')"
          @keypress.space="navigateTo('/attendance')"
          tabindex="0"
          role="button"
          aria-label="Go to attendance dashboard"
        >
          <div class="feature-icon">⏱️</div>
          <h3>Real-time Tracking</h3>
          <p>Mark attendance instantly with facial recognition or manual entry</p>
        </div>
        
        <div 
          class="feature-card" 
          @click="navigateTo('/reports')"
          @keypress.enter="navigateTo('/reports')"
          @keypress.space="navigateTo('/reports')"
          tabindex="0"
          role="button"
          aria-label="Go to reports and analytics page"
        >
          <div class="feature-icon">📈</div>
          <h3>Detailed Reports</h3>
          <p>Export attendance records and view comprehensive analytics</p>
        </div>
        
        <div 
          class="feature-card" 
          @click="navigateTo('/persons')"
          @keypress.enter="navigateTo('/persons')"
          @keypress.space="navigateTo('/persons')"
          tabindex="0"
          role="button"
          aria-label="Go to person management page"
        >
          <div class="feature-icon">⚙️</div>
          <h3>Easy Management</h3>
          <p>Add, edit, or remove persons from the system with ease</p>
        </div>
      </div>
    </section>

    <!-- Quick Actions -->
    <section class="quick-actions">
      <h2 class="section-title">Quick Actions</h2>
      <div class="actions-grid">
        <button 
          @click="navigateTo('/file_import')" 
          class="action-btn"
          aria-label="Upload new person image"
        >
          <span class="action-icon">📤</span>
          <span class="action-text">Upload New Image</span>
        </button>
        <button 
          @click="navigateTo('/recognize')" 
          class="action-btn"
          aria-label="Recognize face from image"
        >
          <span class="action-icon">🔍</span>
          <span class="action-text">Recognize Face</span>
        </button>
        <button 
          @click="navigateTo('/attendance')" 
          class="action-btn"
          aria-label="View attendance records"
        >
          <span class="action-icon">✓</span>
          <span class="action-text">View Attendance</span>
        </button>
        <button 
          @click="navigateTo('/reports')" 
          class="action-btn"
          aria-label="Export attendance reports"
        >
          <span class="action-icon">📊</span>
          <span class="action-text">Export Reports</span>
        </button>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
  margin-bottom: 3rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: white;
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.95;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary {
  background: white;
  color: #667eea;
  font-weight: 600;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 600;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  border-radius: 8px;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border: 1px solid var(--border-color);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
  color: var(--text-primary);
}

.features {
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--border-color);
  text-align: center;
  transition: all 0.3s;
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-color);
}

.feature-card:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

.feature-card:focus:not(:focus-visible) {
  outline: none;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.feature-card p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}

.quick-actions {
  margin-bottom: 3rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-btn {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 2px solid var(--border-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.2s;
  color: var(--text-primary);
}

.action-btn:hover {
  border-color: var(--primary-color);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

.action-btn:hover .action-icon {
  transform: scale(1.1);
}

.action-btn:hover .action-text {
  color: white;
}

.action-icon {
  font-size: 2rem;
}

.action-text {
  font-weight: 600;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
