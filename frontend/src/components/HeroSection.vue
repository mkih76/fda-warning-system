<template>
  <section class="hero">
    <div class="hero-content">
      <!-- 标签 -->
      <div class="hero-badge">
        <span class="badge-icon">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
        </span>
        <span>FDA Warning Letter Intelligence</span>
      </div>
      
      <!-- 主标题 -->
      <h1 class="hero-headline">
        FDA 警告信<br>
        <span class="accent">智能监控平台</span>
      </h1>
      
      <p class="hero-sub">
        实时同步 FDA 官方数据，AI 驱动的智能翻译与深度分析，<br>
        为企业合规提供全方位监控与预警服务
      </p>
      
      <!-- CTA按钮 -->
      <div class="hero-cta">
        <router-link to="/letters" class="cta-primary">
          浏览警告信
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 8l4 4m0 0l-4 4m4-4H3"/>
          </svg>
        </router-link>
        <router-link to="/dashboard" class="cta-secondary">
          数据看板
        </router-link>
      </div>
      
      <!-- 统计数据 -->
      <div class="hero-stats">
        <div class="stat-item">
          <span class="stat-value">986+</span>
          <span class="stat-label">警告信数据</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">100%</span>
          <span class="stat-label">中文翻译</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">AI</span>
          <span class="stat-label">智能分析</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.hero {
  position: relative;
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(180deg, #F0F7FF 0%, #FFFFFF 100%);
  padding-top: 72px;
}

.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 0 24px;
  max-width: 900px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 24px;
  background: rgba(var(--accent-rgb), 0.1);
  font-size: 13px;
  font-weight: 500;
  color: var(--accent);
  margin-bottom: 32px;
}

.badge-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
}

.hero-headline {
  font-size: clamp(42px, 8vw, 72px);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.1;
  color: var(--text);
  margin-bottom: 24px;
}

.accent {
  color: var(--accent);
}

.hero-sub {
  font-size: clamp(16px, 2vw, 19px);
  line-height: 1.7;
  color: var(--text-2);
  margin-bottom: 40px;
  max-width: 640px;
  margin-left: auto;
  margin-right: auto;
}

.hero-cta {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 64px;
}

.cta-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  background: var(--accent);
  color: white;
  font-size: 16px;
  font-weight: 600;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
}

.cta-primary:hover {
  background: var(--accent-dark);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--accent-rgb), 0.3);
}

.cta-secondary {
  display: inline-flex;
  align-items: center;
  padding: 16px 32px;
  border: 2px solid var(--border);
  color: var(--text);
  font-size: 16px;
  font-weight: 600;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
  background: white;
}

.cta-secondary:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.hero-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 48px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 36px;
  font-weight: 800;
  color: var(--accent);
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: 14px;
  color: var(--text-3);
  margin-top: 4px;
}

.stat-divider {
  width: 1px;
  height: 48px;
  background: var(--border);
}

@media (max-width: 640px) {
  .hero-stats { gap: 24px; }
  .stat-value { font-size: 28px; }
  .cta-primary, .cta-secondary { padding: 14px 24px; font-size: 15px; }
}
</style>
