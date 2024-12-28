<template>
  <div class="settings">
    <div class="header">
      <h2>系统设置</h2>
    </div>
    
    <el-tabs v-model="activeTab">
      <!-- 基础设置 -->
      <el-tab-pane label="基础设置" name="basic">
        <el-form :model="basicForm" label-width="120px">
          <el-form-item label="系统名称">
            <el-input v-model="basicForm.systemName" />
          </el-form-item>
          <el-form-item label="管理员邮箱">
            <el-input v-model="basicForm.adminEmail" />
          </el-form-item>
          <el-form-item label="数据保留天数">
            <el-input-number v-model="basicForm.dataRetentionDays" :min="1" :max="365" />
          </el-form-item>
        </el-form>
      </el-tab-pane>
      
      <!-- 通知设置 -->
      <el-tab-pane label="通知设置" name="notification">
        <el-form :model="notificationForm" label-width="120px">
          <el-form-item label="SMTP服务器">
            <el-input v-model="notificationForm.smtpHost" />
          </el-form-item>
          <el-form-item label="SMTP端口">
            <el-input-number v-model="notificationForm.smtpPort" />
          </el-form-item>
          <el-form-item label="SMTP用户名">
            <el-input v-model="notificationForm.smtpUsername" />
          </el-form-item>
          <el-form-item label="SMTP密码">
            <el-input v-model="notificationForm.smtpPassword" type="password" />
          </el-form-item>
          <el-form-item label="发件人">
            <el-input v-model="notificationForm.emailFrom" />
          </el-form-item>
          <el-divider />
          <el-form-item label="Webhook URL">
            <el-input v-model="notificationForm.webhookUrl" />
          </el-form-item>
        </el-form>
      </el-tab-pane>
      
      <!-- 存储设置 -->
      <el-tab-pane label="存储设置" name="storage">
        <el-form :model="storageForm" label-width="120px">
          <el-form-item label="存储类型">
            <el-select v-model="storageForm.type">
              <el-option label="本地存储" value="local" />
              <el-option label="S3存储" value="s3" />
            </el-select>
          </el-form-item>
          
          <template v-if="storageForm.type === 's3'">
            <el-form-item label="S3 Endpoint">
              <el-input v-model="storageForm.s3Endpoint" />
            </el-form-item>
            <el-form-item label="Access Key">
              <el-input v-model="storageForm.s3AccessKey" />
            </el-form-item>
            <el-form-item label="Secret Key">
              <el-input v-model="storageForm.s3SecretKey" type="password" />
            </el-form-item>
            <el-form-item label="Bucket">
              <el-input v-model="storageForm.s3Bucket" />
            </el-form-item>
          </template>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    
    <div class="actions">
      <el-button type="primary" @click="saveSettings">保存设置</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()
const activeTab = ref('basic')

// 表单数据
const basicForm = ref({
  systemName: '',
  adminEmail: '',
  dataRetentionDays: 30
})

const notificationForm = ref({
  smtpHost: '',
  smtpPort: 587,
  smtpUsername: '',
  smtpPassword: '',
  emailFrom: '',
  webhookUrl: ''
})

const storageForm = ref({
  type: 'local',
  s3Endpoint: '',
  s3AccessKey: '',
  s3SecretKey: '',
  s3Bucket: ''
})

// 加载设置
async function loadSettings() {
  try {
    const settings = await settingsStore.getSettings()
    basicForm.value = { ...settings.basic }
    notificationForm.value = { ...settings.notification }
    storageForm.value = { ...settings.storage }
  } catch (error) {
    ElMessage.error('加载设置失败')
  }
}

// 保存设置
async function saveSettings() {
  try {
    await settingsStore.updateSettings({
      basic: basicForm.value,
      notification: notificationForm.value,
      storage: storageForm.value
    })
    ElMessage.success('保存设置成功')
  } catch (error) {
    ElMessage.error('保存设置失败')
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.settings {
  padding: 20px;
}
.header {
  margin-bottom: 20px;
}
.actions {
  margin-top: 20px;
  text-align: right;
}
</style> 