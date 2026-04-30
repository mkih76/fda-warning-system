/**
 * PharmaCos Insight - API Composable
 * Centralized fetch with automatic JWT attachment and error handling.
 */
import { useAuth } from './useAuth.js'

const API = window.location.origin + '/api'

export function useApi() {
  const { token, logout } = useAuth()

  async function apiFetch(path, options = {}) {
    const headers = { ...options.headers }

    if (token.value) {
      headers['Authorization'] = `Bearer ${token.value}`
    }

    if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json'
      options.body = JSON.stringify(options.body)
    }

    const resp = await fetch(`${API}${path}`, { ...options, headers })

    if (resp.status === 401) {
      logout()
      window.location.hash = '#/'
      throw new Error('登录已过期，请重新登录')
    }

    if (!resp.ok) {
      const data = await resp.json().catch(() => ({}))
      throw new Error(data.detail || `请求失败 (${resp.status})`)
    }

    return resp.json()
  }

  return { apiFetch }
}
