<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card">
        <h1>登录</h1>
        <p class="auth-subtitle">登录您的 PharmaCos Insight 账号</p>

        <div v-if="error" class="auth-error">{{ error }}</div>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="email" type="email" placeholder="your@email.com" required />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="password" type="password" placeholder="输入密码" required />
          </div>
          <button type="submit" class="auth-btn" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>

        <div class="auth-footer">
          还没有账号？<router-link to="/register">注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth.js'

const router = useRouter()
const { login } = useAuth()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await login(email.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.message
  }
  loading.value = false
}
</script>

<style scoped>
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f5f5f5; padding: 20px; }
.auth-container { width: 100%; max-width: 420px; }
.auth-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 48px 40px; }
.auth-card h1 { font-size: 28px; font-weight: 700; color: #000; margin: 0 0 8px; text-align: center; }
.auth-subtitle { font-size: 14px; color: #666; text-align: center; margin: 0 0 32px; }
.auth-error { background: #fef2f2; color: #dc2626; padding: 12px 16px; border-radius: 4px; font-size: 14px; margin-bottom: 20px; }
.auth-form { display: flex; flex-direction: column; gap: 20px; }
.form-group label { display: block; font-size: 14px; font-weight: 500; color: #333; margin-bottom: 6px; }
.form-group input { width: 100%; padding: 12px 16px; border: 1px solid #e5e7eb; border-radius: 4px; font-size: 15px; transition: border-color 0.2s; }
.form-group input:focus { outline: none; border-color: #0000C9; box-shadow: 0 0 0 3px rgba(0,0,201,0.08); }
.auth-btn { width: 100%; padding: 14px; background: #0000C9; color: #fff; border: none; border-radius: 4px; font-size: 15px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.auth-btn:hover { background: #0000A3; }
.auth-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.auth-footer { text-align: center; margin-top: 24px; font-size: 14px; color: #666; }
.auth-footer a { color: #0000C9; font-weight: 500; }
</style>
