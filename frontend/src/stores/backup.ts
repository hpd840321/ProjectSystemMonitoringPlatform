import { defineStore } from 'pinia'
import { ref } from 'vue'
import { http } from '@/utils/http'

export const useBackupStore = defineStore('backup', () => {
  // 状态
  const loading = ref(false)
  const backups = ref([])
  const total = ref(0)
  
  // 获取备份列表
  async function listBackups(params) {
    const { page = 1, pageSize = 10 } = params
    const response = await http.get('/api/v1/backups', {
      params: {
        limit: pageSize,
        offset: (page - 1) * pageSize
      }
    })
    backups.value = response.data
    total.value = response.total
    return {
      items: response.data,
      total: response.total
    }
  }
  
  // 创建备份
  async function createBackup() {
    const response = await http.post('/api/v1/backups')
    return response.data
  }
  
  // 恢复备份
  async function restoreBackup(backupId) {
    const response = await http.post(`/api/v1/backups/${backupId}/restore`)
    return response.data
  }
  
  // 删除备份
  async function deleteBackup(backupId) {
    await http.delete(`/api/v1/backups/${backupId}`)
  }
  
  return {
    loading,
    backups,
    total,
    listBackups,
    createBackup,
    restoreBackup,
    deleteBackup
  }
}) 