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
          <div class="article-content" v-html="article.contentHtml"></div>

          <!-- 占位：内容建设中 -->
          <div v-if="!article.contentHtml" class="placeholder-content">
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
import { computed } from 'vue'

const props = defineProps({ sector: { type: String, required: true } })

const sectorNames = { pharma: '制药', cosmetics: '化妆品', food: '食品' }
const sectorName = computed(() => sectorNames[props.sector] || props.sector)

const article = {
  title: '示例文章',
  category: '知识专栏',
  date: '2026-04-30',
  views: 0,
  summary: '内容建设中...',
  contentHtml: ''
}
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

@media (max-width: 1024px) {
  .sector-container { padding: 0 16px; }
  .detail-layout { grid-template-columns: 1fr; gap: 32px; }
  .article-body h1 { font-size: 28px; }
}
</style>
