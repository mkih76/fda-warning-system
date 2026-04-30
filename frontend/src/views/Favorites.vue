<template>
  <div class="favorites-page">
    <!-- 页头 -->
    <div class="page-header">
      <div>
        <h1 class="page-title">我的收藏</h1>
        <p class="page-subtitle">收藏的警告信列表</p>
      </div>
      <div class="page-actions" v-if="favoritesCount > 0">
        <button @click="clearAll" class="btn-ghost">
          清空收藏
        </button>
        <div class="page-status">
          <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
          </svg>
          <span>{{ favoritesCount }} 条收藏</span>
        </div>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!loading && letters.length === 0" class="empty-state">
      <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
      </svg>
      <h3>暂无收藏</h3>
      <p>浏览警告信列表，点击爱心图标即可收藏</p>
      <router-link to="/letters" class="btn-primary">
        浏览警告信
      </router-link>
    </div>

    <!-- 收藏列表 -->
    <div v-else class="letters-grid">
      <LetterCard v-for="letter in letters" :key="letter.id" :letter="letter" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useFavorites } from '../composables/useFavorites.js'
import LetterCard from '../components/LetterCard.vue'

const API = window.location.origin + '/api'
const { favorites, favoritesCount, clearFavorites } = useFavorites()

const letters = ref([])
const loading = ref(true)

async function fetchFavoriteLetters() {
  if (favoritesCount.value === 0) {
    letters.value = []
    loading.value = false
    return
  }

  loading.value = true
  try {
    const letterPromises = favorites.value.map(id =>
      fetch(`${API}/letters/${id}`).then(r => r.json()).catch(() => null)
    )
    const results = await Promise.all(letterPromises)
    letters.value = results.filter(l => l !== null)
  } catch (e) {
    console.error('获取收藏列表失败:', e)
    letters.value = []
  } finally {
    loading.value = false
  }
}

function clearAll() {
  if (confirm('确定要清空所有收藏吗？')) {
    clearFavorites()
    letters.value = []
  }
}

// 监听收藏变化
watch(favorites, () => {
  fetchFavoriteLetters()
}, { deep: true })

onMounted(() => {
  fetchFavoriteLetters()
})
</script>

<style scoped>
.favorites-page {
  max-width: 1280px;
  margin: 0 auto;
  padding: 104px 32px 64px;
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

@media (min-width: 640px) {
  .page-header {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.02em;
  margin: 0;
}

.page-subtitle {
  font-size: 15px;
  color: var(--text-3);
  margin-top: 4px;
}

.page-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-2);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 8px;
  background: var(--accent);
  color: white;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: var(--accent-dark);
}

.btn-ghost {
  padding: 10px 20px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-2);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-ghost:hover {
  border-color: #ef4444;
  color: #ef4444;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: var(--text-3);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: var(--text-3);
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
  opacity: 0.3;
  color: #ef4444;
}

.empty-state h3 {
  font-size: 24px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 8px;
}

.empty-state p {
  font-size: 16px;
  margin: 0 0 24px;
}

.letters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}
</style>
