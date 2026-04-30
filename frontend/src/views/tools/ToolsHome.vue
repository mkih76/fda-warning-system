<template>
  <div class="tools-home">
    <section class="tools-hero">
      <div class="tools-container">
        <span class="tools-badge">Tools</span>
        <h1>实用工具</h1>
        <p>合规辅助工具集，提升工作效率</p>
      </div>
    </section>

    <!-- Global Search -->
    <section class="tools-search-section">
      <div class="tools-container">
        <div class="search-box">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索文章、警告信、法规..."
            @keyup.enter="doSearch"
          />
          <button @click="doSearch" class="search-btn" :disabled="!searchQuery || searching">
            {{ searching ? '搜索中...' : '搜索' }}
          </button>
        </div>

        <!-- Search Results -->
        <div v-if="searchResults.length > 0" class="search-results">
          <div class="results-header">
            <span>找到 {{ searchResults.length }} 条结果</span>
          </div>
          <div
            v-for="r in searchResults"
            :key="`${r.type}-${r.id}`"
            class="result-item"
            @click="$router.push(r.url)"
          >
            <span class="result-type" :class="r.type">{{ r.type === 'article' ? '文章' : '警告信' }}</span>
            <div class="result-content">
              <h4>{{ r.title }}</h4>
              <p>{{ r.summary }}</p>
            </div>
          </div>
        </div>
        <div v-else-if="searched && !searching" class="search-empty">
          未找到相关结果
        </div>
      </div>
    </section>

    <section class="tools-section">
      <div class="tools-container">
        <div class="tools-grid">
          <router-link to="/letters" class="tool-card">
            <div class="tool-icon" style="background: #dc2626">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
            </div>
            <h3>FDA 警告信查询</h3>
            <p>搜索、筛选、分析 986+ 封 FDA 警告信，支持 AI 翻译和风险评估</p>
            <span class="tool-status available">可用</span>
          </router-link>
          <router-link to="/dashboard" class="tool-card">
            <div class="tool-icon" style="background: #0000C9">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M3 3v18h18M9 17V9m4 8V5m4 12v-4"/></svg>
            </div>
            <h3>数据看板</h3>
            <p>FDA 警告信数据可视化，年度趋势、办公室排名、状态分布</p>
            <span class="tool-status available">可用</span>
          </router-link>
          <div class="tool-card disabled">
            <div class="tool-icon" style="background: #7c3aed">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            </div>
            <h3>法规检索</h3>
            <p>跨行业、跨地区的法规全文搜索，支持中英文对照</p>
            <span class="tool-status coming">即将上线</span>
          </div>
          <div class="tool-card disabled">
            <div class="tool-icon" style="background: #059669">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
            </div>
            <h3>GMP 自查清单</h3>
            <p>交互式 GMP 合规自查工具，支持中国/FDA/EU 三套标准</p>
            <span class="tool-status coming">即将上线</span>
          </div>
          <div class="tool-card disabled">
            <div class="tool-icon" style="background: #ea580c">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
            </div>
            <h3>术语词典</h3>
            <p>中英对照行业专业术语查询，覆盖制药/化妆品/食品</p>
            <span class="tool-status coming">即将上线</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const API = window.location.origin + '/api'
const searchQuery = ref('')
const searchResults = ref([])
const searching = ref(false)
const searched = ref(false)

async function doSearch() {
  if (!searchQuery.value) return
  searching.value = true
  searched.value = true
  try {
    const resp = await fetch(`${API}/content/search?q=${encodeURIComponent(searchQuery.value)}`)
    if (resp.ok) {
      const data = await resp.json()
      searchResults.value = data.results || []
    }
  } catch (e) { searchResults.value = [] }
  searching.value = false
}
</script>

<style scoped>
.tools-container { max-width: 1400px; margin: 0 auto; padding: 0 32px; }
.tools-hero { padding: 160px 0 60px; background: linear-gradient(135deg, #374151 0%, #111827 100%); color: #fff; }
.tools-badge { display: inline-block; padding: 4px 16px; background: rgba(255,255,255,0.1); border-radius: 4px; font-size: 12px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 20px; }
.tools-hero h1 { font-size: 48px; font-weight: 800; margin: 0 0 16px; }
.tools-hero p { font-size: 18px; opacity: 0.9; margin: 0; }

/* Search */
.tools-search-section { padding: 0 0 40px; background: #f5f5f5; }
.search-box { display: flex; align-items: center; gap: 12px; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px 16px; max-width: 700px; margin: -24px auto 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.search-box input { flex: 1; border: none; outline: none; font-size: 16px; padding: 8px; }
.search-btn { padding: 10px 24px; background: #0000C9; color: #fff; border: none; border-radius: 4px; font-size: 14px; font-weight: 600; cursor: pointer; }
.search-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.search-results { max-width: 700px; margin: 20px auto 0; }
.results-header { font-size: 13px; color: #666; margin-bottom: 12px; }
.result-item { display: flex; align-items: flex-start; gap: 12px; padding: 16px; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 8px; cursor: pointer; transition: all 0.2s; }
.result-item:hover { border-color: #0000C9; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.result-type { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 3px; white-space: nowrap; margin-top: 2px; }
.result-type.article { background: rgba(0,0,201,0.08); color: #0000C9; }
.result-type.letter { background: rgba(220,38,38,0.08); color: #dc2626; }
.result-content h4 { font-size: 15px; font-weight: 600; color: #000; margin: 0 0 4px; }
.result-content p { font-size: 13px; color: #666; margin: 0; line-height: 1.5; }
.search-empty { max-width: 700px; margin: 20px auto 0; text-align: center; font-size: 14px; color: #999; padding: 24px; }

/* Tools */
.tools-section { padding: 40px 0 80px; }
.tools-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
.tool-card { padding: 32px; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; text-decoration: none; transition: all 0.2s; position: relative; }
.tool-card:not(.disabled):hover { border-color: #0000C9; box-shadow: 0 8px 24px rgba(0,0,0,0.08); transform: translateY(-4px); }
.tool-card.disabled { opacity: 0.6; cursor: default; }
.tool-icon { width: 48px; height: 48px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; }
.tool-card h3 { font-size: 18px; font-weight: 600; color: #000; margin: 0 0 10px; }
.tool-card p { font-size: 14px; color: #666; line-height: 1.7; margin: 0 0 16px; }
.tool-status { font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 4px; }
.tool-status.available { background: rgba(22,163,74,0.1); color: #16a34a; }
.tool-status.coming { background: rgba(245,158,11,0.1); color: #d97706; }

@media (max-width: 1024px) { .tools-container { padding: 0 16px; } .tools-grid { grid-template-columns: 1fr; } .tools-hero { padding: 120px 0 40px; } .search-box { margin: -16px 16px 0; } }
</style>
