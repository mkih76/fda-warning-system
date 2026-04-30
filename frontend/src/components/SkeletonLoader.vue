<template>
  <div class="skeleton-wrapper" :class="type">
    <!-- 卡片骨架 -->
    <template v-if="type === 'card'">
      <div class="skeleton-card" v-for="n in count" :key="n">
        <div class="skeleton-line skeleton-title"></div>
        <div class="skeleton-line skeleton-text"></div>
        <div class="skeleton-line skeleton-text short"></div>
        <div class="skeleton-footer">
          <div class="skeleton-badge"></div>
          <div class="skeleton-button"></div>
        </div>
      </div>
    </template>

    <!-- 列表骨架 -->
    <template v-else-if="type === 'list'">
      <div class="skeleton-list-item" v-for="n in count" :key="n">
        <div class="skeleton-avatar"></div>
        <div class="skeleton-content">
          <div class="skeleton-line skeleton-title"></div>
          <div class="skeleton-line skeleton-text"></div>
        </div>
      </div>
    </template>

    <!-- 表格骨架 -->
    <template v-else-if="type === 'table'">
      <div class="skeleton-table">
        <div class="skeleton-table-header">
          <div class="skeleton-line" v-for="col in columns" :key="col" :style="{ width: col + '%' }"></div>
        </div>
        <div class="skeleton-table-row" v-for="n in count" :key="n">
          <div class="skeleton-line" v-for="col in columns" :key="col" :style="{ width: col + '%' }"></div>
        </div>
      </div>
    </template>

    <!-- 统计卡片骨架 -->
    <template v-else-if="type === 'stats'">
      <div class="skeleton-stat" v-for="n in count" :key="n">
        <div class="skeleton-circle"></div>
        <div class="skeleton-content">
          <div class="skeleton-line skeleton-number"></div>
          <div class="skeleton-line skeleton-label"></div>
        </div>
      </div>
    </template>

    <!-- 默认：通用骨架 -->
    <template v-else>
      <div class="skeleton-line" v-for="n in count" :key="n"
           :class="{ 'skeleton-title': n === 1, 'short': n > 2 }"></div>
    </template>
  </div>
</template>

<script setup>
const props = defineProps({
  type: {
    type: String,
    default: 'lines',
    validator: (val) => ['card', 'list', 'table', 'stats', 'lines'].includes(val)
  },
  count: {
    type: Number,
    default: 3
  },
  columns: {
    type: Array,
    default: () => [30, 40, 20, 10]
  }
})
</script>

<style scoped>
.skeleton-wrapper {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton-line {
  height: 14px;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 10px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-title {
  height: 20px;
  width: 60%;
}

.skeleton-text {
  width: 90%;
}

.skeleton-text.short {
  width: 70%;
}

/* Card Skeleton */
.skeleton-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
}

.skeleton-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.skeleton-badge {
  width: 60px;
  height: 24px;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 12px;
}

.skeleton-button {
  width: 80px;
  height: 32px;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 6px;
}

/* List Skeleton */
.skeleton-list-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 8px;
}

.skeleton-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  flex-shrink: 0;
}

.skeleton-content {
  flex: 1;
}

/* Table Skeleton */
.skeleton-table-header {
  display: flex;
  gap: 16px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px 8px 0 0;
}

.skeleton-table-row {
  display: flex;
  gap: 16px;
  padding: 12px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

/* Stats Skeleton */
.skeleton-stat {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}

.skeleton-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-number {
  height: 28px;
  width: 60%;
}

.skeleton-label {
  height: 12px;
  width: 40%;
}
</style>
