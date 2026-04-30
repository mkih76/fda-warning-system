<template>
  <div class="news-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <span class="section-eyebrow">行业资讯</span>
        <h1>行业动态聚合</h1>
        <p>实时聚合FDA、NMPA及全球制药/化妆品/食品行业最新资讯</p>
      </div>
    </div>

    <!-- 分类标签 -->
    <div class="category-section">
      <div class="category-container">
        <button 
          v-for="cat in categories" 
          :key="cat.value"
          :class="['category-btn', { active: activeCategory === cat.value }]"
          @click="activeCategory = cat.value; fetchNews()"
        >
          {{ cat.label }}
          <span class="count" v-if="cat.count">{{ cat.count }}</span>
        </button>
      </div>
    </div>

    <!-- 新闻列表 -->
    <div class="content-section">
      <div class="content-container">
        <!-- 加载中 -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <!-- 空状态 -->
        <div v-else-if="newsList.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
          </svg>
          <p>暂无新闻数据</p>
          <button @click="runAggregator" class="cta-btn">立即采集</button>
        </div>

        <!-- 新闻网格 -->
        <div v-else class="news-grid">
          <div class="news-card" v-for="news in newsList" :key="news.id">
            <div class="card-category" :class="getCategoryClass(news.category)">
              {{ news.category }}
            </div>
            <h3 class="card-title">{{ news.title }}</h3>
            <p class="card-summary" v-if="news.summary">{{ news.summary }}</p>
            <div class="card-meta">
              <span class="source">{{ news.source }}</span>
              <span class="date">{{ news.publish_date || '日期未知' }}</span>
            </div>
            <a :href="news.source_url" target="_blank" class="read-more">
              阅读原文
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 8l4 4m0 0l-4 4m4-4H3"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- 分页 -->
        <div v-if="total > 0" class="pagination">
          <button @click="prevPage" :disabled="page <= 1" class="page-btn">
            上一页
          </button>
          <span class="page-info">第 {{ page }} 页 / 共 {{ totalPages }} 页</span>
          <button @click="nextPage" :disabled="page >= totalPages" class="page-btn">
            下一页
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API = window.location.origin + '/api'

const newsList = ref([])
const loading = ref(true)
const total = ref(0)
const page = ref(1)
const perPage = 20

const activeCategory = ref('')

const categories = ref([
  { label: '全部', value: '', count: 0 },
  { label: '国际动态', value: '国际动态', count: 0 },
  { label: '国内动态', value: '国内动态', count: 0 },
  { label: '法规信息', value: '法规信息', count: 0 },
  { label: '行业资讯', value: '行业资讯', count: 0 }
])

const totalPages = computed(() => Math.ceil(total.value / perPage) || 1)

function getCategoryClass(category) {
  const classes = {
    '国际动态': 'cat-international',
    '国内动态': 'cat-domestic',
    '法规信息': 'cat-regulation',
    '行业资讯': 'cat-industry'
  }
  return classes[category] || 'cat-default'
}

async function fetchNews() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.set('page', page.value)
    params.set('page_size', perPage)
    if (activeCategory.value) params.set('category', activeCategory.value)

    const resp = await fetch(`${API}/news?${params}`)
    const data = await resp.json()
    newsList.value = data.items || []
    total.value = data.total || 0
    
    // 更新分类计数
    if (data.category_counts) {
      categories.value.forEach(cat => {
        cat.count = data.category_counts[cat.value] || 0
      })
    }
  } catch (e) {
    console.error('获取新闻失败:', e)
    newsList.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function prevPage() {
  if (page.value > 1) {
    page.value--
    fetchNews()
  }
}

function nextPage() {
  if (page.value < totalPages.value) {
    page.value++
    fetchNews()
  }
}

async function runAggregator() {
  try {
    await fetch(`${API}/crawler/news`, { method: 'POST' })
    alert('聚合器已启动，请稍后刷新页面')
  } catch (e) {
    console.error('启动聚合器失败:', e)
  }
}

onMounted(() => {
  fetchNews()
})
</script>

<style scoped>
.news-page {
  min-height: 100vh;
  background: #f8fafc;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
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
  border-color: #10B981;
  color: #10B981;
}

.category-btn.active {
  background: #10B981;
  border-color: #10B981;
  color: white;
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
  border-top-color: #10B981;
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

.cta-btn {
  margin-top: 16px;
  padding: 12px 24px;
  background: #10B981;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.cta-btn:hover {
  background: #059669;
}

/* 新闻网格 */
.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.news-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
}

.news-card:hover {
  border-color: #10B981;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
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

.cat-international {
  background: rgba(0, 147, 208, 0.1);
  color: #0093D0;
}

.cat-domestic {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.cat-regulation {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.cat-industry {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.cat-default {
  background: #f1f5f9;
  color: #64748b;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.card-summary {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 16px 0;
  flex: 1;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 16px;
}

.read-more {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #10B981;
  text-decoration: none;
  transition: gap 0.2s;
}

.read-more svg {
  width: 16px;
  height: 16px;
}

.read-more:hover {
  gap: 10px;
}

/* 分页 */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.page-btn {
  padding: 10px 20px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: #10B981;
  color: #10B981;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #64748b;
}

/* 响应式 */
@media (max-width: 768px) {
  .news-grid {
    grid-template-columns: 1fr;
  }
}
</style>
