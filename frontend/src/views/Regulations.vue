<template>
  <div class="regulations-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <span class="section-eyebrow">法规信息</span>
        <h1>法规动态追踪</h1>
        <p>实时追踪中国NMPA、美国FDA、欧盟EMA等全球药品监管法规动态</p>
      </div>
    </div>

    <!-- 筛选器 -->
    <div class="filters-section">
      <div class="filters-container">
        <div class="filter-group">
          <label>地区</label>
          <select v-model="filterRegion" @change="fetchRegulations">
            <option value="">全部地区</option>
            <option value="中国">中国</option>
            <option value="美国">美国</option>
            <option value="欧盟">欧盟</option>
          </select>
        </div>
        <div class="filter-group">
          <label>行业</label>
          <select v-model="filterIndustry" @change="fetchRegulations">
            <option value="">全部行业</option>
            <option value="制药">制药</option>
            <option value="化妆品">化妆品</option>
            <option value="食品">食品</option>
          </select>
        </div>
        <div class="filter-group">
          <label>时间</label>
          <select v-model="filterTime" @change="fetchRegulations">
            <option value="">全部时间</option>
            <option value="week">最近一周</option>
            <option value="month">最近一月</option>
            <option value="quarter">最近三月</option>
          </select>
        </div>
        <button class="reset-btn" @click="resetFilters">重置</button>
      </div>
    </div>

    <!-- 法规列表 -->
    <div class="content-section">
      <div class="content-container">
        <div class="results-header">
          <span class="results-count">共 {{ total }} 条法规</span>
        </div>

        <!-- 加载中 -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <!-- 空状态 -->
        <div v-else-if="regulations.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <p>暂无法规数据</p>
          <button @click="runCrawler" class="cta-btn">立即采集</button>
        </div>

        <!-- 法规列表 -->
        <div v-else class="regulations-list">
          <div class="regulation-card" v-for="reg in regulations" :key="reg.id">
            <div class="card-header">
              <span class="region-badge" :class="getRegionClass(reg.region)">
                {{ reg.region }}
              </span>
              <span class="source-badge">{{ reg.source }}</span>
              <span class="date">{{ reg.publish_date || '日期未知' }}</span>
            </div>
            <h3 class="card-title">{{ reg.title }}</h3>
            <p class="card-summary" v-if="reg.summary">{{ reg.summary }}</p>
            <div class="card-footer">
              <a :href="reg.url" target="_blank" class="view-link">
                查看原文
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
              <a v-if="reg.pdf_url" :href="reg.pdf_url" target="_blank" class="pdf-link">
                下载PDF
              </a>
            </div>
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

const regulations = ref([])
const loading = ref(true)
const total = ref(0)
const page = ref(1)
const perPage = 20

const filterRegion = ref('')
const filterIndustry = ref('')
const filterTime = ref('')

const totalPages = computed(() => Math.ceil(total.value / perPage) || 1)

function getRegionClass(region) {
  const classes = {
    '中国': 'region-china',
    '美国': 'region-usa',
    '欧盟': 'region-eu'
  }
  return classes[region] || 'region-default'
}

async function fetchRegulations() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.set('page', page.value)
    params.set('page_size', perPage)
    if (filterRegion.value) params.set('region', filterRegion.value)
    if (filterIndustry.value) params.set('industry', filterIndustry.value)
    if (filterTime.value) params.set('time_range', filterTime.value)

    const resp = await fetch(`${API}/regulations?${params}`)
    const data = await resp.json()
    regulations.value = data.items || []
    total.value = data.total || 0
  } catch (e) {
    console.error('获取法规失败:', e)
    regulations.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function resetFilters() {
  filterRegion.value = ''
  filterIndustry.value = ''
  filterTime.value = ''
  page.value = 1
  fetchRegulations()
}

function prevPage() {
  if (page.value > 1) {
    page.value--
    fetchRegulations()
  }
}

function nextPage() {
  if (page.value < totalPages.value) {
    page.value++
    fetchRegulations()
  }
}

async function runCrawler() {
  try {
    await fetch(`${API}/crawler/regulations`, { method: 'POST' })
    alert('爬虫已启动，请稍后刷新页面')
  } catch (e) {
    console.error('启动爬虫失败:', e)
  }
}

onMounted(() => {
  fetchRegulations()
})
</script>

<style scoped>
.regulations-page {
  min-height: 100vh;
  background: #f8fafc;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #0093D0 0%, #0052CC 100%);
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

/* 筛选器 */
.filters-section {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 20px 32px;
}

.filters-container {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  gap: 20px;
  align-items: flex-end;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-group label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filter-group select {
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  min-width: 150px;
  background: white;
  cursor: pointer;
}

.reset-btn {
  padding: 10px 20px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.reset-btn:hover {
  border-color: #0093D0;
  color: #0093D0;
}

/* 内容区域 */
.content-section {
  padding: 40px 32px;
}

.content-container {
  max-width: 1280px;
  margin: 0 auto;
}

.results-header {
  margin-bottom: 24px;
}

.results-count {
  font-size: 14px;
  color: #64748b;
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
  border-top-color: #0093D0;
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
  background: #0093D0;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.cta-btn:hover {
  background: #0077b3;
}

/* 法规列表 */
.regulations-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.regulation-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.2s;
}

.regulation-card:hover {
  border-color: #0093D0;
  box-shadow: 0 4px 12px rgba(0, 147, 208, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.region-badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.region-china {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.region-usa {
  background: rgba(0, 147, 208, 0.1);
  color: #0093D0;
}

.region-eu {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.source-badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  background: #f1f5f9;
  color: #64748b;
}

.date {
  font-size: 13px;
  color: #94a3b8;
  margin-left: auto;
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
}

.card-footer {
  display: flex;
  gap: 16px;
}

.view-link,
.pdf-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s;
}

.view-link {
  color: #0093D0;
}

.view-link svg {
  width: 16px;
  height: 16px;
}

.view-link:hover {
  color: #0077b3;
}

.pdf-link {
  color: #dc2626;
}

.pdf-link:hover {
  color: #b91c1c;
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
  border-color: #0093D0;
  color: #0093D0;
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
  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-group select {
    width: 100%;
  }
}
</style>
