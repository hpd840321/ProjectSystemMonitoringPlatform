import { defineStore } from 'pinia'
import { ref } from 'vue'
import { http } from '@/utils/http'

export const useLogStore = defineStore('log', () => {
  // 状态
  const loading = ref(false)
  const logs = ref([])
  const total = ref(0)
  
  // 获取日志列表
  async function listLogs(params) {
    const {
      page = 1,
      pageSize = 20,
      level,
      source,
      startTime,
      endTime,
      keyword
    } = params
    
    const response = await http.get('/api/v1/logs', {
      params: {
        limit: pageSize,
        offset: (page - 1) * pageSize,
        level,
        source,
        start_time: startTime,
        end_time: endTime,
        keyword
      }
    })
    
    logs.value = response.data
    total.value = response.total
    return {
      items: response.data,
      total: response.total
    }
  }
  
  // 导出日志
  async function exportLogs(params) {
    const response = await http.get('/api/v1/logs/export', {
      params,
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(response.data)
    const link = document.createElement('a')
    link.href = url
    link.download = 'logs.csv'
    link.click()
    window.URL.revokeObjectURL(url)
  }
  
  return {
    loading,
    logs,
    total,
    listLogs,
    exportLogs
  }
}) 