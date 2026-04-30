<template>
  <div class="search-bar">
    <div class="search-input-group">
      <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
      <input
        v-model="query"
        type="text"
        :placeholder="placeholder"
        class="search-input"
        @keyup.enter="emitSearch"
      />
      <button v-if="query" class="clear-btn" @click="clearQuery" title="清除">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '搜索公司名、FDA ID...'
  }
})

const emit = defineEmits(['update:modelValue', 'search'])

const query = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  query.value = val
})

function emitSearch() {
  emit('update:modelValue', query.value)
  emit('search', query.value)
}

function clearQuery() {
  query.value = ''
  emit('update:modelValue', '')
  emit('search', '')
}
</script>

<style scoped>
.search-bar {
  width: 100%;
}

.search-input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: var(--text-3);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 14px 48px 14px 48px;
  font-size: 15px;
  font-family: inherit;
  line-height: 1.5;
  border: 2px solid var(--border);
  border-radius: 10px;
  background: white;
  color: var(--text);
  outline: none;
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: var(--text-3);
}

.search-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 4px rgba(var(--accent-rgb), 0.1);
}

.clear-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 6px;
  background: var(--surface-3);
  color: var(--text-3);
  cursor: pointer;
  transition: all 0.15s ease;
  padding: 0;
}

.clear-btn svg {
  width: 16px;
  height: 16px;
}

.clear-btn:hover {
  background: var(--border);
  color: var(--text);
}
</style>
