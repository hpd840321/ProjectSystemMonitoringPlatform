import { defineStore } from 'pinia'
import { http } from '@/utils/http'
import { message } from 'ant-design-vue'

interface Tenant {
  id: string
  name: string
  code: string
  status: string
}

export const useTenantStore = defineStore('tenant', {
  state: () => ({
    tenants: [] as Tenant[],
    loading: false,
    currentTenant: null as Tenant | null
  }),

  getters: {
    activeTenants: (state) => 
      state.tenants.filter(t => t.status === 'active')
  },

  actions: {
    async fetchTenants() {
      this.loading = true
      try {
        const { data } = await http.get('/api/v1/tenants')
        this.tenants = data
      } catch (error: any) {
        message.error('获取租户列表失败')
        throw error
      } finally {
        this.loading = false
      }
    },

    async selectTenant(tenantId: string) {
      const tenant = this.tenants.find(t => t.id === tenantId)
      if (tenant) {
        this.currentTenant = tenant
        return true
      }
      return false
    }
  },

  persist: {
    key: 'tenant-store',
    paths: ['currentTenant']
  }
}) 