<template>
  <div class="news-home">
    <!-- 顶部通栏 -->
    <div class="top-bar">
      <div class="container">
        <div class="date-info">
          <span class="live-dot"></span>
          <span>{{ currentDate }}</span> · 数据实时更新中
        </div>
        <div class="quick-links">
          <router-link to="/letters">📋 FDA警告信速递</router-link>
          <router-link to="/regulations">📜 法规库</router-link>
          <router-link to="/tools">🛠️ 工具箱</router-link>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <main class="main-content">
      <div class="container">
        <div class="content-grid">

          <!-- ========== 左栏：主要内容 ========== -->
          <div class="left-column">

            <!-- 头条新闻 -->
            <section class="hero-section">
              <div class="hero-card">
                <div class="hero-inner">
                  <div class="hero-img-placeholder">
                    <span class="icon-overlay">📰</span>
                  </div>
                  <div class="hero-body">
                    <span class="hero-tag">📢 头条关注</span>
                    <h2>FDA发布2026年度化妆品设施注册新指南，涉及多项合规要求更新</h2>
                    <p>美国FDA于近日更新了化妆品设施注册与产品列名指南文件，新增了对海外生产企业的数据提交要求，国内出口化妆品企业需重点关注MoCRA法规下的最新合规要点。</p>
                    <div class="hero-meta">
                      <span>📅 2026-04-28</span>
                      <span>👁️ 12,860 阅读</span>
                      <router-link to="/regulations" class="read-more">阅读全文 →</router-link>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- 三个行业快捷入口卡片 -->
            <section class="industry-cards">
              <router-link to="/pharma" class="industry-card card-pharma">
                <h4>💊 制药行业</h4>
                <p class="card-subtitle">Pharmaceutical Industry</p>
                <ul class="mini-list">
                  <li>NMPA发布新版《药品生产质量管理规范》附录</li>
                  <li>ICH Q12指南在国内落地实施进展</li>
                  <li>2026年第一季度创新药获批盘点</li>
                  <li>FDA对三家印度原料药企业发出警告信</li>
                </ul>
              </router-link>
              <router-link to="/cosmetics" class="industry-card card-cosmetic">
                <h4>💄 化妆品行业</h4>
                <p class="card-subtitle">Cosmetics Industry</p>
                <ul class="mini-list">
                  <li>欧盟SCCS发布新一批化妆品成分安全评估意见</li>
                  <li>《化妆品安全评估技术导则》修订征求意见</li>
                  <li>MoCRA框架下化妆品不良反应报告要求解析</li>
                  <li>防晒产品SPF宣称合规要点梳理</li>
                </ul>
              </router-link>
              <router-link to="/food" class="industry-card card-food">
                <h4>🍽️ 食品行业</h4>
                <p class="card-subtitle">Food Industry</p>
                <ul class="mini-list">
                  <li>市场监管总局发布新版《食品添加剂使用标准》</li>
                  <li>FSSC 22000 V6.0版认证过渡期安排</li>
                  <li>功能性食品宣称合规与广告审查要点</li>
                  <li>进出口食品安全管理办法最新修订动态</li>
                </ul>
              </router-link>
            </section>

            <!-- FDA警告信专区 -->
            <section class="card">
              <div class="section-header">
                <h3><span class="dot-indicator dot-fda"></span> ⚠️ FDA 警告信速递</h3>
                <router-link to="/letters" class="more-link">查看全部 →</router-link>
              </div>
              <ul class="article-list">
                <li v-for="letter in latestLetters.slice(0, 4)" :key="letter.id" @click="$router.push(`/letters/${letter.id}`)">
                  <span class="article-tag tag-fda">FDA</span>
                  <span class="article-title">{{ letter.company_name }} - {{ letter.subject }}</span>
                  <span class="article-date">{{ letter.issue_date }}</span>
                </li>
              </ul>
            </section>

            <!-- 法规信息 -->
            <section class="card">
              <div class="section-header">
                <h3><span class="dot-indicator dot-pharma"></span> 📜 法规政策动态</h3>
                <router-link to="/regulations" class="more-link">法规库 →</router-link>
              </div>
              <ul class="article-list">
                <li v-for="article in latestArticles.filter(a => a.sector === 'pharma').slice(0, 4)" :key="article.id" @click="$router.push(`/${article.sector}/article/${article.slug}`)">
                  <span class="article-tag" :class="getTagClass(article.sector)">{{ getSectorName(article.sector) }}</span>
                  <span class="article-title">{{ article.title }}</span>
                  <span class="article-date">{{ article.published_at ? new Date(article.published_at).toLocaleDateString('zh-CN') : '' }}</span>
                </li>
                <li v-if="latestArticles.length === 0">
                  <span class="article-tag tag-pharma">制药</span>
                  <span class="article-title">NMPA发布《药品上市后变更管理办法》修订征求意见稿</span>
                  <span class="article-date">2026-04-27</span>
                </li>
                <li v-if="latestArticles.length === 0">
                  <span class="article-tag tag-cosmetic">化妆品</span>
                  <span class="article-title">《化妆品功效宣称评价规范》新增功效分类要求</span>
                  <span class="article-date">2026-04-20</span>
                </li>
                <li v-if="latestArticles.length === 0">
                  <span class="article-tag tag-food">食品</span>
                  <span class="article-title">GB 2760-2026《食品添加剂使用标准》正式发布</span>
                  <span class="article-date">2026-04-16</span>
                </li>
              </ul>
            </section>

            <!-- 前沿科技 -->
            <section class="card">
              <div class="section-header">
                <h3><span class="dot-indicator dot-tech"></span> 🔬 前沿科技与行业洞察</h3>
                <router-link to="/articles" class="more-link">更多科技 →</router-link>
              </div>
              <ul class="article-list">
                <li v-for="article in latestArticles.filter(a => a.sector === 'cosmetics' || a.sector === 'food').slice(0, 4)" :key="article.id" @click="$router.push(`/${article.sector}/article/${article.slug}`)">
                  <span class="article-tag" :class="getTagClass(article.sector)">{{ getSectorName(article.sector) }}</span>
                  <span class="article-title">{{ article.title }}</span>
                  <span class="article-date">{{ article.published_at ? new Date(article.published_at).toLocaleDateString('zh-CN') : '' }}</span>
                </li>
                <li v-if="latestArticles.length === 0">
                  <span class="article-tag tag-tech">科技</span>
                  <span class="article-title">AI辅助药物研发：2026年全球AI制药管线分析报告</span>
                  <span class="article-date">2026-04-26</span>
                </li>
                <li v-if="latestArticles.length === 0">
                  <span class="article-tag tag-tech">科技</span>
                  <span class="article-title">合成生物学在化妆品活性成分开发中的前沿应用</span>
                  <span class="article-date">2026-04-21</span>
                </li>
                <li v-if="latestArticles.length === 0">
                  <span class="article-tag tag-tech">科技</span>
                  <span class="article-title">植物基替代蛋白技术突破与食品安全评估新进展</span>
                  <span class="article-date">2026-04-17</span>
                </li>
              </ul>
            </section>
          </div>

          <!-- ========== 右栏：侧边栏 ========== -->
          <aside class="sidebar">
            <!-- 热门文章 -->
            <div class="card sidebar-card">
              <h4>🔥 本周热门文章</h4>
              <ul class="hot-list">
                <li><span class="rank-num">1</span><span>FDA警告信深度解读：数据完整性缺陷的十大常见问题</span></li>
                <li><span class="rank-num">2</span><span>化妆品安全评估报告编写指南（2026版）</span></li>
                <li><span class="rank-num">3</span><span>中国药品出口欧盟合规路径全解析</span></li>
                <li><span class="rank-num">4</span><span>保健食品注册与备案双轨制实务问答</span></li>
                <li><span class="rank-num">5</span><span>2026年全球原料药供应链格局变化分析</span></li>
                <li><span class="rank-num">6</span><span>化妆品新原料注册备案数据年度汇总</span></li>
                <li><span class="rank-num">7</span><span>FSMA配套法规下输美食品企业应对策略</span></li>
                <li><span class="rank-num">8</span><span>NMPA飞行检查常见缺陷项统计报告</span></li>
              </ul>
            </div>

            <!-- 标签云 -->
            <div class="card sidebar-card">
              <h4>🏷️ 热门标签</h4>
              <div class="tag-cloud">
                <router-link to="/letters">FDA警告信</router-link>
                <router-link to="/general/gmp-panorama">GMP合规</router-link>
                <router-link to="/cosmetics">化妆品安全评估</router-link>
                <router-link to="/regulations">NMPA法规</router-link>
                <router-link to="/letters">数据完整性</router-link>
                <router-link to="/pharma">原料药</router-link>
                <router-link to="/cosmetics">MoCRA</router-link>
                <router-link to="/food">食品添加剂</router-link>
                <router-link to="/pharma">ICH指南</router-link>
                <router-link to="/general">飞行检查</router-link>
                <router-link to="/cosmetics">功效宣称</router-link>
                <router-link to="/food">FSSC22000</router-link>
              </div>
            </div>

            <!-- 订阅提示 -->
            <div class="card sidebar-card subscribe-card">
              <h4>📬 邮件订阅</h4>
              <p>每周五推送行业周报，涵盖最新法规、FDA警告信、行业科技动态。</p>

              <form @submit.prevent="handleSubscribe" class="subscribe-form">
                <input
                  v-model="subscribeName"
                  type="text"
                  placeholder="您的称呼（可选）"
                  class="subscribe-input"
                />
                <input
                  v-model="subscribeEmail"
                  type="email"
                  placeholder="请输入工作邮箱"
                  class="subscribe-input"
                  required
                />
                <button
                  type="submit"
                  class="subscribe-btn"
                  :disabled="subscribing"
                >
                  {{ subscribing ? '订阅中...' : '立即订阅' }}
                </button>
              </form>

              <p
                v-if="subscribeMessage"
                class="subscribe-message"
                :class="{ 'success': subscribeSuccess, 'error': !subscribeSuccess }"
              >
                {{ subscribeMessage }}
              </p>
            </div>
          </aside>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API = window.location.origin + '/api'

// ==================== 日期 ====================
const currentDate = computed(() => {
  const now = new Date()
  const options = { year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'short' }
  return now.toLocaleDateString('zh-CN', options)
})

// ==================== 数据状态 ====================
const loading = ref({
  headlines: true,
  industry: true,
  letters: true,
  hot: true,
  articles: true
})

// 头条新闻
const headlines = ref([
  {
    id: 0,
    title: 'FDA发布2026年度化妆品设施注册新指南，涉及多项合规要求更新',
    summary: '美国FDA于近日更新了化妆品设施注册与产品列名指南文件...',
    sector: 'cosmetics',
    published_at: '2026-04-28',
    view_count: 12860
  }
])

// 三个行业动态
const industryNews = ref({
  pharma: [
    { id: 1, title: 'NMPA发布新版《药品生产质量管理规范》附录', category_name: 'GMP法规' },
    { id: 2, title: 'ICH Q12指南在国内落地实施进展', category_name: 'ICH指南' },
    { id: 3, title: '2026年第一季度创新药获批盘点', category_name: '行业动态' },
    { id: 4, title: 'FDA对三家印度原料药企业发出警告信', category_name: 'FDA警告信' },
  ],
  cosmetics: [
    { id: 5, title: '欧盟SCCS发布新一批化妆品成分安全评估意见', category_name: '安全评估' },
    { id: 6, title: '《化妆品安全评估技术导则》修订征求意见', category_name: '法规动态' },
    { id: 7, title: 'MoCRA框架下化妆品不良反应报告要求解析', category_name: 'MoCRA' },
    { id: 8, title: '防晒产品SPF宣称合规要点梳理', category_name: '合规指南' },
  ],
  food: [
    { id: 9, title: '市场监管总局发布新版《食品添加剂使用标准》', category_name: '食品安全' },
    { id: 10, title: 'FSSC 22000 V6.0版认证过渡期安排', category_name: '认证标准' },
    { id: 11, title: '功能性食品宣称合规与广告审查要点', category_name: '合规指南' },
    { id: 12, title: '进出口食品安全管理办法最新修订动态', category_name: '进出口' },
  ]
})

// FDA警告信
const latestLetters = ref([
  { id: 1, company_name: '浙江某原料药企业', subject: '数据完整性与清洁验证缺陷', issue_date: '2026-04-25' },
  { id: 2, company_name: '印度制药公司', subject: 'OOS调查不充分', issue_date: '2026-04-22' },
  { id: 3, company_name: '美国化妆品代工厂', subject: 'GMP不合规，微生物污染', issue_date: '2026-04-18' },
  { id: 4, company_name: '膳食补充剂企业', subject: '标签宣称违规', issue_date: '2026-04-15' },
])

// 最新文章
const latestArticles = ref([])

// 热门文章
const hotArticles = ref([
  { id: 1, title: 'FDA警告信深度解读：数据完整性缺陷的十大常见问题', view_count: 5200 },
  { id: 2, title: '化妆品安全评估报告编写指南（2026版）', view_count: 4800 },
  { id: 3, title: '中国药品出口欧盟合规路径全解析', view_count: 4500 },
  { id: 4, title: '保健食品注册与备案双轨制实务问答', view_count: 4200 },
  { id: 5, title: '2026年全球原料药供应链格局变化分析', view_count: 3900 },
  { id: 6, title: '化妆品新原料注册备案数据年度汇总', view_count: 3600 },
  { id: 7, title: 'FSMA配套法规下输美食品企业应对策略', view_count: 3300 },
  { id: 8, title: 'NMPA飞行检查常见缺陷项统计报告', view_count: 3000 },
])

// 订阅表单
const subscribeEmail = ref('')
const subscribeName = ref('')
const subscribing = ref(false)
const subscribeMessage = ref('')
const subscribeSuccess = ref(false)

// ==================== 辅助函数 ====================
const sectorNames = { pharma: '制药', cosmetics: '化妆品', food: '食品', tech: '科技' }
function getSectorName(s) { return sectorNames[s] || s }

function getTagClass(sector) {
  const classes = {
    pharma: 'tag-pharma',
    cosmetics: 'tag-cosmetic',
    food: 'tag-food',
    tech: 'tag-tech'
  }
  return classes[sector] || 'tag-pharma'
}

function formatDate(dateStr) {
  if (!dateStr) return '待确定'
  try {
    return new Date(dateStr).toLocaleDateString('zh-CN')
  } catch {
    return dateStr
  }
}

function formatNumber(num) {
  if (!num) return '0'
  return num.toLocaleString()
}

// ==================== API调用 ====================

async function fetchHeadlines() {
  loading.headlines = true
  try {
    const resp = await fetch(`${API}/portal/headlines?limit=1`)
    if (resp.ok) {
      const data = await resp.json()
      if (data && data.length > 0) {
        headlines.value = data
      }
    }
  } catch (e) {
    console.error('获取头条失败:', e)
  } finally {
    loading.headlines = false
  }
}

async function fetchIndustryNews() {
  loading.industry = true
  try {
    const [pharmaResp, cosmeticsResp, foodResp] = await Promise.all([
      fetch(`${API}/portal/industry/pharma?limit=4`),
      fetch(`${API}/portal/industry/cosmetics?limit=4`),
      fetch(`${API}/portal/industry/food?limit=4`)
    ])

    if (pharmaResp.ok) {
      const data = await pharmaResp.json()
      if (data && data.length > 0) industryNews.value.pharma = data
    }
    if (cosmeticsResp.ok) {
      const data = await cosmeticsResp.json()
      if (data && data.length > 0) industryNews.value.cosmetics = data
    }
    if (foodResp.ok) {
      const data = await foodResp.json()
      if (data && data.length > 0) industryNews.value.food = data
    }
  } catch (e) {
    console.error('获取行业动态失败:', e)
  } finally {
    loading.industry = false
  }
}

async function fetchLatestLetters() {
  loading.letters = true
  try {
    const resp = await fetch(`${API}/letters?page=1&page_size=4`)
    if (resp.ok) {
      const data = await resp.json()
      if (data.items && data.items.length > 0) {
        latestLetters.value = data.items.map(l => ({
          id: l.id,
          company_name: l.company_name,
          subject: l.subject || 'CGMP违规',
          issue_date: l.issue_date || '待确定',
        }))
      }
    }
  } catch (e) {
    console.error('获取FDA警告信失败:', e)
  } finally {
    loading.letters = false
  }
}

async function fetchHotArticles() {
  loading.hot = true
  try {
    const resp = await fetch(`${API}/portal/hot?limit=8&days=30`)
    if (resp.ok) {
      const data = await resp.json()
      if (data && data.length > 0) {
        hotArticles.value = data
      }
    }
  } catch (e) {
    console.error('获取热门文章失败:', e)
  } finally {
    loading.hot = false
  }
}

async function fetchLatestArticles() {
  loading.articles = true
  try {
    const resp = await fetch(`${API}/content/home`)
    if (resp.ok) {
      const data = await resp.json()
      latestArticles.value = data.latest_articles || []
    }
  } catch (e) {
    console.error('获取最新文章失败:', e)
  } finally {
    loading.articles = false
  }
}

async function handleSubscribe() {
  if (!subscribeEmail.value) {
    subscribeMessage.value = '请输入邮箱地址'
    subscribeSuccess.value = false
    return
  }

  subscribing.value = true
  subscribeMessage.value = ''

  try {
    const resp = await fetch(`${API}/portal/subscribe`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: subscribeEmail.value,
        name: subscribeName.value || null,
        sectors: ['pharma', 'cosmetics', 'food']
      })
    })

    const data = await resp.json()
    subscribeMessage.value = data.message
    subscribeSuccess.value = data.success

    if (data.success) {
      subscribeEmail.value = ''
      subscribeName.value = ''
    }
  } catch (e) {
    subscribeMessage.value = '订阅失败，请稍后重试'
    subscribeSuccess.value = false
  } finally {
    subscribing.value = false
  }
}

// ==================== 初始化 ====================
onMounted(() => {
  // 并行加载所有数据
  fetchHeadlines()
  fetchIndustryNews()
  fetchLatestLetters()
  fetchHotArticles()
  fetchLatestArticles()
})
</script>

<style scoped>
.news-home {
  min-height: 100vh;
  background: #f4f6f8;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Segoe UI', sans-serif;
  color: #2c3e50;
}

.container {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
}

/* 顶部通栏 */
.top-bar {
  background: #051e2d;
  color: #c0cdd5;
  font-size: 0.8rem;
  padding: 8px 0;
  margin-top: var(--header-height, 62px);
}

.top-bar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4cd964;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(76, 217, 100, 0.6); }
  50% { box-shadow: 0 0 0 8px rgba(76, 217, 100, 0); }
}

.quick-links a {
  color: #c0cdd5;
  text-decoration: none;
  margin-left: 20px;
  transition: color 0.2s;
}

.quick-links a:hover {
  color: #fff;
}

/* 主内容区 */
.main-content {
  padding: 24px 0 40px;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  align-items: start;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

/* 左栏 */
.left-column {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 头条新闻 */
.hero-card {
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.10);
  border: 1px solid #e2e8f0;
  transition: box-shadow 0.25s;
}

.hero-card:hover {
  box-shadow: 0 12px 40px rgba(0,0,0,0.13);
}

.hero-inner {
  display: flex;
  min-height: 240px;
}

.hero-img-placeholder {
  width: 44%;
  background: linear-gradient(160deg, #0b3d5f 0%, #10547a 40%, #1a7fb5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  flex-shrink: 0;
}

.icon-overlay {
  opacity: 0.85;
}

.hero-body {
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: 1;
}

.hero-tag {
  display: inline-block;
  background: #e8f4f9;
  color: #0b3d5f;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 10px;
  width: fit-content;
}

.hero-body h2 {
  font-size: 1.55rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
  line-height: 1.35;
}

.hero-body p {
  color: #5a6c7d;
  font-size: 0.9rem;
  margin-bottom: 14px;
  line-height: 1.6;
}

.hero-meta {
  display: flex;
  gap: 16px;
  font-size: 0.8rem;
  color: #8899a6;
  align-items: center;
  flex-wrap: wrap;
}

.read-more {
  margin-left: auto;
  color: #1a7fb5;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.read-more:hover {
  color: #0b3d5f;
}

/* 三栏行业卡片 */
.industry-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

@media (max-width: 768px) {
  .industry-cards {
    grid-template-columns: 1fr;
  }
  .hero-inner {
    flex-direction: column;
  }
  .hero-img-placeholder {
    width: 100%;
    height: 140px;
  }
}

.industry-card {
  background: #fff;
  border-radius: 10px;
  padding: 18px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  border: 1px solid #e2e8f0;
  border-top: 3px solid transparent;
  transition: all 0.25s;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
}

.industry-card:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.10);
  transform: translateY(-2px);
}

.card-pharma { border-top-color: #0b5c7a; }
.card-cosmetic { border-top-color: #b8517a; }
.card-food { border-top-color: #5b8c3e; }

.industry-card h4 {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.card-subtitle {
  font-size: 0.75rem;
  color: #8899a6;
  margin-bottom: 10px;
}

.mini-list {
  list-style: none;
  padding: 0;
  flex: 1;
}

.mini-list li {
  padding: 6px 0;
  border-bottom: 1px dotted #eef1f4;
  font-size: 0.84rem;
  line-height: 1.4;
  color: #2c3e50;
}

.mini-list li:last-child {
  border-bottom: none;
}

/* 卡片容器 */
.card {
  background: #fff;
  border-radius: 10px;
  padding: 18px 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  border: 1px solid #e2e8f0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e8ecf1;
}

.section-header h3 {
  font-size: 1.15rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot-indicator {
  width: 4px;
  height: 20px;
  border-radius: 2px;
  display: inline-block;
}

.dot-fda { background: #c0392b; }
.dot-pharma { background: #0b5c7a; }
.dot-tech { background: #6c3fa0; }

.more-link {
  font-size: 0.82rem;
  color: #1a7fb5;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.more-link:hover {
  color: #0b3d5f;
}

/* 文章列表 */
.article-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.article-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border-bottom: 1px dashed #e8ecf1;
  cursor: pointer;
  transition: background 0.2s;
  border-radius: 6px;
  margin: 1px 0;
}

.article-list li:last-child {
  border-bottom: none;
}

.article-list li:hover {
  background: #f8fafc;
}

.article-tag {
  flex-shrink: 0;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 14px;
  letter-spacing: 0.4px;
  white-space: nowrap;
}

.tag-fda { background: #fef2f2; color: #c0392b; }
.tag-pharma { background: #e6f2f8; color: #0b5c7a; }
.tag-cosmetic { background: #fdf0f5; color: #b8517a; }
.tag-food { background: #eef5e8; color: #5b8c3e; }
.tag-tech { background: #f5f0fa; color: #6c3fa0; }

.article-title {
  flex: 1;
  font-size: 0.9rem;
  font-weight: 500;
  line-height: 1.45;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #2c3e50;
}

.article-date {
  flex-shrink: 0;
  font-size: 0.75rem;
  color: #8899a6;
  white-space: nowrap;
}

/* 侧边栏 */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-card {
  transition: box-shadow 0.25s;
}

.sidebar-card:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.10);
}

.sidebar-card h4 {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #2c3e50;
}

/* 热门列表 */
.hot-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.hot-list li {
  padding: 8px 0;
  border-bottom: 1px dotted #eef1f4;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.85rem;
  line-height: 1.4;
  cursor: pointer;
  transition: color 0.2s;
}

.hot-list li:last-child {
  border-bottom: none;
}

.hot-list li:hover {
  color: #1a7fb5;
}

.rank-num {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #e8ecf1;
  text-align: center;
  line-height: 22px;
  font-weight: 700;
  font-size: 0.75rem;
  color: #5a6c7d;
}

.hot-list li:nth-child(1) .rank-num,
.hot-list li:nth-child(2) .rank-num,
.hot-list li:nth-child(3) .rank-num {
  background: #e8913a;
  color: #fff;
}

/* 标签云 */
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-cloud a {
  display: inline-block;
  padding: 5px 13px;
  border-radius: 20px;
  font-size: 0.78rem;
  text-decoration: none;
  background: #f0f4f8;
  color: #5a6c7d;
  transition: all 0.25s;
}

.tag-cloud a:hover {
  background: #0b3d5f;
  color: #fff;
}

/* 订阅卡片 */
.subscribe-card {
  background: linear-gradient(135deg, #f8fafc 0%, #eef5f9 100%);
  border: 2px dashed #c5d9e8;
}

.subscribe-card p {
  font-size: 0.84rem;
  color: #5a6c7d;
  margin-bottom: 12px;
}

.subscribe-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  font-size: 0.85rem;
  margin-bottom: 10px;
  outline: none;
  transition: border-color 0.2s;
}

.subscribe-input:focus {
  border-color: #0b3d5f;
}

.subscribe-btn {
  width: 100%;
  padding: 10px;
  background: #0b3d5f;
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background 0.25s;
}

.subscribe-btn:hover {
  background: #072d45;
}

.subscribe-btn:disabled {
  background: #8899a6;
  cursor: not-allowed;
}

.subscribe-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.subscribe-message {
  font-size: 0.82rem;
  margin-top: 8px;
  padding: 8px 12px;
  border-radius: 6px;
}

.subscribe-message.success {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.subscribe-message.error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}
</style>
