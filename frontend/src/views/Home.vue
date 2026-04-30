<template>
  <div class="pfizer-wrapper">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg">
        <img 
          src="https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=1920&q=80" 
          alt="Pharmaceutical Laboratory" 
          class="hero-image"
          loading="eager"
        />
        <div class="hero-overlay"></div>
      </div>
      <div class="hero-content">
        <h1>科学<br><span class="accent">赢得</span>胜利</h1>
        <p>我们不懈追求科学突破和革命性药物，为每个人创造更健康的世界</p>
        <router-link to="/letters" class="hero-cta">
          探索我们的科学
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 8l4 4m0 0l-4 4m4-4H3"/>
          </svg>
        </router-link>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="stats-container">
        <div class="stat-card" v-for="stat in stats" :key="stat.label">
          <div class="stat-number">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="feature-section">
      <div class="feature-container">
        <div class="section-header">
          <span class="section-eyebrow">核心功能</span>
          <h2 class="section-title">全方位合规保障</h2>
        </div>
        
        <div class="features-grid">
          <div class="feature-card" v-for="area in focusAreas" :key="area.title">
            <div class="feature-icon" :style="{ background: area.bg }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path v-html="area.icon"/>
              </svg>
            </div>
            <h3>{{ area.title }}</h3>
            <p>{{ area.desc }}</p>
            <router-link to="/letters" class="focus-link">
              了解更多
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 5l7 7-7 7"/>
              </svg>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="process-section">
      <div class="process-container">
        <div class="process-header">
          <span class="section-eyebrow">工作流程</span>
          <h2 class="section-title">从数据到洞察</h2>
        </div>
        
        <div class="process-steps">
          <div class="process-step" v-for="(step, i) in steps" :key="i">
            <div class="step-image">
              <img :src="step.image" :alt="step.title" loading="lazy"/>
            </div>
            <div class="step-content">
              <div class="step-number">0{{ i + 1 }}</div>
              <h3>{{ step.title }}</h3>
              <p>{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- News Section -->
    <section class="news-section">
      <div class="news-container">
        <div class="section-header">
          <span class="section-eyebrow">最新动态</span>
          <h2 class="section-title">FDA 执法趋势</h2>
        </div>
        
        <div class="news-grid">
          <div class="news-card" v-for="news in newsItems" :key="news.title">
            <div class="news-image">
              <img :src="news.image" :alt="news.title" loading="lazy"/>
            </div>
            <div class="news-content">
              <span class="news-date">{{ news.date }}</span>
              <h3>{{ news.title }}</h3>
              <p>{{ news.desc }}</p>
            </div>
          </div>
        </div>
        
        <router-link to="/news" class="more-link">
          更多资讯
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 8l4 4m0 0l-4 4m4-4H3"/>
          </svg>
        </router-link>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-bg">
        <img 
          src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1920&q=80" 
          alt="Medical Research" 
          class="cta-image"
          loading="lazy"
        />
        <div class="cta-overlay"></div>
      </div>
      <div class="cta-container">
        <h2>加入我们的合规监控平台</h2>
        <p>实时追踪 FDA 警告信，AI 智能分析，保障您的药品合规之路</p>
        <div class="cta-buttons">
          <router-link to="/letters" class="cta-primary">
            立即开始
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 8l4 4m0 0l-4 4m4-4H3"/>
            </svg>
          </router-link>
          <router-link to="/dashboard" class="cta-secondary-light">
            查看数据看板
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const stats = [
  { value: '986+', label: '警告信数据' },
  { value: '100%', label: '中文翻译' },
  { value: '24h', label: '数据同步' },
  { value: 'AI', label: '智能分析' }
]

const focusAreas = [
  {
    title: '实时 FDA 数据同步',
    desc: '每日自动抓取 FDA 官方数据，警告信发布后 24 小时内即可查看。',
    icon: 'M13 2L3 14h9l-1 8 10-12h-9l1-8z',
    bg: 'rgba(0, 147, 208, 0.1)'
  },
  {
    title: 'AI 翻译与摘要',
    desc: 'GPT 级 AI 将完整警告信翻译成中文，提取关键违规项，生成简洁摘要。',
    icon: 'M3 5h12M9 3v2m3.356 9.356l2.293 2.293M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9 14l2 2 4-4',
    bg: 'rgba(16, 185, 129, 0.1)'
  },
  {
    title: 'CGMP 自动化分类',
    desc: '根据 FDA 六大 CGMP 体系自动分类，精准定位需要关注的质量系统。',
    icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
    bg: 'rgba(139, 92, 246, 0.1)'
  },
  {
    title: '风险智能优先级',
    desc: '基于违规严重程度、国家风险画像和执法趋势，AI 驱动风险评分。',
    icon: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z M9 12l2 2 4-4',
    bg: 'rgba(245, 158, 11, 0.1)'
  },
  {
    title: '全文精准检索',
    desc: '支持按企业名称、产品类型、违规关键词或 CFR 引用检索所有警告信。',
    icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z M10 10l4 4',
    bg: 'rgba(236, 72, 153, 0.1)'
  },
  {
    title: '数据可视化看板',
    desc: '交互式仪表盘展示按年份、办公室、产品类别和违规类型的执法趋势。',
    icon: 'M3 3v18h18 M9 17V9m4 8V5m4 12v-4',
    bg: 'rgba(6, 182, 212, 0.1)'
  }
]

const steps = [
  {
    title: '数据采集',
    desc: '爬虫每日从 FDA 官方来源抓取最新警告信并更新数据库',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80'
  },
  {
    title: 'AI 处理',
    desc: '每封信经过翻译→分类→摘要流水线处理，采用最先进的 LLM 模型',
    image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&q=80'
  },
  {
    title: '洞察呈现',
    desc: '通过简洁的 Web 界面查看结构化数据、违规趋势和 AI 生成的摘要',
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=80'
  }
]

const newsItems = [
  {
    title: 'CGMP 违规趋势分析',
    desc: '2024年FDA针对药品生产企业的CGMP违规警告信数量持续上升，重点关注数据完整性问题。',
    date: '2024年4月',
    image: 'https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=600&q=80'
  },
  {
    title: 'AI 在药品合规中的应用',
    desc: '人工智能技术正在改变药品合规监控方式，自动化翻译和分析大幅提升了效率。',
    date: '2024年3月',
    image: 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&q=80'
  },
  {
    title: '高风险企业预警',
    desc: '系统识别出11家高风险企业，建议重点关注其合规状态和后续执法行动。',
    date: '2024年2月',
    image: 'https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&q=80'
  }
]
</script>

<style scoped>
.pfizer-wrapper {
  background: white;
}

/* Hero Section */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0, 82, 204, 0.9) 0%, rgba(0, 147, 208, 0.8) 100%);
}

.hero-content {
  position: relative;
  z-index: 10;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  width: 100%;
}

.hero-content h1 {
  font-size: clamp(48px, 8vw, 96px);
  font-weight: 800;
  line-height: 1;
  color: white;
  margin-bottom: 24px;
  letter-spacing: -0.03em;
}

.accent {
  color: #60a5fa;
}

.hero-content p {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
  max-width: 600px;
  line-height: 1.6;
  margin-bottom: 40px;
}

.hero-cta {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 32px;
  background: white;
  color: #0052CC;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s;
}

.hero-cta svg {
  width: 20px;
  height: 20px;
  transition: transform 0.2s;
}

.hero-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.hero-cta:hover svg {
  transform: translateX(4px);
}

/* Stats Section */
.stats-section {
  background: #f8fafc;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.stats-container {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
}

.stat-card {
  padding: 48px 32px;
  text-align: center;
  border-right: 1px solid #e5e7eb;
}

.stat-card:last-child {
  border-right: none;
}

.stat-number {
  font-size: 48px;
  font-weight: 800;
  color: #0093D0;
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* Feature Section */
.feature-section {
  padding: 100px 32px;
  background: white;
}

.feature-container {
  max-width: 1280px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 64px;
}

.section-eyebrow {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #0093D0;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 12px;
}

.section-title {
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 700;
  color: #1a1a2e;
  letter-spacing: -0.02em;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

@media (max-width: 900px) {
  .features-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 600px) {
  .features-grid { grid-template-columns: 1fr; }
}

.feature-card {
  padding: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s;
  background: white;
}

.feature-card:hover {
  border-color: #0093D0;
  box-shadow: 0 8px 32px rgba(0, 147, 208, 0.1);
}

.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.feature-icon svg {
  width: 28px;
  height: 28px;
  color: #0093D0;
}

.feature-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 12px;
}

.feature-card p {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.7;
  margin-bottom: 20px;
}

.focus-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #0093D0;
  text-decoration: none;
  transition: gap 0.2s;
}

.focus-link:hover {
  gap: 10px;
}

/* Process Section */
.process-section {
  padding: 100px 32px;
  background: #f8fafc;
}

.process-container {
  max-width: 1280px;
  margin: 0 auto;
}

.process-header {
  text-align: center;
  margin-bottom: 64px;
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 48px;
}

@media (max-width: 900px) {
  .process-steps { grid-template-columns: 1fr; }
}

.process-step {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.step-image {
  height: 200px;
  overflow: hidden;
}

.step-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.process-step:hover .step-image img {
  transform: scale(1.05);
}

.step-content {
  padding: 24px;
}

.step-number {
  font-size: 48px;
  font-weight: 800;
  color: #0093D0;
  opacity: 0.2;
  line-height: 1;
  margin-bottom: 12px;
}

.step-content h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 8px;
}

.step-content p {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
}

/* News Section */
.news-section {
  padding: 100px 32px;
  background: white;
}

.news-container {
  max-width: 1280px;
  margin: 0 auto;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  margin-bottom: 48px;
}

@media (max-width: 900px) {
  .news-grid { grid-template-columns: 1fr; }
}

.news-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s;
}

.news-card:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.news-image {
  height: 200px;
  overflow: hidden;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.news-card:hover .news-image img {
  transform: scale(1.05);
}

.news-content {
  padding: 24px;
}

.news-date {
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.news-content h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a2e;
  margin: 8px 0 12px;
}

.news-content p {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
}

.more-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #0093D0;
  text-decoration: none;
}

.more-link svg {
  width: 20px;
  height: 20px;
  transition: transform 0.2s;
}

.more-link:hover svg {
  transform: translateX(4px);
}

/* CTA Section */
.cta-section {
  position: relative;
  padding: 120px 32px;
  overflow: hidden;
}

.cta-bg {
  position: absolute;
  inset: 0;
}

.cta-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cta-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0, 82, 204, 0.95) 0%, rgba(0, 147, 208, 0.9) 100%);
}

.cta-container {
  position: relative;
  z-index: 10;
  max-width: 700px;
  margin: 0 auto;
  text-align: center;
}

.cta-section h2 {
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 700;
  color: white;
  margin-bottom: 16px;
  letter-spacing: -0.02em;
}

.cta-section p {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 40px;
}

.cta-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  background: white;
  color: #0052CC;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s;
}

.cta-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.cta-secondary-light {
  display: inline-flex;
  align-items: center;
  padding: 16px 32px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  color: white;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s;
}

.cta-secondary-light:hover {
  border-color: white;
  background: rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stat-card {
    border-bottom: 1px solid #e5e7eb;
  }
}
</style>
