/**
 * PharmaCos Insight - Authentication Composable
 * Manages user state, login, register, logout.
 */
import { ref, computed } from 'vue'

const API = window.location.origin + '/api'

const user = ref(null)
const token = ref(localStorage.getItem('pharmacos-token') || '')

// Initialize user from stored token
if (token.value) {
  fetchMe().catch(() => {
    // Token expired or invalid — clear it
    token.value = ''
    localStorage.removeItem('pharmacos-token')
  })
}

const isLoggedIn = computed(() => !!user.value)
const isAdmin = computed(() => user.value?.role === 'admin')
const isPro = computed(() => ['pro', 'enterprise', 'admin'].includes(user.value?.role))

async function fetchMe() {
  const resp = await fetch(`${API}/auth/me`, {
    headers: { Authorization: `Bearer ${token.value}` }
  })
  if (!resp.ok) throw new Error('Not authenticated')
  user.value = await resp.json()
}

async function login(email, password) {
  const resp = await fetch(`${API}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  const data = await resp.json()
  if (!resp.ok) throw new Error(data.detail || '登录失败')
  token.value = data.access_token
  user.value = data.user
  localStorage.setItem('pharmacos-token', token.value)
  return data
}

async function register(email, password, nickname) {
  const resp = await fetch(`${API}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, nickname })
  })
  const data = await resp.json()
  if (!resp.ok) throw new Error(data.detail || '注册失败')
  token.value = data.access_token
  user.value = data.user
  localStorage.setItem('pharmacos-token', token.value)
  return data
}

function logout() {
  user.value = null
  token.value = ''
  localStorage.removeItem('pharmacos-token')
}

export function useAuth() {
  return {
    user,
    token,
    isLoggedIn,
    isAdmin,
    isPro,
    login,
    register,
    logout,
    fetchMe,
  }
}
