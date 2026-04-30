<template>
  <header class="pf-header" :class="{ scrolled: isScrolled }">
    <!-- Top utility bar -->
    <div class="pf-utility-bar">
      <div class="pf-container">
        <div class="pf-utility-inner">
          <span class="pf-utility-link">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>
            中文
          </span>
          <span class="pf-utility-divider">|</span>
          <a href="https://www.fda.gov" target="_blank" class="pf-utility-link">FDA.gov</a>
        </div>
      </div>
    </div>

    <!-- Main header -->
    <div class="pf-header-main">
      <div class="pf-container">
        <div class="pf-header-inner">
          <!-- Logo -->
          <router-link to="/" class="pf-logo">
            <svg viewBox="0 0 200 50" class="pf-logo-svg">
              <rect x="0" y="8" width="34" height="34" rx="4" fill="#0000C9"/>
              <text x="42" y="24" font-size="14" font-weight="700" fill="#0000C9" font-family="Noto Sans, Arial, sans-serif">FDA</text>
              <text x="42" y="40" font-size="10" font-weight="400" fill="#333" font-family="Noto Sans, Arial, sans-serif">警告信智能平台</text>
            </svg>
          </router-link>

          <!-- Desktop Navigation -->
          <nav class="pf-nav">
            <router-link to="/" class="pf-nav-link" :class="{ active: $route.path === '/' }">首页</router-link>
            <div class="pf-nav-dropdown" @mouseenter="activeDropdown = 'science'" @mouseleave="activeDropdown = null">
              <router-link to="/letters" class="pf-nav-link" :class="{ active: $route.path.startsWith('/letters') }">
                警告信
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
              </router-link>
              <div class="pf-dropdown" v-show="activeDropdown === 'science'">
                <router-link to="/letters" class="pf-dropdown-item">全部警告信</router-link>
                <router-link to="/letters" class="pf-dropdown-item">高风险企业</router-link>
                <router-link to="/letters" class="pf-dropdown-item">最新发布</router-link>
                <router-link to="/letters" class="pf-dropdown-item">按签发办公室</router-link>
              </div>
            </div>
            <router-link to="/dashboard" class="pf-nav-link" :class="{ active: $route.path === '/dashboard' }">数据看板</router-link>
            <div class="pf-nav-dropdown" @mouseenter="activeDropdown = 'news'" @mouseleave="activeDropdown = null">
              <a href="#" class="pf-nav-link" :class="{ active: $route.path.startsWith('/articles') || $route.path.startsWith('/news') }" @click.prevent>
                新闻与洞察
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
              </a>
              <div class="pf-dropdown" v-show="activeDropdown === 'news'">
                <router-link to="/articles" class="pf-dropdown-item">深度内容</router-link>
                <router-link to="/news" class="pf-dropdown-item">行业资讯</router-link>
                <router-link to="/regulations" class="pf-dropdown-item">法规信息</router-link>
              </div>
            </div>
            <router-link to="/favorites" class="pf-nav-link" :class="{ active: $route.path === '/favorites' }">
              收藏
              <span v-if="favoritesCount > 0" class="pf-nav-badge">{{ favoritesCount }}</span>
            </router-link>
          </nav>

          <!-- Right actions -->
          <div class="pf-header-actions">
            <router-link to="/letters" class="pf-btn pf-btn-primary">开始探索</router-link>
          </div>

          <!-- Mobile toggle -->
          <button class="pf-mobile-toggle" @click="toggleMobile" :class="{ open: mobileOpen }">
            <span></span><span></span><span></span>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div class="pf-mobile-menu" :class="{ open: mobileOpen }">
      <div class="pf-mobile-inner">
        <router-link to="/" class="pf-mobile-link" @click="closeMobile">首页</router-link>
        <router-link to="/letters" class="pf-mobile-link" @click="closeMobile">警告信</router-link>
        <router-link to="/dashboard" class="pf-mobile-link" @click="closeMobile">数据看板</router-link>
        <router-link to="/articles" class="pf-mobile-link" @click="closeMobile">深度内容</router-link>
        <router-link to="/news" class="pf-mobile-link" @click="closeMobile">行业资讯</router-link>
        <router-link to="/regulations" class="pf-mobile-link" @click="closeMobile">法规信息</router-link>
        <router-link to="/favorites" class="pf-mobile-link" @click="closeMobile">
          收藏
          <span v-if="favoritesCount > 0" class="pf-nav-badge">{{ favoritesCount }}</span>
        </router-link>
        <div class="pf-mobile-cta">
          <router-link to="/letters" class="pf-btn pf-btn-primary pf-btn-block" @click="closeMobile">开始探索</router-link>
        </div>
      </div>
    </div>
    <div class="pf-mobile-overlay" v-show="mobileOpen" @click="closeMobile"></div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useFavorites } from '../composables/useFavorites.js'

const route = useRoute()
const { favoritesCount } = useFavorites()
const isScrolled = ref(false)
const mobileOpen = ref(false)
const activeDropdown = ref(null)

const handleScroll = () => { isScrolled.value = window.scrollY > 10 }
onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))

function toggleMobile() { mobileOpen.value = !mobileOpen.value }
function closeMobile() { mobileOpen.value = false }

watch(() => route.path, () => closeMobile())
</script>

<style scoped>
.pf-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: #fff;
}

/* Utility bar */
.pf-utility-bar {
  background: #f5f5f5;
  border-bottom: 1px solid #e5e7eb;
  padding: 6px 0;
  font-size: 12px;
}

.pf-utility-inner {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-end;
}

.pf-utility-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #666;
  text-decoration: none;
  transition: color 0.2s;
}

a.pf-utility-link:hover { color: #0000C9; }

.pf-utility-divider { color: #ccc; }

/* Main header */
.pf-header-main {
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  transition: box-shadow 0.3s;
}

.pf-header.scrolled .pf-header-main {
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.pf-header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  gap: 24px;
}

/* Logo */
.pf-logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  flex-shrink: 0;
}

.pf-logo-svg {
  height: 40px;
  width: auto;
}

/* Navigation */
.pf-nav {
  display: flex;
  align-items: center;
  gap: 0;
}

.pf-nav-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 24px 16px;
  font-size: 15px;
  font-weight: 500;
  color: #333;
  text-decoration: none;
  transition: color 0.2s;
  position: relative;
  white-space: nowrap;
}

.pf-nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 16px;
  right: 16px;
  height: 3px;
  background: #0000C9;
  transform: scaleX(0);
  transition: transform 0.2s;
}

.pf-nav-link:hover,
.pf-nav-link.active {
  color: #0000C9;
}

.pf-nav-link:hover::after,
.pf-nav-link.active::after {
  transform: scaleX(1);
}

.pf-nav-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  background: #dc2626;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  border-radius: 9px;
}

/* Dropdown */
.pf-nav-dropdown { position: relative; }

.pf-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 200px;
  background: #fff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 10px 40px rgba(0,0,0,0.12);
  border-radius: 0 0 4px 4px;
  padding: 8px 0;
  z-index: 100;
}

.pf-dropdown-item {
  display: block;
  padding: 10px 20px;
  font-size: 14px;
  color: #333;
  text-decoration: none;
  transition: all 0.15s;
}

.pf-dropdown-item:hover {
  background: #F2F9FC;
  color: #0000C9;
}

/* Header actions */
.pf-header-actions { display: flex; align-items: center; gap: 12px; }

/* Buttons */
.pf-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
  white-space: nowrap;
}

.pf-btn-primary {
  background: #0000C9;
  color: #fff;
}

.pf-btn-primary:hover {
  background: #0000A3;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,201,0.3);
}

.pf-btn-block { width: 100%; }

/* Mobile toggle */
.pf-mobile-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  z-index: 1001;
}

.pf-mobile-toggle span {
  display: block;
  width: 24px;
  height: 2px;
  background: #000;
  transition: all 0.3s;
  transform-origin: center;
}

.pf-mobile-toggle.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.pf-mobile-toggle.open span:nth-child(2) { opacity: 0; }
.pf-mobile-toggle.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

/* Mobile menu */
.pf-mobile-menu {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #fff;
  z-index: 999;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  overflow-y: auto;
  padding-top: 120px;
}

.pf-mobile-menu.open { transform: translateX(0); }

.pf-mobile-inner { padding: 24px; }

.pf-mobile-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 0;
  font-size: 18px;
  font-weight: 500;
  color: #333;
  text-decoration: none;
  border-bottom: 1px solid #f0f0f0;
  transition: color 0.2s;
}

.pf-mobile-link:hover { color: #0000C9; }

.pf-mobile-cta { margin-top: 24px; }

.pf-mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 998;
}

/* Container */
.pf-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
}

/* Responsive */
@media (max-width: 1024px) {
  .pf-nav, .pf-header-actions { display: none; }
  .pf-mobile-toggle { display: flex; }
  .pf-container { padding: 0 16px; }
  .pf-utility-bar { display: none; }
  .pf-header-inner { height: 60px; }
  .pf-mobile-menu { padding-top: 60px; }
}

@media (min-width: 1025px) {
  .pf-mobile-menu, .pf-mobile-overlay { display: none !important; }
}
</style>
