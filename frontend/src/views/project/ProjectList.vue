<template>
  <div class="project-list">
    <div class="header">
      <h2>项目列表</h2>
      <el-button type="primary" @click="showCreateDialog">
        创建项目
      </el-button>
    </div>

    <el-table :data="projects" v-loading="loading">
      <el-table-column prop="name" label="项目名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="server_count" label="服务器数量" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" @click="viewProject(row)">查看</el-button>
            <el-button size="small" type="danger" @click="deleteProject(row)">
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建项目对话框 -->
    <el-dialog v-model="dialogVisible" title="创建项目">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input type="textarea" v-model="form.description" />
        </el-form-item>
        <el-form-item label="最大服务器数" prop="max_servers">
          <el-input-number v-model="form.max_servers" :min="1" :max="100" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createProject" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useProjectStore } from '@/stores/project'

const router = useRouter()
const projectStore = useProjectStore()

const loading = ref(false)
const projects = ref([])
const dialogVisible = ref(false)
const submitting = ref(false)

const form = ref({
  name: '',
  description: '',
  max_servers: 10
})

const rules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入项目描述', trigger: 'blur' }]
}

// 获取项目列表
const fetchProjects = async () => {
  loading.value = true
  try {
    projects.value = await projectStore.fetchProjects()
  } catch (error) {
    ElMessage.error('获取项目列表失败')
  } finally {
    loading.value = false
  }
}

// 创建项目
const createProject = async () => {
  submitting.value = true
  try {
    await projectStore.createProject(form.value)
    ElMessage.success('创建项目成功')
    dialogVisible.value = false
    await fetchProjects()
  } catch (error) {
    ElMessage.error('创建项目失败')
  } finally {
    submitting.value = false
  }
}

// 删除项目
const deleteProject = async (project) => {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', {
      type: 'warning'
    })
    await projectStore.deleteProject(project.id)
    ElMessage.success('删除项目成功')
    await fetchProjects()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除项目失败')
    }
  }
}

// 查看项目详情
const viewProject = (project) => {
  router.push(`/projects/${project.id}`)
}

// 获取状态样式
const getStatusType = (status: string) => {
  const map = {
    active: 'success',
    maintaining: 'warning',
    suspended: 'info',
    archived: 'danger'
  }
  return map[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const map = {
    active: '运行中',
    maintaining: '维护中',
    suspended: '已暂停',
    archived: '已归档'
  }
  return map[status] || status
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.project-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 