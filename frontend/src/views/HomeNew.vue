<template>
  <div class="pf-home">
    <!-- Hero Banner - Full width with dark overlay -->
    <section class="pf-hero">
      <div class="pf-hero-bg">
        <div class="pf-hero-overlay"></div>
      </div>
      <div class="pf-container">
        <div class="pf-hero-content">
          <h1>REGULATORY<br/>INTELLIGENCE<br/>PLATFORM</h1>
          <p>制药·化妆品·食品行业知识与合规平台，覆盖政策法规、GMP 实务、药典解读等专业知识，AI 驱动，助力中国健康行业企业合规发展。</p>
          <div class="pf-hero-actions">
            <router-link to="/letters" class="pf-btn pf-btn-white">开始探索</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Three Sector Entry Cards -->
    <section class="pf-section pf-section-white">
      <div class="pf-container">
        <div class="pf-section-header">
          <h4 class="pf-eyebrow">行业板块</h4>
          <h2>三大行业知识体系</h2>
          <p>每个板块自成体系，涵盖行业动态、政策法规、知识专栏、案例研究</p>
        </div>
        <div class="sector-cards-grid">
          <router-link to="/pharma" class="sector-entry-card" style="--sector-color: #0000C9">
            <div class="sector-entry-icon">
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/></svg>
            </div>
            <h3>制药 Pharma</h3>
            <p>GMP 实务、药典解读、注册申报、质量控制、工艺验证</p>
            <span class="sector-entry-link">了解更多 →</span>
          </router-link>
          <router-link to="/cosmetics" class="sector-entry-card" style="--sector-color: #C45B9C">
            <div class="sector-entry-icon">
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z"/></svg>
            </div>
            <h3>化妆品 Cosmetics</h3>
            <p>配方安全、功效评价、原料合规、标签宣称、市场趋势</p>
            <span class="sector-entry-link">了解更多 →</span>
          </router-link>
          <router-link to="/food" class="sector-entry-card" style="--sector-color: #2D8C3C">
            <div class="sector-entry-icon">
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 8.25v-1.5m0 1.5c-1.355 0-2.697.056-4.024.166C6.845 8.51 6 9.473 6 10.608v2.513m6-4.87c1.355 0 2.697.055 4.024.165C17.155 8.51 18 9.473 18 10.608v2.513m-3-4.87v-1.5m-6 1.5v-1.5m12 9.75l-1.5.75a3.354 3.354 0 01-3 0 3.354 3.354 0 00-3 0 3.354 3.354 0 01-3 0 3.354 3.354 0 00-3 0 3.354 3.354 0 01-3 0L3 16.5m15-3.38a48.474 48.474 0 00-6-.371c-2.032 0-4.034.126-6 .371m12 0c.39.049.777.102 1.163.16 1.07.16 1.837 1.094 1.837 2.175v5.17c0 .62-.504 1.124-1.125 1.124H4.125A1.125 1.125 0 013 20.625v-5.17c0-1.08.768-2.014 1.837-2.174A47.78 47.78 0 016 13.12M12.265 3.11a.375.375 0 11-.53 0L12 2.845l.265.265z"/></svg>
            </div>
            <h3>食品 Food</h3>
            <p>食品安全管理体系、添加剂合规、标签标识、进出口合规</p>
            <span class="sector-entry-link">了解更多 →</span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Two Column - Image + Text (Pfizer style) -->
    <section class="pf-section pf-section-white">
      <div class="pf-container">
        <div class="pf-two-col">
          <div class="pf-two-col-img">
            <div class="pf-img-placeholder pf-img-rounded">
              <svg viewBox="0 0 600 450" fill="none">
                <rect width="600" height="450" rx="8" fill="#F2F9FC"/>
                <circle cx="300" cy="200" r="80" fill="#0000C9" opacity="0.1"/>
                <path d="M260 200h80M300 160v80" stroke="#0000C9" stroke-width="3" stroke-linecap="round"/>
                <text x="300" y="340" text-anchor="middle" font-size="16" fill="#0000C9" font-family="Noto Sans, Arial">AI 智能分析引擎</text>
              </svg>
            </div>
          </div>
          <div class="pf-two-col-text">
            <h4>AI 驱动的智能翻译与分析</h4>
            <p>采用最先进的 AI 大语言模型，自动翻译 FDA 英文警告信为精准中文，同时智能识别违规类型、风险等级和关键 CFR 条款引用。</p>
            <router-link to="/letters" class="pf-btn pf-btn-primary">了解更多</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Article List Section - Light blue background (Pfizer style) -->
    <section class="pf-section pf-section-light">
      <div class="pf-container">
        <div class="pf-two-col pf-two-col-reverse">
          <div class="pf-two-col-text">
            <h4>最新警告信动态</h4>
            <p>实时同步 FDA 官方数据，第一时间推送最新发布的警告信，确保您不错过任何重要的合规风险信号。</p>
            <div class="pf-article-list">
              <div v-for="(letter, i) in latestLetters" :key="i" class="pf-article-item" @click="$router.push(`/letters/${letter.id}`)">
                <span class="pf-article-date">{{ letter.issue_date }}</span>
                <span class="pf-article-sep">|</span>
                <span class="pf-article-type">{{ letter.issuing_office }}</span>
                <a class="pf-article-title">{{ letter.company_name }} - {{ letter.subject }}</a>
              </div>
            </div>
            <router-link to="/letters" class="pf-btn pf-btn-primary" style="margin-top: 24px;">查看全部警告信</router-link>
          </div>
          <div class="pf-two-col-img">
            <div class="pf-img-placeholder pf-img-rounded">
              <svg viewBox="0 0 600 450" fill="none">
                <rect width="600" height="450" rx="8" fill="#fff"/>
                <rect x="40" y="40" width="520" height="60" rx="6" fill="#F2F9FC"/>
                <rect x="40" y="120" width="520" height="60" rx="6" fill="#F2F9FC"/>
                <rect x="40" y="200" width="520" height="60" rx="6" fill="#F2F9FC"/>
                <rect x="40" y="280" width="520" height="60" rx="6" fill="#F2F9FC"/>
                <circle cx="70" cy="70" r="12" fill="#dc2626" opacity="0.2"/>
                <circle cx="70" cy="150" r="12" fill="#f59e0b" opacity="0.2"/>
                <circle cx="70" cy="230" r="12" fill="#22c55e" opacity="0.2"/>
                <circle cx="70" cy="310" r="12" fill="#0000C9" opacity="0.2"/>
                <rect x="100" y="62" width="180" height="8" rx="4" fill="#cbd5e1"/>
                <rect x="100" y="78" width="120" height="6" rx="3" fill="#e2e8f0"/>
                <rect x="100" y="142" width="200" height="8" rx="4" fill="#cbd5e1"/>
                <rect x="100" y="158" width="100" height="6" rx="3" fill="#e2e8f0"/>
                <rect x="100" y="222" width="160" height="8" rx="4" fill="#cbd5e1"/>
                <rect x="100" y="238" width="140" height="6" rx="3" fill="#e2e8f0"/>
                <rect x="100" y="302" width="220" height="8" rx="4" fill="#cbd5e1"/>
                <rect x="100" y="318" width="80" height="6" rx="3" fill="#e2e8f0"/>
                <text x="300" y="390" text-anchor="middle" font-size="14" fill="#666" font-family="Noto Sans, Arial">警告信列表预览</text>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section - White background -->
    <section class="pf-section pf-section-white">
      <div class="pf-container">
        <div class="pf-section-header">
          <h4 class="pf-eyebrow">数据洞察</h4>
          <h2>用数据驱动合规决策</h2>
          <p>我们实时同步 FDA 官方数据，通过 AI 智能分析，为您提供深度的行业洞察和风险预警。</p>
        </div>
        <div class="pf-stats-grid">
          <div class="pf-stat-card">
            <span class="pf-stat-number">986</span>
            <span class="pf-stat-label">警告信总数</span>
          </div>
          <div class="pf-stat-card">
            <span class="pf-stat-number">100%</span>
            <span class="pf-stat-label">中文翻译</span>
          </div>
          <div class="pf-stat-card">
            <span class="pf-stat-number">12</span>
            <span class="pf-stat-label">签发办公室</span>
          </div>
          <div class="pf-stat-card">
            <span class="pf-stat-number">24h</span>
            <span class="pf-stat-label">实时同步</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Features - Light blue bg -->
    <section class="pf-section pf-section-light">
      <div class="pf-container">
        <div class="pf-two-col">
          <div class="pf-two-col-img">
            <div class="pf-img-placeholder pf-img-rounded">
              <svg viewBox="0 0 600 450" fill="none">
                <rect width="600" height="450" rx="8" fill="#fff"/>
                <rect x="60" y="60" width="220" height="150" rx="8" fill="#F2F9FC" stroke="#0000C9" stroke-width="1" opacity="0.5"/>
                <rect x="320" y="60" width="220" height="150" rx="8" fill="#F2F9FC" stroke="#0000C9" stroke-width="1" opacity="0.5"/>
                <rect x="60" y="250" width="220" height="150" rx="8" fill="#F2F9FC" stroke="#0000C9" stroke-width="1" opacity="0.5"/>
                <rect x="320" y="250" width="220" height="150" rx="8" fill="#F2F9FC" stroke="#0000C9" stroke-width="1" opacity="0.5"/>
                <text x="170" y="145" text-anchor="middle" font-size="13" fill="#0000C9" font-family="Noto Sans, Arial">实时数据同步</text>
                <text x="430" y="145" text-anchor="middle" font-size="13" fill="#0000C9" font-family="Noto Sans, Arial">AI 智能翻译</text>
                <text x="170" y="335" text-anchor="middle" font-size="13" fill="#0000C9" font-family="Noto Sans, Arial">风险评估</text>
                <text x="430" y="335" text-anchor="middle" font-size="13" fill="#0000C9" font-family="Noto Sans, Arial">数据可视化</text>
              </svg>
            </div>
          </div>
          <div class="pf-two-col-text">
            <h4>全方位合规保障</h4>
            <p>我们提供完整的 FDA 警告信监控和分析解决方案，涵盖数据采集、AI 处理、风险评估到数据可视化的全链路。</p>
            <div class="pf-feature-list">
              <div class="pf-feature-item">
                <div class="pf-feature-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0000C9" stroke-width="2"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                </div>
                <div>
                  <strong>实时数据同步</strong>
                  <span>每日自动同步 FDA 官方数据</span>
                </div>
              </div>
              <div class="pf-feature-item">
                <div class="pf-feature-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0000C9" stroke-width="2"><path d="M3 5h12M9 3v2m3.356 9.356l2.293 2.293M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <div>
                  <strong>AI 智能翻译</strong>
                  <span>100% 准确翻译为中文</span>
                </div>
              </div>
              <div class="pf-feature-item">
                <div class="pf-feature-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0000C9" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                </div>
                <div>
                  <strong>风险评估</strong>
                  <span>AI 驱动的风险评分</span>
                </div>
              </div>
              <div class="pf-feature-item">
                <div class="pf-feature-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0000C9" stroke-width="2"><path d="M3 3v18h18M9 17V9m4 8V5m4 12v-4"/></svg>
                </div>
                <div>
                  <strong>数据可视化</strong>
                  <span>交互式仪表盘展示趋势</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Workflow Section - White -->
    <section class="pf-section pf-section-white">
      <div class="pf-container">
        <div class="pf-section-header">
          <h4 class="pf-eyebrow">工作流程</h4>
          <h2>从数据到洞察</h2>
          <p>三步流水线确保您获得最准确、最及时的 FDA 警告信信息</p>
        </div>
        <div class="pf-steps-grid">
          <div class="pf-step-card">
            <div class="pf-step-num">01</div>
            <div class="pf-step-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0000C9" stroke-width="2"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
            </div>
            <h4>数据采集</h4>
            <p>爬虫每日从 FDA 官方来源抓取最新警告信并更新数据库</p>
          </div>
          <div class="pf-step-card">
            <div class="pf-step-num">02</div>
            <div class="pf-step-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0000C9" stroke-width="2"><path d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            </div>
            <h4>AI 处理</h4>
            <p>每封信经过翻译、分类、摘要流水线处理，采用最先进的 LLM 模型</p>
          </div>
          <div class="pf-step-card">
            <div class="pf-step-num">03</div>
            <div class="pf-step-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0000C9" stroke-width="2"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            </div>
            <h4>洞察呈现</h4>
            <p>通过简洁的 Web 界面查看结构化数据、违规趋势和 AI 生成的摘要</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA - Dark blue (Pfizer style) -->
    <section class="pf-cta">
      <div class="pf-container">
        <div class="pf-cta-content">
          <h2>准备好开始了吗？</h2>
          <p>立即探索 FDA 警告信数据库，利用 AI 智能分析保障您的合规之路</p>
          <div class="pf-cta-actions">
            <router-link to="/letters" class="pf-btn pf-btn-white">免费开始使用</router-link>
            <router-link to="/dashboard" class="pf-btn pf-btn-outline-white">查看演示</router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const latestLetters = ref([
  { id: 1, company_name: '某制药有限公司', subject: 'CGMP 违规 - 数据完整性问题', issue_date: '03.15.2024', issuing_office: 'CDER' },
  { id: 2, company_name: '某生物科技公司', subject: '生产过程控制不符合要求', issue_date: '02.28.2024', issuing_office: 'CDRH' },
  { id: 3, company_name: '某食品有限公司', subject: '标签标识不符合规定', issue_date: '02.10.2024', issuing_office: 'CFSAN' },
  { id: 4, company_name: '某医疗器械公司', subject: '质量体系不符合要求', issue_date: '01.22.2024', issuing_office: 'CDRH' },
])
</script>

<style scoped>
.pf-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
}

/* ═══════════════════════════════════════
   Hero Banner
═══════════════════════════════════════ */
.pf-hero {
  position: relative;
  min-height: 600px;
  display: flex;
  align-items: center;
  padding-top: 140px;
  padding-bottom: 80px;
}

.pf-hero-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #000049 0%, #0000C9 50%, #003FE2 100%);
}

.pf-hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.4);
}

.pf-hero-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
}

.pf-hero-content h1 {
  font-size: 64px;
  font-weight: 800;
  color: #fff;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin: 0 0 24px;
  text-transform: uppercase;
}

.pf-hero-content p {
  font-size: 18px;
  color: rgba(255,255,255,0.9);
  line-height: 1.7;
  margin: 0 0 32px;
  max-width: 560px;
}

.pf-hero-actions {
  display: flex;
  gap: 16px;
}

/* ═══════════════════════════════════════
   Buttons
═══════════════════════════════════════ */
.pf-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 32px;
  font-size: 15px;
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

.pf-btn-white {
  background: #fff;
  color: #0000C9;
}

.pf-btn-white:hover {
  background: #F2F9FC;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.pf-btn-outline-white {
  background: transparent;
  color: #fff;
  border: 2px solid rgba(255,255,255,0.5);
}

.pf-btn-outline-white:hover {
  background: rgba(255,255,255,0.1);
  border-color: #fff;
}

/* ═══════════════════════════════════════
   Sections
═══════════════════════════════════════ */
.pf-section {
  padding: 80px 0;
}

.pf-section-white { background: #fff; }
.pf-section-light { background: #F2F9FC; }

/* Section header */
.pf-section-header {
  text-align: center;
  margin-bottom: 60px;
  max-width: 640px;
  margin-left: auto;
  margin-right: auto;
}

.pf-eyebrow {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #0000C9;
  margin: 0 0 12px;
}

.pf-section-header h2 {
  font-size: 36px;
  font-weight: 700;
  color: #000;
  margin: 0 0 16px;
  line-height: 1.2;
}

.pf-section-header p {
  font-size: 16px;
  color: #666;
  line-height: 1.7;
  margin: 0;
}

/* ═══════════════════════════════════════
   Sector Entry Cards
═══════════════════════════════════════ */
.sector-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.sector-entry-card {
  padding: 40px 32px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.25s;
  position: relative;
  overflow: hidden;
}

.sector-entry-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--sector-color);
  transform: scaleX(0);
  transition: transform 0.25s;
  transform-origin: left;
}

.sector-entry-card:hover {
  border-color: var(--sector-color);
  box-shadow: 0 12px 32px rgba(0,0,0,0.1);
  transform: translateY(-6px);
}

.sector-entry-card:hover::before { transform: scaleX(1); }

.sector-entry-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: color-mix(in srgb, var(--sector-color) 8%, transparent);
  color: var(--sector-color);
  margin-bottom: 20px;
}

.sector-entry-card h3 {
  font-size: 22px;
  font-weight: 700;
  color: #000;
  margin: 0 0 10px;
}

.sector-entry-card p {
  font-size: 14px;
  color: #666;
  line-height: 1.7;
  margin: 0 0 20px;
}

.sector-entry-link {
  font-size: 14px;
  font-weight: 600;
  color: var(--sector-color);
  transition: gap 0.2s;
}

/* ═══════════════════════════════════════
   Two Column Layout (Pfizer core pattern)
═══════════════════════════════════════ */
.pf-two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.pf-two-col-reverse {
  direction: rtl;
}

.pf-two-col-reverse > * {
  direction: ltr;
}

.pf-two-col-img { width: 100%; }

.pf-img-placeholder {
  width: 100%;
  aspect-ratio: 4/3;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.pf-img-placeholder svg {
  width: 100%;
  height: 100%;
}

.pf-img-rounded {
  border-radius: 8px;
}

.pf-two-col-text h4 {
  font-size: 28px;
  font-weight: 700;
  color: #000;
  margin: 0 0 16px;
  line-height: 1.3;
}

.pf-two-col-text > p {
  font-size: 16px;
  color: #333;
  line-height: 1.8;
  margin: 0 0 24px;
}

/* ═══════════════════════════════════════
   Article List (Pfizer style)
═══════════════════════════════════════ */
.pf-article-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.pf-article-item {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 12px 0;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.15s;
}

.pf-article-item:hover {
  padding-left: 8px;
}

.pf-article-date {
  font-size: 13px;
  color: #666;
  white-space: nowrap;
  font-family: 'Noto Sans', Arial, sans-serif;
}

.pf-article-sep {
  color: #ccc;
  font-size: 12px;
}

.pf-article-type {
  font-size: 13px;
  color: #0000C9;
  font-weight: 500;
  white-space: nowrap;
}

.pf-article-title {
  font-size: 14px;
  color: #0000C9;
  text-decoration: none;
  transition: color 0.15s;
}

.pf-article-item:hover .pf-article-title {
  color: #0000A3;
  text-decoration: underline;
}

/* ═══════════════════════════════════════
   Stats Grid
═══════════════════════════════════════ */
.pf-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}

.pf-stat-card {
  text-align: center;
  padding: 40px 24px;
  background: #F2F9FC;
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.pf-stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,201,0.1);
}

.pf-stat-number {
  display: block;
  font-size: 48px;
  font-weight: 800;
  color: #0000C9;
  line-height: 1;
  margin-bottom: 8px;
}

.pf-stat-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

/* ═══════════════════════════════════════
   Feature List
═══════════════════════════════════════ */
.pf-feature-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.pf-feature-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.pf-feature-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,201,0.08);
  border-radius: 8px;
}

.pf-feature-item div:last-child {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pf-feature-item strong {
  font-size: 15px;
  font-weight: 600;
  color: #000;
}

.pf-feature-item span {
  font-size: 14px;
  color: #666;
}

/* ═══════════════════════════════════════
   Steps Grid
═══════════════════════════════════════ */
.pf-steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.pf-step-card {
  text-align: center;
  padding: 48px 32px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  position: relative;
  transition: box-shadow 0.2s, transform 0.2s;
}

.pf-step-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  transform: translateY(-4px);
}

.pf-step-num {
  position: absolute;
  top: 16px;
  right: 20px;
  font-size: 48px;
  font-weight: 800;
  color: #000;
  opacity: 0.04;
  line-height: 1;
}

.pf-step-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,201,0.08);
  border-radius: 16px;
  margin: 0 auto 20px;
}

.pf-step-card h4 {
  font-size: 20px;
  font-weight: 600;
  color: #000;
  margin: 0 0 12px;
}

.pf-step-card p {
  font-size: 14px;
  color: #666;
  line-height: 1.7;
  margin: 0;
}

/* ═══════════════════════════════════════
   CTA Section
═══════════════════════════════════════ */
.pf-cta {
  background: #0000C9;
  padding: 80px 0;
}

.pf-cta-content {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.pf-cta-content h2 {
  font-size: 36px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 16px;
}

.pf-cta-content p {
  font-size: 18px;
  color: rgba(255,255,255,0.9);
  margin: 0 0 32px;
}

.pf-cta-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

/* ═══════════════════════════════════════
   Responsive
═══════════════════════════════════════ */
@media (max-width: 1024px) {
  .pf-container { padding: 0 16px; }

  .pf-hero {
    min-height: 500px;
    padding-top: 120px;
    padding-bottom: 60px;
  }

  .pf-hero-content h1 { font-size: 48px; }

  .pf-two-col {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .pf-two-col-reverse { direction: ltr; }

  .pf-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .pf-steps-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .sector-cards-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .pf-section { padding: 60px 0; }
}

@media (max-width: 640px) {
  .pf-hero-content h1 { font-size: 36px; }
  .pf-hero-content p { font-size: 16px; }
  .pf-hero { min-height: 450px; padding-top: 100px; }
  .pf-stats-grid { grid-template-columns: 1fr 1fr; gap: 16px; }
  .pf-stat-number { font-size: 36px; }
  .pf-two-col-text h4 { font-size: 24px; }
  .pf-section-header h2 { font-size: 28px; }
  .pf-cta-content h2 { font-size: 28px; }
}
</style>
