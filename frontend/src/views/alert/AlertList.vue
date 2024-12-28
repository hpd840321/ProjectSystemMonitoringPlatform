<template>
  <div class="alert-list">
    <div class="header">
      <h2>告警管理</h2>
      <el-button type="primary" @click="createRule">添加规则</el-button>
    </div>
    
    <!-- 告警规则列表 -->
    <el-tabs v-model="activeTab">
      <el-tab-pane label="告警规则" name="rules">
        <el-table :data="rules" v-loading="loading">
          <el-table-column prop="name" label="规则名称" />
          <el-table-column prop="metric" label="监控指标" />
          <el-table-column prop="condition" label="触发条件" />
          <el-table-column prop="threshold" label="阈值" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-switch
                v-model="row.enabled"
                @change="toggleRule(row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="editRule(row)">
                编辑
              </el-button>
              <el-button type="danger" size="small" @click="deleteRule(row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <!-- 告警历史 -->
      <el-tab-pane label="告警历史" name="history">
        <el-table :data="alerts" v-loading="loading">
          <el-table-column prop="created_at" label="触发时间">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="rule.name" label="规则名称" />
          <el-table-column prop="target" label="告警对象" />
          <el-table-column prop="message" label="告警内容" />
          <el-table-column prop="level" label="级别">
            <template #default="{ row }">
              <el-tag :type="getAlertLevelType(row.level)">
                {{ row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="getAlertStatusType(row.status)">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
        
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          @current-change="loadAlerts"
        />
      </el-tab-pane>
    </el-tabs>
    
    <!-- 规则表单对话框 -->
    <el-dialog
      v-model="ruleDialogVisible"
      :title="editingRule ? '编辑规则' : '添加规则'"
    >
      <el-form :model="ruleForm" label-width="100px">
        <el-form-item label="规则名称" prop="name">
          <el-input v-model="ruleForm.name" />
        </el-form-item>
        <el-form-item label="监控指标" prop="metric">
          <el-select v-model="ruleForm.metric">
            <el-option label="CPU使用率" value="cpu_usage" />
            <el-option label="内存使用率" value="memory_usage" />
            <el-option label="磁盘使用率" value="disk_usage" />
          </el-select>
        </el-form-item>
        <el-form-item label="触发条件" prop="condition">
          <el-select v-model="ruleForm.condition">
            <el-option label="大于" value=">" />
            <el-option label="小于" value="<" />
          </el-select>
        </el-form-item>
        <el-form-item label="阈值" prop="threshold">
          <el-input-number v-model="ruleForm.threshold" />
        </el-form-item>
        <el-form-item label="通知方式">
          <el-checkbox-group v-model="ruleForm.notifications">
            <el-checkbox label="email">邮件</el-checkbox>
            <el-checkbox label="webhook">Webhook</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="ruleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRule">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAlertStore } from '@/stores/alert'
import { formatDate } from '@/utils/format'

const alertStore = useAlertStore()
const loading = ref(false)
const activeTab = ref('rules')
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const rules = ref([])
const alerts = ref([])

// 规则表单
const ruleDialogVisible = ref(false)
const editingRule = ref(null)
const ruleForm = ref({
  name: '',
  metric: '',
  condition: '',
  threshold: 0,
  notifications: []
})

// 加载告警规则
async function loadRules() {
  loading.value = true
  try {
    rules.value = await alertStore.listRules()
  } catch (error) {
    ElMessage.error('加载告警规则失败')
  }
  loading.value = false
}

// 加载告警历史
async function loadAlerts() {
  loading.value = true
  try {
    const result = await alertStore.listAlerts({
      page: page.value,
      pageSize: pageSize.value
    })
    alerts.value = result.items
    total.value = result.total
  } catch (error) {
    ElMessage.error('加载告警历史失败')
  }
  loading.value = false
}

// 创建规则
function createRule() {
  editingRule.value = null
  ruleForm.value = {
    name: '',
    metric: '',
    condition: '',
    threshold: 0,
    notifications: []
  }
  ruleDialogVisible.value = true
}

// 编辑规则
function editRule(rule) {
  editingRule.value = rule
  ruleForm.value = { ...rule }
  ruleDialogVisible.value = true
}

// 保存规则
async function saveRule() {
  try {
    if (editingRule.value) {
      await alertStore.updateRule(editingRule.value.id, ruleForm.value)
      ElMessage.success('更新规则成功')
    } else {
      await alertStore.createRule(ruleForm.value)
      ElMessage.success('创建规则成功')
    }
    ruleDialogVisible.value = false
    loadRules()
  } catch (error) {
    ElMessage.error('保存规则失败')
  }
}

// 删除规则
async function deleteRule(rule) {
  try {
    await alertStore.deleteRule(rule.id)
    ElMessage.success('删除规则成功')
    loadRules()
  } catch (error) {
    ElMessage.error('删除规则失败')
  }
}

// 启用/禁用规则
async function toggleRule(rule) {
  try {
    await alertStore.updateRule(rule.id, {
      enabled: rule.enabled
    })
    ElMessage.success(rule.enabled ? '启用规则成功' : '禁用规则成功')
  } catch (error) {
    rule.enabled = !rule.enabled
    ElMessage.error('操作失败')
  }
}

// 获取告警级别样式
function getAlertLevelType(level) {
  const map = {
    critical: 'danger',
    warning: 'warning',
    info: 'info'
  }
  return map[level] || 'info'
}

// 获取告警状态样式
function getAlertStatusType(status) {
  const map = {
    active: 'danger',
    resolved: 'success'
  }
  return map[status] || 'info'
}

onMounted(() => {
  loadRules()
  loadAlerts()
})
</script>

<style scoped>
.alert-list {
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 