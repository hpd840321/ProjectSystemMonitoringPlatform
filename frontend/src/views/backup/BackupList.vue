<template>
  <div class="backup-list">
    <div class="header">
      <h2>系统备份</h2>
      <el-button type="primary" @click="createBackup">创建备份</el-button>
    </div>
    
    <el-table :data="backups" v-loading="loading">
      <el-table-column prop="filename" label="备份文件" />
      <el-table-column prop="created_at" label="创建时间">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="size" label="大小">
        <template #default="{ row }">
          {{ formatSize(row.size) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button 
            type="warning"
            size="small"
            @click="restoreBackup(row)"
            :disabled="row.status !== 'success'"
          >
            恢复
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="deleteBackup(row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-pagination
      v-model:current-page="page"
      v-model:page-size="pageSize"
      :total="total"
      @current-change="loadBackups"
    />
    
    <el-dialog
      v-model="restoreDialogVisible"
      title="恢复备份"
      width="30%"
    >
      <p>确定要恢复此备份吗？这将覆盖当前系统数据。</p>
      <template #footer>
        <el-button @click="restoreDialogVisible = false">取消</el-button>
        <el-button type="warning" @click="confirmRestore">确定恢复</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useBackupStore } from '@/stores/backup'
import { formatDate, formatSize } from '@/utils/format'

const backupStore = useBackupStore()
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const backups = ref([])
const restoreDialogVisible = ref(false)
const selectedBackup = ref(null)

// 加载备份列表
async function loadBackups() {
  loading.value = true
  try {
    const result = await backupStore.listBackups({
      page: page.value,
      pageSize: pageSize.value
    })
    backups.value = result.items
    total.value = result.total
  } catch (error) {
    ElMessage.error('加载备份列表失败')
  }
  loading.value = false
}

// 创建备份
async function createBackup() {
  try {
    await backupStore.createBackup()
    ElMessage.success('创建备份成功')
    loadBackups()
  } catch (error) {
    ElMessage.error('创建备份失败')
  }
}

// 恢复备份
function restoreBackup(backup) {
  selectedBackup.value = backup
  restoreDialogVisible.value = true
}

// 确认恢复
async function confirmRestore() {
  try {
    await backupStore.restoreBackup(selectedBackup.value.id)
    ElMessage.success('恢复备份成功')
    restoreDialogVisible.value = false
  } catch (error) {
    ElMessage.error('恢复备份失败')
  }
}

// 删除备份
async function deleteBackup(backup) {
  try {
    await ElMessageBox.confirm('确定要删除此备份吗？')
    await backupStore.deleteBackup(backup.id)
    ElMessage.success('删除备份成功')
    loadBackups()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除备份失败')
    }
  }
}

// 获取状态样式
function getStatusType(status) {
  const map = {
    pending: 'info',
    success: 'success',
    failed: 'danger'
  }
  return map[status] || 'info'
}

onMounted(() => {
  loadBackups()
})
</script>

<style scoped>
.backup-list {
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 