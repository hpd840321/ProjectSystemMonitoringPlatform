<template>
  <div class="system-settings">
    <a-card title="系统设置">
      <a-tabs v-model:activeKey="activeTab">
        <a-tab-pane key="basic" tab="基本设置">
          <a-form
            :model="basicSettings"
            :rules="basicRules"
            @finish="onBasicFinish"
            layout="vertical"
          >
            <a-form-item label="系统名称" name="system_name">
              <a-input v-model:value="basicSettings.system_name" />
            </a-form-item>

            <a-form-item label="系统Logo" name="system_logo">
              <a-upload
                v-model:fileList="logoFileList"
                :customRequest="uploadLogo"
                :showUploadList="false"
              >
                <div class="logo-uploader">
                  <img v-if="basicSettings.system_logo" :src="basicSettings.system_logo" class="logo-image" />
                  <div v-else class="logo-placeholder">
                    <upload-outlined />
                    <div>点击上传</div>
                  </div>
    </div>
              </a-upload>
            </a-form-item>

            <a-form-item label="系统描述" name="system_description">
              <a-textarea v-model:value="basicSettings.system_description" :rows="4" />
            </a-form-item>

            <a-form-item>
              <a-button type="primary" html-type="submit">保存设置</a-button>
            </a-form-item>
          </a-form>
        </a-tab-pane>

        <a-tab-pane key="email" tab="邮件设置">
          <a-form
            :model="emailSettings"
            :rules="emailRules"
            @finish="onEmailFinish"
            layout="vertical"
          >
            <a-form-item label="SMTP服务器" name="smtp_host">
              <a-input v-model:value="emailSettings.smtp_host" />
            </a-form-item>

            <a-form-item label="SMTP端口" name="smtp_port">
              <a-input-number v-model:value="emailSettings.smtp_port" />
            </a-form-item>

            <a-form-item label="发件人邮箱" name="smtp_user">
              <a-input v-model:value="emailSettings.smtp_user" />
            </a-form-item>

            <a-form-item label="邮箱密码" name="smtp_password">
              <a-input-password v-model:value="emailSettings.smtp_password" />
            </a-form-item>

            <a-form-item label="SSL加密" name="smtp_ssl">
              <a-switch v-model:checked="emailSettings.smtp_ssl" />
            </a-form-item>

            <a-form-item>
              <a-space>
                <a-button type="primary" html-type="submit">保存设置</a-button>
                <a-button @click="onTestEmail">测试邮件</a-button>
              </a-space>
            </a-form-item>
          </a-form>
        </a-tab-pane>

        <a-tab-pane key="backup" tab="备份设置">
          <a-form
            :model="backupSettings"
            :rules="backupRules"
            @finish="onBackupFinish"
            layout="vertical"
          >
            <a-form-item label="自动备份" name="auto_backup">
              <a-switch v-model:checked="backupSettings.auto_backup" />
            </a-form-item>

            <a-form-item label="备份周期" name="backup_cycle">
              <a-select v-model:value="backupSettings.backup_cycle">
                <a-select-option value="daily">每天</a-select-option>
                <a-select-option value="weekly">每周</a-select-option>
                <a-select-option value="monthly">每月</a-select-option>
              </a-select>
            </a-form-item>

            <a-form-item label="备份时间" name="backup_time">
              <a-time-picker v-model:value="backupSettings.backup_time" format="HH:mm" />
            </a-form-item>

            <a-form-item label="保留天数" name="retention_days">
              <a-input-number v-model:value="backupSettings.retention_days" :min="1" />
            </a-form-item>

            <a-form-item>
              <a-button type="primary" html-type="submit">保存设置</a-button>
            </a-form-item>
          </a-form>
        </a-tab-pane>

        <a-tab-pane key="security" tab="安全设置">
          <a-form
            :model="securitySettings"
            :rules="securityRules"
            @finish="onSecurityFinish"
            layout="vertical"
          >
            <a-form-item label="密码策略" name="password_policy">
              <a-checkbox-group v-model:value="securitySettings.password_policy">
                <a-checkbox value="uppercase">必须包含大写字母</a-checkbox>
                <a-checkbox value="lowercase">必须包含小写字母</a-checkbox>
                <a-checkbox value="numbers">必须包含数字</a-checkbox>
                <a-checkbox value="special">必须包含特殊字符</a-checkbox>
              </a-checkbox-group>
            </a-form-item>

            <a-form-item label="最小密码长度" name="min_password_length">
              <a-input-number v-model:value="securitySettings.min_password_length" :min="6" />
            </a-form-item>

            <a-form-item label="密码有效期(天)" name="password_expiry_days">
              <a-input-number v-model:value="securitySettings.password_expiry_days" :min="0" />
            </a-form-item>

            <a-form-item label="登录失败锁定" name="login_lock">
              <a-input-group compact>
                <a-input-number
                  v-model:value="securitySettings.max_login_attempts"
                  :min="1"
                  style="width: 100px"
                  placeholder="尝试次数"
                />
                <a-input-number
                  v-model:value="securitySettings.lock_duration"
                  :min="1"
                  style="width: 100px"
                  placeholder="锁定时间(分钟)"
                />
              </a-input-group>
            </a-form-item>

            <a-form-item>
              <a-button type="primary" html-type="submit">保存设置</a-button>
            </a-form-item>
          </a-form>
        </a-tab-pane>
      </a-tabs>
    </a-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { UploadOutlined } from '@ant-design/icons-vue';
import { useSettingsStore } from '@/stores/settings';
import type { UploadProps } from 'ant-design-vue';

export default defineComponent({
  name: 'SystemSettings',

  components: {
    UploadOutlined
  },

  setup() {
    const settingsStore = useSettingsStore();
    const activeTab = ref('basic');
    const logoFileList = ref([]);

    // 基本设置
    const basicSettings = reactive({
      system_name: '',
      system_logo: '',
      system_description: ''
    });

    const basicRules = {
      system_name: [{ required: true, message: '请输入系统名称' }]
    };

    // 邮件设置
    const emailSettings = reactive({
      smtp_host: '',
      smtp_port: 465,
      smtp_user: '',
      smtp_password: '',
      smtp_ssl: true
    });

    const emailRules = {
      smtp_host: [{ required: true, message: '请输入SMTP服务器' }],
      smtp_port: [{ required: true, message: '请输入SMTP端口' }],
      smtp_user: [{ required: true, message: '请输入发件人邮箱' }]
    };

    // 备份设置
    const backupSettings = reactive({
      auto_backup: false,
      backup_cycle: 'daily',
      backup_time: null,
      retention_days: 7
    });

    const backupRules = {
      backup_time: [{ required: true, message: '请选择备份时间' }],
      retention_days: [{ required: true, message: '请输入保留天数' }]
    };

    // 安全设置
    const securitySettings = reactive({
      password_policy: ['lowercase', 'numbers'],
      min_password_length: 8,
      password_expiry_days: 90,
      max_login_attempts: 5,
      lock_duration: 30
    });

    const securityRules = {
      min_password_length: [{ required: true, message: '请输入最小密码长度' }]
    };

    onMounted(async () => {
      await loadSettings();
    });

    const loadSettings = async () => {
      try {
        const settings = await settingsStore.getSettings();
        Object.assign(basicSettings, settings.basic);
        Object.assign(emailSettings, settings.email);
        Object.assign(backupSettings, settings.backup);
        Object.assign(securitySettings, settings.security);
      } catch (error) {
        message.error('加载设置失败');
      }
    };

    const uploadLogo: UploadProps['customRequest'] = async (options) => {
      try {
        const result = await settingsStore.uploadLogo(options.file);
        basicSettings.system_logo = result.url;
        message.success('上传成功');
      } catch (error) {
        message.error('上传失败');
      }
    };

    const onBasicFinish = async (values: any) => {
      try {
        await settingsStore.updateSettings('basic', values);
        message.success('保存成功');
      } catch (error) {
        message.error('保存失败');
      }
    };

    const onEmailFinish = async (values: any) => {
      try {
        await settingsStore.updateSettings('email', values);
        message.success('保存成功');
  } catch (error) {
        message.error('保存失败');
      }
    };

    const onBackupFinish = async (values: any) => {
      try {
        await settingsStore.updateSettings('backup', values);
        message.success('保存成功');
      } catch (error) {
        message.error('保存失败');
      }
    };

    const onSecurityFinish = async (values: any) => {
      try {
        await settingsStore.updateSettings('security', values);
        message.success('保存成功');
  } catch (error) {
        message.error('保存失败');
      }
    };

    const onTestEmail = async () => {
      try {
        await settingsStore.testEmail(emailSettings);
        message.success('测试邮件发送成功');
      } catch (error) {
        message.error('测试邮件发送失败');
      }
    };

    return {
      activeTab,
      logoFileList,
      basicSettings,
      basicRules,
      emailSettings,
      emailRules,
      backupSettings,
      backupRules,
      securitySettings,
      securityRules,
      uploadLogo,
      onBasicFinish,
      onEmailFinish,
      onBackupFinish,
      onSecurityFinish,
      onTestEmail
    };
  }
});
</script>

<style scoped>
.system-settings {
  padding: 24px;
  background: #f0f2f5;
}

.logo-uploader {
  width: 128px;
  height: 128px;
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.logo-placeholder {
  text-align: center;
  color: #999;
}
</style> 