import { defineStore } from 'pinia'
import { ref } from 'vue'
import { http } from '@/utils/http'

export const useProjectStore = defineStore('project', () => {
  const currentTenant = ref(null)
  const projects = ref([])

  // 获取项目列表
  const fetchProjects = async () => {
    const response = await http.get(`/tenants/${currentTenant.value.id}/projects`)
    projects.value = response.data
    return response.data
  }

  // 创建项目
  const createProject = async (data) => {
    const response = await http.post('/projects', data)
    return response.data
  }

  // 获取项目详情
  const fetchProjectDetail = async (projectId: string) => {
    const response = await http.get(`/projects/${projectId}`)
    return response.data
  }

  // 获取项目服务器列表
  const fetchProjectServers = async (projectId: string) => {
    const response = await http.get(`/projects/${projectId}/servers`)
    return response.data
  }

  // 添加服务器
  const addServer = async (projectId: string, data) => {
    const response = await http.post(`/projects/${projectId}/servers`, data)
    return response.data
  }

  // 移除服务器
  const removeServer = async (projectId: string, serverId: string) => {
    await http.delete(`/projects/${projectId}/servers/${serverId}`)
  }

  // 更新服务器指标
  const updateServerMetrics = async (serverId: string, data) => {
    await http.put(`/projects/servers/${serverId}/metrics`, data)
  }

  return {
    projects,
    fetchProjects,
    createProject,
    fetchProjectDetail,
    fetchProjectServers,
    addServer,
    removeServer,
    updateServerMetrics
  }
}) 