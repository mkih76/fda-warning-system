<template>
  <div class="detail-page">
    <!-- 面包屑 -->
    <div class="breadcrumb">
      <router-link to="/letters" class="back-link">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        <span>返回列表</span>
      </router-link>
      <div v-if="letter" class="toolbar">
        <button @click="copyText(letter.fda_id)" class="toolbar-btn" title="复制 FDA ID">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
        </button>
        <button @click="copyText(letter.company_name)" class="toolbar-btn" title="复制公司名">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 骨架屏 -->
    <div v-if="loading" class="skeleton-wrapper">
      <div class="skeleton skeleton-title"></div>
      <div class="skeleton skeleton-subtitle"></div>
      <div class="skeleton-grid">
        <div v-for="i in 6" :key="i" class="skeleton skeleton-card"></div>
      </div>
      <div class="skeleton skeleton-content"></div>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
      </svg>
      <p class="error-text">{{ error }}</p>
      <router-link to="/letters" class="error-link">返回列表重新浏览</router-link>
    </div>

    <!-- 正文 -->
    <template v-if="letter">
      <!-- 标题区 -->
      <div class="title-section">
        <div class="badges">
          <span :class="letter.status === 'active' ? 'status-active' : 'status-closed'">
            {{ statusLabel }}
          </span>
          <span class="badge-office">{{ letter.issuing_office || 'FDA' }}</span>
          <span v-if="letter.country" class="badge-country">{{ letter.country }}</span>
          <span v-if="letter.fei_number" class="badge-fei">FEI: {{ letter.fei_number }}</span>
        </div>
        <h1 class="letter-title">{{ letter.subject }}</h1>
        <p class="company-name">{{ letter.company_name }}</p>
      </div>

      <!-- 信息卡片 -->
      <div class="card">
        <div class="card-header">
          <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <h2 class="header-title">基本信息</h2>
        </div>
        <div class="info-grid">
          <div v-for="field in infoFields" :key="field.key" class="info-item">
            <div class="info-icon">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" v-html="field.icon" viewBox="0 0 24 24"/>
            </div>
            <div class="info-content">
              <p class="info-label">{{ field.label }}</p>
              <p class="info-value">{{ field.value }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 分析 -->
      <div v-if="letter.analysis" class="card">
        <div class="card-header">
          <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
          <h2 class="header-title">AI 分析</h2>
          <div class="header-right">
            <span v-if="letter.analysis.risk_level" class="risk-badge" :class="riskLevelClass(letter.analysis.risk_level)">
              {{ riskLevelLabel(letter.analysis.risk_level) }}
            </span>
            <span v-if="letter.analysis.violation_type" class="violation-badge">
              {{ letter.analysis.violation_type }}
            </span>
          </div>
        </div>
        <div class="card-body">
          <!-- 中文摘要 -->
          <div v-if="letter.analysis.summary_zh" class="summary-box">
            <div class="summary-header">
              <span class="summary-label">中文摘要</span>
              <button @click="copyText(letter.analysis.summary_zh)" class="copy-btn" title="复制摘要">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
              </button>
            </div>
            <p class="summary-text">{{ letter.analysis.summary_zh }}</p>
          </div>
          <!-- 英文摘要 -->
          <div v-if="letter.analysis.summary_en" class="summary-section">
            <h3 class="section-label">English Summary</h3>
            <p class="section-text">{{ letter.analysis.summary_en }}</p>
          </div>
          <!-- 关键发现 -->
          <div v-if="letter.analysis.key_findings && letter.analysis.key_findings.length" class="findings-section">
            <h3 class="section-label">关键发现</h3>
            <div class="findings-list">
              <div v-for="(finding, i) in letter.analysis.key_findings" :key="i" class="finding-item">
                <span class="finding-num">{{ i + 1 }}</span>
                <p class="finding-text">{{ finding }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CFR 引用 + 违规分类 -->
      <div class="two-col">
        <!-- CFR 引用 -->
        <div class="card">
          <div class="card-header">
            <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <h2 class="header-title">CFR 条款引用</h2>
            <span v-if="letter.citations?.length" class="count">{{ letter.citations.length }} 条</span>
          </div>
          <div class="card-body">
            <div v-if="letter.citations?.length" class="cfr-list">
              <span v-for="c in letter.citations" :key="c.cfr_section" class="cfr-badge">
                21 CFR {{ c.cfr_section }}
              </span>
            </div>
            <div v-else class="empty-box">暂无 CFR 引用</div>
          </div>
        </div>

        <!-- 违规分类 -->
        <div class="card">
          <div class="card-header">
            <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
            </svg>
            <h2 class="header-title">违规分类</h2>
            <span v-if="letter.violations?.length" class="count">{{ letter.violations.length }} 项</span>
          </div>
          <div class="card-body">
            <div v-if="letter.violations?.length" class="violations-list">
              <div v-for="v in letter.violations" :key="v.violation_type" class="violation-item">
                <span class="severity-badge" :class="severityClass(v.severity)">{{ severityLabel(v.severity) }}</span>
                <div class="violation-info">
                  <p class="violation-type">{{ v.system_category }} / {{ v.violation_type }}</p>
                  <p class="violation-desc">{{ v.description || v.description_zh }}</p>
                </div>
              </div>
            </div>
            <div v-else class="empty-box">暂无违规记录</div>
          </div>
        </div>
      </div>

      <!-- 信件正文（中英双语并排） -->
      <div class="two-col" v-if="letter.analysis?.translation_zh || letter.full_text">
        <!-- 中文翻译 -->
        <div v-if="letter.analysis?.translation_zh" class="card letter-card">
          <div class="card-header card-header-blue">
            <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
            </svg>
            <h2 class="header-title">中文翻译</h2>
            <span class="char-count">{{ letter.analysis.translation_zh.length.toLocaleString() }} 字</span>
            <button @click="copyText(letter.analysis.translation_zh)" class="copy-btn" title="复制翻译">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
              </svg>
            </button>
          </div>
          <div class="letter-body">
            <div class="letter-content" v-html="formatLetterContent(letter.analysis.translation_zh)"></div>
          </div>
        </div>

        <!-- 英文原文 -->
        <div v-if="letter.full_text" class="card letter-card">
          <div class="card-header">
            <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <h2 class="header-title">英文原文</h2>
            <span class="char-count">{{ letter.full_text.length.toLocaleString() }} 字符</span>
            <a v-if="letter.url" :href="letter.url" target="_blank" class="fda-link">
              FDA 原文
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
            </a>
            <button @click="copyText(letter.full_text)" class="copy-btn" title="复制原文">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
              </svg>
            </button>
          </div>
          <div class="letter-body">
            <div class="letter-content letter-mono" v-html="formatLetterContent(letter.full_text, true)"></div>
          </div>
        </div>
      </div>

      <!-- 关联警告信 -->
      <div v-if="relatedLetters.length" class="card">
        <div class="card-header">
          <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
          <h2 class="header-title">同一企业记录</h2>
          <span class="count">{{ relatedLetters.length }} 封</span>
        </div>
        <div class="card-body">
          <div class="related-list">
            <div v-for="rl in relatedLetters" :key="rl.fda_id" class="related-item">
              <div class="related-dot" :class="rl.status === 'active' ? 'dot-active' : 'dot-closed'"></div>
              <div class="related-info">
                <router-link :to="`/letters/${rl.id}`" class="related-link">
                  {{ rl.subject || rl.fda_id }}
                </router-link>
                <p class="related-meta">{{ rl.posted_date }} · {{ rl.issuing_office }}</p>
              </div>
              <span class="related-status">{{ rl.status === 'active' ? '进行中' : '已关闭' }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const API = window.location.origin + '/api'

const letter = ref(null)
const loading = ref(true)
const error = ref(null)
const relatedLetters = ref([])

const statusLabel = computed(() => {
  const map = { active: '进行中', closed: '已关闭', escalated: '升级中' }
  return map[letter.value?.status] || letter.value?.status || '未知'
})

const infoFields = computed(() => {
  const l = letter.value
  if (!l) return []
  return [
    { key: 'fda_id', label: 'FDA ID', value: l.fda_id, icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 012-2h2a2 2 0 012 2v1m-4 0v9"/>' },
    { key: 'posted_date', label: '公布日期', value: l.posted_date || '—', icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>' },
    { key: 'issue_date', label: '签发日期', value: l.issue_date || '—', icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>' },
    { key: 'fei_number', label: 'FEI 编号', value: l.fei_number || '—', icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>' },
    { key: 'country', label: '国家', value: l.country || '—', icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>' },
    { key: 'closeout', label: '关闭日期', value: l.closeout_date || '—', icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>' },
  ]
})

function severityClass(s) {
  return {
    critical: 'severity-critical',
    major: 'severity-major',
    minor: 'severity-minor'
  }[s] || 'severity-default'
}

function severityLabel(s) {
  return { critical: '严重', major: '主要', minor: '轻微' }[s] || s || '未知'
}

function riskLevelClass(level) {
  return {
    'High': 'risk-high',
    'Medium': 'risk-medium',
    'Low': 'risk-low',
  }[level] || 'risk-default'
}

function riskLevelLabel(level) {
  return { High: '⚠️ 高风险', Medium: '中等风险', Low: '低风险' }[level] || level || '未知'
}

function copyText(text) {
  navigator.clipboard.writeText(text).catch(() => {})
}

function formatLetterContent(text, isEnglish = false) {
  if (!text) return ''
  let html = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  const paragraphs = html.split(/\n{2,}/)
  const formatted = paragraphs.map(p => {
    p = p.trim()
    if (!p) return ''
    const isHeading = /^[A-Z\s\-:.,]{20,}$/.test(p) || 
                      /^第[一二三四五六七八九十]+[条部章节]/.test(p) ||
                      /^[一二三四五六七八九十]+[、.]/.test(p) ||
                      /^(摘要|Summary|SUBJECT|RE:|WARNING|NOTICE|DEAR|REGARDING|CONCLUSION|FINDINGS|VIOLATIONS|COMMENTS|RECOMMENDATIONS|RESPONSE|ACTION REQUIRED)/i.test(p.split('\n')[0])
    const isChineseHeading = /^\s*[一二三四五六七八九十]+[、.．]/.test(p) ||
                             /^\s*第[一二三四五六七八九十百千]+[条章节部]/.test(p) ||
                             /^\s*[（(][一二三四五六七八九十]+[）)]/.test(p) ||
                             p.length < 50 && /^[A-Z\u4e00-\u9fff].*[：:]\s*$/.test(p)
    if (isHeading || isChineseHeading) {
      return `<h3 class="letter-heading">${p.replace(/\n/g, '<br/>')}</h3>`
    }
    if (isEnglish) {
      p = p.replace(/(\d{3}\.\d+[a-z]?(?:\([a-z]\))?)/gi, '<span class="cfr-inline">$1</span>')
    }
    return `<p class="letter-para">${p.replace(/\n/g, '<br/>')}</p>`
  }).filter(Boolean)
  return formatted.join('')
}

onMounted(async () => {
  try {
    const resp = await fetch(`${API}/letters/${route.params.id}`)
    if (!resp.ok) { error.value = '未找到该警告信'; return }
    letter.value = await resp.json()
    if (letter.value.company_name) {
      try {
        const relResp = await fetch(`${API}/letters/company/${encodeURIComponent(letter.value.company_name)}`)
        if (relResp.ok) {
          const all = await relResp.json()
          relatedLetters.value = all.filter(l => l.fda_id !== letter.value.fda_id).slice(0, 5)
        }
      } catch {}
    }
  } catch(e) { error.value = '加载失败，请稍后重试' }
  finally { loading.value = false }
})
</script>

<style scoped>
.detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 104px 32px 64px;
}

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-2);
  transition: color 0.2s;
}

.back-link:hover { color: var(--accent); }
.back-link:hover svg { transform: translateX(-4px); }
.back-link svg { transition: transform 0.2s; }

.toolbar {
  display: flex;
  gap: 8px;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: white;
  color: var(--text-2);
  cursor: pointer;
  transition: all 0.2s;
}

.toolbar-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

/* Skeleton */
.skeleton-wrapper { display: flex; flex-direction: column; gap: 20px; }
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: 8px;
}
.skeleton-title { height: 40px; width: 60%; }
.skeleton-subtitle { height: 24px; width: 40%; }
.skeleton-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.skeleton-card { height: 100px; }
.skeleton-content { height: 300px; }

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* Error */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 0;
  color: var(--text-3);
}
.error-icon { width: 64px; height: 64px; margin-bottom: 16px; opacity: 0.3; }
.error-text { font-size: 18px; font-weight: 500; margin-bottom: 8px; }
.error-link { color: var(--accent); font-size: 14px; }
.error-link:hover { text-decoration: underline; }

/* Title section */
.title-section { margin-bottom: 32px; }
.badges { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.letter-title { font-size: 28px; font-weight: 700; color: var(--text); margin: 0 0 8px 0; line-height: 1.3; }
.company-name { font-size: 18px; color: var(--text-2); margin: 0; }

/* Badges */
.status-active {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 14px; border-radius: 6px;
  font-size: 13px; font-weight: 600;
  background: rgba(220, 38, 38, 0.1); color: var(--danger);
}
.status-closed {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 14px; border-radius: 6px;
  font-size: 13px; font-weight: 600;
  background: rgba(16, 185, 129, 0.1); color: var(--success);
}
.badge-office, .badge-country, .badge-fei {
  display: inline-block; padding: 6px 12px; border-radius: 6px;
  font-size: 12px; font-weight: 500;
  background: var(--surface-3); color: var(--text-2);
}

/* Card */
.card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  margin-bottom: 20px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
}

.card-header-blue {
  background: rgba(0, 149, 255, 0.05);
}

.header-icon { width: 20px; height: 20px; color: var(--accent); flex-shrink: 0; }
.header-title { font-size: 14px; font-weight: 600; color: var(--text); margin: 0; text-transform: uppercase; letter-spacing: 0.05em; }
.header-right { display: flex; gap: 8px; margin-left: auto; align-items: center; }
.count { font-size: 12px; color: var(--text-3); margin-left: auto; }

.card-body { padding: 20px; }

/* Info grid */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

.info-item { display: flex; align-items: flex-start; gap: 12px; }

.info-icon {
  width: 36px; height: 36px; border-radius: 8px;
  background: rgba(0, 149, 255, 0.1); color: var(--accent);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.info-label { font-size: 12px; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.05em; margin: 0; }
.info-value { font-size: 14px; font-weight: 600; color: var(--text); margin: 4px 0 0 0; }

/* Summary */
.summary-box {
  background: rgba(0, 149, 255, 0.05);
  border: 1px solid rgba(0, 149, 255, 0.15);
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 16px;
}
.summary-header { display: flex; align-items: center; margin-bottom: 8px; }
.summary-label { font-size: 12px; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em; }
.summary-text { font-size: 14px; line-height: 1.7; color: var(--text); margin: 0; }

.summary-section { margin-bottom: 16px; }
.section-label { font-size: 12px; font-weight: 600; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 8px 0; }
.section-text { font-size: 14px; line-height: 1.7; color: var(--text-2); margin: 0; }

/* Findings */
.findings-section { margin-top: 16px; }
.findings-list { display: flex; flex-direction: column; gap: 8px; }
.finding-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 12px; background: var(--surface-3); border-radius: 8px;
}
.finding-num {
  width: 24px; height: 24px; border-radius: 50%;
  background: var(--accent); color: white;
  font-size: 12px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.finding-text { font-size: 14px; color: var(--text); line-height: 1.6; margin: 0; }

/* Two column */
.two-col {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

@media (min-width: 768px) {
  .two-col { grid-template-columns: 1fr 1fr; }
}

/* Risk badges */
.risk-badge { padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; }
.risk-high { background: rgba(220, 38, 38, 0.1); color: var(--danger); }
.risk-medium { background: rgba(245, 158, 11, 0.1); color: var(--warning); }
.risk-low { background: rgba(0, 149, 255, 0.1); color: var(--accent); }
.violation-badge { padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 500; background: var(--surface-3); color: var(--text-2); }

/* CFR */
.cfr-list { display: flex; flex-wrap: wrap; gap: 8px; }
.cfr-badge {
  display: inline-block; padding: 6px 12px; border-radius: 6px;
  font-size: 12px; font-family: monospace; font-weight: 500;
  background: rgba(0, 149, 255, 0.08); color: var(--accent);
}

/* Violations */
.violations-list { display: flex; flex-direction: column; gap: 12px; }
.violation-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 12px; background: var(--surface-3); border-radius: 8px;
}
.severity-badge {
  padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;
  flex-shrink: 0;
}
.severity-critical { background: rgba(220, 38, 38, 0.1); color: var(--danger); }
.severity-major { background: rgba(245, 158, 11, 0.1); color: var(--warning); }
.severity-minor { background: rgba(0, 149, 255, 0.1); color: var(--accent); }
.severity-default { background: var(--surface-3); color: var(--text-3); }
.violation-info { min-width: 0; }
.violation-type { font-size: 13px; font-weight: 600; color: var(--text); margin: 0; }
.violation-desc { font-size: 12px; color: var(--text-3); margin: 4px 0 0 0; }

.empty-box { padding: 24px; text-align: center; color: var(--text-3); font-size: 14px; }

/* Letter body */
.letter-card { display: flex; flex-direction: column; }
.letter-body { flex: 1; overflow-y: auto; max-height: 600px; padding: 20px; }
.char-count { font-size: 12px; color: var(--text-3); margin-left: auto; font-family: monospace; }
.copy-btn {
  display: flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border-radius: 6px;
  border: none; background: transparent; color: var(--text-3);
  cursor: pointer; transition: all 0.15s;
}
.copy-btn:hover { background: var(--surface-3); color: var(--accent); }
.fda-link {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 12px; color: var(--accent); margin-left: 8px;
}
.fda-link:hover { text-decoration: underline; }

/* Letter content formatting */
.letter-content {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  color: #333333;
}
.letter-mono { font-family: 'SF Mono', 'Fira Code', monospace; font-size: 13px; }
.letter-content :deep(.letter-heading) {
  font-size: 16px; font-weight: 700; line-height: 1.6;
  color: #333; margin: 24px 0 12px 0;
  padding-bottom: 8px; border-bottom: 1px solid #e5e7eb;
}
.letter-content :deep(.letter-heading:first-child) { margin-top: 0; }
.letter-content :deep(.letter-para) {
  font-size: 15px; line-height: 1.7; color: #444;
  margin-bottom: 12px;
}
.letter-content :deep(.letter-para:last-child) { margin-bottom: 0; }
.letter-content :deep(.cfr-inline) {
  color: var(--accent); font-weight: 600;
  background: rgba(0, 149, 255, 0.08);
  padding: 0 4px; border-radius: 3px;
}

/* Related letters */
.related-list { display: flex; flex-direction: column; gap: 8px; }
.related-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px; border-radius: 8px;
  transition: background 0.15s;
}
.related-item:hover { background: var(--surface-3); }
.related-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-active { background: var(--success); }
.dot-closed { background: var(--text-3); }
.related-info { flex: 1; min-width: 0; }
.related-link {
  font-size: 14px; font-weight: 500; color: var(--text);
  display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.related-link:hover { color: var(--accent); }
.related-meta { font-size: 12px; color: var(--text-3); margin: 4px 0 0 0; }
.related-status { font-size: 12px; color: var(--text-3); flex-shrink: 0; }

@media (max-width: 640px) {
  .detail-page { padding: 88px 16px 48px; }
  .info-grid { grid-template-columns: 1fr; }
  .two-col { grid-template-columns: 1fr; }
}
</style>
