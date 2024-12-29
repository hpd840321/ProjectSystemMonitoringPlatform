import { defineStore } from 'pinia'
import { http } from '@/utils/http'
import { message } from 'ant-design-vue'

interface RegisterData {
  username: string
  email: string
  password: string
  confirmPassword: string
  tenantId?: string
  captcha: string
}

interface LoginData {
  username: string
  password: string
  captcha: string
}

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: null,
    token: null,
    loading: false
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
    async register(data: RegisterData) {
      this.loading = true
      try {
        await http.post('/api/v1/auth/register', data)
        message.success('注册成功')
        return true
      } catch (error: any) {
        message.error(error.response?.data?.detail || '注册失败')
        throw error
      } finally {
        this.loading = false
      }
    },

    async login(data: LoginData) {
      this.loading = true
      try {
        const response = await http.post('/api/v1/auth/login', data)
        this.token = response.data.token
        this.currentUser = response.data.user
        return true
      } catch (error: any) {
        message.error(error.response?.data?.detail || '登录失败')
        throw error
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.token = null
      this.currentUser = null
    }
  },

  persist: {
    key: 'user-store',
    paths: ['token']
  }
}) 