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

          <!-- Links -->
          <div class="pf-footer-links">
            <div class="pf-footer-col">
              <h4>平台功能</h4>
              <router-link to="/letters">警告信列表</router-link>
              <router-link to="/dashboard">数据看板</router-link>
              <router-link to="/favorites">我的收藏</router-link>
            </div>
            <div class="pf-footer-col">
              <h4>内容资源</h4>
              <router-link to="/articles">深度内容</router-link>
              <router-link to="/news">行业资讯</router-link>
              <router-link to="/regulations">法规信息</router-link>
            </div>
            <div class="pf-footer-col">
              <h4>关于我们</h4>
              <a href="https://github.com/mkih76/fda-warning-system" target="_blank">GitHub</a>
              <a href="https://www.fda.gov" target="_blank">FDA 官方网站</a>
              <a href="mailto:contact@example.com">联系我们</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="pf-footer-bottom">
      <div class="pf-container">
        <div class="pf-footer-bottom-inner">
          <p>&copy; {{ new Date().getFullYear() }} FDA 警告信智能平台. All rights reserved.</p>
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
  padding: 64px 0 48px;
}

.pf-footer-grid {
  display: grid;
  grid-template-columns: 1.2fr 2fr;
  gap: 80px;
}

.pf-footer-brand {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.pf-footer-logo-svg {
  height: 40px;
  width: auto;
}

.pf-footer-desc {
  font-size: 14px;
  line-height: 1.7;
  color: rgba(255,255,255,0.6);
  margin: 0;
  max-width: 320px;
}

.pf-footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.pf-footer-col h4 {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 20px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.pf-footer-col a {
  display: block;
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  padding: 6px 0;
  transition: color 0.2s;
}

.pf-footer-col a:hover { color: #fff; }

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
    grid-template-columns: 1fr;
    gap: 48px;
  }
  .pf-footer-links {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 640px) {
  .pf-footer-links {
    grid-template-columns: 1fr 1fr;
    gap: 32px;
  }
  .pf-footer-bottom-inner {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}
</style>
