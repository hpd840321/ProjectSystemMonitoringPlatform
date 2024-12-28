<template>
  <div class="log-list">
    <div class="header">
      <h2>日志查看</h2>
      <div class="filters">
        <el-select v-model="filters.level" placeholder="日志级别" clearable>
          <el-option label="ERROR" value="error" />
          <el-option label="WARN" value="warn" />
          <el-option label="INFO" value="info" />
          <el-option label="DEBUG" value="debug" />
        </el-select>
        <el-select v-model="filters.source" placeholder="日志来源" clearable>
          <el-option label="系统" value="system" />
          <el-option label="应用" value="app" />
          <el-option label="审计" value="audit" />
        </el-select>
        <el-date-picker
          v-model="filters.timeRange"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
        />
        <el-input
          v-model="filters.keyword"
          placeholder="搜索关键字"
          clearable
          style="width: 200px"
        />
        <el-button type="primary" @click="search">搜索</el-button>
      </div>
    </div>
    
    <el-table :data="logs" v-loading="loading" stripe>
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
      <el-table-column prop="source" label="来源" width="120" />
      <el-table-column prop="message" label="内容" show-overflow-tooltip />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="showDetail(row)">
            详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-pagination
      v-model:current-page="page"
      v-model:page-size="pageSize"
      :total="total"
      @current-change="loadLogs"
    />
    
    <!-- 日志详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="日志详情"
      width="60%"
    >
      <div v-if="selectedLog" class="log-detail">
        <div class="detail-item">
          <span class="label">时间:</span>
          <span>{{ formatDate(selectedLog.timestamp) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">级别:</span>
          <el-tag :type="getLogLevelType(selectedLog.level)">
            {{ selectedLog.level }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">来源:</span>
          <span>{{ selectedLog.source }}</span>
        </div>
        <div class="detail-item">
          <span class="label">内容:</span>
          <pre>{{ selectedLog.message }}</pre>
        </div>
        <div class="detail-item">
          <span class="label">上下文:</span>
          <pre>{{ JSON.stringify(selectedLog.context, null, 2) }}</pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useLogStore } from '@/stores/log'
import { formatDate } from '@/utils/format'

const logStore = useLogStore()
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const logs = ref([])

// 筛选条件
const filters = reactive({
  level: '',
  source: '',
  timeRange: [],
  keyword: ''
})

// 日志详情
const detailDialogVisible = ref(false)
const selectedLog = ref(null)

// 加载日志列表
async function loadLogs() {
  loading.value = true
  try {
    const result = await logStore.listLogs({
      page: page.value,
      pageSize: pageSize.value,
      ...filters,
      startTime: filters.timeRange?.[0],
      endTime: filters.timeRange?.[1]
    })
    logs.value = result.items
    total.value = result.total
  } catch (error) {
    ElMessage.error('加载日志失败')
  }
  loading.value = false
}

// 搜索
function search() {
  page.value = 1
  loadLogs()
}

// 显示日志详情
function showDetail(log) {
  selectedLog.value = log
  detailDialogVisible.value = true
}

// 获取日志级别样式
function getLogLevelType(level) {
  const map = {
    error: 'danger',
    warn: 'warning',
    info: 'info',
    debug: ''
  }
  return map[level.toLowerCase()] || ''
}

onMounted(() => {
  loadLogs()
})
</script>

<style scoped>
.log-list {
  padding: 20px;
}
.header {
  margin-bottom: 20px;
}
.filters {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}
.log-detail {
  .detail-item {
    margin-bottom: 15px;
    .label {
      font-weight: bold;
      margin-right: 10px;
    }
    pre {
      margin: 10px 0;
      padding: 10px;
      background: #f5f7fa;
      border-radius: 4px;
    }
  }
}
</style> 