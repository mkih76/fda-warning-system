<template>
  <div class="max-w-7xl mx-auto px-6 py-10">
    <!-- 页头 -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold text-pharma-900 dark:text-dark-100 transition-colors">数据看板</h1>
        <p class="text-pharma-400 dark:text-dark-400 mt-1 transition-colors">FDA 警告信数据分析与可视化</p>
      </div>
      <div class="flex items-center gap-2 text-sm text-pharma-400 dark:text-dark-400 bg-white dark:bg-dark-800 rounded-2xl px-4 py-2 border border-gray-100/50 dark:border-dark-600 shadow-sm transition-colors">
        <span class="w-2 h-2 bg-teal-500 rounded-full animate-pulse"></span>
        <span>数据更新至 {{ stats.max_year }} 年</span>
      </div>
    </div>

    <div v-if="loading" class="text-center py-20">
      <div class="animate-spin w-10 h-10 border-3 border-teal-500 border-t-transparent rounded-full mx-auto mb-4"></div>
      <p class="text-pharma-400 dark:text-dark-400 text-sm">加载中...</p>
    </div>

    <div v-else>
      <!-- ═══ 指标卡片 ROW ═══ -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div class="card !p-5 text-center">
          <p class="text-3xl font-bold text-pharma-900 dark:text-dark-100 transition-colors">{{ stats.total }}</p>
          <p class="text-sm text-pharma-400 dark:text-dark-400 mt-1 transition-colors">警告信总数</p>
        </div>
        <div class="card !p-5 text-center">
          <p class="text-3xl font-bold text-red-500">{{ stats.active }}</p>
          <p class="text-sm text-pharma-400 dark:text-dark-400 mt-1 transition-colors">活跃中</p>
        </div>
        <div class="card !p-5 text-center">
          <p class="text-3xl font-bold text-green-500">{{ stats.closed }}</p>
          <p class="text-sm text-pharma-400 dark:text-dark-400 mt-1 transition-colors">已关闭</p>
        </div>
        <div class="card !p-5 text-center">
          <p class="text-3xl font-bold text-teal-500">{{ stats.office_count }}</p>
          <p class="text-sm text-pharma-400 dark:text-dark-400 mt-1 transition-colors">签发办公室</p>
        </div>
      </div>

      <!-- ═══ 图表 ROW 1 ═══ -->
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <!-- 年度趋势 -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-pharma-900 dark:text-dark-100 transition-colors">年度发布趋势</h2>
            <span class="text-xs text-pharma-400 dark:text-dark-400 transition-colors">{{ stats.min_year }} — {{ stats.max_year }}</span>
          </div>
          <div class="space-y-2.5">
            <div v-for="y in yearlyCounts" :key="y.year"
                 class="flex items-center gap-3">
              <span class="text-xs font-semibold text-pharma-500 dark:text-dark-400 w-10 flex-shrink-0 transition-colors">{{ y.year }}</span>
              <div class="flex-1 bg-gray-100 dark:bg-dark-700 rounded-full h-5 overflow-hidden transition-colors">
                <div class="h-full bg-gradient-to-r from-teal-400 to-teal-500 rounded-full transition-all duration-500"
                     :style="{ width: y.pct + '%' }"></div>
              </div>
              <span class="text-sm font-bold text-pharma-700 dark:text-dark-200 w-16 text-right flex-shrink-0 transition-colors">{{ y.count }} 封</span>
            </div>
            <div v-if="yearlyCounts.length === 0" class="text-center py-10 text-pharma-400 dark:text-dark-400 text-sm transition-colors">
              暂无年度数据
            </div>
          </div>
        </div>
        <!-- 状态分布 -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-pharma-900 dark:text-dark-100 transition-colors">状态分布</h2>
          </div>
          <div class="space-y-4 pt-2">
            <!-- 活跃 -->
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-2">
                  <span class="w-3 h-3 rounded-full bg-red-500"></span>
                  <span class="text-sm font-medium text-pharma-700 dark:text-dark-200 transition-colors">活跃中</span>
                </div>
                <div class="text-right">
                  <span class="text-lg font-bold text-pharma-900 dark:text-dark-100 transition-colors">{{ stats.active }}</span>
                  <span class="text-xs text-pharma-400 dark:text-dark-400 ml-1 transition-colors">封</span>
                </div>
              </div>
              <div class="bg-gray-100 dark:bg-dark-700 rounded-full h-3 overflow-hidden transition-colors">
                <div class="h-full bg-gradient-to-r from-red-400 to-red-500 rounded-full transition-all duration-500"
                     :style="{ width: statusPercentages.activeBar + '%' }"></div>
              </div>
              <p class="text-xs text-pharma-400 dark:text-dark-400 mt-1 transition-colors">占比 {{ statusPercentages.activePct }}%</p>
            </div>
            <!-- 已关闭 -->
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-2">
                  <span class="w-3 h-3 rounded-full bg-green-500"></span>
                  <span class="text-sm font-medium text-pharma-700 dark:text-dark-200 transition-colors">已关闭</span>
                </div>
                <div class="text-right">
                  <span class="text-lg font-bold text-pharma-900 dark:text-dark-100 transition-colors">{{ stats.closed }}</span>
                  <span class="text-xs text-pharma-400 dark:text-dark-400 ml-1 transition-colors">封</span>
                </div>
              </div>
              <div class="bg-gray-100 dark:bg-dark-700 rounded-full h-3 overflow-hidden transition-colors">
                <div class="h-full bg-gradient-to-r from-green-400 to-green-500 rounded-full transition-all duration-500"
                     :style="{ width: (100 - statusPercentages.activeBar) + '%' }"></div>
              </div>
              <p class="text-xs text-pharma-400 dark:text-dark-400 mt-1 transition-colors">占比 {{ statusPercentages.closedPct }}%</p>
            </div>
            <!-- 总数 -->
            <div class="pt-2 border-t border-gray-100 dark:border-dark-600 transition-colors">
              <div class="flex items-center justify-between">
                <span class="text-sm text-pharma-400 dark:text-dark-400 transition-colors">总计</span>
                <span class="text-xl font-bold text-pharma-900 dark:text-dark-100 transition-colors">{{ stats.total }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══ 图表 ROW 2 ═══ -->
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <!-- 办公室分布 -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-pharma-900 dark:text-dark-100 transition-colors">签发办公室 TOP 10</h2>
          </div>
          <div class="space-y-2 max-h-[300px] overflow-y-auto pr-1">
            <div v-for="(office, i) in topOffices" :key="office.name"
                 class="flex items-center gap-2 py-1.5">
              <span class="text-xs font-bold text-pharma-400 dark:text-dark-400 w-5 flex-shrink-0 text-center transition-colors">{{ i + 1 }}</span>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-xs font-medium text-pharma-700 dark:text-dark-200 truncate transition-colors" :title="office.name">{{ office.name }}</span>
                  <span class="text-xs font-semibold text-pharma-500 dark:text-dark-400 flex-shrink-0 ml-2 transition-colors">{{ office.count }}</span>
                </div>
                <div class="bg-gray-100 dark:bg-dark-700 rounded-full h-2.5 overflow-hidden transition-colors">
                  <div class="h-full rounded-full transition-all duration-500"
                       :style="{ width: office.pct + '%', backgroundColor: ['#00b894','#8b5cf6','#3b82f6','#f59e0b','#ef4444','#ec4899','#14b8a6','#6366f1','#f97316','#84cc16'][i] }"></div>
                </div>
              </div>
            </div>
            <div v-if="topOffices.length === 0" class="text-center py-10 text-pharma-400 dark:text-dark-400 text-sm transition-colors">
              暂无数据
            </div>
          </div>
        </div>
        <!-- 月度分布 -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-pharma-900 dark:text-dark-100 transition-colors">月度发布量</h2>
            <div class="flex gap-1">
              <button v-for="y in availableYears" :key="y"
                      @click="selectedYear = y"
                      :class="selectedYear === y
                        ? 'px-3 py-1 text-xs font-medium text-white bg-teal-500 rounded-full'
                        : 'px-3 py-1 text-xs text-pharma-500 dark:text-dark-400 bg-gray-100 dark:bg-dark-700 rounded-full hover:bg-gray-200 dark:hover:bg-dark-600 transition-colors'">
                {{ y }}
              </button>
            </div>
          </div>
          <div class="grid grid-cols-3 sm:grid-cols-4 gap-2">
            <div v-for="row in monthlyRows" :key="row.month"
                 class="bg-gray-50 dark:bg-dark-700/50 rounded-lg p-2.5 transition-colors">
              <p class="text-[10px] text-pharma-400 dark:text-dark-400 mb-1 truncate transition-colors">{{ row.label }}</p>
              <p class="text-lg font-bold text-pharma-900 dark:text-dark-100 transition-colors">{{ row.count }}</p>
              <div class="mt-1.5 bg-gray-200 dark:bg-dark-600 rounded-full h-1.5 overflow-hidden transition-colors">
                <div class="h-full bg-gradient-to-r from-teal-400 to-teal-500 rounded-full transition-all duration-500"
                     :style="{ width: Math.max(row.pct, row.count > 0 ? 5 : 0) + '%' }"></div>
              </div>
            </div>
          </div>
          <div v-if="monthlyRows.length === 0" class="text-center py-6 text-pharma-400 dark:text-dark-400 text-sm transition-colors">
            暂无月度数据
          </div>
        </div>
      </div>

      <!-- ═══ TOP 企业 ═══ -->
      <div class="card">
        <h2 class="text-lg font-semibold text-pharma-900 dark:text-dark-100 mb-4 transition-colors">警告信最多的企业</h2>
        <div class="overflow-x-auto">
          <table class="min-w-full text-sm">
            <thead>
              <tr class="border-b border-gray-100 dark:border-dark-600">
                <th class="text-left py-3 px-2 text-pharma-400 dark:text-dark-400 font-medium transition-colors">#</th>
                <th class="text-left py-3 px-2 text-pharma-400 dark:text-dark-400 font-medium transition-colors">企业名称</th>
                <th class="text-right py-3 px-2 text-pharma-400 dark:text-dark-400 font-medium transition-colors">警告信数</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(c, i) in topCompanies" :key="c.company"
                  class="border-b border-gray-50 dark:border-dark-700 hover:bg-gray-50/50 dark:hover:bg-dark-700/50 transition-colors">
                <td class="py-3 px-2 text-pharma-400 dark:text-dark-400 w-8 transition-colors">{{ i + 1 }}</td>
                <td class="py-3 px-2">
                  <router-link :to="'/company/'+encodeURIComponent(c.company)"
                              class="text-pharma-700 dark:text-dark-200 hover:text-teal-500 dark:hover:text-teal-400 transition-colors">
                    {{ c.company }}
                  </router-link>
                </td>
                <td class="py-3 px-2 text-right">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-teal-50 dark:bg-teal-900/30 text-teal-600 dark:text-teal-400 text-xs font-semibold transition-colors">
                    {{ c.count }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
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

// 调试：暴露到 window 以便控制台调试
window._chart = Chart
window._getCanvas = (id) => document.getElementById(id)

const API = window.location.origin + '/api'
const loading = ref(true)
const stats = ref({ total: 0, active: 0, closed: 0, min_year: '', max_year: '', office_count: 0 })
const topCompanies = ref([])
const availableYears = ref([])
const selectedYear = ref('')
const timelineData = ref([])
const officeData = ref({})

const trendChart = ref(null)
const statusChart = ref(null)
const officeChart = ref(null)
const monthlyChart = ref(null)

// 轮询等待 canvas 进入 DOM（兼容 Vue SPA 的异步渲染）
function waitForCanvas(predicate, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const start = Date.now()
    const check = () => {
      const els = document.querySelectorAll('canvas')
      for (const el of els) {
        if (predicate(el)) { resolve(el); return }
      }
      if (Date.now() - start > timeout) {
        reject(new Error(`Canvas timeout after ${timeout}ms`))
      } else {
        setTimeout(check, 30)
      }
    }
    check()
  })
}

// 用 setTimeout 延迟确保 canvas 已挂载到 document
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

let trendInstance = null
let statusInstance = null
let officeInstance = null
let monthlyInstance = null

const { isDark } = useDarkMode()

// 暗色模式下的颜色
const chartColors = computed(() => ({
  teal: '#00b894',
  tealLight: 'rgba(0,184,148,0.15)',
  red: '#ef4444',
  green: '#22c55e',
  grid: isDark.value ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)',
  text: isDark.value ? '#8b949e' : '#6a6a8a',
  textStrong: isDark.value ? '#c9d1d9' : '#4a4a6a',
  tooltipBg: isDark.value ? '#21262d' : '#1a1a2e',
  tooltipTitle: '#ffffff',
  tooltipBody: isDark.value ? '#c9d1d9' : '#d0d0e0',
}))

const PALETTE = ['#00b894','#8b5cf6','#3b82f6','#f59e0b','#ef4444','#ec4899','#14b8a6','#6366f1','#f97316','#84cc16']

function destroyChart(instance) {
  if (instance) { instance.destroy(); instance = null }
}

function makeChartOptions(overrides = {}) {
  const c = chartColors.value
  const base = {
    responsive: false,
    maintainAspectRatio: false,
    animation: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: c.tooltipBg,
        titleColor: c.tooltipTitle,
        bodyColor: c.tooltipBody,
        cornerRadius: 8,
        padding: 10,
      },
      ...(overrides.plugins || {}),
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: { color: c.grid },
        ticks: { color: c.text, font: { size: 11 } },
        ...((overrides.scales || {}).y || {}),
      },
      x: {
        grid: { display: false },
        ticks: { color: c.text, font: { size: 11 } },
        ...((overrides.scales || {}).x || {}),
      },
    },
    interaction: { intersect: false, mode: 'index' },
  }
  return base
}

/**
 * 年度趋势折线图
 * API返回 {date:"2021-02", count:N} — 按年聚合
 */
function renderTrendChart(timelineData) {
  waitForCanvas(el => el.id === 'chart-trend').then(el => {
    try {
      console.log('[DEBUG renderTrendChart] found el:', el, 'cw:', el.width, 'ch:', el.height)
      destroyChart(trendInstance)

      // 按年聚合：{date:"2021-02"} → {year:"2021", count:sum}
      const byYear = {}
      for (const d of timelineData) {
        const year = d.date.substring(0, 4)
        byYear[year] = (byYear[year] || 0) + d.count
      }
      const labels = Object.keys(byYear).sort()
      const counts = labels.map(y => byYear[y])
      const c = chartColors.value

      // 固定像素尺寸
      const container = el.parentElement
      const cw = container.clientWidth || 600
      const ch = container.clientHeight || 280
      el.width = cw
      el.height = ch
      container.style.width = cw + 'px'
      container.style.height = ch + 'px'

      trendInstance = new Chart(el, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: '警告信数',
            data: counts,
            borderColor: c.teal,
            backgroundColor: ctx => {
              const g = ctx.chart.ctx.createLinearGradient(0, 0, 0, ctx.chart.height)
              g.addColorStop(0, 'rgba(0,184,148,0.25)')
              g.addColorStop(1, 'rgba(0,184,148,0.01)')
              return g
            },
            fill: true,
            tension: 0.3,
            pointRadius: 5,
            pointBackgroundColor: isDark.value ? '#161b22' : '#fff',
            pointBorderColor: c.teal,
            pointBorderWidth: 2,
            pointHoverRadius: 7,
            borderWidth: 2.5,
          }]
        },
        options: makeChartOptions({
          scales: {
            y: { beginAtZero: true, grid: { color: c.grid }, ticks: { color: c.text, font: { size: 11 } } },
            x: { grid: { display: false }, ticks: { color: c.text, font: { size: 11 } } }
          }
        })
      })
      console.log('[DEBUG renderTrendChart] success, instance:', trendInstance)
    } catch(err) {
      console.error('[DEBUG renderTrendChart] error:', err)
    }
  }).catch(err => {
    console.error('[DEBUG renderTrendChart] wait failed:', err)
  })
}

/**
 * 状态饼图 — 数据直接来自 summary
 */
function renderStatusChart(summary) {
  waitForCanvas(el => el.id === 'chart-status').then(el => {
    try {
      console.log('[DEBUG renderStatusChart] found el')
      destroyChart(statusInstance)
      const c = chartColors.value
    // 固定像素尺寸
    const container = el.parentElement
    const cw = container.clientWidth || 500
    const ch = container.clientHeight || 280
    el.width = cw
    el.height = ch
    container.style.width = cw + 'px'
    container.style.height = ch + 'px'

    statusInstance = new Chart(el, {
      type: 'doughnut',
      data: {
        labels: ['活跃中', '已关闭'],
        datasets: [{
          data: [summary.active, summary.closed],
          backgroundColor: [c.red, c.green],
          borderWidth: 0,
          hoverOffset: 8,
        }]
      },
      options: {
        responsive: false,
        maintainAspectRatio: false,
        animation: false,
        cutout: '65%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 16,
              usePointStyle: true,
              color: c.textStrong,
              font: { size: 13 }
            }
          },
          tooltip: {
            backgroundColor: c.tooltipBg,
            titleColor: c.tooltipTitle,
            bodyColor: c.tooltipBody,
            cornerRadius: 8,
            padding: 10,
            callbacks: {
              label: ctx => ` ${ctx.label}: ${ctx.parsed} 封 (${((ctx.parsed / (summary.total || 1)) * 100).toFixed(1)}%)`
            }
          }
        }
      }
    })
    console.log('[DEBUG renderStatusChart] success')
  } catch(err) {
    console.error('[DEBUG renderStatusChart] error:', err)
  }
  })
}

/**
 * 办公室分布水平条图
 * officeData: {office_name: count} — 来自 /api/stats.by_office
 */
function renderOfficeChart(officeData) {
  waitForCanvas(el => el.id === 'chart-office').then(el => {
    try {
      console.log('[DEBUG renderOfficeChart] found el')
      destroyChart(officeInstance)
      const c = chartColors.value

      // 固定像素尺寸
      const container = el.parentElement
      const cw = container.clientWidth || 600
      const ch = container.clientHeight || 300
      el.width = cw
      el.height = ch
      container.style.width = cw + 'px'
      container.style.height = ch + 'px'

      // dict → 排序数组
      const sorted = Object.entries(officeData).sort(([, a], [, b]) => b - a).slice(0, 10)
      const labels = []
      let cderSum = 0
      for (const [name, count] of sorted) {
        if (name.includes('CDER') || name.includes('Drug Evaluation')) {
          cderSum += count
        } else {
          labels.push({ name, count })
        }
      }
      if (cderSum > 0) labels.unshift({ name: 'CDER (药物审评中心)', count: cderSum })
      const top = labels.slice(0, 10)

      officeInstance = new Chart(el, {
        type: 'bar',
        data: {
          labels: top.map(d => d.name.replace(/^(Center for |Division of )/, '')).reverse(),
          datasets: [{
            label: '警告信数',
            data: top.map(d => d.count).reverse(),
            backgroundColor: top.map((_, i) => PALETTE[i % PALETTE.length]).reverse(),
            borderRadius: 4,
            borderSkipped: false,
          }]
        },
        options: makeChartOptions({
          indexAxis: 'y',
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.parsed.x} 封`
              }
            }
          },
          scales: {
            x: { beginAtZero: true, grid: { color: chartColors.value.grid }, ticks: { color: chartColors.value.text, font: { size: 11 } } },
            y: { grid: { display: false }, ticks: { color: chartColors.value.textStrong, font: { size: 11 } } }
          }
        })
      })
      officeInstance.resize()
      console.log('[DEBUG renderOfficeChart] success')
    } catch(err) {
      console.error('[DEBUG renderOfficeChart] error:', err)
    }
  }).catch(err => {
    console.error('[DEBUG renderOfficeChart] wait failed:', err)
  })
}

/**
 * 月度柱状图
 */
function renderMonthlyChart() {
  waitForCanvas(el => el.id === 'chart-monthly').then(el => {
    try {
      console.log('[DEBUG renderMonthlyChart] found el')
      destroyChart(monthlyInstance)
      const c = chartColors.value

      // 固定像素尺寸
      const container = el.parentElement
      const cw = container.clientWidth || 500
      const ch = container.clientHeight || 260
      el.width = cw
      el.height = ch
      container.style.width = cw + 'px'
      container.style.height = ch + 'px'

      const yearData = monthlyData.value.filter(d => d.month && d.month.startsWith(selectedYear.value))
      const months = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, '0'))
      const counts = months.map(m => {
        const found = yearData.find(d => d.month && d.month.endsWith('-' + m))
        return found ? found.count : 0
      })
      const monthLabels = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']

      monthlyInstance = new Chart(el, {
        type: 'bar',
        data: {
          labels: monthLabels,
          datasets: [{
            label: `${selectedYear.value}年`,
            data: counts,
            backgroundColor: counts.map(cVal => cVal > 0 ? 'rgba(0,184,148,0.75)' : (isDark.value ? 'rgba(255,255,255,0.03)' : 'rgba(0,0,0,0.03)')),
            borderColor: counts.map(cVal => cVal > 0 ? 'rgba(0,184,148,1)' : 'transparent'),
            borderWidth: 1,
            borderRadius: 3,
            borderSkipped: false,
          }]
        },
        options: makeChartOptions({
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                title: ctx => `${selectedYear.value}年 ${ctx[0].label}`,
                label: ctx => ` ${ctx.parsed.y} 封`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: c.grid },
              ticks: { color: c.text, font: { size: 10 }, stepSize: 1 }
            },
            x: {
              grid: { display: false },
              ticks: { color: c.text, font: { size: 10 } }
            }
          }
        })
      })
      monthlyInstance.resize()
      console.log('[DEBUG renderMonthlyChart] success')
    } catch(err) {
      console.error('[DEBUG renderMonthlyChart] error:', err)
    }
  }).catch(err => {
    console.error('[DEBUG renderMonthlyChart] wait failed:', err)
  })
}

const monthlyData = ref([])

const yearlyCounts = computed(() => {
  const byYear = {}
  for (const d of timelineData.value) {
    const year = d.date.substring(0, 4)
    byYear[year] = (byYear[year] || 0) + d.count
  }
  const sorted = Object.entries(byYear).sort(([a], [b]) => a.localeCompare(b))
  const maxVal = Math.max(...sorted.map(([, c]) => c), 1)
  return sorted.map(([year, count]) => ({ year, count, pct: (count / maxVal) * 100 }))
})

const statusPercentages = computed(() => {
  const total = stats.value.total || 1
  return {
    activePct: ((stats.value.active / total) * 100).toFixed(1),
    closedPct: ((stats.value.closed / total) * 100).toFixed(1),
    activeBar: (stats.value.active / total) * 100,
  }
})

const topOffices = computed(() => {
  const entries = Object.entries(officeData.value)
  let cderSum = 0
  const filtered = []
  for (const [name, count] of entries) {
    if (name.includes('CDER') || name.includes('Drug Evaluation')) {
      cderSum += count
    } else {
      filtered.push({ name, count })
    }
  }
  if (cderSum > 0) filtered.unshift({ name: 'CDER (药物审评中心)', count: cderSum })
  const sorted = filtered.sort((a, b) => b.count - a.count).slice(0, 10)
  const maxVal = Math.max(...sorted.map(d => d.count), 1)
  return sorted.map(d => ({ ...d, pct: (d.count / maxVal) * 100 }))
})

const monthlyRows = computed(() => {
  const yearData = monthlyData.value.filter(d => d.month && d.month.startsWith(selectedYear.value))
  const months = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, '0'))
  const monthLabels = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
  const maxVal = Math.max(...yearData.map(d => d.count), 1)
  return months.map((m, i) => {
    const found = yearData.find(d => d.month && d.month.endsWith('-' + m))
    return {
      label: `${selectedYear.value}年${monthLabels[i]}`,
      month: m,
      count: found ? found.count : 0,
      pct: (found ? found.count : 0) / maxVal * 100
    }
  })
})

onMounted(async () => {
  try {
    const [summaryRes, timelineRes, monthlyRes, topRes, statsRes] = await Promise.all([
      fetch(`${API}/dashboard/summary`).then(r => r.json()),
      fetch(`${API}/letters/stats/timeline`).then(r => r.json()),
      fetch(`${API}/dashboard/monthly`).then(r => r.json()),
      fetch(`${API}/dashboard/top-companies`).then(r => r.json()),
      fetch(`${API}/stats`).then(r => r.json()),
    ])

    stats.value = summaryRes
    timelineData.value = timelineRes
    monthlyData.value = monthlyRes
    topCompanies.value = topRes
    officeData.value = statsRes.by_office || {}

    // 可选年份
    const years = [...new Set(monthlyRes.map(d => d.month.substring(0, 4)))].sort()
    availableYears.value = years
    selectedYear.value = years[years.length - 1]

    await nextTick()
    console.log('[DEBUG] nextTick done, rendering charts...')
    console.log('[DEBUG] trendChart ref:', trendChart.value)
    console.log('[DEBUG] statusChart ref:', statusChart.value)
    console.log('[DEBUG] officeChart ref:', officeChart.value)
    console.log('[DEBUG] monthlyChart ref:', monthlyChart.value)
    console.log('[DEBUG] getElementById chart-trend:', document.getElementById('chart-trend'))
    // 延迟 150ms 确保 Vue 完全渲染 DOM
    await new Promise(r => setTimeout(r, 150))
    renderTrendChart(timelineRes)
    renderStatusChart(summaryRes)
    renderOfficeChart(statsRes.by_office || {})
    renderMonthlyChart()
    console.log('[DEBUG] all charts rendered')
  } catch (e) {
    console.error('Dashboard 加载失败:', e)
  } finally {
    loading.value = false
  }
})
</script>
