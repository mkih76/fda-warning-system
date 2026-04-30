<template>
  <div class="articles-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <span class="section-eyebrow">深度内容</span>
        <h1>专业分析与合规指南</h1>
        <p>基于FDA真实数据的深度分析、合规指南与案例研究</p>
      </div>
    </div>

    <!-- 分类标签 -->
    <div class="category-section">
      <div class="category-container">
        <button 
          v-for="cat in categories" 
          :key="cat.value"
          :class="['category-btn', { active: activeCategory === cat.value }]"
          @click="activeCategory = cat.value"
        >
          <span class="cat-icon">{{ cat.icon }}</span>
          {{ cat.label }}
          <span class="count" v-if="cat.count">{{ cat.count }}</span>
        </button>
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="content-section">
      <div class="content-container">
        <!-- 加载中 -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <!-- 空状态 -->
        <div v-else-if="articles.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
          <p>暂无文章</p>
        </div>

        <!-- 文章网格 -->
        <div v-else class="articles-grid">
          <a 
            v-for="article in articles" 
            :key="article.id"
            :href="article.source_url" 
            target="_blank" 
            rel="noopener noreferrer"
            class="article-card"
          >
            <div class="card-category" :class="getCategoryClass(article.category)">
              {{ article.category }}
            </div>
            <h3 class="card-title">{{ article.title }}</h3>
            <div class="card-footer">
              <span class="source-name">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="link-icon">
                  <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                  <polyline points="15 3 21 3 21 9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
                {{ article.source_name }}
              </span>
              <span class="arrow">→</span>
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const API = window.location.origin + '/api'

const articles = ref([])
const loading = ref(true)
const activeCategory = ref('')

const categories = ref([
  { label: '全部', value: '', icon: '📚', count: 0 },
  { label: '深度分析', value: '深度分析', icon: '📊', count: 0 },
  { label: '合规指南', value: '合规指南', icon: '📘', count: 0 },
  { label: '案例研究', value: '案例研究', icon: '📋', count: 0 },
])

function getCategoryClass(category) {
  const classes = {
    '深度分析': 'cat-analysis',
    '合规指南': 'cat-guide',
    '案例研究': 'cat-case',
    '行业文章': 'cat-article'
  }
  return classes[category] || 'cat-default'
}

async function fetchArticles() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (activeCategory.value) params.set('category', activeCategory.value)
    
    const resp = await fetch(`${API}/articles?${params}`)
    const data = await resp.json()
    articles.value = data.items || []
    
    // 更新分类计数
    if (!activeCategory.value) {
      const counts = {}
      articles.value.forEach(a => {
        counts[a.category] = (counts[a.category] || 0) + 1
      })
      categories.value.forEach(cat => {
        cat.count = counts[cat.value] || 0
      })
    }
  } catch (e) {
    console.error('获取文章失败:', e)
    articles.value = []
  } finally {
    loading.value = false
  }
}

watch(activeCategory, () => {
  fetchArticles()
})

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.articles-page {
  min-height: 100vh;
  background: #f8fafc;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #0000C9 0%, #000049 100%);
  padding: 120px 32px 60px;
  text-align: center;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
}

.section-eyebrow {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 12px;
}

.page-header h1 {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 700;
  color: white;
  margin: 0 0 16px 0;
}

.page-header p {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

/* 分类标签 */
.category-section {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 16px 32px;
  position: sticky;
  top: 56px;
  z-index: 50;
}

.category-container {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.category-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  background: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-btn:hover {
  border-color: #0000C9;
  color: #0000C9;
}

.category-btn.active {
  background: #0000C9;
  border-color: #0000C9;
  color: white;
}

.cat-icon {
  font-size: 16px;
}

.count {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.1);
}

.category-btn.active .count {
  background: rgba(255, 255, 255, 0.2);
}

/* 内容区域 */
.content-section {
  padding: 40px 32px;
}

.content-container {
  max-width: 1280px;
  margin: 0 auto;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 0;
  color: #64748b;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #0000C9;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 0;
  color: #64748b;
}

.empty-state svg {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.3;
}

/* 文章网格 */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
}

.article-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.article-card:hover {
  border-color: #0000C9;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.1);
  transform: translateY(-2px);
}

.card-category {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 12px;
  width: fit-content;
}

.cat-analysis {
  background: rgba(0, 102, 204, 0.1);
  color: #0000C9;
}

.cat-guide {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.cat-case {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.cat-article {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.cat-default {
  background: #f1f5f9;
  color: #64748b;
}

.card-title {
  font-size: 17px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 16px 0;
  line-height: 1.5;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.source-name {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #0000C9;
  font-weight: 500;
}

.link-icon {
  width: 14px;
  height: 14px;
}

.arrow {
  font-size: 18px;
  color: #94a3b8;
  transition: all 0.2s;
}

.article-card:hover .arrow {
  color: #0000C9;
  transform: translateX(4px);
}

/* 响应式 */
@media (max-width: 768px) {
  .articles-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    padding: 100px 20px 40px;
  }
  
  .content-section {
    padding: 24px 16px;
  }
}
</style>
