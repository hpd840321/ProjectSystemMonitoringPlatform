<template>
  <div class="server-detail">
    <div class="header">
      <div class="title">
        <h2>{{ server?.name }}</h2>
        <el-tag :type="getStatusType(server?.status)">
          {{ getStatusText(server?.status) }}
        </el-tag>
      </div>
    </div>

    <el-descriptions :column="2" border>
      <el-descriptions-item label="主机地址">
        {{ server?.host }}
      </el-descriptions-item>
      <el-descriptions-item label="Agent ID">
        {{ server?.agent_id || '未绑定' }}
      </el-descriptions-item>
      <el-descriptions-item label="最后心跳">
        {{ formatDate(server?.last_heartbeat) || '暂无数据' }}
      </el-descriptions-item>
      <el-descriptions-item label="描述">
        {{ server?.description }}
      </el-descriptions-item>
    </el-descriptions>

    <div class="metrics-panel">
      <div class="panel-header">
        <h3>实时指标</h3>
        <el-button-group>
          <el-button size="small" @click="refreshMetrics">刷新</el-button>
          <el-button size="small" @click="startAutoRefresh">自动刷新</el-button>
        </el-button-group>
      </div>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="metric-card">
            <template #header>
              <div class="card-header">
                <span>CPU使用率</span>
                <el-tag :type="getUsageStatus(metrics?.cpu_usage)">
                  {{ metrics?.cpu_usage }}%
                </el-tag>
              </div>
            </template>
            <div class="chart-container">
              <line-chart :data="cpuHistory" />
            </div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="metric-card">
            <template #header>
              <div class="card-header">
                <span>内存使用率</span>
                <el-tag :type="getUsageStatus(metrics?.memory_usage)">
                  {{ metrics?.memory_usage }}%
                </el-tag>
              </div>
            </template>
            <div class="chart-container">
              <line-chart :data="memoryHistory" />
            </div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="metric-card">
            <template #header>
              <div class="card-header">
                <span>磁盘使用率</span>
                <el-tag :type="getUsageStatus(metrics?.disk_usage)">
                  {{ metrics?.disk_usage }}%
                </el-tag>
              </div>
            </template>
            <div class="chart-container">
              <line-chart :data="diskHistory" />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="log-panel">
      <div class="panel-header">
        <h3>系统日志</h3>
        <el-select v-model="logType" size="small">
          <el-option label="系统日志" value="system" />
          <el-option label="应用日志" value="application" />
          <el-option label="安全日志" value="security" />
        </el-select>
      </div>
      <el-table :data="logs" height="300" v-loading="logsLoading">
        <el-table-column prop="timestamp" label="时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.timestamp) }}
          </template>
        </el-table-column>
        <el-table-column prop="level" label="级别" width="100">
          <template #default="{ row }">
            <el-tag :type="getLogLevelType(row.level)">
              {{ row.level }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="内容" />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useProjectStore } from '@/stores/project'
import { formatDate } from '@/utils/date'
import LineChart from '@/components/charts/LineChart.vue'

const route = useRoute()
const projectStore = useProjectStore()

const server = ref(null)
const metrics = ref(null)
const logs = ref([])
const logsLoading = ref(false)
const logType = ref('system')

// 指标历史数据
const cpuHistory = ref([])
const memoryHistory = ref([])
const diskHistory = ref([])

let refreshTimer = null

// 获取服务器详情
const fetchServerDetail = async () => {
  try {
    const { projectId, serverId } = route.params
    server.value = await projectStore.fetchServerDetail(projectId, serverId)
    metrics.value = server.value.metrics
  } catch (error) {
    ElMessage.error('获取服务器详情失败')
  }
}

// 刷新指标数据
const refreshMetrics = async () => {
  try {
    const { serverId } = route.params
    const newMetrics = await projectStore.fetchServerMetrics(serverId)
    metrics.value = newMetrics
    
    // 更新历史数据
    updateMetricsHistory(newMetrics)
  } catch (error) {
    ElMessage.error('��取指标数据失败')
  }
}

// 更新指标历史数据
const updateMetricsHistory = (newMetrics) => {
  const now = new Date().getTime()
  
  cpuHistory.value.push({
    time: now,
    value: newMetrics.cpu_usage
  })
  
  memoryHistory.value.push({
    time: now,
    value: newMetrics.memory_usage
  })
  
  diskHistory.value.push({
    time: now,
    value: newMetrics.disk_usage
  })
  
  // 保留最近30个数据点
  if (cpuHistory.value.length > 30) {
    cpuHistory.value.shift()
    memoryHistory.value.shift()
    diskHistory.value.shift()
  }
}

// 开始自动刷新
const startAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
  refreshTimer = setInterval(refreshMetrics, 5000)
}

// 获取日志数据
const fetchLogs = async () => {
  logsLoading.value = true
  try {
    const { projectId, serverId } = route.params
    logs.value = await projectStore.fetchServerLogs(projectId, serverId, {
      type: logType.value
    })
  } catch (error) {
    ElMessage.error('获取日志数据失败')
  } finally {
    logsLoading.value = false
  }
}

// 监听日志类型变化
watch(logType, fetchLogs)

onMounted(() => {
  fetchServerDetail()
  fetchLogs()
  startAutoRefresh()
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.server-detail {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.metrics-panel,
.log-panel {
  margin-top: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.metric-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 200px;
}
</style> 