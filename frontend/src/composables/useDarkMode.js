import { ref, watch, onMounted } from 'vue'

const STORAGE_KEY = 'fda-dark-mode'

/**
 * 全局暗色模式状态
 * 在 Navbar 中通过 toggleDark() 切换，App.vue 监听并同步到 <html> class
 */
const isDark = ref(false)

function applyClass(val) {
  if (val) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

export function useDarkMode() {
  function toggleDark() {
    isDark.value = !isDark.value
  }

  function setDark(val) {
    isDark.value = val
  }

  // 初始化：优先 localStorage，否则跟随系统偏好
  onMounted(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored !== null) {
      isDark.value = stored === 'true'
    } else {
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    applyClass(isDark.value)
  })

  // 监听变化：同步到 DOM + localStorage
  watch(isDark, (val) => {
    applyClass(val)
    localStorage.setItem(STORAGE_KEY, val)
  })

  return { isDark, toggleDark, setDark }
}
