<template>
  <div class="letter-card" @click="$router.push('/letters/' + letter.id)">
    <div class="card-header">
      <span class="status-badge" :class="letter.status === 'active' ? 'status-active' : 'status-closed'">
        {{ letter.status === 'active' ? '进行中' : '已关闭' }}
      </span>
      <button
        class="favorite-btn"
        :class="{ 'is-favorite': isFavorite(letter.id) }"
        @click.stop="toggleFavorite(letter.id)"
        :title="isFavorite(letter.id) ? '取消收藏' : '收藏'"
      >
        <svg viewBox="0 0 24 24" :fill="isFavorite(letter.id) ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
        </svg>
      </button>
    </div>

    <div class="card-body">
      <h3 class="company-name">{{ letter.company_name }}</h3>
      <p class="summary-preview">{{ summaryText }}</p>
    </div>

    <div class="card-footer">
      <div class="footer-meta">
        <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        <span>{{ letter.posted_date || '—' }}</span>
      </div>
      <span class="office-tag">{{ letter.issuing_office || 'FDA' }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useFavorites } from '../composables/useFavorites.js'

const props = defineProps({
  letter: {
    type: Object,
    required: true
  }
})

const { isFavorite, toggleFavorite } = useFavorites()

const summaryText = computed(() => {
  const src = props.letter.analysis?.summary_zh || props.letter.subject || ''
  return src.length > 120 ? src.slice(0, 120) + '...' : src
})
</script>

<style scoped>
.letter-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--card-shadow);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.letter-card:hover {
  border-color: var(--accent);
  box-shadow: var(--card-shadow-hover);
  transform: translateY(-2px);
}

/* Header */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.favorite-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: #94a3b8;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
}

.favorite-btn:hover {
  color: #ef4444;
  transform: scale(1.1);
}

.favorite-btn.is-favorite {
  color: #ef4444;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.status-active {
  background: rgba(220, 38, 38, 0.1);
  color: var(--danger);
}

.status-closed {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
}

.fda-id {
  font-size: 13px;
  font-weight: 500;
  font-family: 'SF Mono', 'Fira Code', monospace;
  color: var(--text-3);
}

/* Body */
.card-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.company-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.3;
  margin: 0;
}

.summary-preview {
  font-size: 14px;
  color: var(--text-2);
  line-height: 1.6;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Footer */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid var(--border-light);
}

.footer-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-3);
}

.meta-icon {
  width: 16px;
  height: 16px;
}

.office-tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  background: var(--surface-3);
  color: var(--text-2);
}
</style>
