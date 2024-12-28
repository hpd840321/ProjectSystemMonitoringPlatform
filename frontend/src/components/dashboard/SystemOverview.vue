<template>
  <div class="system-overview">
    <el-row :gutter="20">
      <!-- 系统状态卡片 -->
      <el-col :span="6" v-for="item in statusCards" :key="item.title">
        <el-card shadow="hover" :class="item.type">
          <div class="status-card">
            <div class="icon">
              <el-icon><component :is="item.icon" /></el-icon>
            </div>
            <div class="content">
              <div class="title">{{ item.title }}</div>
              <div class="value">{{ item.value }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 资源使用趋势图 -->
    <el-row :gutter="20" class="charts">
      <el-col :span="8">
        <ResourceTrendChart
          title="CPU使用率"
          :data="cpuTrend"
        />
      </el-col>
      <el-col :span="8">
        <ResourceTrendChart
          title="内存使用率"
          :data="memoryTrend"
        />
      </el-col>
      <el-col :span="8">
        <ResourceTrendChart
          title="磁盘使用率"
          :data="diskTrend"
        />
      </el-col>
    </el-row>
    
    <!-- 系统健康状态 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>服务状态</span>
            </div>
          </template>
          <el-table :data="serviceStatus" stripe>
            <el-table-column prop="name" label="服务名称" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="uptime" label="运行时间" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>告警统计</span>
            </div>
          </template>
          <div class="alert-stats">
            <div class="stat-item" v-for="stat in alertStats" :key="stat.level">
              <div class="label">{{ stat.label }}</div>
              <div class="count" :class="stat.level">{{ stat.count }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Monitor, CPU, Memory, Storage } from '@element-plus/icons-vue'
import ResourceTrendChart from '@/components/charts/ResourceTrendChart.vue'

// 状态卡片数据
const statusCards = ref([
  {
    title: '在线服务器',
    value: '42/45',
    icon: Monitor,
    type: 'success'
  },
  {
    title: 'CPU使用率',
    value: '65%',
    icon: CPU,
    type: 'warning'
  },
  {
    title: '内存使用率',
    value: '78%',
    icon: Memory,
    type: 'danger'
  },
  {
    title: '磁盘使用率',
    value: '45%',
    icon: Storage,
    type: 'info'
  }
])

// 趋势图数据
const cpuTrend = ref({
  timestamps: [],
  values: []
})
const memoryTrend = ref({
  timestamps: [],
  values: []
})
const diskTrend = ref({
  timestamps: [],
  values: []
})

// 服务状态数据
const serviceStatus = ref([
  { name: 'Agent服务', status: 'running', uptime: '10天' },
  { name: '监控服务', status: 'running', uptime: '10天' },
  { name: '告警服务', status: 'running', uptime: '10天' },
  { name: '日志服务', status: 'warning', uptime: '5天' }
])

// 告警统计
const alertStats = ref([
  { label: '严重告警', level: 'critical', count: 2 },
  { label: '警���', level: 'warning', count: 5 },
  { label: '信息', level: 'info', count: 12 }
])

// 获取状态样式
function getStatusType(status: string) {
  const map: Record<string, string> = {
    running: 'success',
    warning: 'warning',
    error: 'danger'
  }
  return map[status] || 'info'
}

// 加载数据
async function loadData() {
  // TODO: 从API获取数据
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.system-overview {
  padding: 20px;
}
.status-card {
  display: flex;
  align-items: center;
  .icon {
    font-size: 24px;
    margin-right: 15px;
  }
  .content {
    .title {
      font-size: 14px;
      color: #909399;
    }
    .value {
      font-size: 24px;
      font-weight: bold;
      margin-top: 5px;
    }
  }
}
.charts {
  margin: 20px 0;
}
.alert-stats {
  display: flex;
  justify-content: space-around;
  .stat-item {
    text-align: center;
    .label {
      font-size: 14px;
      color: #909399;
    }
    .count {
      font-size: 24px;
      font-weight: bold;
      margin-top: 5px;
      &.critical { color: #F56C6C; }
      &.warning { color: #E6A23C; }
      &.info { color: #409EFF; }
    }
  }
}
</style> 