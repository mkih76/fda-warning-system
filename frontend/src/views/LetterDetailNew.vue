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
          <div class="skeleton skeleton-content"></div>
        </div>
      </div>
    </div>

    <!-- 内容 -->
    <div v-else-if="letter" class="content-section">
      <div class="container">
        <!-- 顶部栏：FDA链接、风险等级、违规类型 -->
        <div class="top-bar">
          <div class="top-bar-left">
            <a v-if="letter.url" :href="letter.url" target="_blank" class="fda-link">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              <span>查看FDA原文</span>
            </a>
          </div>
          <div class="top-bar-right">
            <span v-if="letter.analysis?.risk_level" class="risk-badge" :class="getRiskBadgeClass(letter.analysis.risk_level)">
              {{ letter.analysis.risk_level }}风险
            </span>
            <span v-if="letter.analysis?.violation_type" class="violation-badge">
              {{ letter.analysis.violation_type }}
            </span>
          </div>
        </div>

        <!-- 学术论文主内容区 -->
        <div class="academic-paper">
          <!-- 论文标题 -->
          <h1 class="paper-title">{{ cleanText(letter.company_name || '无标题') }}</h1>

          <!-- 元数据块 -->
          <div class="paper-metadata">
            <div class="metadata-row">
              <span class="metadata-label">发布日期：</span>
              <span class="metadata-value">{{ letter.issue_date || '未知' }}</span>
            </div>
            <div class="metadata-row">
              <span class="metadata-label">签发办公室：</span>
              <span class="metadata-value">{{ letter.issuing_office || '未知' }}</span>
            </div>
            <div class="metadata-row">
              <span class="metadata-label">风险等级：</span>
              <span class="metadata-value">{{ letter.analysis?.risk_level || '未评估' }}</span>
            </div>
            <div class="metadata-row">
              <span class="metadata-label">违规类型：</span>
              <span class="metadata-value">{{ letter.analysis?.violation_type || '未分类' }}</span>
            </div>
          </div>

          <!-- 摘要部分 -->
          <div v-if="letter.analysis?.summary_zh" class="paper-abstract">
            <h2 class="abstract-title">摘要</h2>
            <div class="abstract-content" v-html="cleanText(letter.analysis.summary_zh)"></div>
          </div>

          <!-- 正文内容（中文翻译） -->
          <div v-if="letter.analysis?.translation_zh" class="paper-body">
            <div class="body-content" v-html="formatTranslation(letter.analysis.translation_zh)"></div>
          </div>

          <!-- 无内容提示 -->
          <div v-else class="no-content">
            <p>暂无中文翻译内容</p>
          </div>
        </div>

        <!-- 版权信息 -->
        <div class="copyright">
          <p>© FDA警告信翻译系统 | 内容仅供学术研究参考</p>
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
          <router-link to="/letters" class="btn-primary">
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

const route = useRoute()
const router = useRouter()

const API = window.location.origin + '/api'
const letter = ref(null)
const loading = ref(true)

// 清除所有 * 和 # 符号
function cleanText(text) {
  if (!text) return ''
  // 使用正则替换所有 * 和 # 符号
  let cleaned = text.replace(/[\*#]/g, '')
  // 将换行转换为 <br> 以保留段落
  cleaned = cleaned.replace(/\n/g, '<br>')
  return cleaned
}

// 格式化翻译文本为学术论文格式
function formatTranslation(text) {
  if (!text) return ''
  
  // 先清除特殊符号
  let cleaned = text.replace(/[\*#]/g, '')
  
  // 将双换行转换为段落标记
  let paragraphs = cleaned.split(/\n\s*\n/)
  let formatted = paragraphs.map(para => {
    let trimmed = para.trim()
    if (trimmed) {
      return `<p>${trimmed.replace(/\n/g, ' ')}</p>`
    }
    return ''
  }).join('')
  
  return formatted
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

function getRiskBadgeClass(riskLevel) {
  const classes = {
    'High': 'risk-high',
    'Medium': 'risk-medium',
    'Low': 'risk-low'
  }
  return classes[riskLevel] || 'risk-medium'
}

// 初始化
onMounted(() => {
  fetchLetter()
})
</script>

<style scoped>
/* 基础变量 */
:root {
  --pfizer-blue: #0000C9;
  --text-primary: #2c3e50;
  --text-secondary: #7f8c8d;
  --border-color: #e0e0e0;
  --bg-light: #f8f9fa;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Page Layout */
.detail-page {
  min-height: 100vh;
  background: var(--bg-light);
  padding-top: 60px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 页头 */
.page-header {
  background: white;
  border-bottom: 1px solid var(--border-color);
  padding: 16px 0;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: white;
}

.breadcrumb {
  font-size: 14px;
}

.breadcrumb a {
  color: var(--pfizer-blue);
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.separator {
  margin: 0 8px;
  color: var(--text-secondary);
}

.current {
  color: var(--text-secondary);
}

/* 加载骨架 */
.loading-section {
  padding: 40px 0;
}

.skeleton-detail {
  max-width: 800px;
  margin: 0 auto;
}

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-title {
  height: 40px;
  width: 70%;
  margin-bottom: 24px;
}

.skeleton-content {
  height: 400px;
  width: 100%;
}

/* 顶部栏 */
.top-bar {
  background: white;
  border-radius: 8px;
  padding: 16px 24px;
  margin-bottom: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.top-bar-left {
  display: flex;
  gap: 16px;
}

.fda-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--pfizer-blue);
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.2s;
}

.fda-link:hover {
  opacity: 0.8;
  text-decoration: underline;
}

.fda-link svg {
  width: 20px;
  height: 20px;
}

.top-bar-right {
  display: flex;
  gap: 12px;
}

.risk-badge,
.violation-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.risk-high {
  background: #fee;
  color: #c00;
  border: 1px solid #fcc;
}

.risk-medium {
  background: #fef3c7;
  color: #d97706;
  border: 1px solid #fde68a;
}

.risk-low {
  background: #d1fae5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.violation-badge {
  background: #e0e7ff;
  color: #4f46e5;
  border: 1px solid #c7d2fe;
}

/* 学术论文样式 */
.academic-paper {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-radius: 8px;
  padding: 48px 56px;
}

/* 论文标题 */
.paper-title {
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--pfizer-blue);
  color: var(--text-primary);
  line-height: 1.4;
}

/* 元数据块 */
.paper-metadata {
  background: var(--bg-light);
  padding: 20px;
  margin-bottom: 32px;
  border-left: 4px solid var(--pfizer-blue);
  font-size: 14px;
}

.metadata-row {
  margin-bottom: 8px;
  display: flex;
  flex-wrap: wrap;
}

.metadata-row:last-child {
  margin-bottom: 0;
}

.metadata-label {
  font-weight: 600;
  width: 100px;
  color: var(--text-primary);
}

.metadata-value {
  color: var(--text-secondary);
  flex: 1;
}

/* 摘要样式 */
.paper-abstract {
  margin-bottom: 40px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
  font-style: italic;
}

.abstract-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--pfizer-blue);
  letter-spacing: 1px;
}

.abstract-content {
  font-size: 15px;
  line-height: 1.7;
  color: var(--text-primary);
}

/* 正文样式 */
.paper-body {
  margin-top: 24px;
}

.body-content {
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-primary);
}

.body-content p {
  margin-bottom: 1.2em;
  text-align: justify;
}

.body-content p:last-child {
  margin-bottom: 0;
}

/* 无内容提示 */
.no-content {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
  font-size: 16px;
}

/* 版权信息 */
.copyright {
  margin-top: 48px;
  text-align: center;
  padding: 24px 0;
  border-top: 1px solid var(--border-color);
  font-size: 12px;
  color: var(--text-secondary);
}

/* 错误状态 */
.error-section {
  padding: 80px 0;
}

.error-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 8px;
  max-width: 500px;
  margin: 0 auto;
}

.error-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  color: #e74c3c;
}

.error-state h2 {
  font-size: 24px;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.error-state p {
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.btn-primary {
  display: inline-block;
  padding: 10px 24px;
  background: var(--pfizer-blue);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: opacity 0.2s;
}

.btn-primary:hover {
  opacity: 0.9;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 0 16px;
  }
  
  .academic-paper {
    padding: 24px 20px;
  }
  
  .paper-title {
    font-size: 20px;
  }
  
  .body-content {
    font-size: 15px;
  }
  
  .top-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .top-bar-left,
  .top-bar-right {
    justify-content: center;
  }
  
  .metadata-row {
    flex-direction: column;
  }
  
  .metadata-label {
    width: auto;
    margin-bottom: 4px;
  }
}

@media (max-width: 480px) {
  .academic-paper {
    padding: 20px 16px;
  }
  
  .paper-title {
    font-size: 18px;
  }
  
  .body-content {
    font-size: 14px;
    line-height: 1.7;
  }
  
  .paper-metadata {
    padding: 16px;
  }
}

/* 辅助类 */
.w-5 { width: 20px; }
.h-5 { height: 20px; }
</style>
