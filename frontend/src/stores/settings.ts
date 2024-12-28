import { defineStore } from 'pinia'
import { ref } from 'vue'
import { http } from '@/utils/http'
import type { SystemSettings } from '@/types/settings'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<SystemSettings | null>(null)
  
  // 获取系统设置
  async function getSettings() {
    const response = await http.get('/api/v1/settings')
    settings.value = response.data
    return response.data
  }
  
  // 更新系统设置
  async function updateSettings(data: SystemSettings) {
    const response = await http.put('/api/v1/settings', data)
    settings.value = response.data
    return response.data
  }
  
  return {
    settings,
    getSettings,
    updateSettings
  }
}) 