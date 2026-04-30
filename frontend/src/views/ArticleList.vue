<template>
  <div class="article-list-page">
    <div class="page-header-bar">
      <div class="sector-container">
        <nav class="breadcrumb">
          <router-link to="/">首页</router-link>
          <span>/</span>
          <router-link :to="`/${sector}`">{{ sectorName }}</router-link>
          <span>/</span>
          <span class="current">{{ categoryName || '全部文章' }}</span>
        </nav>
        <h1>{{ categoryName || sectorName + '文章' }}</h1>
        <p class="page-desc">{{ categoryDesc || '浏览所有' + sectorName + '板块文章' }}</p>
      </div>
    </div>

    <div class="sector-container">
      <div class="list-layout">
        <!-- 筛选侧栏 -->
        <aside class="filter-sidebar">
          <h4>内容分类</h4>
          <router-link :to="`/${sector}`" class="filter-link" :class="{ active: !categorySlug }">全部</router-link>
          <router-link
            v-for="cat in categories"
            :key="cat.slug"
            :to="`/${sector}/${cat.slug}`"
            class="filter-link"
            :class="{ active: categorySlug === cat.slug }"
          >{{ cat.name }}</router-link>
        </aside>

        <!-- 文章列表 -->
        <div class="list-main">
          <div class="list-header">
            <span class="results-count">共 {{ articles.length }} 篇文章</span>
            <input v-model="searchQuery" type="text" placeholder="搜索文章..." class="search-input" />
          </div>

          <div v-if="articles.length === 0" class="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <h3>暂无文章</h3>
            <p>内容正在建设中，敬请期待</p>
          </div>

          <div v-else class="article-cards">
            <div
              v-for="(article, i) in articles"
              :key="i"
              class="article-card"
              @click="$router.push(`/${sector}/article/${article.slug}`)"
            >
              <div class="card-meta">
                <span class="card-cat">{{ article.category }}</span>
                <span class="card-date">{{ article.date }}</span>
              </div>
              <h3>{{ article.title }}</h3>
              <p>{{ article.summary }}</p>
              <div class="card-footer">
                <span v-if="article.access_level !== 'free'" class="access-badge pro">会员</span>
                <span class="read-count">{{ article.views }} 阅读</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const API = window.location.origin + '/api'

const props = defineProps({ sector: { type: String, required: true } })
const route = useRoute()
const searchQuery = ref('')
const apiArticles = ref([])
const totalArticles = ref(0)
const loading = ref(false)

async function fetchArticles() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.set('sector', props.sector)
    if (route.params.category) params.set('category', route.params.category)
    if (searchQuery.value) params.set('search', searchQuery.value)
    const resp = await fetch(`${API}/content/articles?${params}`)
    if (resp.ok) {
      const data = await resp.json()
      apiArticles.value = data.items || []
      totalArticles.value = data.total || 0
    }
  } catch (e) { /* silent */ }
  loading.value = false
}

onMounted(fetchArticles)
watch(() => route.params.category, fetchArticles)

const sectorNames = { pharma: '制药', cosmetics: '化妆品', food: '食品' }
const sectorName = computed(() => sectorNames[props.sector] || props.sector)
const categorySlug = computed(() => route.params.category)
const categoryName = computed(() => categorySlug.value)
const categoryDesc = computed(() => '')

// 占位分类数据
const sectorCategories = {
  pharma: [
    { name: '行业动态', slug: 'industry-news' },
    { name: '政策法规', slug: 'regulations' },
    { name: 'GMP 实务', slug: 'gmp-practice' },
    { name: '药典解读', slug: 'pharmacopoeia' },
    { name: '注册申报', slug: 'registration' },
    { name: '质量控制', slug: 'quality-control' },
    { name: '工艺验证', slug: 'process-validation' },
    { name: '案例研究', slug: 'case-studies' },
  ],
  cosmetics: [
    { name: '行业动态', slug: 'industry-news' },
    { name: '政策法规', slug: 'regulations' },
    { name: '配方与安全', slug: 'formulation-safety' },
    { name: '功效评价', slug: 'efficacy-testing' },
    { name: '原料合规', slug: 'ingredient-compliance' },
    { name: '标签与宣称', slug: 'labeling-claims' },
    { name: '生产质量管理', slug: 'manufacturing-qm' },
    { name: '市场趋势', slug: 'trends' },
  ],
  food: [
    { name: '行业动态', slug: 'industry-news' },
    { name: '政策法规', slug: 'regulations' },
    { name: '食品安全管理体系', slug: 'food-safety-mgmt' },
    { name: '添加剂与新原料', slug: 'food-additives' },
    { name: '标签标识', slug: 'food-labeling' },
    { name: '进出口合规', slug: 'food-import-export' },
    { name: '营养与健康声称', slug: 'nutrition-claims' },
    { name: '市场趋势', slug: 'trends' },
  ]
}

const categories = computed(() => sectorCategories[props.sector] || [])

// Articles from API
const articles = computed(() => apiArticles.value)
</script>

<style scoped>
.sector-container { max-width: 1400px; margin: 0 auto; padding: 0 32px; }

.page-header-bar {
  background: #f5f5f5;
  border-bottom: 1px solid #e5e7eb;
  padding: 120px 0 40px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #999;
  margin-bottom: 16px;
}

.breadcrumb a { color: #666; text-decoration: none; }
.breadcrumb a:hover { color: #0000C9; }
.breadcrumb .current { color: #000; }

.page-header-bar h1 {
  font-size: 36px;
  font-weight: 700;
  color: #000;
  margin: 0 0 8px;
}

.page-desc { font-size: 16px; color: #666; margin: 0; }

.list-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 48px;
  padding: 40px 0 80px;
}

.filter-sidebar { padding-top: 8px; }

.filter-sidebar h4 {
  font-size: 14px;
  font-weight: 600;
  color: #000;
  margin: 0 0 16px;
}

.filter-link {
  display: block;
  padding: 8px 12px;
  font-size: 14px;
  color: #666;
  text-decoration: none;
  border-radius: 4px;
  margin-bottom: 4px;
  transition: all 0.15s;
}

.filter-link:hover { color: #0000C9; background: #F2F9FC; }
.filter-link.active { color: #0000C9; background: #F2F9FC; font-weight: 600; }

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.results-count { font-size: 14px; color: #666; }

.search-input {
  padding: 8px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 14px;
  width: 260px;
  transition: border-color 0.2s;
}

.search-input:focus { outline: none; border-color: #0000C9; }

.empty-state {
  text-align: center;
  padding: 80px 0;
  color: #999;
}

.empty-state h3 { font-size: 18px; color: #666; margin: 16px 0 8px; }
.empty-state p { font-size: 14px; color: #999; }

.article-cards { display: flex; flex-direction: column; gap: 20px; }

.article-card {
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.article-card:hover {
  border-color: #0000C9;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  transform: translateY(-2px);
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.card-cat { font-size: 12px; color: #0000C9; font-weight: 600; text-transform: uppercase; }
.card-date { font-size: 12px; color: #999; }

.article-card h3 { font-size: 18px; font-weight: 600; color: #000; margin: 0 0 8px; }
.article-card p { font-size: 14px; color: #666; line-height: 1.7; margin: 0 0 12px; }

.card-footer { display: flex; align-items: center; gap: 12px; }

.access-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

.access-badge.pro { background: rgba(0,0,201,0.08); color: #0000C9; }

.read-count { font-size: 12px; color: #999; }

@media (max-width: 1024px) {
  .sector-container { padding: 0 16px; }
  .list-layout { grid-template-columns: 1fr; gap: 24px; }
  .filter-sidebar { display: flex; flex-wrap: wrap; gap: 8px; }
  .filter-sidebar h4 { width: 100%; }
}
</style>
