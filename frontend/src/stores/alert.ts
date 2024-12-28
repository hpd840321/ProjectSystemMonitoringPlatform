import { defineStore } from 'pinia'
import { ref } from 'vue'
import { http } from '@/utils/http'

export const useAlertStore = defineStore('alert', () => {
  // 状态
  const loading = ref(false)
  const rules = ref([])
  const alerts = ref([])
  const total = ref(0)
  
  // 获取告警规则列表
  async function listRules() {
    const response = await http.get('/api/v1/alert-rules')
    rules.value = response.data
    return response.data
  }
  
  // 创建告警规则
  async function createRule(data) {
    const response = await http.post('/api/v1/alert-rules', data)
    return response.data
  }
  
  // 更新告警规则
  async function updateRule(ruleId, data) {
    const response = await http.put(`/api/v1/alert-rules/${ruleId}`, data)
    return response.data
  }
  
  // 删除告警规则
  async function deleteRule(ruleId) {
    await http.delete(`/api/v1/alert-rules/${ruleId}`)
  }
  
  // 获取告警历史
  async function listAlerts(params) {
    const { page = 1, pageSize = 10 } = params
    const response = await http.get('/api/v1/alerts', {
      params: {
        limit: pageSize,
        offset: (page - 1) * pageSize
      }
    })
    alerts.value = response.data
    total.value = response.total
    return {
      items: response.data,
      total: response.total
    }
  }
  
  return {
    loading,
    rules,
    alerts,
    total,
    listRules,
    createRule,
    updateRule,
    deleteRule,
    listAlerts
  }
}) 