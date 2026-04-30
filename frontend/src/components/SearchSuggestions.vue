<template>
  <div class="suggestions-wrapper" v-if="showSuggestions && (suggestions.companies.length > 0 || suggestions.subjects.length > 0)">
    <div class="suggestions-dropdown">
      <!-- 公司名称建议 -->
      <div v-if="suggestions.companies.length > 0" class="suggestion-group">
        <div class="suggestion-label">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
          公司名称
        </div>
        <button
          v-for="company in suggestions.companies"
          :key="company"
          class="suggestion-item"
          @click="selectSuggestion(company)"
        >
          <span class="suggestion-text" v-html="highlightMatch(company)"></span>
        </button>
      </div>

      <!-- 主题建议 -->
      <div v-if="suggestions.subjects.length > 0" class="suggestion-group">
        <div class="suggestion-label">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          主题
        </div>
        <button
          v-for="subject in suggestions.subjects"
          :key="subject"
          class="suggestion-item"
          @click="selectSuggestion(subject)"
        >
          <span class="suggestion-text" v-html="highlightMatch(subject)"></span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  query: {
    type: String,
    default: ''
  },
  showSuggestions: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select'])

const API = import.meta.env.VITE_API_URL || (window.location.origin + '/api')
const suggestions = ref({ companies: [], subjects: [] })
let debounceTimer = null

function highlightMatch(text) {
  if (!props.query) return text
  const regex = new RegExp(`(${props.query})`, 'gi')
  return text.replace(regex, '<mark class="highlight">$1</mark>')
}

function selectSuggestion(text) {
  emit('select', text)
}

async function fetchSuggestions(query) {
  if (query.length < 2) {
    suggestions.value = { companies: [], subjects: [] }
    return
  }

  try {
    const resp = await fetch(`${API}/search/suggestions?q=${encodeURIComponent(query)}`)
    const data = await resp.json()
    suggestions.value = data
  } catch (e) {
    console.error('获取搜索建议失败:', e)
    suggestions.value = { companies: [], subjects: [] }
  }
}

watch(() => props.query, (newQuery) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    fetchSuggestions(newQuery)
  }, 300)
})
</script>

<style scoped>
.suggestions-wrapper {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 1000;
  margin-top: 4px;
}

.suggestions-dropdown {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  max-height: 400px;
  overflow-y: auto;
}

.suggestion-group {
  padding: 8px 0;
}

.suggestion-group + .suggestion-group {
  border-top: 1px solid #f1f5f9;
}

.suggestion-label {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.suggestion-item {
  display: block;
  width: 100%;
  padding: 10px 16px;
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 14px;
  color: #1a1a2e;
}

.suggestion-item:hover {
  background: #f0f7ff;
}

.suggestion-text {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.suggestion-text :deep(.highlight) {
  background: #fef08a;
  color: #1a1a2e;
  padding: 1px 2px;
  border-radius: 2px;
}
</style>
