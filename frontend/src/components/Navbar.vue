<template>
  <header class="header">
    <div class="header-inner">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <svg viewBox="0 0 120 40" class="logo-svg">
          <text x="0" y="30" font-size="28" font-weight="700" fill="#0093D0">FDA</text>
        </svg>
      </router-link>
      
      <!-- Main Navigation (PC) -->
      <nav class="main-nav">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link to="/letters" class="nav-link">警告信</router-link>
        <router-link to="/articles" class="nav-link">深度内容</router-link>
        <router-link to="/regulations" class="nav-link">法规信息</router-link>
        <router-link to="/news" class="nav-link">行业资讯</router-link>
        <router-link to="/dashboard" class="nav-link">数据看板</router-link>
        <router-link to="/favorites" class="nav-link nav-favorites">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
          </svg>
          收藏
          <span v-if="favoritesCount > 0" class="favorites-badge">{{ favoritesCount }}</span>
        </router-link>
      </nav>
      
      <!-- Right Navigation (PC) -->
      <div class="header-right">
        <button class="search-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          搜索
        </button>
      </div>
      
      <!-- Mobile Menu Toggle -->
      <button class="mobile-toggle" @click="toggleMobileMenu">
        <span :class="{ open: mobileMenuOpen }"></span>
        <span :class="{ open: mobileMenuOpen }"></span>
        <span :class="{ open: mobileMenuOpen }"></span>
      </button>
    </div>
    
    <!-- Mobile Menu -->
    <div class="mobile-menu" :class="{ open: mobileMenuOpen }">
      <nav class="mobile-nav">
        <router-link to="/" class="mobile-nav-link" @click="closeMobileMenu">首页</router-link>
        <router-link to="/letters" class="mobile-nav-link" @click="closeMobileMenu">警告信</router-link>
        <router-link to="/articles" class="mobile-nav-link" @click="closeMobileMenu">深度内容</router-link>
        <router-link to="/regulations" class="mobile-nav-link" @click="closeMobileMenu">法规信息</router-link>
        <router-link to="/news" class="mobile-nav-link" @click="closeMobileMenu">行业资讯</router-link>
        <router-link to="/dashboard" class="mobile-nav-link" @click="closeMobileMenu">数据看板</router-link>
        <router-link to="/favorites" class="mobile-nav-link" @click="closeMobileMenu">
          <span class="flex items-center gap-2">
            收藏
            <span v-if="favoritesCount > 0" class="favorites-badge">{{ favoritesCount }}</span>
          </span>
        </router-link>
      </nav>
      <div class="mobile-menu-footer">
        <button class="mobile-search-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          搜索
        </button>
      </div>
    </div>
    
    <!-- Overlay -->
    <div class="mobile-overlay" :class="{ open: mobileMenuOpen }" @click="closeMobileMenu"></div>
  </header>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useFavorites } from '../composables/useFavorites.js'

const route = useRoute()
const mobileMenuOpen = ref(false)
const { favoritesCount } = useFavorites()

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

// 路由变化时关闭菜单
watch(() => route.path, () => {
  closeMobileMenu()
})
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.logo-svg {
  height: 32px;
  width: auto;
}

/* Main Navigation */
.main-nav {
  display: flex;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  font-size: 15px;
  font-weight: 500;
  color: #1a1a2e;
  text-decoration: none;
  transition: color 0.2s;
  border-radius: 6px;
}

.nav-link:hover {
  color: #0093D0;
  background: #f0f7ff;
}

.nav-favorites {
  position: relative;
  gap: 6px;
}

.favorites-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  background: #ef4444;
  color: white;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

/* Header Right */
.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.search-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #0093D0;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.search-btn svg {
  width: 18px;
  height: 18px;
}

.search-btn:hover {
  background: #0077b3;
}

/* Mobile Toggle */
.mobile-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  z-index: 1001;
}

.mobile-toggle span {
  width: 24px;
  height: 2px;
  background: #1a1a2e;
  transition: all 0.3s;
  transform-origin: center;
}

.mobile-toggle span.open:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.mobile-toggle span.open:nth-child(2) {
  opacity: 0;
}

.mobile-toggle span.open:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* Mobile Menu */
.mobile-menu {
  position: fixed;
  top: 72px;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  z-index: 999;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
}

.mobile-menu.open {
  transform: translateX(0);
}

.mobile-nav {
  flex: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  padding: 16px;
  font-size: 18px;
  font-weight: 500;
  color: #1a1a2e;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
}

.mobile-nav-link:hover {
  background: #f0f7ff;
  color: #0093D0;
}

.mobile-menu-footer {
  padding: 24px;
  border-top: 1px solid #e5e7eb;
}

.mobile-search-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 20px;
  background: #0093D0;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
}

.mobile-search-btn svg {
  width: 20px;
  height: 20px;
}

/* Overlay */
.mobile-overlay {
  position: fixed;
  top: 72px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 998;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
}

.mobile-overlay.open {
  opacity: 1;
  visibility: visible;
}

/* Responsive */
@media (max-width: 1024px) {
  .header-inner {
    padding: 0 16px;
  }
  
  .main-nav {
    display: none;
  }
  
  .mobile-toggle {
    display: flex;
  }
  
  .header-right {
    display: none;
  }
}

@media (min-width: 1025px) {
  .mobile-menu,
  .mobile-overlay {
    display: none;
  }
}
</style>
