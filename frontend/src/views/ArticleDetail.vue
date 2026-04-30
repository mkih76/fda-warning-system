<template>
  <div class="article-detail-page">
    <div class="page-header-bar">
      <div class="sector-container">
        <nav class="breadcrumb">
          <router-link to="/">首页</router-link>
          <span>/</span>
          <router-link :to="`/${sector}`">{{ sectorName }}</router-link>
          <span>/</span>
          <span class="current">{{ article.title || '文章详情' }}</span>
        </nav>
      </div>
    </div>

    <div class="sector-container">
      <div class="detail-layout">
        <!-- 正文 -->
        <article class="article-body">
          <div class="article-meta-top">
            <span class="meta-cat">{{ article.category }}</span>
            <span class="meta-date">{{ article.date }}</span>
            <span class="meta-views">{{ article.views }} 阅读</span>
          </div>
          <h1>{{ article.title }}</h1>
          <p class="article-summary">{{ article.summary }}</p>
          <!-- Full content (free or authorized) -->
          <div v-if="canAccess" class="article-content" v-html="article.content_html || article.content"></div>

          <!-- Partial content + paywall (unauthorized) -->
          <template v-else-if="article.content">
            <div class="article-content article-partial" v-html="article.content_html || article.content"></div>
            <div class="paywall-overlay">
              <div class="paywall-content">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#0000C9" stroke-width="1.5"><path d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z"/></svg>
                <h3>会员专享内容</h3>
                <p>升级为专业版会员即可阅读全文</p>
                <div class="paywall-actions">
                  <template v-if="!isLoggedIn">
                    <router-link to="/login" class="pf-btn pf-btn-primary">登录</router-link>
                    <router-link to="/register" class="pf-btn pf-btn-outline-blue">注册免费账号</router-link>
                  </template>
                  <template v-else>
                    <button class="pf-btn pf-btn-primary">升级会员</button>
                  </template>
                </div>
              </div>
            </div>
          </template>

          <!-- 占位：内容建设中 -->
          <div v-else class="placeholder-content">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5">
              <path d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/>
            </svg>
            <h3>内容建设中</h3>
            <p>该文章内容正在准备中，请稍后访问</p>
          </div>
        </article>

        <!-- 侧栏 -->
        <aside class="article-sidebar">
          <div class="sidebar-card">
            <h4>目录</h4>
            <p class="sidebar-hint">文章发布后自动生成</p>
          </div>

          <div class="sidebar-card">
            <h4>相关文章</h4>
            <p class="sidebar-hint">暂无相关文章</p>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'

const API = window.location.origin + '/api'
const { user, isLoggedIn, isPro } = useAuth()

const props = defineProps({ sector: { type: String, required: true } })
const route = useRoute()

const sectorNames = { pharma: '制药', cosmetics: '化妆品', food: '食品' }
const sectorName = computed(() => sectorNames[props.sector] || props.sector)

const canAccess = computed(() => {
  if (article.value.access_level === 'free') return true
  if (isPro.value) return true
  return false
})

const article = ref({
  title: '加载中...',
  category_name: '',
  published_at: '',
  view_count: 0,
  summary: '',
  content: '',
  content_html: '',
})

const loading = ref(true)

onMounted(async () => {
  const slug = route.params.slug
  if (!slug) { loading.value = false; return }
  try {
    const resp = await fetch(`${API}/content/articles/${slug}`)
    if (resp.ok) {
      article.value = await resp.json()
    }
  } catch (e) { /* silent */ }
  loading.value = false
})
</script>

<style scoped>
.sector-container { max-width: 1400px; margin: 0 auto; padding: 0 32px; }

.page-header-bar {
  background: #f5f5f5;
  border-bottom: 1px solid #e5e7eb;
  padding: 120px 0 20px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #999;
}

.breadcrumb a { color: #666; text-decoration: none; }
.breadcrumb a:hover { color: #0000C9; }
.breadcrumb .current { color: #000; }

.detail-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 60px;
  padding: 40px 0 80px;
}

.article-body h1 {
  font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'Songti SC', 'Times New Roman', serif;
  font-size: 26px;
  font-weight: 700;
  color: #000;
  line-height: 1.4;
  margin: 16px 0 20px;
  letter-spacing: 1px;
  text-align: center;
}

.article-meta-top {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}

.meta-cat { font-size: 12px; color: #0000C9; font-weight: 600; text-transform: uppercase; }
.meta-date { font-size: 13px; color: #999; }
.meta-views { font-size: 13px; color: #999; }

.article-summary {
  font-family: 'Noto Sans SC', 'Source Han Sans SC', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  color: #444;
  line-height: 1.7;
  margin: 0 auto 28px;
  padding: 16px 20px;
  max-width: 680px;
  text-align: justify;
  background: #fafafa;
  border-left: 3px solid #0000C9;
}

/* ── 论文级排版 ── */
.article-content {
  font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'Songti SC', 'Times New Roman', serif;
  font-size: 15px;
  line-height: 1.8;
  color: #1a1a1a;
  max-width: 780px;
}

/* 段落：首行缩进 + 两端对齐 */
.article-content :deep(p) {
  margin: 0 0 16px;
  text-indent: 2em;
  text-align: justify;
  line-height: 1.8;
  orphans: 3;
  widows: 3;
}

/* 标题不缩进 */
.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3),
.article-content :deep(h4),
.article-content :deep(h5) {
  text-indent: 0;
  text-align: left;
}

/* 一级标题：文章大标题（h1 在内容中） */
.article-content :deep(h1) {
  font-size: 22px;
  font-weight: 700;
  color: #000;
  margin: 36px 0 12px;
  line-height: 1.4;
  letter-spacing: 0.5px;
}

/* 二级标题：如 "一、检查前准备" */
.article-content :deep(h2) {
  font-size: 17px;
  font-weight: 700;
  color: #000;
  margin: 32px 0 10px;
  padding-bottom: 6px;
  border-bottom: 1px solid #d0d0d0;
  line-height: 1.5;
}

/* 三级标题：如 "1.1 了解检查类型" */
.article-content :deep(h3) {
  font-size: 15px;
  font-weight: 700;
  color: #222;
  margin: 24px 0 8px;
  line-height: 1.5;
}

/* 四级标题 */
.article-content :deep(h4) {
  font-size: 14px;
  font-weight: 700;
  color: #333;
  margin: 20px 0 6px;
}

/* 列表 */
.article-content :deep(ul),
.article-content :deep(ol) {
  margin: 0 0 16px;
  padding-left: 2em;
  text-indent: 0;
}

.article-content :deep(li) {
  margin-bottom: 6px;
  line-height: 1.7;
  text-indent: 0;
}

/* 表格：论文风格 — 三线表 */
.article-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px auto 24px;
  font-size: 14px;
  font-family: 'Noto Sans SC', 'Source Han Sans SC', 'Microsoft YaHei', sans-serif;
}

.article-content :deep(thead) {
  background: transparent;
}

.article-content :deep(th) {
  padding: 8px 12px;
  text-align: center;
  font-weight: 700;
  color: #000;
  border-top: 2px solid #000;
  border-bottom: 1px solid #000;
  font-size: 13px;
}

.article-content :deep(td) {
  padding: 7px 12px;
  text-align: center;
  border-bottom: 1px solid #ccc;
  color: #222;
  font-size: 13px;
}

.article-content :deep(tbody tr:last-child td) {
  border-bottom: 2px solid #000;
}

.article-content :deep(tbody tr:hover) {
  background: transparent;
}

/* 引用 / 注释 */
.article-content :deep(blockquote) {
  margin: 16px 0 20px;
  padding: 10px 16px;
  border-left: 3px solid #999;
  background: transparent;
  color: #555;
  font-size: 13px;
  font-style: normal;
}

.article-content :deep(blockquote p) {
  margin: 0 0 4px;
  text-indent: 0;
}

.article-content :deep(blockquote p:last-child) {
  margin-bottom: 0;
}

/* 加粗 */
.article-content :deep(strong) {
  font-weight: 700;
  color: #000;
}

/* 斜体 */
.article-content :deep(em) {
  font-style: italic;
}

/* 代码 */
.article-content :deep(code) {
  background: #f5f5f5;
  padding: 1px 4px;
  border-radius: 2px;
  font-size: 13px;
  font-family: 'SFMono-Regular', Consolas, 'Courier New', monospace;
}

/* 链接 */
.article-content :deep(a) {
  color: #0000C9;
  text-decoration: none;
  border-bottom: 1px solid rgba(0,0,201,0.25);
}

.article-content :deep(a:hover) {
  border-bottom-color: #0000C9;
}

/* 分割线 */
.article-content :deep(hr) {
  border: none;
  border-top: 1px solid #ccc;
  margin: 28px 0;
}

/* 删除线 */
.article-content :deep(del) {
  color: #999;
  text-decoration: line-through;
}

/* 脚注样式（blockquote 内最后一行灰色小字） */
.article-content :deep(blockquote) {
  font-family: 'Noto Sans SC', 'Source Han Sans SC', 'Microsoft YaHei', sans-serif;
}

.placeholder-content {
  text-align: center;
  padding: 80px 0;
}

.placeholder-content h3 { font-size: 20px; color: #666; margin: 16px 0 8px; }
.placeholder-content p { font-size: 14px; color: #999; }

.article-sidebar { padding-top: 8px; }

.sidebar-card {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.sidebar-card h4 {
  font-size: 14px;
  font-weight: 600;
  color: #000;
  margin: 0 0 12px;
}

.sidebar-hint { font-size: 13px; color: #999; margin: 0; }

/* Paywall */
.article-partial {
  max-height: 600px;
  overflow: hidden;
  position: relative;
  mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
}

.paywall-overlay {
  background: linear-gradient(to bottom, rgba(255,255,255,0), #fff 20%);
  padding: 60px 0 20px;
  margin-top: -40px;
  text-align: center;
}

.paywall-content {
  background: #F2F9FC;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 48px 40px;
  max-width: 480px;
  margin: 0 auto;
}

.paywall-content h3 { font-size: 22px; font-weight: 700; color: #000; margin: 16px 0 8px; }
.paywall-content p { font-size: 15px; color: #666; margin: 0 0 24px; }

.paywall-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

.pf-btn { display: inline-flex; align-items: center; justify-content: center; padding: 12px 28px; font-size: 14px; font-weight: 600; border-radius: 4px; text-decoration: none; transition: all 0.2s; cursor: pointer; border: none; }
.pf-btn-primary { background: #0000C9; color: #fff; }
.pf-btn-primary:hover { background: #0000A3; }
.pf-btn-outline-blue { background: transparent; color: #0000C9; border: 1px solid #0000C9; }
.pf-btn-outline-blue:hover { background: rgba(0,0,201,0.05); }

@media (max-width: 1024px) {
  .sector-container { padding: 0 16px; }
  .detail-layout { grid-template-columns: 1fr; gap: 32px; }
  .article-body h1 { font-size: 28px; }
}
</style>
