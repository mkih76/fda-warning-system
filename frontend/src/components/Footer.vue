<template>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <!-- 品牌 -->
        <div class="footer-brand">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">
              <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </div>
          <div class="brand-text">
            <span class="brand-name">FDA 警告信平台</span>
            <span class="brand-desc">FDA Warning Letter Intelligence</span>
          </div>
        </div>

        <!-- 链接 -->
        <div class="footer-links">
          <div class="link-group">
            <h4 class="link-title">功能</h4>
            <router-link to="/letters" class="link">警告信列表</router-link>
            <router-link to="/dashboard" class="link">数据看板</router-link>
          </div>
          <div class="link-group">
            <h4 class="link-title">资源</h4>
            <a href="https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters" target="_blank" class="link">FDA 官方数据</a>
            <span class="link status-link">
              <span class="status-dot"></span>
              系统运行中
            </span>
          </div>
        </div>
      </div>

      <!-- 底部 -->
      <div class="footer-bottom">
        <p class="footer-copy">
          数据来源：<a href="https://www.fda.gov" target="_blank" rel="noopener">FDA.gov</a> — 美国联邦政府公共领域数据
        </p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--accent-darker);
  padding: 64px 32px 32px;
}

.footer-inner {
  max-width: 1280px;
  margin: 0 auto;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 48px;
  margin-bottom: 48px;
}

@media (min-width: 640px) {
  .footer-grid {
    grid-template-columns: 2fr 1fr 1fr;
  }
}

.footer-brand {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: white;
  color: var(--accent-darker);
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.brand-name {
  font-size: 18px;
  font-weight: 700;
  color: white;
}

.brand-desc {
  font-size: 13px;
  color: rgba(255,255,255,0.6);
}

.footer-links {
  display: flex;
  gap: 64px;
}

.link-group {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.link-title {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.4);
  text-transform: uppercase;
  margin: 0;
}

.link {
  font-size: 14px;
  color: rgba(255,255,255,0.8);
  transition: color 0.2s;
}

.link:hover {
  color: white;
}

.status-link {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10B981;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.footer-bottom {
  padding-top: 32px;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.footer-copy {
  font-size: 13px;
  color: rgba(255,255,255,0.5);
  text-align: center;
  margin: 0;
}

.footer-copy a {
  color: rgba(255,255,255,0.8);
  transition: color 0.2s;
}

.footer-copy a:hover {
  color: white;
}
</style>
