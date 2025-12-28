<script setup lang="ts">
import { ref } from 'vue'

const isMobileMenuOpen = ref(false)

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
</script>

<template>
  <div class="app-container">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <div class="logo-icon">👤</div>
          <div class="logo-text">
            <h1>FaceRecognition</h1>
            <p>Attendance System</p>
          </div>
        </div>

        <!-- Desktop Navigation -->
        <nav class="desktop-nav">
          <router-link to="/" class="nav-link">
            <span class="nav-icon">🏠</span>
            <span>Home</span>
          </router-link>
          <router-link to="/file_import" class="nav-link">
            <span class="nav-icon">📤</span>
            <span>Upload</span>
          </router-link>
          <router-link to="/recognize" class="nav-link">
            <span class="nav-icon">🔍</span>
            <span>Recognize</span>
          </router-link>
          <router-link to="/attendance" class="nav-link">
            <span class="nav-icon">✓</span>
            <span>Attendance</span>
          </router-link>
          <router-link to="/reports" class="nav-link">
            <span class="nav-icon">📊</span>
            <span>Reports</span>
          </router-link>
        </nav>

        <!-- Mobile Menu Button -->
        <button class="mobile-menu-btn" @click="toggleMobileMenu">
          <span v-if="!isMobileMenuOpen">☰</span>
          <span v-else>✕</span>
        </button>
      </div>

      <!-- Mobile Navigation -->
      <nav v-if="isMobileMenuOpen" class="mobile-nav">
        <router-link to="/" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">🏠</span>
          <span>Home</span>
        </router-link>
        <router-link to="/file_import" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">📤</span>
          <span>Upload</span>
        </router-link>
        <router-link to="/recognize" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">🔍</span>
          <span>Recognize</span>
        </router-link>
        <router-link to="/attendance" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">✓</span>
          <span>Attendance</span>
        </router-link>
        <router-link to="/reports" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">📊</span>
          <span>Reports</span>
        </router-link>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <p>&copy; 2025 FaceRecognition Attendance System. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  font-size: 2.5rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.logo-text h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: white;
}

.logo-text p {
  font-size: 0.875rem;
  margin: 0;
  opacity: 0.9;
  color: white;
}

.desktop-nav {
  display: flex;
  gap: 0.5rem;
}

.mobile-nav {
  display: none;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
  background: rgba(255, 255, 255, 0.1);
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.25);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.nav-icon {
  font-size: 1.25rem;
}

.mobile-menu-btn {
  display: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.mobile-menu-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.main-content {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
}

.footer {
  background: var(--gray-800);
  color: var(--gray-300);
  text-align: center;
  padding: 2rem;
  margin-top: auto;
}

.footer p {
  margin: 0;
  font-size: 0.875rem;
}

@media (max-width: 1024px) {
  .desktop-nav {
    display: none;
  }

  .mobile-menu-btn {
    display: block;
  }

  .mobile-nav {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 1rem 2rem;
    background: rgba(0, 0, 0, 0.1);
  }

  .main-content {
    padding: 1rem;
  }
}

@media (max-width: 640px) {
  .header-content {
    padding: 1rem;
  }

  .logo-text h1 {
    font-size: 1.25rem;
  }

  .logo-text p {
    font-size: 0.75rem;
  }

  .logo-icon {
    font-size: 2rem;
  }
}
</style>
