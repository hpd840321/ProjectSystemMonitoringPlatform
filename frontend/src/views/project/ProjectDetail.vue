<template>
  <div class="project-detail">
    <div class="header">
      <div class="title">
        <h2>{{ project?.name }}</h2>
        <el-tag :type="getStatusType(project?.status)">
          {{ getStatusText(project?.status) }}
        </el-tag>
      </div>
      <el-button type="primary" @click="showAddServerDialog">
        添加服务器
      </el-button>
    </div>

    <el-descriptions :column="3" border>
      <el-descriptions-item label="项目描述">
        {{ project?.description }}
      </el-descriptions-item>
      <el-descriptions-item label="服务器数量">
        {{ project?.server_count }}
      </el-descriptions-item>
      <el-descriptions-item label="创建时间">
        {{ formatDate(project?.created_at) }}
      </el-descriptions-item>
    </el-descriptions>

    <div class="server-list">
      <h3>服务器列表</h3>
      <el-table :data="servers" v-loading="loading">
        <el-table-column prop="name" label="服务器名称" />
        <el-table-column prop="host" label="主机地址" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getServerStatusType(row.status)">
              {{ getServerStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="资源使用">
          <template #default="{ row }">
            <div v-if="row.metrics">
              <el-progress
                :percentage="row.metrics.cpu_usage"
                :status="getUsageStatus(row.metrics.cpu_usage)"
              >
                CPU: {{ row.metrics.cpu_usage }}%
              </el-progress>
              <el-progress
                :percentage="row.metrics.memory_usage"
                :status="getUsageStatus(row.metrics.memory_usage)"
              >
                内存: {{ row.metrics.memory_usage }}%
              </el-progress>
              <el-progress
                :percentage="row.metrics.disk_usage"
                :status="getUsageStatus(row.metrics.disk_usage)"
              >
                磁盘: {{ row.metrics.disk_usage }}%
              </el-progress>
            </div>
            <span v-else>暂无数据</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="viewServerDetail(row)">
                详情
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="removeServer(row)"
              >
                移除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加服务器对话框 -->
    <el-dialog v-model="dialogVisible" title="添加服务器">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="服务器名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="主机地址" prop="host">
          <el-input v-model="form.host" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="form.description" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="addServer"
          :loading="submitting"
        >
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useProjectStore } from '@/stores/project'
import { formatDate } from '@/utils/date'

const route = useRoute()
const projectStore = useProjectStore()

const loading = ref(false)
const project = ref(null)
const servers = ref([])
const dialogVisible = ref(false)
const submitting = ref(false)

const form = ref({
  name: '',
  host: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入服务器名称', trigger: 'blur' }],
  host: [{ required: true, message: '请输入主机地址', trigger: 'blur' }],
  description: [{ required: true, message: '请输入描述', trigger: 'blur' }]
}

// 获取项目详情
const fetchProjectDetail = async () => {
  loading.value = true
  try {
    const projectId = route.params.id as string
    project.value = await projectStore.fetchProjectDetail(projectId)
    servers.value = await projectStore.fetchProjectServers(projectId)
  } catch (error) {
    ElMessage.error('获取项目详情失败')
  } finally {
    loading.value = false
  }
}

// 添加服务器
const addServer = async () => {
  submitting.value = true
  try {
    const projectId = route.params.id as string
    await projectStore.addServer(projectId, form.value)
    ElMessage.success('添加服务器成功')
    dialogVisible.value = false
    await fetchProjectDetail()
  } catch (error) {
    ElMessage.error('添加服务器失败')
  } finally {
    submitting.value = false
  }
}

// 移除服务器
const removeServer = async (server) => {
  try {
    await ElMessageBox.confirm('确定要移除该服务器吗？', '提示', {
      type: 'warning'
    })
    const projectId = route.params.id as string
    await projectStore.removeServer(projectId, server.id)
    ElMessage.success('移除服务器成功')
    await fetchProjectDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('移除服务器失败')
    }
  }
}

// 查看服务器详情
const viewServerDetail = (server) => {
  router.push(`/projects/${route.params.id}/servers/${server.id}`)
}

onMounted(() => {
  fetchProjectDetail()
})
</script>

<style scoped>
.project-detail {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.server-list {
  margin-top: 20px;
}
</style> 