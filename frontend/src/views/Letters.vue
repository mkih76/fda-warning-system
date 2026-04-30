<template>
  <div class="letters-page">
    <!-- 页头 -->
    <div class="page-header">
      <div>
        <h1 class="page-title">警告信列表</h1>
        <p class="page-subtitle">浏览 FDA 最新警告信，支持搜索和筛选</p>
      </div>
      <div class="page-status">
        <span class="status-dot"></span>
        <span>共 {{ total }} 条记录</span>
      </div>
    </div>

    <!-- 搜索 + 筛选栏 -->
    <div class="filter-bar">
      <div class="filter-row">
        <!-- 搜索组件 -->
        <div class="search-wrapper">
          <SearchBar v-model="searchQuery" placeholder="搜索公司名、FDA ID..." @search="doSearch" />
        </div>
        <!-- 办公室筛选 -->
        <select v-model="filterOffice" @change="applyFilters" class="filter-select">
          <option value="">全部办公室</option>
          <option v-for="o in offices" :key="o" :value="o">{{ o }}</option>
        </select>
        <!-- 状态筛选 -->
        <select v-model="filterStatus" @change="applyFilters" class="filter-select">
          <option value="">全部状态</option>
          <option value="active">进行中</option>
          <option value="closed">已关闭</option>
        </select>
        <button @click="doSearch" class="btn-primary">搜索</button>
      </div>
      
      <!-- 高级筛选 -->
      <div class="filter-row filter-advanced">
        <select v-model="filterViolationType" @change="applyFilters" class="filter-select">
          <option value="">全部违规类型</option>
          <option v-for="v in violationTypes" :key="v" :value="v">{{ v }}</option>
        </select>
        <select v-model="filterRiskLevel" @change="applyFilters" class="filter-select">
          <option value="">全部风险等级</option>
          <option value="High">高风险</option>
          <option value="Medium">中风险</option>
          <option value="Low">低风险</option>
        </select>
        <input v-model="filterDateFrom" type="date" class="filter-input" />
        <span class="filter-separator">至</span>
        <input v-model="filterDateTo" type="date" class="filter-input" />
        <button @click="resetFilters" class="btn-ghost">重置</button>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!loading && letters.length === 0" class="empty-state">
      <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
      </svg>
      <p>暂无数据</p>
    </div>

    <!-- 信件列表 -->
    <div v-else class="letters-grid">
      <LetterCard v-for="letter in letters" :key="letter.id" :letter="letter" />
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination">
      <div class="page-info">
        显示第 {{ (page - 1) * perPage + 1 }}-{{ Math.min(page * perPage, total) }} 条，共 {{ total }} 条
      </div>
      <div class="page-controls">
        <button @click="changePage(page - 1)" :disabled="page <= 1" class="page-btn">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        
        <template v-for="p in visiblePages" :key="p">
          <button v-if="p === '...'" disabled class="page-btn page-ellipsis">...</button>
          <button v-else @click="changePage(p)" :class="['page-btn', p === page ? 'page-btn-active' : '']">
            {{ p }}
          </button>
        </template>
        
        <button @click="changePage(page + 1)" :disabled="page >= maxPage" class="page-btn">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import SearchBar from '../components/SearchBar.vue'
import LetterCard from '../components/LetterCard.vue'

const API = window.location.origin + '/api'
const letters = ref([])
const loading = ref(true)
const page = ref(1)
const total = ref(0)
const perPage = 20
const searchQuery = ref('')
const filterOffice = ref('')
const filterStatus = ref('')
const offices = ref([])
const filterViolationType = ref('')
const filterRiskLevel = ref('')
const filterDateFrom = ref('')
const filterDateTo = ref('')
const violationTypes = ref([])

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

function applyFilters() {
  page.value = 1
  fetchData()
}

function doSearch() {
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

onMounted(() => {
  fetchOffices()
  fetchViolationTypes()
  fetchData()
})
</script>

<style scoped>
.letters-page {
  max-width: 1280px;
  margin: 0 auto;
  padding: 104px 32px 64px;
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

@media (min-width: 640px) {
  .page-header {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.02em;
  margin: 0;
}

.page-subtitle {
  font-size: 15px;
  color: var(--text-3);
  margin-top: 4px;
}

.page-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-2);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success);
}

.filter-bar {
  background: white;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: var(--card-shadow);
}

.filter-row {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (min-width: 640px) {
  .filter-row {
    flex-direction: row;
    align-items: center;
  }
}

.filter-advanced {
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
  margin-top: 16px;
}

.search-wrapper {
  flex: 1;
}

.filter-select {
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: white;
  color: var(--text);
  font-size: 14px;
  min-width: 150px;
  cursor: pointer;
}

.filter-input {
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: white;
  color: var(--text);
  font-size: 14px;
}

.filter-separator {
  color: var(--text-3);
  font-size: 14px;
}

.btn-primary {
  padding: 12px 28px;
  border-radius: 8px;
  background: var(--accent);
  color: white;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: var(--accent-dark);
}

.btn-ghost {
  padding: 12px 28px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-2);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-ghost:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: var(--text-3);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: var(--text-3);
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.3;
}

.letters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.pagination {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
}

@media (min-width: 640px) {
  .pagination {
    flex-direction: row;
    justify-content: space-between;
  }
}

.page-info {
  font-size: 14px;
  color: var(--text-3);
}

.page-controls {
  display: flex;
  gap: 8px;
}

.page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  height: 40px;
  padding: 0 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: white;
  color: var(--text-2);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}

.page-btn-active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-ellipsis {
  border: none;
  background: transparent;
}
</style>
