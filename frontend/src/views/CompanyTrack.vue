<template>
  <div class="max-w-4xl mx-auto px-6 py-10">
    <h1 class="text-3xl font-bold text-pharma-900 dark:text-dark-100 mb-2 transition-colors">企业追踪</h1>
    <p class="text-pharma-400 dark:text-dark-400 mb-8 transition-colors">查询企业 FDA 警告信历史</p>

    <div class="flex gap-3 mb-8">
      <input v-model="companyName" @keyup.enter="search" placeholder="输入企业名称..."
             class="flex-1 px-5 py-3 rounded-xl border border-gray-200 dark:border-dark-600 bg-white dark:bg-dark-800 focus:outline-none focus:ring-2 focus:ring-teal-400/50 text-sm text-pharma-900 dark:text-dark-100 placeholder-pharma-300 dark:placeholder-dark-400 transition-colors">
      <button @click="search" class="btn-primary text-sm px-6">查询</button>
    </div>

    <div v-if="loading" class="text-center py-20 text-pharma-400 dark:text-dark-400">查询中...</div>

    <div v-if="timeline && timeline.length > 0" class="space-y-4">
      <div v-for="item in timeline" :key="item.fda_id"
           @click="$router.push('/letters/'+item.fda_id)" class="card cursor-pointer">
        <div class="flex items-center gap-2 mb-2">
          <span :class="item.status==='active'?'badge-active':'badge-closed'">{{ item.status==='active'?'活跃':'已关闭'}}</span>
          <span class="text-xs text-pharma-300 dark:text-dark-400 transition-colors">{{ item.posted_date }}</span>
        </div>
        <h3 class="font-semibold text-pharma-900 dark:text-dark-100 transition-colors">{{ item.subject }}</h3>
        <p class="text-xs text-pharma-400 dark:text-dark-400 mt-1 transition-colors">办公室: {{ item.issuing_office }}{{ item.closeout_date ? ' · 关闭: ' + item.closeout_date : '' }}</p>
      </div>
    </div>
    <div v-else-if="searched" class="text-center py-20 text-pharma-400 dark:text-dark-400">未找到该企业的警告信记录</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const API = window.location.origin + '/api'
const companyName = ref('')
const timeline = ref(null)
const searched = ref(false)
const loading = ref(false)

async function search() {
  if (!companyName.value) return
  loading.value = true; searched.value = true
  try {
    const resp = await fetch(`${API}/letters/company/${encodeURIComponent(companyName.value)}`)
    timeline.value = await resp.json()
  } catch(e) { timeline.value = [] }
  finally { loading.value = false }
}
</script>
