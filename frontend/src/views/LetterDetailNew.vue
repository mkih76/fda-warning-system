<template>
  <div class="detail-page">
    <!-- 页头 -->
    <div class="page-header">
      <div class="container">
        <nav class="breadcrumb">
          <router-link to="/">首页</router-link>
          <span class="separator">/</span>
          <router-link to="/letters">警告信</router-link>
          <span class="separator">/</span>
          <span class="current">{{ letter.company_name || '详情' }}</span>
        </nav>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-section">
      <div class="container">
        <div class="skeleton-detail">
          <div class="skeleton skeleton-title"></div>
          <div class="skeleton skeleton-subtitle"></div>
          <div class="skeleton-grid">
            <div class="skeleton skeleton-card"></div>
            <div class="skeleton skeleton-card"></div>
          </div>
          <div class="skeleton skeleton-content"></div>
        </div>
      </div>
    </div>

    <!-- 内容 -->
    <div v-else-if="letter" class="content-section">
      <div class="container">
        <!-- 信件头部 -->
        <div class="letter-header animate-fade-in-up">
          <div class="header-top">
            <div class="header-badges">
              <span class="badge badge-dot" :class="getStatusBadgeClass(letter.status)">
                {{ letter.status === 'active' ? '进行中' : '已关闭' }}
              </span>
              <span v-if="letter.analysis?.risk_level" class="badge" :class="getRiskBadgeClass(letter.analysis.risk_level)">
                {{ letter.analysis.risk_level }}风险
              </span>
              <span v-if="letter.country" class="badge badge-info">
                {{ letter.country }}
              </span>
            </div>
            <div class="header-actions">
              <button
                class="btn btn-ghost btn-icon"
                :class="{ 'is-favorite': isFavorite(letter.id) }"
                @click="toggleFavorite(letter.id)"
                :title="isFavorite(letter.id) ? '取消收藏' : '收藏'"
              >
                <svg class="w-5 h-5" viewBox="0 0 24 24" :fill="isFavorite(letter.id) ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </button>
              <a v-if="letter.url" :href="letter.url" target="_blank" class="btn btn-secondary btn-sm">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                查看原文
              </a>
              <button @click="goBack" class="btn btn-ghost btn-sm">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                返回列表
              </button>
            </div>
          </div>

          <h1 class="letter-title">{{ letter.company_name }}</h1>

          <div class="letter-meta-grid">
            <div class="meta-card">
              <div class="meta-icon">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                </svg>
              </div>
              <div>
                <span class="meta-label">FDA ID</span>
                <span class="meta-value">{{ letter.fda_id }}</span>
              </div>
            </div>

            <div v-if="letter.issuing_office" class="meta-card">
              <div class="meta-icon">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <span class="meta-label">签发办公室</span>
                <span class="meta-value">{{ letter.issuing_office }}</span>
              </div>
            </div>

            <div v-if="letter.issue_date" class="meta-card">
              <div class="meta-icon">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <span class="meta-label">发布日期</span>
                <span class="meta-value">{{ letter.issue_date }}</span>
              </div>
            </div>

            <div v-if="letter.fei_number" class="meta-card">
              <div class="meta-icon">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <span class="meta-label">FEI 号</span>
                <span class="meta-value">{{ letter.fei_number }}</span>
              </div>
            </div>
          </div>

          <div class="letter-subject">
            <h3>主题</h3>
            <p>{{ letter.subject }}</p>
          </div>
        </div>

        <!-- 主要内容区域 -->
        <div class="letter-body">
          <!-- 左侧：AI 分析 + 违规项 -->
          <div class="main-content">
            <!-- AI 分析卡片 -->
            <div v-if="letter.analysis" class="card ai-card animate-fade-in-up delay-100">
              <div class="card-header">
                <div class="card-title">
                  <div class="title-icon ai-icon">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h2>AI 智能分析</h2>
                  <span v-if="letter.analysis.model_used" class="badge badge-info">
                    {{ letter.analysis.model_used }}
                  </span>
                </div>
              </div>
              <div class="card-body">
                <!-- 风险等级 -->
                <div v-if="letter.analysis.risk_level" class="risk-assessment">
                  <div class="risk-header">
                    <span class="risk-label">风险评估</span>
                    <span class="badge badge-lg" :class="getRiskBadgeClass(letter.analysis.risk_level)">
                      {{ letter.analysis.risk_level }}风险
                    </span>
                  </div>
                  <div class="risk-bar">
                    <div class="risk-progress" :style="{ width: getRiskWidth(letter.analysis.risk_level) }"
                         :class="getRiskBarClass(letter.analysis.risk_level)"></div>
                  </div>
                </div>

                <!-- 违规类型 -->
                <div v-if="letter.analysis.violation_type" class="violation-type">
                  <span class="label">违规类型</span>
                  <span class="value">{{ letter.analysis.violation_type }}</span>
                </div>

                <!-- 中文摘要 -->
                <div v-if="letter.analysis.summary_zh" class="summary">
                  <h3>中文摘要</h3>
                  <div class="summary-content">
                    <p>{{ letter.analysis.summary_zh }}</p>
                  </div>
                </div>

                <!-- 英文摘要 -->
                <div v-if="letter.analysis.summary_en" class="summary">
                  <h3>英文摘要</h3>
                  <div class="summary-content">
                    <p>{{ letter.analysis.summary_en }}</p>
                  </div>
                </div>

                <!-- 关键发现 -->
                <div v-if="letter.analysis.key_findings?.length" class="key-findings">
                  <h3>关键发现</h3>
                  <ul class="findings-list">
                    <li v-for="(finding, index) in letter.analysis.key_findings" :key="index">
                      <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span>{{ finding }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- 违规项列表 -->
            <div v-if="letter.violations?.length" class="card violations-card animate-fade-in-up delay-200">
              <div class="card-header">
                <div class="card-title">
                  <div class="title-icon violations-icon">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </div>
                  <h2>违规项 ({{ letter.violations.length }})</h2>
                </div>
              </div>
              <div class="card-body">
                <div class="violations-list">
                  <div v-for="(violation, index) in letter.violations" :key="index" class="violation-item">
                    <div class="violation-header">
                      <span class="badge" :class="getSeverityBadgeClass(violation.severity)">
                        {{ violation.severity || 'major' }}
                      </span>
                      <span v-if="violation.system_category" class="violation-category">
                        {{ violation.system_category }}
                      </span>
                    </div>
                    <h4 v-if="violation.violation_type">{{ violation.violation_type }}</h4>
                    <p v-if="violation.description">{{ violation.description }}</p>
                    <p v-if="violation.description_zh" class="description-zh">
                      {{ violation.description_zh }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- CFR 引用 -->
            <div v-if="letter.citations?.length" class="card citations-card animate-fade-in-up delay-300">
              <div class="card-header">
                <div class="card-title">
                  <div class="title-icon citations-icon">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  <h2>CFR 引用 ({{ letter.citations.length }})</h2>
                </div>
              </div>
              <div class="card-body">
                <div class="citations-list">
                  <div v-for="(citation, index) in letter.citations" :key="index" class="citation-item">
                    <div class="citation-code">
                      <span class="cfr-part">21 CFR {{ citation.cfr_part }}</span>
                      <span v-if="citation.cfr_section" class="cfr-section">.{{ citation.cfr_section }}</span>
                    </div>
                    <p v-if="citation.cfr_text" class="citation-text">{{ citation.cfr_text }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 完整译文 - 学术论文排版 -->
            <div v-if="letter.analysis?.translation_zh" class="card translation-card animate-fade-in-up delay-400">
              <div class="card-header">
                <div class="card-title">
                  <div class="title-icon translation-icon">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M3 5h12M9 3v2m3.356 9.356l2.293 2.293M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9 14l2 2 4-4" />
                    </svg>
                  </div>
                  <h2>完整译文</h2>
                </div>
              </div>
              <div class="card-body">
                <div class="translation-content academic-format" v-html="formatTranslation(letter.analysis.translation_zh)"></div>
              </div>
            </div>
          </div>

          <!-- 右侧边栏 -->
          <aside class="sidebar">
            <!-- 快速信息 -->
            <div class="card info-card animate-fade-in-right delay-100">
              <div class="card-header">
                <h3>快速信息</h3>
              </div>
              <div class="card-body">
                <div class="info-list">
                  <div v-if="letter.posted_date" class="info-item">
                    <span class="info-label">发布日期</span>
                    <span class="info-value">{{ letter.posted_date }}</span>
                  </div>
                  <div v-if="letter.closeout_date" class="info-item">
                    <span class="info-label">关闭日期</span>
                    <span class="info-value">{{ letter.closeout_date }}</span>
                  </div>
                  <div v-if="letter.response_date" class="info-item">
                    <span class="info-label">回复日期</span>
                    <span class="info-value">{{ letter.response_date }}</span>
                  </div>
                  <div v-if="letter.status" class="info-item">
                    <span class="info-label">状态</span>
                    <span class="badge" :class="getStatusBadgeClass(letter.status)">
                      {{ letter.status === 'active' ? '进行中' : '已关闭' }}
                    </span>
                  </div>
                  <div v-if="letter.country" class="info-item">
                    <span class="info-label">国家</span>
                    <span class="info-value">{{ letter.country }}</span>
                  </div>
                  <div v-if="letter.region" class="info-item">
                    <span class="info-label">地区</span>
                    <span class="info-value">{{ letter.region }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 相关链接 -->
            <div v-if="letter.url" class="card links-card animate-fade-in-right delay-200">
              <div class="card-header">
                <h3>相关链接</h3>
              </div>
              <div class="card-body">
                <a :href="letter.url" target="_blank" class="link-item">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  <span>FDA 官方原文</span>
                </a>
              </div>
            </div>

            <!-- 分享 -->
            <div class="card share-card animate-fade-in-right delay-300">
              <div class="card-header">
                <h3>分享</h3>
              </div>
              <div class="card-body">
                <div class="share-buttons">
                  <button @click="copyLink" class="share-btn" title="复制链接">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                    <span>复制链接</span>
                  </button>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-section">
      <div class="container">
        <div class="error-state">
          <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2>警告信未找到</h2>
          <p>请求的警告信不存在或已被删除</p>
          <router-link to="/letters" class="btn btn-primary">
            返回列表
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFavorites } from '../composables/useFavorites.js'

const route = useRoute()
const router = useRouter()
const { isFavorite, toggleFavorite } = useFavorites()

const API = window.location.origin + '/api'
const letter = ref(null)
const loading = ref(true)

// 格式化翻译文本为学术论文格式
function formatTranslation(text) {
  if (!text) return ''

  // 清除 * 和 # 符号
  let cleaned = text.replace(/[\*#]/g, '')

  // 分割段落（双换行或更多换行分隔）
  const paragraphs = cleaned.split(/\n{2,}/)

  let formatted = paragraphs.map((para, index) => {
    let trimmed = para.trim()
    if (!trimmed) return ''

    // 保留原始换行结构
    let content = trimmed.replace(/\n/g, '<br>')

    // 检查是否是标题行（全部大写、短行、含冒号等）
    const firstLine = trimmed.split('\n')[0].trim()
    const isTitle = (
      firstLine.length < 50 &&
      (firstLine === firstLine.toUpperCase() || /^[A-Z\s\-:.,]+$/.test(firstLine) ||
       /^(第[一二三四五六七八九十]+[条部章节]|摘要|Summary|SUBJECT|DEAR|REGARDING|CONCLUSION|FINDINGS|VIOLATIONS|COMMENTS|RECOMMENDATIONS|RESPONSE|WARNING)/.test(firstLine))
    )

    if (isTitle && index > 0) {
      // 标题样式
      return `<h3 class="letter-heading">${content}</h3>`
    }

    // 检测信头部分（日期、地址等）
    const startsWithSpecial = /^(Dear|To:|From:|Date:|Subject:|Re:|邮编|P\.O\.|RE:|\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i.test(trimmed)

    if (startsWithSpecial && index === 0) {
      // 信头部分不缩进
      return `<div class="letter-header-content">${content}</div>`
    }

    // 普通段落添加首行缩进
    return `<p class="letter-para">${content}</p>`
  }).join('')

  return formatted
}

// 方法
function goBack() {
  router.back()
}

async function fetchLetter() {
  loading.value = true
  try {
    const resp = await fetch(`${API}/letters/${route.params.id}`)
    if (!resp.ok) throw new Error('Letter not found')
    letter.value = await resp.json()
  } catch (e) {
    console.error('获取警告信详情失败:', e)
    letter.value = null
  } finally {
    loading.value = false
  }
}

async function copyLink() {
  try {
    await navigator.clipboard.writeText(window.location.href)
    alert('链接已复制')
  } catch (e) {
    console.error('复制失败:', e)
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

function getSeverityBadgeClass(severity) {
  const classes = {
    'critical': 'badge-danger',
    'major': 'badge-warning',
    'minor': 'badge-info'
  }
  return classes[severity] || 'badge-warning'
}

function getRiskWidth(riskLevel) {
  const widths = {
    'High': '100%',
    'Medium': '66%',
    'Low': '33%'
  }
  return widths[riskLevel] || '0%'
}

function getRiskBarClass(riskLevel) {
  const classes = {
    'High': 'risk-high',
    'Medium': 'risk-medium',
    'Low': 'risk-low'
  }
  return classes[riskLevel] || ''
}

// 初始化
onMounted(() => {
  fetchLetter()
})
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════
   Page Layout
═══════════════════════════════════════════════════════════════ */
.detail-page {
  min-height: 100vh;
  background: var(--bg-secondary);
  padding-top: var(--header-height);
}

/* ═══════════════════════════════════════════════════════════════
   Page Header
═══════════════════════════════════════════════════════════════ */
.page-header {
  background: #f5f5f5;
  border-bottom: 1px solid var(--border-default);
  padding: var(--space-4) 0;
  margin-bottom: 0; /* 移除避免与顶部栏重叠 */
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--text-tertiary);
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

/* ═══════════════════════════════════════════════════════════════
   Loading
═══════════════════════════════════════════════════════════════ */
.loading-section {
  padding: var(--space-10) 0;
}

.skeleton-detail {
  max-width: 800px;
}

.skeleton-title {
  height: 40px;
  width: 60%;
  margin-bottom: var(--space-4);
}

.skeleton-subtitle {
  height: 24px;
  width: 40%;
  margin-bottom: var(--space-8);
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.skeleton-card {
  height: 100px;
}

.skeleton-content {
  height: 200px;
}

/* ═══════════════════════════════════════════════════════════════
   Content Section
═══════════════════════════════════════════════════════════════ */
.content-section {
  padding: var(--space-8) 0 var(--space-16);
}

/* Letter Header */
.letter-header {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: 8px;
  padding: var(--space-8);
  margin-bottom: var(--space-8);
}

.header-top {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

@media (min-width: 768px) {
  .header-top {
    flex-direction: row;
    align-items: flex-start;
    justify-content: space-between;
  }
}

.header-badges {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.is-favorite {
  color: var(--color-danger-500) !important;
}

.letter-title {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-6);
}

@media (min-width: 768px) {
  .letter-title {
    font-size: var(--text-4xl);
  }
}

.letter-meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.meta-card {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
}

.meta-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F2F9FC;
  color: #0000C9;
  border-radius: var(--radius-lg);
}


.meta-label {
  display: block;
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  margin-bottom: 2px;
}

.meta-value {
  display: block;
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.letter-subject {
  padding-top: var(--space-6);
  border-top: 1px solid var(--border-default);
}

.letter-subject h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.letter-subject p {
  font-size: var(--text-base);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
}

/* ═══════════════════════════════════════════════════════════════
   Letter Body
═══════════════════════════════════════════════════════════════ */
.letter-body {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-8);
}

@media (min-width: 1024px) {
  .letter-body {
    grid-template-columns: 1fr 300px;
  }
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/* Cards */
.card {
  background: var(--bg-primary);
  border: 1px solid #e5e7eb;
  border-radius: 8px;
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
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.card-title h2,
.card-title h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.title-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
}

.ai-icon {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.violations-icon {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.citations-icon {
  background: rgba(0, 0, 201, 0.1);
  color: #0000C9;
}

.translation-icon {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.card-body {
  padding: var(--space-6);
}

/* ═══════════════════════════════════════════════════════════════
   AI Card
═══════════════════════════════════════════════════════════════ */
.risk-assessment {
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border-default);
}

.risk-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.risk-label {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-secondary);
}

.badge-lg {
  padding: var(--space-1-5) var(--space-3);
  font-size: var(--text-sm);
}

.risk-bar {
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.risk-progress {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width var(--duration-slow) var(--ease-out);
}

.risk-high {
  background: linear-gradient(90deg, var(--color-danger-500), var(--color-danger-600));
}

.risk-medium {
  background: linear-gradient(90deg, var(--color-warning-500), var(--color-warning-600));
}

.risk-low {
  background: linear-gradient(90deg, var(--color-success-500), var(--color-success-600));
}

.violation-type {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border-default);
}

.violation-type .label {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
}

.violation-type .value {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  padding: var(--space-1) var(--space-3);
  background: var(--bg-tertiary);
  border-radius: var(--radius-full);
}

.summary {
  margin-bottom: var(--space-6);
}

.summary:last-child {
  margin-bottom: 0;
}

.summary h3 {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-3);
}

.summary-content {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
}

.summary-content p {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
}

.key-findings h3 {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-3);
}

.findings-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.findings-list li {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.findings-list li svg {
  color: var(--color-success-500);
  margin-top: 2px;
}

/* ═══════════════════════════════════════════════════════════════
   Violations Card
═══════════════════════════════════════════════════════════════ */
.violations-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.violation-item {
  padding: var(--space-4);
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border-left: 4px solid var(--border-default);
}

.violation-item:has(.badge-danger) {
  border-left-color: var(--color-danger-500);
}

.violation-item:has(.badge-warning) {
  border-left-color: var(--color-warning-500);
}

.violation-item:has(.badge-info) {
  border-left-color: var(--color-info-500);
}

.violation-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}

.violation-category {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  padding: 2px 8px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-full);
}

.violation-item h4 {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.violation-item p {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
}

.description-zh {
  margin-top: var(--space-2);
  padding-top: var(--space-2);
  border-top: 1px solid var(--border-default);
}

/* ═══════════════════════════════════════════════════════════════
   Citations Card
═══════════════════════════════════════════════════════════════ */
.citations-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.citation-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
}

.citation-code {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: #0000C9;
}

.cfr-part {
  color: #0000C9;
}

.cfr-section {
  color: #3333D4;
}

.citation-text {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
}

/* ═══════════════════════════════════════════════════════════════
   Translation Card - Academic Paper Format
═══════════════════════════════════════════════════════════════ */
.translation-content {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  max-height: 800px;
  overflow-y: auto;
}

.translation-content pre {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
}

/* 学术论文排版样式 */
.academic-format {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 16px;
  line-height: 2;
  color: var(--text-primary);
  padding: 32px 40px;
  background: white;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  text-align: justify; /* 两端对齐 */
}

/* 信件标题样式 */
.academic-format :deep(.letter-heading) {
  font-size: 18px;
  font-weight: 700;
  color: #0000C9;
  margin: 28px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-default);
  line-height: 1.5;
}

.academic-format :deep(.letter-heading:first-child) {
  margin-top: 0;
}

/* 信头样式（日期、收件人等） */
.academic-format :deep(.letter-header-content) {
  margin-bottom: 16px;
  line-height: 1.8;
  font-size: 15px;
  color: var(--text-secondary);
}

/* 段落样式 - 学术论文格式 */
.academic-format :deep(.letter-para) {
  font-size: 16px;
  line-height: 2;
  color: var(--text-primary);
  margin-bottom: 1.5em;
  text-indent: 2em; /* 首行缩进 2 个字符 */
}

/* 第一段不缩进（开头问候语等） */
.academic-format :deep(.letter-para:first-of-type) {
  text-indent: 0;
}

/* 段落内的换行保持 */
.academic-format :deep(.letter-para br) {
  content: '';
  display: block;
  margin: 4px 0;
}

/* ═══════════════════════════════════════════════════════════════
   Sidebar Cards
═══════════════════════════════════════════════════════════════ */
.info-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.info-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--border-default);
}

.info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-label {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
}

.info-value {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.link-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  color: #0000C9;
  text-decoration: none;
  transition: all var(--duration-fast);
}

.link-item:hover {
  background: #F2F9FC;
}


.share-buttons {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.share-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-3);
  background: var(--bg-secondary);
  border: none;
  border-radius: var(--radius-lg);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all var(--duration-fast);
}

.share-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

/* ═══════════════════════════════════════════════════════════════
   Error State
═══════════════════════════════════════════════════════════════ */
.error-section {
  padding: var(--space-16) 0;
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--space-12);
}

.error-icon {
  width: 80px;
  height: 80px;
  color: var(--text-tertiary);
  opacity: 0.5;
  margin-bottom: var(--space-6);
}

.error-state h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.error-state p {
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin-bottom: var(--space-6);
}
</style>
