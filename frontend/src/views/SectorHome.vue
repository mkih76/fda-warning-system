<template>
  <div class="sector-home">
    <!-- Hero Banner with background image -->
    <section class="sector-hero">
      <div class="sector-hero-bg">
        <img :src="sectorConfig.heroImage" :alt="sectorConfig.title" class="sector-hero-img" />
        <div class="sector-hero-overlay" :style="{ background: heroGradient }"></div>
      </div>
      <div class="sector-container">
        <div class="sector-hero-content">
          <span class="sector-badge">{{ sectorConfig.nameEn }}</span>
          <h1>{{ sectorConfig.title }}</h1>
          <p>{{ sectorConfig.description }}</p>
          <div class="sector-hero-actions">
            <router-link :to="`/${sector}`" class="pf-btn pf-btn-white">浏览全部</router-link>
            <router-link to="/letters" class="pf-btn pf-btn-outline">查看警告信</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 分类入口 - 带图片的卡片 -->
    <section class="sector-section sector-section-white">
      <div class="sector-container">
        <div class="sector-section-header">
          <h4 class="sector-eyebrow">内容分类</h4>
          <h2>{{ sectorConfig.name }}知识体系</h2>
          <p class="sector-section-desc">{{ sectorConfig.sectionDesc }}</p>
        </div>
        <div class="category-grid">
          <router-link
            v-for="(cat, i) in sectorConfig.categories"
            :key="cat.slug"
            :to="`/${sector}/${cat.slug}`"
            class="category-card"
          >
            <div class="category-card-img">
              <img :src="cat.image" :alt="cat.name" loading="lazy" />
              <div class="category-card-overlay"></div>
              <div class="category-icon-badge" :style="{ background: sectorConfig.color }">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" :d="cat.icon" />
                </svg>
              </div>
            </div>
            <div class="category-card-body">
              <h4>{{ cat.name }}</h4>
              <p>{{ cat.desc }}</p>
              <span class="category-link">了解更多 →</span>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 最新文章 - 双栏布局 -->
    <section class="sector-section sector-section-light">
      <div class="sector-container">
        <div class="sector-two-col">
          <div class="sector-two-col-text">
            <h4 class="sector-eyebrow">最新发布</h4>
            <h2>{{ sectorConfig.name }}最新动态</h2>
            <p class="sector-section-desc">{{ sectorConfig.name }}板块的最新文章和行业动态</p>
            <div class="article-list">
              <div
                v-for="(article, i) in latestArticles"
                :key="i"
                class="article-item"
                @click="$router.push(`/${sector}/article/${article.slug}`)"
              >
                <span class="article-date">{{ article.date }}</span>
                <span class="article-sep">|</span>
                <span class="article-cat">{{ article.category }}</span>
                <a class="article-title">{{ article.title }}</a>
              </div>
            </div>
            <router-link :to="`/${sector}`" class="pf-btn pf-btn-primary" style="margin-top: 24px;">
              查看全部 {{ sectorConfig.name }}内容
            </router-link>
          </div>
          <div class="sector-two-col-visual">
            <div class="visual-card">
              <img :src="sectorConfig.latestImage" :alt="sectorConfig.name" class="visual-img" />
              <div class="visual-card-overlay">
                <span class="visual-label">{{ sectorConfig.name }}板块</span>
                <span class="visual-sublabel">最新专业内容</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 数据统计 -->
    <section class="sector-section sector-section-white">
      <div class="sector-container">
        <div class="sector-section-header">
          <h4 class="sector-eyebrow">数据总览</h4>
          <h2>用数据驱动合规决策</h2>
        </div>
        <div class="sector-stats-grid">
          <div class="sector-stat-card" v-for="stat in sectorConfig.stats" :key="stat.label">
            <span class="sector-stat-number" :style="{ color: sectorConfig.color }">{{ stat.value }}</span>
            <span class="sector-stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'

const API = window.location.origin + '/api'

const props = defineProps({
  sector: { type: String, required: true }
})

const apiArticles = ref([])

onMounted(async () => {
  try {
    const resp = await fetch(`${API}/content/sector/${props.sector}`)
    if (resp.ok) {
      const data = await resp.json()
      apiArticles.value = data.latest_articles || []
    }
  } catch (e) { /* silent */ }
})

const sectorConfigs = {
  pharma: {
    name: '制药', nameEn: 'Pharma',
    title: '制药行业知识平台',
    description: '覆盖 GMP、药典、注册申报、质量控制等专业知识，助力中国制药企业合规出海',
    sectionDesc: '从法规解读到工艺验证，八大知识板块覆盖制药全生命周期',
    color: '#0000C9', darkColor: '#000049', lightColor: '#F2F9FC',
    heroImage: 'https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=1600&q=80',
    latestImage: 'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80',
    categories: [
      { name: '行业动态', slug: 'industry-news', desc: '全球新药批准、集采动态、行业并购', image: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600&q=75', icon: 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 1v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z' },
      { name: '政策法规', slug: 'regulations', desc: 'NMPA/FDA/EMA 新规解读，合规指南', image: 'https://images.unsplash.com/photo-1589994965851-a8f479c573a9?w=600&q=75', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
      { name: 'GMP 实务', slug: 'gmp-practice', desc: 'cGMP 检查要点、483 观察项分析', image: 'https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=600&q=75', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' },
      { name: '药典解读', slug: 'pharmacopoeia', desc: '中国药典、USP、EP 对比分析', image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=75', icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
      { name: '注册申报', slug: 'registration', desc: 'ANDA、DMF、eCTD、中美双报', image: 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=600&q=75', icon: 'M7 20l4-16m2 16l4-16M6 9h14M4 15h14' },
      { name: '质量控制', slug: 'quality-control', desc: '分析方法、实验室管理、标准物质', image: 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=600&q=75', icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z' },
      { name: '工艺验证', slug: 'process-validation', desc: 'PV 三阶段、持续工艺验证、技术转移', image: 'https://images.unsplash.com/photo-1581093450021-4a7360e9a6b5?w=600&q=75', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z' },
      { name: '案例研究', slug: 'case-studies', desc: '警告信深度解析、483 案例库', image: 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&q=75', icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' },
    ],
    stats: [
      { value: '50+', label: '专业知识文章' },
      { value: '986', label: 'FDA 警告信' },
      { value: '12', label: '覆盖法规体系' },
      { value: '24h', label: '政策更新时效' },
    ]
  },
  cosmetics: {
    name: '化妆品', nameEn: 'Cosmetics',
    title: '化妆品行业知识平台',
    description: '覆盖配方安全、功效评价、原料合规、标签宣称等专业知识，服务中国美妆产业',
    sectionDesc: '从原料筛选到功效验证，八大板块覆盖化妆品合规全链路',
    color: '#C45B9C', darkColor: '#8B2252', lightColor: '#FDF2F8',
    heroImage: 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=1600&q=80',
    latestImage: 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&q=80',
    categories: [
      { name: '行业动态', slug: 'industry-news', desc: '新原料备案、国际美妆集团动态', image: 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600&q=75', icon: 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 1v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z' },
      { name: '政策法规', slug: 'regulations', desc: '《化妆品监督管理条例》及配套文件解读', image: 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=600&q=75', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
      { name: '配方与安全', slug: 'formulation-safety', desc: '安全评估、防腐体系、微生物控制', image: 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=600&q=75', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' },
      { name: '功效评价', slug: 'efficacy-testing', desc: '人体功效试验、体外替代方法', image: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&q=75', icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z' },
      { name: '原料合规', slug: 'ingredient-compliance', desc: '新原料备案、已使用原料目录、禁限用物质', image: 'https://images.unsplash.com/photo-1585435465945-bef5a93f8849?w=600&q=75', icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
      { name: '标签与宣称', slug: 'labeling-claims', desc: '标签合规、功效宣称用语边界', image: 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=600&q=75', icon: 'M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z' },
      { name: '生产质量管理', slug: 'manufacturing-qm', desc: 'GMP 检查要点、委托生产', image: 'https://images.unsplash.com/photo-1581093450021-4a7360e9a6b5?w=600&q=75', icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' },
      { name: '市场趋势', slug: 'trends', desc: '成分趋势、品类增长、消费者洞察', image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&q=75', icon: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6' },
    ],
    stats: [
      { value: '30+', label: '专业知识文章' },
      { value: '2000+', label: '原料合规数据' },
      { value: '15', label: '覆盖法规体系' },
      { value: '48h', label: '政策更新时效' },
    ]
  },
  food: {
    name: '食品', nameEn: 'Food',
    title: '食品行业知识平台',
    description: '覆盖食品安全管理体系、添加剂合规、标签标识、进出口合规等专业知识',
    sectionDesc: '从原料溯源到出口合规，八大板块守护食品安全每一道关',
    color: '#2D8C3C', darkColor: '#1A5C28', lightColor: '#F0FDF4',
    heroImage: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1600&q=80',
    latestImage: 'https://images.unsplash.com/photo-1577219491135-ce3957368d02?w=800&q=80',
    categories: [
      { name: '行业动态', slug: 'industry-news', desc: '食品安全抽检、新原料公告、市场趋势', image: 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=600&q=75', icon: 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 1v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z' },
      { name: '政策法规', slug: 'regulations', desc: 'GB 食品安全标准、FSMA、EU 食品法规', image: 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=600&q=75', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
      { name: '食品安全管理体系', slug: 'food-safety-mgmt', desc: 'HACCP、ISO 22000、FSSC 22000', image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=75', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' },
      { name: '添加剂与新原料', slug: 'food-additives', desc: 'GB 2760、新食品原料申报、GRAS', image: 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=600&q=75', icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
      { name: '标签标识', slug: 'food-labeling', desc: 'GB 7718、营养标签、特殊膳食标签', image: 'https://images.unsplash.com/photo-1589452271712-64b8a66c3929?w=600&q=75', icon: 'M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z' },
      { name: '进出口合规', slug: 'food-import-export', desc: '进口食品备案、出口合规、FSVP', image: 'https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=600&q=75', icon: 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064' },
      { name: '营养与健康声称', slug: 'nutrition-claims', desc: '保健食品、功能声称、特医食品', image: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&q=75', icon: 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z' },
      { name: '市场趋势', slug: 'trends', desc: '植物基、益生菌、功能性食品', image: 'https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&q=75', icon: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6' },
    ],
    stats: [
      { value: '30+', label: '专业知识文章' },
      { value: '1000+', label: '食品安全标准' },
      { value: '10', label: '覆盖法规体系' },
      { value: '24h', label: '政策更新时效' },
    ]
  }
}

const sectorConfig = computed(() => sectorConfigs[props.sector])
const heroGradient = computed(() => {
  const c = sectorConfig.value
  return `linear-gradient(135deg, ${c.color}cc 0%, ${c.darkColor}ee 100%)`
})

// Use API data if available, otherwise show placeholder
const latestArticles = computed(() => {
  if (apiArticles.value.length > 0) {
    return apiArticles.value.map(a => ({
      slug: a.slug,
      date: a.published_at ? new Date(a.published_at).toLocaleDateString('zh-CN') : '',
      category: a.category_name || a.sector,
      title: a.title,
    }))
  }
  return [
    { slug: 'sample-1', date: '04.28.2026', category: '政策法规', title: '示例文章标题 — 正在建设中' },
    { slug: 'sample-2', date: '04.25.2026', category: '知识专栏', title: '内容即将上线，敬请期待' },
    { slug: 'sample-3', date: '04.22.2026', category: '行业动态', title: '更多内容正在准备中...' },
  ]
})
</script>

<style scoped>
.sector-home { background: #fff; }

.sector-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
}

/* ═══ Hero ═══ */
.sector-hero {
  position: relative;
  padding: 160px 0 100px;
  color: #fff;
  overflow: hidden;
  min-height: 480px;
  display: flex;
  align-items: center;
}

.sector-hero-bg {
  position: absolute;
  inset: 0;
}

.sector-hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.sector-hero-overlay {
  position: absolute;
  inset: 0;
}

.sector-hero-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
}

.sector-badge {
  display: inline-block;
  padding: 6px 18px;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 6px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 24px;
}

.sector-hero h1 {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.1;
  margin: 0 0 20px;
  letter-spacing: -0.02em;
}

.sector-hero p {
  font-size: 18px;
  opacity: 0.9;
  line-height: 1.7;
  margin: 0 0 32px;
  max-width: 560px;
}

.sector-hero-actions { display: flex; gap: 16px; flex-wrap: wrap; }

.pf-btn-white {
  display: inline-flex;
  align-items: center;
  padding: 14px 32px;
  background: #fff;
  color: #0000C9;
  font-weight: 700;
  font-size: 15px;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.25s;
}

.pf-btn-white:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}

.pf-btn-outline {
  display: inline-flex;
  align-items: center;
  padding: 14px 32px;
  background: transparent;
  color: #fff;
  font-weight: 600;
  font-size: 15px;
  border: 2px solid rgba(255,255,255,0.4);
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.25s;
}

.pf-btn-outline:hover {
  background: rgba(255,255,255,0.1);
  border-color: rgba(255,255,255,0.7);
}

.pf-btn-primary {
  display: inline-flex;
  align-items: center;
  padding: 12px 28px;
  background: #0000C9;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.25s;
}

.pf-btn-primary:hover {
  background: #0000A3;
  transform: translateY(-1px);
}

/* ═══ Sections ═══ */
.sector-section { padding: 100px 0; }
.sector-section-white { background: #fff; }
.sector-section-light { background: #F8FAFC; }

.sector-section-header {
  text-align: center;
  margin-bottom: 56px;
}

.sector-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #0000C9;
  margin: 0 0 12px;
}

.sector-section-header h2 {
  font-size: 36px;
  font-weight: 800;
  color: #0a0a0a;
  margin: 0 0 12px;
  letter-spacing: -0.01em;
}

.sector-section-desc {
  font-size: 16px;
  color: #64748b;
  margin: 0 auto;
  max-width: 500px;
  line-height: 1.6;
}

/* ═══ Category Grid ═══ */
.category-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.category-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.category-card:hover {
  border-color: transparent;
  box-shadow: 0 12px 40px rgba(0,0,0,0.1);
  transform: translateY(-6px);
}

.category-card-img {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.category-card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.category-card:hover .category-card-img img {
  transform: scale(1.08);
}

.category-card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 40%, rgba(0,0,0,0.3) 100%);
}

.category-icon-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(8px);
}

.category-card-body {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.category-card-body h4 {
  font-size: 16px;
  font-weight: 700;
  color: #0a0a0a;
  margin: 0 0 8px;
}

.category-card-body p {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 12px;
  flex: 1;
}

.category-link {
  font-size: 13px;
  font-weight: 600;
  color: #0000C9;
}

/* ═══ Two Column ═══ */
.sector-two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.sector-two-col-text h2 {
  font-size: 32px;
  font-weight: 800;
  color: #0a0a0a;
  margin: 0 0 12px;
}

.sector-two-col-text > p {
  font-size: 16px;
  color: #64748b;
  margin: 0 0 28px;
  line-height: 1.6;
}

.article-list { display: flex; flex-direction: column; }

.article-item {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 14px 0;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
  transition: padding-left 0.2s;
  overflow: hidden;
  min-width: 0;
}

.article-item:hover { padding-left: 8px; }

.article-date { font-size: 13px; color: #94a3b8; white-space: nowrap; font-weight: 500; }
.article-sep { color: #cbd5e1; font-size: 12px; }
.article-cat { font-size: 13px; color: #0000C9; font-weight: 600; white-space: nowrap; }
.article-title {
  font-size: 14px;
  color: #1e293b;
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
  flex: 1;
}
.article-item:hover .article-title { color: #0000C9; text-decoration: underline; }

.sector-two-col-visual {
  display: flex;
  justify-content: center;
}

.visual-card {
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  aspect-ratio: 4/3;
}

.visual-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.visual-card-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 32px 24px 24px;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 100%);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.visual-label {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.visual-sublabel {
  font-size: 13px;
  color: rgba(255,255,255,0.7);
}

/* ═══ Stats ═══ */
.sector-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.sector-stat-card {
  text-align: center;
  padding: 40px 24px;
  background: #F8FAFC;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s;
}

.sector-stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}

.sector-stat-number {
  display: block;
  font-size: 42px;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 8px;
}

.sector-stat-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

/* ═══ Responsive ═══ */
@media (max-width: 1024px) {
  .sector-container { padding: 0 20px; }
  .sector-hero { padding: 140px 0 80px; min-height: 400px; }
  .sector-hero h1 { font-size: 40px; }
  .category-grid { grid-template-columns: repeat(2, 1fr); }
  .sector-two-col { grid-template-columns: 1fr; gap: 48px; }
  .sector-stats-grid { grid-template-columns: repeat(2, 1fr); }
  .sector-section { padding: 80px 0; }
}

@media (max-width: 640px) {
  .sector-hero { padding: 120px 0 60px; min-height: 360px; }
  .sector-hero h1 { font-size: 32px; }
  .sector-hero p { font-size: 16px; }
  .category-grid { grid-template-columns: 1fr; }
  .category-card-img { height: 140px; }
  .sector-stats-grid { grid-template-columns: 1fr 1fr; gap: 16px; }
  .sector-section-header h2 { font-size: 28px; }
  .sector-two-col-text h2 { font-size: 24px; }
  .sector-stat-number { font-size: 32px; }
  .sector-hero-actions { flex-direction: column; }
  .pf-btn-white, .pf-btn-outline { text-align: center; justify-content: center; }
}
</style>
