import { ref, computed, watch } from 'vue'

const STORAGE_KEY = 'fda-favorites'

/**
 * 收藏功能 composable
 * 使用 localStorage 存储收藏的警告信 ID
 */
const favorites = ref(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'))

// 监听变化并持久化
watch(favorites, (val) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(val))
}, { deep: true })

export function useFavorites() {
  /**
   * 检查是否已收藏
   */
  function isFavorite(letterId) {
    return favorites.value.includes(letterId)
  }

  /**
   * 切换收藏状态
   */
  function toggleFavorite(letterId) {
    const index = favorites.value.indexOf(letterId)
    if (index > -1) {
      favorites.value.splice(index, 1)
    } else {
      favorites.value.push(letterId)
    }
  }

  /**
   * 添加收藏
   */
  function addFavorite(letterId) {
    if (!isFavorite(letterId)) {
      favorites.value.push(letterId)
    }
  }

  /**
   * 移除收藏
   */
  function removeFavorite(letterId) {
    const index = favorites.value.indexOf(letterId)
    if (index > -1) {
      favorites.value.splice(index, 1)
    }
  }

  /**
   * 获取所有收藏
   */
  function getAllFavorites() {
    return [...favorites.value]
  }

  /**
   * 清空所有收藏
   */
  function clearFavorites() {
    favorites.value = []
  }

  /**
   * 收藏数量
   */
  const favoritesCount = computed(() => favorites.value.length)

  return {
    favorites,
    favoritesCount,
    isFavorite,
    toggleFavorite,
    addFavorite,
    removeFavorite,
    getAllFavorites,
    clearFavorites
  }
}
