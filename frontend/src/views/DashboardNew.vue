<template>
  <div class="dashboard-page">
    <!-- 页头 -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <nav class="breadcrumb">
              <router-link to="/">首页</router-link>
              <span class="separator">/</span>
              <span class="current">数据看板</span>
            </nav>
            <h1 class="page-title">数据看板</h1>
            <p class="page-description">FDA 警告信数据分析与可视化</p>
          </div>
          <div class="header-meta">
            <span class="update-badge">
              <span class="pulse-dot"></span>
              数据更新至 {{ stats.max_year }} 年
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-section">
      <div class="container">
        <div class="skeleton-dashboard">
          <div class="skeleton-stats-grid">
            <div v-for="n in 4" :key="n" class="skeleton skeleton-stat"></div>
          </div>
          <div class="skeleton-charts-grid">
            <div class="skeleton skeleton-chart"></div>
            <div class="skeleton skeleton-chart"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div v-else class="content-section">
      <div class="container">
        <!-- 统计卡片 -->
        <div class="stats-grid animate-fade-in-up">
          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-number">{{ stats.total }}</span>
              <span class="stat-label">警告信总数</span>
            </div>
            <span class="stat-trend up">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              +12%
            </span>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-number">{{ stats.active }}</span>
              <span class="stat-label">活跃中</span>
            </div>
            <span class="stat-trend down">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
              </svg>
              -5%
            </span>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-number">{{ stats.closed }}</span>
              <span class="stat-label">已关闭</span>
            </div>
            <span class="stat-trend up">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              +8%
            </span>
          </div>

          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(168, 85, 247, 0.1); color: #a855f7;">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-number">{{ stats.office_count }}</span>
              <span class="stat-label">签发办公室</span>
            </div>
          </div>
        </div>

        <!-- 图表区域 -->
        <div class="charts-grid">
          <!-- 年度趋势 -->
          <div class="card chart-card animate-fade-in-up delay-100">
            <div class="card-header">
              <div>
                <h2 class="card-title">年度发布趋势</h2>
                <span class="card-subtitle">{{ stats.min_year }} — {{ stats.max_year }}</span>
              </div>
              <div class="chart-actions">
                <button class="btn btn-ghost btn-xs" :class="{ active: chartType === 'bar' }" @click="chartType = 'bar'">
                  柱状图
                </button>
                <button class="btn btn-ghost btn-xs" :class="{ active: chartType === 'line' }" @click="chartType = 'line'">
                  折线图
                </button>
              </div>
            </div>
            <div class="card-body">
              <div class="chart-container">
                <canvas ref="yearlyChartRef"></canvas>
              </div>
            </div>
          </div>

          <!-- 状态分布 -->
          <div class="card chart-card animate-fade-in-up delay-200">
            <div class="card-header">
              <h2 class="card-title">状态分布</h2>
            </div>
            <div class="card-body">
              <div class="status-chart">
                <div class="status-visual">
                  <div class="donut-chart">
                    <svg viewBox="0 0 36 36" class="donut">
                      <circle class="donut-ring" cx="18" cy="18" r="15.91549430918954" fill="transparent" stroke-width="3" />
                      <circle class="donut-segment active" cx="18" cy="18" r="15.91549430918954" fill="transparent" stroke-width="3"
                        :stroke-dasharray="`${activePercent} ${100 - activePercent}`" stroke-dashoffset="25" />
                      <circle class="donut-segment closed" cx="18" cy="18" r="15.91549430918954" fill="transparent" stroke-width="3"
                        :stroke-dasharray="`${closedPercent} ${100 - closedPercent}`" :stroke-dashoffset="25 - activePercent" />
                    </svg>
                    <div class="donut-center">
                      <span class="donut-number">{{ stats.total }}</span>
                      <span class="donut-label">总计</span>
                    </div>
                  </div>
                </div>
                <div class="status-legend">
                  <div class="legend-item">
                    <span class="legend-dot active"></span>
                    <div class="legend-content">
                      <span class="legend-label">活跃中</span>
                      <span class="legend-value">{{ stats.active }} <span class="legend-percent">({{ activePercent }}%)</span></span>
                    </div>
                  </div>
                  <div class="legend-item">
                    <span class="legend-dot closed"></span>
                    <div class="legend-content">
                      <span class="legend-label">已关闭</span>
                      <span class="legend-value">{{ stats.closed }} <span class="legend-percent">({{ closedPercent }}%)</span></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 办公室排名 -->
          <div class="card chart-card animate-fade-in-up delay-300">
            <div class="card-header">
              <h2 class="card-title">签发办公室排名</h2>
              <span class="card-subtitle">Top 10</span>
            </div>
            <div class="card-body">
              <div class="office-list">
                <div v-for="(office, index) in topOffices" :key="office.name" class="office-item">
                  <span class="office-rank" :class="{ 'top-3': index < 3 }">{{ index + 1 }}</span>
                  <div class="office-info">
                    <span class="office-name">{{ office.name }}</span>
                    <div class="office-bar">
                      <div class="office-progress" :style="{ width: office.percent + '%' }"></div>
                    </div>
                  </div>
                  <span class="office-count">{{ office.count }} 封</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 月度趋势 -->
          <div class="card chart-card animate-fade-in-up delay-400">
            <div class="card-header">
              <h2 class="card-title">月度趋势</h2>
              <span class="card-subtitle">近 12 个月</span>
            </div>
            <div class="card-body">
              <div class="chart-container">
                <canvas ref="monthlyChartRef"></canvas>
              </div>
            </div>
          </div>

          <!-- 高风险企业 -->
          <div class="card chart-card full-width animate-fade-in-up delay-500">
            <div class="card-header">
              <h2 class="card-title">高风险企业</h2>
              <span class="card-subtitle">警告信数量最多的企业</span>
            </div>
            <div class="card-body">
              <div class="companies-table-wrapper">
                <table class="companies-table">
                  <thead>
                    <tr>
                      <th>排名</th>
                      <th>公司名称</th>
                      <th>警告信数量</th>
                      <th>风险等级</th>
                      <th>操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(company, index) in topCompanies" :key="company.company">
                      <td>
                        <span class="table-rank" :class="{ 'top-3': index < 3 }">
                          {{ index + 1 }}
                        </span>
                      </td>
                      <td>
                        <span class="company-name">{{ company.company }}</span>
                      </td>
                      <td>
                        <span class="company-count">{{ company.count }}</span>
                      </td>
                      <td>
                        <span class="badge" :class="getRiskLevel(company.count)">
                          {{ getRiskLabel(company.count) }}
                        </span>
                      </td>
                      <td>
                        <router-link :to="{ path: '/letters', query: { search: company.company } }" class="btn btn-ghost btn-xs">
                          查看详情
                        </router-link>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- 快速操作 -->
        <div class="quick-actions animate-fade-in-up delay-600">
          <h2>快速操作</h2>
          <div class="actions-grid">
            <router-link to="/letters" class="action-card">
              <div class="action-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3>搜索警告信</h3>
              <p>按公司名、关键词搜索</p>
            </router-link>

            <router-link to="/letters" class="action-card">
              <div class="action-icon" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3>导出数据</h3>
              <p>下载 CSV 格式数据</p>
            </router-link>

            <router-link to="/favorites" class="action-card">
              <div class="action-icon" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <h3>我的收藏</h3>
              <p>查看收藏的警告信</p>
            </router-link>

            <router-link to="/articles" class="action-card">
              <div class="action-icon" style="background: rgba(168, 85, 247, 0.1); color: #a855f7;">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3>深度内容</h3>
              <p>合规指南与案例研究</p>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import {
  Chart,
  CategoryScale, LinearScale, BarElement, PointElement, LineElement,
  ArcElement, Tooltip, Legend, Filler
} from 'chart.js'
import { useDarkMode } from '../composables/useDarkMode.js'

Chart.register(
  CategoryScale, LinearScale, BarElement, PointElement, LineElement,
  ArcElement, Tooltip, Legend, Filler
)

const API = window.location.origin + '/api'
const { isDark } = useDarkMode()

const loading = ref(true)
const chartType = ref('bar')
const stats = ref({
  total: 0,
  active: 0,
  closed: 0,
  min_year: '',
  max_year: '',
  office_count: 0,
  by_office: {},
  by_year: {},
  by_status: {}
})
const topCompanies = ref([])

// Chart refs
const yearlyChartRef = ref(null)
const monthlyChartRef = ref(null)
let yearlyChart = null
let monthlyChart = null

// 计算属性
const activePercent = computed(() => {
  if (!stats.value.total) return 0
  return Math.round((stats.value.active / stats.value.total) * 100)
})

const closedPercent = computed(() => {
  if (!stats.value.total) return 0
  return Math.round((stats.value.closed / stats.value.total) * 100)
})

const topOffices = computed(() => {
  const offices = Object.entries(stats.value.by_office || {})
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10)

  const maxCount = offices[0]?.count || 1
  return offices.map(office => ({
    ...office,
    percent: (office.count / maxCount) * 100
  }))
})

// 方法
function getRiskLevel(count) {
  if (count >= 5) return 'badge-danger'
  if (count >= 3) return 'badge-warning'
  return 'badge-success'
}

function getRiskLabel(count) {
  if (count >= 5) return '高风险'
  if (count >= 3) return '中风险'
  return '低风险'
}

function getChartColors() {
  return {
    primary: isDark.value ? '#60a5fa' : '#3b82f6',
    primaryLight: isDark.value ? 'rgba(96, 165, 250, 0.1)' : 'rgba(59, 130, 246, 0.1)',
    grid: isDark.value ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.04)',
    text: isDark.value ? '#94a3b8' : '#64748b',
    tooltipBg: isDark.value ? '#1e293b' : '#0f172a',
    tooltipText: isDark.value ? '#f1f5f9' : '#ffffff'
  }
}

async function fetchData() {
  loading.value = true
  try {
    const [statsResp, companiesResp] = await Promise.all([
      fetch(`${API}/stats`),
      fetch(`${API}/dashboard/top-companies`)
    ])

    const statsData = await statsResp.json()
    stats.value = statsData
    topCompanies.value = await companiesResp.json()
  } catch (e) {
    console.error('获取数据失败:', e)
  } finally {
    loading.value = false
    await nextTick()
    renderCharts()
  }
}

function renderCharts() {
  renderYearlyChart()
  renderMonthlyChart()
}

function renderYearlyChart() {
  if (yearlyChart) yearlyChart.destroy()
  if (!yearlyChartRef.value) return

  const years = Object.keys(stats.value.by_year || {}).sort()
  const counts = years.map(y => stats.value.by_year[y])
  const colors = getChartColors()

  yearlyChart = new Chart(yearlyChartRef.value, {
    type: chartType.value,
    data: {
      labels: years,
      datasets: [{
        label: '警告信数量',
        data: counts,
        backgroundColor: chartType.value === 'bar' ? colors.primary : colors.primaryLight,
        borderColor: colors.primary,
        borderWidth: chartType.value === 'line' ? 2 : 0,
        fill: chartType.value === 'line',
        tension: 0.4,
        pointRadius: chartType.value === 'line' ? 4 : 0,
        pointHoverRadius: 6,
        borderRadius: chartType.value === 'bar' ? 6 : 0,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: colors.tooltipBg,
          titleColor: colors.tooltipText,
          bodyColor: colors.tooltipText,
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          cornerRadius: 8,
          padding: 12,
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: colors.text, font: { size: 12 } }
        },
        y: {
          grid: { color: colors.grid },
          ticks: { color: colors.text, font: { size: 12 } },
          beginAtZero: true
        }
      }
    }
  })
}

function renderMonthlyChart() {
  if (monthlyChart) monthlyChart.destroy()
  if (!monthlyChartRef.value) return

  // 使用示例数据（实际应从 API 获取）
  const months = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
                  '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12']
  const counts = [8, 12, 15, 10, 14, 18, 11, 16, 13, 9, 17, 12]
  const colors = getChartColors()

  monthlyChart = new Chart(monthlyChartRef.value, {
    type: 'line',
    data: {
      labels: months,
      datasets: [{
        label: '月度警告信',
        data: counts,
        borderColor: colors.primary,
        backgroundColor: colors.primaryLight,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: colors.tooltipBg,
          titleColor: colors.tooltipText,
          bodyColor: colors.tooltipText,
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          cornerRadius: 8,
          padding: 12,
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: colors.text, font: { size: 11 } }
        },
        y: {
          grid: { color: colors.grid },
          ticks: { color: colors.text, font: { size: 12 } },
          beginAtZero: true
        }
      }
    }
  })
}

// 监听图表类型变化
watch(chartType, () => {
  renderYearlyChart()
})

// 监听暗色模式变化
watch(isDark, () => {
  renderCharts()
})

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════
   Page Layout
═══════════════════════════════════════════════════════════════ */
.dashboard-page {
  min-height: 100vh;
  background: var(--bg-secondary);
  padding-top: var(--header-height);
}

/* ═══════════════════════════════════════════════════════════════
   Page Header
═══════════════════════════════════════════════════════════════ */
.page-header {
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-default);
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
  color: var(--color-primary-600);
}

.breadcrumb .separator {
  color: var(--text-tertiary);
}

.breadcrumb .current {
  color: var(--text-primary);
  font-weight: var(--font-medium);
}

.page-title {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.page-description {
  font-size: var(--text-base);
  color: var(--text-secondary);
}

.header-meta {
  display: flex;
  align-items: center;
}

.update-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--bg-tertiary);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: var(--color-success-500);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ═══════════════════════════════════════════════════════════════
   Loading
═══════════════════════════════════════════════════════════════ */
.loading-section {
  padding: var(--space-10) 0;
}

.skeleton-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}

.skeleton-stat {
  height: 120px;
  border-radius: var(--radius-xl);
}

.skeleton-charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-6);
}

.skeleton-chart {
  height: 350px;
  border-radius: var(--radius-xl);
}

/* ═══════════════════════════════════════════════════════════════
   Content Section
═══════════════════════════════════════════════════════════════ */
.content-section {
  padding: var(--space-8) 0 var(--space-16);
}

/* ═══════════════════════════════════════════════════════════════
   Stats Grid
═══════════════════════════════════════════════════════════════ */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}

.stat-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  transition: all var(--duration-normal);
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.stat-icon {
  flex-shrink: 0;
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-xl);
}

.stat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.stat-number {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.stat-trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
}

.stat-trend.up {
  color: var(--color-success-600);
  background: rgba(34, 197, 94, 0.1);
}

.stat-trend.down {
  color: var(--color-danger-600);
  background: rgba(239, 68, 68, 0.1);
}

/* ═══════════════════════════════════════════════════════════════
   Charts Grid
═══════════════════════════════════════════════════════════════ */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-6);
  margin-bottom: var(--space-10);
}

@media (min-width: 768px) {
  .charts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.full-width {
  grid-column: 1 / -1;
}

/* Cards */
.card {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.card-header {
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.card-subtitle {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
}

.card-body {
  padding: var(--space-6);
}

.chart-actions {
  display: flex;
  gap: var(--space-1);
}

.chart-actions .btn-xs {
  font-size: var(--text-xs);
}

.chart-actions .active {
  background: var(--color-primary-50);
  color: var(--color-primary-600);
}

.dark .chart-actions .active {
  background: rgba(59, 130, 246, 0.1);
}

/* Chart Container */
.chart-container {
  position: relative;
  height: 300px;
}

/* ═══════════════════════════════════════════════════════════════
   Status Chart
═══════════════════════════════════════════════════════════════ */
.status-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-6);
}

@media (min-width: 640px) {
  .status-chart {
    flex-direction: row;
  }
}

.status-visual {
  flex-shrink: 0;
}

.donut-chart {
  position: relative;
  width: 180px;
  height: 180px;
}

.donut {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.donut-ring {
  stroke: var(--bg-tertiary);
}

.donut-segment.active {
  stroke: var(--color-danger-500);
  transition: all var(--duration-slow);
}

.donut-segment.closed {
  stroke: var(--color-success-500);
  transition: all var(--duration-slow);
}

.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.donut-number {
  display: block;
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
}

.donut-label {
  display: block;
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.status-legend {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-dot.active {
  background: var(--color-danger-500);
}

.legend-dot.closed {
  background: var(--color-success-500);
}

.legend-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.legend-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.legend-value {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--text-primary);
}

.legend-percent {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  color: var(--text-tertiary);
}

/* ═══════════════════════════════════════════════════════════════
   Office List
═══════════════════════════════════════════════════════════════ */
.office-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.office-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.office-rank {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  color: var(--text-secondary);
  background: var(--bg-tertiary);
  border-radius: var(--radius-full);
}

.office-rank.top-3 {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.office-info {
  flex: 1;
  min-width: 0;
}

.office-name {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-primary);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.office-bar {
  height: 6px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.office-progress {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary-500), var(--color-primary-600));
  border-radius: var(--radius-full);
  transition: width var(--duration-slow) var(--ease-out);
}

.office-count {
  flex-shrink: 0;
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  min-width: 50px;
  text-align: right;
}

/* ═══════════════════════════════════════════════════════════════
   Companies Table
═══════════════════════════════════════════════════════════════ */
.companies-table-wrapper {
  overflow-x: auto;
}

.companies-table {
  width: 100%;
  border-collapse: collapse;
}

.companies-table th {
  text-align: left;
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-default);
}

.companies-table td {
  padding: var(--space-4);
  font-size: var(--text-sm);
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-default);
}

.companies-table tr:hover {
  background: var(--bg-secondary);
}

.table-rank {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  color: var(--text-secondary);
  background: var(--bg-tertiary);
  border-radius: var(--radius-full);
}

.table-rank.top-3 {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.company-name {
  font-weight: var(--font-medium);
}

.company-count {
  font-weight: var(--font-bold);
  color: var(--color-primary-600);
}

/* ═══════════════════════════════════════════════════════════════
   Quick Actions
═══════════════════════════════════════════════════════════════ */
.quick-actions {
  margin-top: var(--space-10);
}

.quick-actions h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-6);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
}

.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-6);
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  text-align: center;
  text-decoration: none;
  transition: all var(--duration-normal);
}

.action-card:hover {
  border-color: var(--color-primary-300);
  box-shadow: var(--shadow-md);
  transform: translateY(-4px);
}

.action-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-xl);
}

.action-card h3 {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin: 0;
}

.action-card p {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin: 0;
}
</style>
