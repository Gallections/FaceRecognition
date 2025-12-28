<script setup lang="ts">
import { ref } from 'vue'

const isMobileMenuOpen = ref(false)

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
</script>

<template>
  <div class="app-container">
    <!-- Skip to main content for accessibility -->
    <a href="#main-content" class="skip-to-main">Skip to main content</a>
    
    <!-- Header -->
    <header class="header" role="banner">
      <div class="header-content">
        <div class="logo">
          <div class="logo-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2M12 11a4 4 0 100-8 4 4 0 000 8z"/>
            </svg>
          </div>
          <div class="logo-text">
            <h1>FaceRecognition</h1>
            <p>Attendance System</p>
          </div>
        </div>

        <!-- Desktop Navigation -->
        <nav class="desktop-nav" aria-label="Main navigation">
          <router-link to="/" class="nav-link">
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
            </span>
            <span>Home</span>
          </router-link>
          <router-link to="/file_import" class="nav-link">
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>
              </svg>
            </span>
            <span>People</span>
          </router-link>
          <router-link to="/recognize" class="nav-link">
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
            </span>
            <span>Recognize</span>
          </router-link>
          <router-link to="/attendance" class="nav-link">
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 11l3 3L22 4"/>
                <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
              </svg>
            </span>
            <span>Attendance</span>
          </router-link>
          <router-link to="/reports" class="nav-link">
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </span>
            <span>Reports</span>
          </router-link>
        </nav>

        <!-- Mobile Menu Button -->
        <button class="mobile-menu-btn" @click="toggleMobileMenu">
          <svg v-if="!isMobileMenuOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
          <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <!-- Mobile Navigation -->
      <nav v-if="isMobileMenuOpen" class="mobile-nav" aria-label="Mobile navigation">
        <router-link to="/" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </span>
          <span>Home</span>
        </router-link>
        <router-link to="/file_import" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>
            </svg>
          </span>
          <span>People</span>
        </router-link>
        <router-link to="/recognize" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="M21 21l-4.35-4.35"/>
            </svg>
          </span>
          <span>Recognize</span>
        </router-link>
        <router-link to="/attendance" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 11l3 3L22 4"/>
              <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
            </svg>
          </span>
          <span>Attendance</span>
        </router-link>
        <router-link to="/reports" class="nav-link" @click="toggleMobileMenu">
          <span class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="20" x2="18" y2="10"/>
              <line x1="12" y1="20" x2="12" y2="4"/>
              <line x1="6" y1="20" x2="6" y2="14"/>
            </svg>
          </span>
          <span>Reports</span>
        </router-link>
      </nav>
    </header>

    <!-- Main Content -->
    <main id="main-content" class="main-content" role="main">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer" role="contentinfo">
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
  background: var(--bg-dark);
  color: var(--text-inverse);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-4) var(--space-6);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-6);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.logo-icon {
  background: rgba(255, 255, 255, 0.08);
  padding: var(--space-2);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.logo-icon svg {
  color: rgba(255, 255, 255, 0.9);
}

.logo-text h1 {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-inverse);
  letter-spacing: -0.02em;
}

.logo-text p {
  font-size: var(--font-size-xs);
  color: rgba(255, 255, 255, 0.7);
  font-weight: var(--font-weight-normal);
}

.desktop-nav {
  display: flex;
  gap: var(--space-1);
}

.mobile-nav {
  display: none;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
  transition: all var(--transition-fast);
  background: transparent;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-inverse);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.12);
  color: var(--text-inverse);
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.85;
}

.nav-icon svg {
  color: currentColor;
  stroke-width: 2;
}

.nav-link:hover .nav-icon,
.nav-link.router-link-active .nav-icon {
  opacity: 1;
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
  padding: var(--space-8) var(--space-6);
}

.footer {
  background: var(--bg-primary);
  border-top: 1px solid var(--border-color);
  padding: var(--space-6);
  text-align: center;
  color: var(--text-tertiary);
}

.footer p {
  margin: 0;
  font-size: var(--font-size-sm);
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
    padding: var(--space-6) var(--space-4);
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
