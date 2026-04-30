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
  font-size: 36px;
  font-weight: 700;
  color: #000;
  line-height: 1.3;
  margin: 16px 0;
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
  font-size: 18px;
  color: #666;
  line-height: 1.7;
  margin: 0 0 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid #e5e7eb;
}

.article-content {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
}

.article-content :deep(p) {
  margin: 0 0 20px;
  line-height: 1.8;
  text-align: justify;
}

.article-content :deep(h1) {
  font-size: 28px;
  font-weight: 700;
  color: #000;
  margin: 40px 0 16px;
  line-height: 1.3;
}

.article-content :deep(h2) {
  font-size: 22px;
  font-weight: 700;
  color: #000;
  margin: 36px 0 14px;
  padding-bottom: 10px;
  border-bottom: 2px solid #0000C9;
  line-height: 1.4;
}

.article-content :deep(h3) {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 28px 0 12px;
  line-height: 1.4;
}

.article-content :deep(h4) {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 24px 0 10px;
}

.article-content :deep(ul),
.article-content :deep(ol) {
  margin: 0 0 20px;
  padding-left: 28px;
}

.article-content :deep(li) {
  margin-bottom: 8px;
  line-height: 1.7;
}

.article-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0 28px;
  font-size: 15px;
}

.article-content :deep(thead) {
  background: #f0f0f0;
}

.article-content :deep(th) {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #000;
  border-bottom: 2px solid #0000C9;
}

.article-content :deep(td) {
  padding: 10px 16px;
  border-bottom: 1px solid #e5e7eb;
  color: #333;
}

.article-content :deep(tr:hover) {
  background: #fafafa;
}

.article-content :deep(blockquote) {
  margin: 20px 0 24px;
  padding: 16px 20px;
  border-left: 4px solid #0000C9;
  background: #f8f9fa;
  color: #555;
  font-size: 15px;
}

.article-content :deep(blockquote p) {
  margin: 0 0 8px;
}

.article-content :deep(blockquote p:last-child) {
  margin-bottom: 0;
}

.article-content :deep(strong) {
  font-weight: 600;
  color: #1a1a1a;
}

.article-content :deep(em) {
  font-style: italic;
}

.article-content :deep(code) {
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 14px;
  font-family: 'SFMono-Regular', Consolas, monospace;
}

.article-content :deep(a) {
  color: #0000C9;
  text-decoration: none;
  border-bottom: 1px solid rgba(0,0,201,0.3);
}

.article-content :deep(a:hover) {
  border-bottom-color: #0000C9;
}

.article-content :deep(hr) {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 32px 0;
}

.article-content :deep(del) {
  color: #999;
  text-decoration: line-through;
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
