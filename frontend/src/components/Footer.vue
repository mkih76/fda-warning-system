<template>
  <footer class="pf-footer">
    <!-- Main footer -->
    <div class="pf-footer-main">
      <div class="pf-container">
        <div class="pf-footer-grid">
          <!-- Brand -->
          <div class="pf-footer-brand">
            <svg viewBox="0 0 180 40" class="pf-footer-logo-svg">
              <rect x="0" y="4" width="32" height="32" rx="4" fill="#fff"/>
              <text x="5" y="26" font-size="18" font-weight="700" fill="#0000C9" font-family="Noto Sans, Arial, sans-serif">F</text>
              <text x="40" y="20" font-size="13" font-weight="700" fill="#fff" font-family="Noto Sans, Arial, sans-serif">FDA</text>
              <text x="40" y="34" font-size="9" font-weight="400" fill="rgba(255,255,255,0.7)" font-family="Noto Sans, Arial, sans-serif">警告信智能平台</text>
            </svg>
            <p class="pf-footer-desc">AI 驱动的 FDA 警告信监控与智能分析系统，助力中国制药企业合规出海，覆盖 986+ 封警告信，100% 中文翻译。</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="pf-footer-bottom">
      <div class="pf-container">
        <div class="pf-footer-bottom-inner">
          <p>&copy; {{ new Date().getFullYear() }} PharmaCos Insight. All rights reserved.</p>
          <div class="pf-footer-bottom-links">
            <a href="https://github.com/mkih76/fda-warning-system" target="_blank">GitHub</a>
            <span>|</span>
            <span>数据来源：<a href="https://www.fda.gov" target="_blank">FDA.gov</a></span>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.pf-footer {
  background: #000;
  color: #fff;
}

.pf-footer-main {
  padding: 36px 0 24px;
}

.pf-footer-grid {
  display: flex;
}

.pf-footer-brand {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.pf-footer-logo-svg {
  height: 36px;
  width: auto;
}

.pf-footer-desc {
  font-size: 13px;
  line-height: 1.6;
  color: rgba(255,255,255,0.6);
  margin: 0;
  max-width: 480px;
}

/* Bottom bar */
.pf-footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding: 20px 0;
}

.pf-footer-bottom-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: rgba(255,255,255,0.4);
}

.pf-footer-bottom-inner p { margin: 0; }

.pf-footer-bottom-links {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pf-footer-bottom-links a {
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  transition: color 0.2s;
}

.pf-footer-bottom-links a:hover { color: #fff; }

.pf-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
}

@media (max-width: 1024px) {
  .pf-footer-grid {
    flex-direction: column;
    gap: 24px;
  }
}

@media (max-width: 640px) {
  .pf-footer-bottom-inner {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}
</style>
