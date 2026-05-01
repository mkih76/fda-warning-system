<template>
  <div class="letters-page">
    <!-- 页头 -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div class="header-text">
            <nav class="breadcrumb">
              <router-link to="/">首页</router-link>
              <span class="separator">/</span>
              <span class="current">警告信列表</span>
            </nav>
            <h1 class="page-title">警告信列表</h1>
            <p class="page-description">
              浏览 FDA 最新警告信，支持搜索和筛选
            </p>
          </div>
          <div class="header-actions">
            <button @click="exportCSV" class="btn btn-secondary" :disabled="exporting">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              {{ exporting ? '导出中...' : '导出 CSV' }}
            </button>
            <div class="results-count">
              <span class="count-number">{{ total }}</span>
              <span class="count-label">条记录</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索与筛选 -->
    <div class="filter-section">
      <div class="container">
        <div class="filter-card">
          <!-- 主搜索栏 -->
          <div class="search-bar">
            <div class="search-input-wrapper">
              <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="搜索公司名、FDA ID、主题..."
                class="search-input"
                @input="handleSearchInput"
                @keyup.enter="doSearch"
              />
              <button v-if="searchQuery" @click="clearSearch" class="clear-btn">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <button @click="doSearch" class="btn btn-primary search-btn">
              搜索
            </button>
          </div>

          <!-- 搜索建议 -->
          <SearchSuggestions
            :query="searchQuery"
            :show-suggestions="showSuggestions"
            @select="selectSuggestion"
          />

          <!-- 筛选器 -->
          <div class="filters">
            <div class="filter-row">
              <div class="filter-group">
                <label class="filter-label">签发办公室</label>
                <select v-model="filterOffice" @change="applyFilters" class="select">
                  <option value="">全部办公室</option>
                  <option v-for="office in offices" :key="office" :value="office">
                    {{ office }}
                  </option>
                </select>
              </div>

              <div class="filter-group">
                <label class="filter-label">状态</label>
                <select v-model="filterStatus" @change="applyFilters" class="select">
                  <option value="">全部状态</option>
                  <option value="active">进行中</option>
                  <option value="closed">已关闭</option>
                </select>
              </div>

              <div class="filter-group">
                <label class="filter-label">违规类型</label>
                <select v-model="filterViolationType" @change="applyFilters" class="select">
                  <option value="">全部类型</option>
                  <option v-for="vType in violationTypes" :key="vType" :value="vType">
                    {{ vType }}
                  </option>
                </select>
              </div>

              <div class="filter-group">
                <label class="filter-label">风险等级</label>
                <select v-model="filterRiskLevel" @change="applyFilters" class="select">
                  <option value="">全部等级</option>
                  <option value="High">高风险</option>
                  <option value="Medium">中风险</option>
                  <option value="Low">低风险</option>
                </select>
              </div>
            </div>

            <div class="filter-row">
              <div class="filter-group date-range">
                <label class="filter-label">日期范围</label>
                <div class="date-inputs">
                  <input
                    v-model="filterDateFrom"
                    type="date"
                    class="input date-input"
                    placeholder="开始日期"
                  />
                  <span class="date-separator">至</span>
                  <input
                    v-model="filterDateTo"
                    type="date"
                    class="input date-input"
                    placeholder="结束日期"
                  />
                </div>
              </div>

              <div class="filter-actions">
                <button @click="applyFilters" class="btn btn-primary btn-sm">
                  应用筛选
                </button>
                <button @click="resetFilters" class="btn btn-ghost btn-sm">
                  重置
                </button>
              </div>
            </div>

            <!-- 活跃筛选标签 -->
            <div v-if="hasActiveFilters" class="active-filters">
              <span class="active-filters-label">当前筛选：</span>
              <div class="filter-tags">
                <span v-if="searchQuery" class="tag tag-removable" @click="clearSearch">
                  搜索: {{ searchQuery }}
                  <span class="tag-remove">×</span>
                </span>
                <span v-if="filterOffice" class="tag tag-removable" @click="filterOffice = ''; applyFilters()">
                  {{ filterOffice }}
                  <span class="tag-remove">×</span>
                </span>
                <span v-if="filterStatus" class="tag tag-removable" @click="filterStatus = ''; applyFilters()">
                  {{ filterStatus === 'active' ? '进行中' : '已关闭' }}
                  <span class="tag-remove">×</span>
                </span>
                <span v-if="filterViolationType" class="tag tag-removable" @click="filterViolationType = ''; applyFilters()">
                  {{ filterViolationType }}
                  <span class="tag-remove">×</span>
                </span>
                <span v-if="filterRiskLevel" class="tag tag-removable" @click="filterRiskLevel = ''; applyFilters()">
                  {{ filterRiskLevel }}风险
                  <span class="tag-remove">×</span>
                </span>
              </div>
              <button @click="resetFilters" class="btn btn-ghost btn-xs">
                清除全部
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-section">
      <div class="container">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-grid">
          <div v-for="n in 6" :key="n" class="skeleton-card">
            <div class="skeleton skeleton-header"></div>
            <div class="skeleton skeleton-body"></div>
            <div class="skeleton skeleton-footer"></div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else-if="letters.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3>暂无警告信</h3>
          <p>尝试调整筛选条件或搜索关键词</p>
          <button @click="resetFilters" class="btn btn-primary">
            重置筛选
          </button>
        </div>

        <!-- 信件列表 -->
        <div v-else>
          <div class="letters-grid">
            <div
              v-for="(letter, index) in letters"
              :key="letter.id"
              class="letter-card animate-fade-in-up"
              :style="{ animationDelay: `${index * 50}ms` }"
              @click="$router.push(`/letters/${letter.id}`)"
            >
              <!-- 卡片头部 -->
              <div class="letter-header">
                <div class="letter-badges">
                  <span class="badge badge-dot" :class="getStatusBadgeClass(letter.status)">
                    {{ letter.status === 'active' ? '进行中' : '已关闭' }}
                  </span>
                  <span v-if="letter.risk_level" class="badge" :class="getRiskBadgeClass(letter.risk_level)">
                    {{ letter.risk_level }}
                  </span>
                </div>
                <button
                  class="favorite-btn"
                  :class="{ 'is-favorite': isFavorite(letter.id) }"
                  @click.stop="toggleFavorite(letter.id)"
                  :title="isFavorite(letter.id) ? '取消收藏' : '收藏'"
                >
                  <svg viewBox="0 0 24 24" :fill="isFavorite(letter.id) ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </button>
              </div>

              <!-- 卡片内容 -->
              <div class="letter-content">
                <div class="letter-id">{{ letter.fda_id }}</div>
                <h3 class="letter-company">{{ letter.company_name }}</h3>
                <p class="letter-subject">{{ cleanText(letter.summary_zh || letter.subject) }}</p>
              </div>

              <!-- 卡片元数据 -->
              <div class="letter-meta">
                <div class="meta-item">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>{{ letter.issue_date || '待确定' }}</span>
                </div>
                <div class="meta-item">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  <span>{{ letter.issuing_office || 'FDA' }}</span>
                </div>
              </div>

              <!-- AI 分析预览 -->
              <div v-if="letter.summary_zh" class="letter-preview">
                <div class="preview-label">AI 摘要</div>
                <p class="preview-text">{{ letter.summary_zh }}</p>
              </div>
            </div>
          </div>

          <!-- 分页 -->
          <div v-if="total > perPage" class="pagination-wrapper">
            <div class="pagination-info">
              显示第 {{ (page - 1) * perPage + 1 }}-{{ Math.min(page * perPage, total) }} 条，共 {{ total }} 条
            </div>
            <div class="pagination">
              <button
                @click="changePage(page - 1)"
                :disabled="page <= 1"
                class="pagination-btn"
                title="上一页"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>

              <template v-for="p in visiblePages" :key="p">
                <button
                  v-if="p === '...'"
                  disabled
                  class="pagination-ellipsis"
                >
                  ...
                </button>
                <button
                  v-else
                  @click="changePage(p)"
                  :class="['pagination-btn', p === page ? 'pagination-btn-active' : '']"
                >
                  {{ p }}
                </button>
              </template>

              <button
                @click="changePage(page + 1)"
                :disabled="page >= maxPage"
                class="pagination-btn"
                title="下一页"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFavorites } from '../composables/useFavorites.js'
import SearchSuggestions from '../components/SearchSuggestions.vue'

const API = window.location.origin + '/api'
const { isFavorite, toggleFavorite } = useFavorites()

// 过滤 *# 等无关注释符号
function cleanText(text) {
  if (!text) return ''
  return text.replace(/[*#]/g, '').replace(/\s+/g, ' ').trim()
}

// 状态
const letters = ref([])
const loading = ref(true)
const exporting = ref(false)
const page = ref(1)
const total = ref(0)
const perPage = 20

// 搜索与筛选
const searchQuery = ref('')
const showSuggestions = ref(false)
const filterOffice = ref('')
const filterStatus = ref('')
const filterViolationType = ref('')
const filterRiskLevel = ref('')
const filterDateFrom = ref('')
const filterDateTo = ref('')

// 选项数据
const offices = ref([])
const violationTypes = ref([])

// 计算属性
const maxPage = computed(() => Math.ceil(total.value / perPage) || 1)

const visiblePages = computed(() => {
  const pages = []
  const totalPages = maxPage.value
  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) pages.push(i)
    return pages
  }
  pages.push(1)
  if (page.value > 3) pages.push('...')
  for (let i = Math.max(2, page.value - 1); i <= Math.min(totalPages - 1, page.value + 1); i++) {
    pages.push(i)
  }
  if (page.value < totalPages - 2) pages.push('...')
  pages.push(totalPages)
  return pages
})

const hasActiveFilters = computed(() => {
  return searchQuery.value || filterOffice.value || filterStatus.value ||
         filterViolationType.value || filterRiskLevel.value ||
         filterDateFrom.value || filterDateTo.value
})

// 方法
function handleSearchInput() {
  showSuggestions.value = searchQuery.value.length >= 2
}

function selectSuggestion(text) {
  searchQuery.value = text
  showSuggestions.value = false
  doSearch()
}

function clearSearch() {
  searchQuery.value = ''
  showSuggestions.value = false
  applyFilters()
}

function doSearch() {
  page.value = 1
  showSuggestions.value = false
  fetchData()
}

function applyFilters() {
  page.value = 1
  fetchData()
}

function resetFilters() {
  searchQuery.value = ''
  filterOffice.value = ''
  filterStatus.value = ''
  filterViolationType.value = ''
  filterRiskLevel.value = ''
  filterDateFrom.value = ''
  filterDateTo.value = ''
  page.value = 1
  fetchData()
}

function changePage(p) {
  if (p < 1 || p > maxPage.value) return
  page.value = p
  fetchData()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function fetchData() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.set('page', page.value)
    params.set('page_size', perPage)
    if (searchQuery.value) params.set('search', searchQuery.value)
    if (filterOffice.value) params.set('office', filterOffice.value)
    if (filterStatus.value) params.set('status', filterStatus.value)
    if (filterViolationType.value) params.set('violation_type', filterViolationType.value)
    if (filterRiskLevel.value) params.set('risk_level', filterRiskLevel.value)
    if (filterDateFrom.value) params.set('date_from', filterDateFrom.value)
    if (filterDateTo.value) params.set('date_to', filterDateTo.value)

    const resp = await fetch(`${API}/letters?${params}`)
    const data = await resp.json()
    letters.value = data.items || []
    total.value = data.total || 0
  } catch (e) {
    console.error('获取警告信失败:', e)
    letters.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

async function fetchOffices() {
  try {
    const resp = await fetch(`${API}/offices`)
    offices.value = await resp.json()
  } catch (e) {
    console.error('获取办公室列表失败:', e)
  }
}

async function fetchViolationTypes() {
  try {
    const resp = await fetch(`${API}/violation-types`)
    violationTypes.value = await resp.json()
  } catch (e) {
    console.error('获取违规类型失败:', e)
  }
}

async function exportCSV() {
  exporting.value = true
  try {
    const params = new URLSearchParams()
    if (searchQuery.value) params.set('search', searchQuery.value)
    if (filterOffice.value) params.set('office', filterOffice.value)
    if (filterStatus.value) params.set('status', filterStatus.value)

    const resp = await fetch(`${API}/letters/export/csv?${params}`)
    const blob = await resp.blob()

    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `fda_letters_${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (e) {
    console.error('导出失败:', e)
    alert('导出失败，请稍后重试')
  } finally {
    exporting.value = false
  }
}

function getStatusBadgeClass(status) {
  return status === 'active' ? 'badge-danger' : 'badge-success'
}

function getRiskBadgeClass(riskLevel) {
  const classes = {
    'High': 'badge-danger',
    'Medium': 'badge-warning',
    'Low': 'badge-success'
  }
  return classes[riskLevel] || 'badge-info'
}

// 初始化
onMounted(() => {
  fetchOffices()
  fetchViolationTypes()
  fetchData()
})
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════
   Page Layout
═══════════════════════════════════════════════════════════════ */
.letters-page {
  min-height: 100vh;
  background: #ffffff;
  padding-top: var(--header-height);
  font-family: 'Noto Sans', 'Noto Sans SC', Arial, sans-serif;
}

/* ═══════════════════════════════════════════════════════════════
   Page Header
═══════════════════════════════════════════════════════════════ */
.page-header {
  background: #f5f5f5;
  border-bottom: 1px solid #e5e7eb;
  padding: var(--space-8) 0;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

@media (min-width: 768px) {
  .header-content {
    flex-direction: row;
    align-items: flex-end;
    justify-content: space-between;
  }
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  margin-bottom: var(--space-2);
}

.breadcrumb a {
  color: var(--text-secondary);
  text-decoration: none;
}

.breadcrumb a:hover {
  color: #0000C9;
}

.breadcrumb .separator {
  color: var(--text-tertiary);
}

.breadcrumb .current {
  color: var(--text-primary);
  font-weight: var(--font-medium);
}

.page-title {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  color: #000;
  margin-bottom: var(--space-2);
  font-family: 'Noto Sans', Arial, sans-serif;
}

.page-description {
  font-size: var(--text-base);
  color: var(--text-secondary);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.results-count {
  display: flex;
  align-items: baseline;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-4);
  background: var(--bg-tertiary);
  border-radius: 4px;
}

.count-number {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: #0000C9;
}

.count-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

/* ═══════════════════════════════════════════════════════════════
   Filter Section
═══════════════════════════════════════════════════════════════ */
.filter-section {
  padding: var(--space-6) 0;
}

.filter-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: 8px;
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
}

/* Search Bar */
.search-bar {
  display: flex;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
  position: relative;
}

.search-input-wrapper {
  flex: 1;
  position: relative;
}

.search-icon {
  position: absolute;
  left: var(--space-4);
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: var(--text-tertiary);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: var(--space-3) var(--space-10) var(--space-3) var(--space-12);
  background: var(--bg-secondary);
  border: 2px solid var(--border-default);
  border-radius: 4px;
  font-size: var(--text-base);
  color: var(--text-primary);
  transition: all var(--duration-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary-500);
  background: var(--bg-primary);
  box-shadow: 0 0 0 3px rgba(0, 0, 201, 0.15);
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.clear-btn {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  padding: var(--space-1);
  color: var(--text-tertiary);
  border-radius: var(--radius-md);
  transition: all var(--duration-fast);
}

.clear-btn:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.search-btn {
  flex-shrink: 0;
}

/* Filters */
.filters {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  align-items: flex-end;
}

.filter-group {
  flex: 1;
  min-width: 150px;
}

.filter-label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-secondary);
  margin-bottom: var(--space-2);
}

.date-range {
  flex: 2;
  min-width: 250px;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.date-input {
  flex: 1;
}

.date-separator {
  color: var(--text-tertiary);
  font-size: var(--text-sm);
}

.filter-actions {
  display: flex;
  gap: var(--space-2);
  align-items: flex-end;
}

/* Active Filters */
.active-filters {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--border-default);
  flex-wrap: wrap;
}

.active-filters-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-secondary);
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

/* ═══════════════════════════════════════════════════════════════
   Content Section
═══════════════════════════════════════════════════════════════ */
.content-section {
  padding: var(--space-6) 0 var(--space-12);
}

/* Loading Grid */
.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: var(--space-6);
}

.skeleton-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: 8px;
  padding: var(--space-5);
}

.skeleton-header {
  height: 24px;
  width: 40%;
  margin-bottom: var(--space-4);
}

.skeleton-body {
  height: 60px;
  margin-bottom: var(--space-4);
}

.skeleton-footer {
  height: 16px;
  width: 60%;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-16) var(--space-6);
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  color: var(--text-tertiary);
  opacity: 0.5;
  margin-bottom: var(--space-6);
}

.empty-state h3 {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.empty-state p {
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin-bottom: var(--space-6);
}

/* ═══════════════════════════════════════════════════════════════
   Letters Grid
═══════════════════════════════════════════════════════════════ */
.letters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: var(--space-6);
}

.letter-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: 8px;
  padding: var(--space-5);
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-default);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.letter-card:hover {
  border-color: #0000C9;
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

/* Letter Header */
.letter-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.letter-badges {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.favorite-btn {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  border-radius: var(--radius-lg);
  transition: all var(--duration-fast);
}

.favorite-btn:hover {
  color: var(--color-danger-500);
  background: rgba(239, 68, 68, 0.1);
}

.favorite-btn.is-favorite {
  color: var(--color-danger-500);
}

.favorite-btn svg {
  width: 20px;
  height: 20px;
}

/* Letter Content */
.letter-content {
  flex: 1;
}

.letter-id {
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  color: var(--text-tertiary);
  margin-bottom: var(--space-2);
}

.letter-company {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
  line-height: var(--leading-tight);
}

.letter-subject {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Letter Meta */
.letter-meta {
  display: flex;
  gap: var(--space-4);
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-default);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}

.meta-item svg {
  flex-shrink: 0;
}

/* Letter Preview */
.letter-preview {
  background: var(--bg-tertiary);
  border-radius: 4px;
  padding: var(--space-3);
}

.preview-label {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  color: var(--text-secondary);
  margin-bottom: var(--space-1);
}

.preview-text {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 0;
}

/* ═══════════════════════════════════════════════════════════════
   Pagination
═══════════════════════════════════════════════════════════════ */
.pagination-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  margin-top: var(--space-10);
  padding-top: var(--space-6);
  border-top: 1px solid var(--border-default);
}

@media (min-width: 640px) {
  .pagination-wrapper {
    flex-direction: row;
    justify-content: space-between;
  }
}

.pagination-info {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}
</style>
