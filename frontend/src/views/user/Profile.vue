<template>
  <div class="profile">
    <a-row :gutter="24">
      <a-col :span="8">
        <a-card>
          <template #cover>
            <div class="avatar-wrapper">
              <a-avatar :size="128" :src="userInfo.avatar">
                {{ userInfo.username?.charAt(0).toUpperCase() }}
              </a-avatar>
              <div class="avatar-upload">
                <a-upload
                  :customRequest="uploadAvatar"
                  :showUploadList="false"
                  accept="image/*"
                >
                  <a-button type="link">更换头像</a-button>
                </a-upload>
              </div>
            </div>
          </template>
          <template #title>{{ userInfo.username }}</template>
          <template #extra>
            <a-tag :color="getRoleColor(userInfo.role)">
              {{ getRoleText(userInfo.role) }}
            </a-tag>
          </template>
          <a-descriptions :column="1">
            <a-descriptions-item label="邮箱">
              {{ userInfo.email }}
            </a-descriptions-item>
            <a-descriptions-item label="手机">
              {{ userInfo.phone || '未设置' }}
            </a-descriptions-item>
            <a-descriptions-item label="创建时间">
              {{ formatDate(userInfo.created_at) }}
            </a-descriptions-item>
            <a-descriptions-item label="最后登录">
              {{ formatDate(userInfo.last_login) }}
            </a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>

      <a-col :span="16">
        <a-card>
          <a-tabs v-model:activeKey="activeTab">
            <a-tab-pane key="basic" tab="基本信息">
              <a-form
                :model="basicForm"
                :rules="basicRules"
                @finish="onBasicFinish"
                layout="vertical"
              >
                <a-form-item label="用户名" name="username">
                  <a-input v-model:value="basicForm.username" />
                </a-form-item>

                <a-form-item label="手机号" name="phone">
                  <a-input v-model:value="basicForm.phone" />
                </a-form-item>

                <a-form-item label="个人简介" name="bio">
                  <a-textarea
                    v-model:value="basicForm.bio"
                    :rows="4"
                    placeholder="请输入个人简介"
                  />
                </a-form-item>

                <a-form-item>
                  <a-button type="primary" html-type="submit">保存</a-button>
                </a-form-item>
              </a-form>
            </a-tab-pane>

            <a-tab-pane key="security" tab="安全设置">
              <a-form
                :model="securityForm"
                :rules="securityRules"
                @finish="onSecurityFinish"
                layout="vertical"
              >
                <a-form-item label="原密码" name="old_password">
                  <a-input-password v-model:value="securityForm.old_password" />
                </a-form-item>

                <a-form-item label="新密码" name="new_password">
                  <a-input-password v-model:value="securityForm.new_password" />
                </a-form-item>

                <a-form-item label="确认新密码" name="confirm_password">
                  <a-input-password v-model:value="securityForm.confirm_password" />
                </a-form-item>

                <a-form-item>
                  <a-button type="primary" html-type="submit">修改密码</a-button>
                </a-form-item>
              </a-form>
            </a-tab-pane>

            <a-tab-pane key="notification" tab="通知设置">
              <a-form
                :model="notificationForm"
                @finish="onNotificationFinish"
                layout="vertical"
              >
                <a-form-item label="系统通知">
                  <a-checkbox-group v-model:value="notificationForm.system_notify">
                    <a-checkbox value="email">邮件通知</a-checkbox>
                    <a-checkbox value="sms">短信通知</a-checkbox>
                    <a-checkbox value="web">站内通知</a-checkbox>
                  </a-checkbox-group>
                </a-form-item>

                <a-form-item label="告警通知">
                  <a-checkbox-group v-model:value="notificationForm.alert_notify">
                    <a-checkbox value="email">邮件通知</a-checkbox>
                    <a-checkbox value="sms">短信通知</a-checkbox>
                    <a-checkbox value="web">站内通知</a-checkbox>
                  </a-checkbox-group>
                </a-form-item>

                <a-form-item>
                  <a-button type="primary" html-type="submit">保存设置</a-button>
                </a-form-item>
              </a-form>
            </a-tab-pane>
          </a-tabs>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { useUserStore } from '@/stores/user';
import type { UploadProps } from 'ant-design-vue';
import { formatDate } from '@/utils/date';

export default defineComponent({
  name: 'Profile',

  setup() {
    const userStore = useUserStore();
    const activeTab = ref('basic');
    const userInfo = ref({});

    // 基本信息表单
    const basicForm = reactive({
      username: '',
      phone: '',
      bio: ''
    });

    const basicRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
      ],
      phone: [
        { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' }
      ]
    };

    // 安全设置表单
    const securityForm = reactive({
      old_password: '',
      new_password: '',
      confirm_password: ''
    });

    const validateConfirmPassword = async (_rule: any, value: string) => {
      if (value !== securityForm.new_password) {
        throw new Error('两次输入的密码不一致');
      }
    };

    const securityRules = {
      old_password: [
        { required: true, message: '请输入原密码', trigger: 'blur' }
      ],
      new_password: [
        { required: true, message: '请输入新密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
      ],
      confirm_password: [
        { required: true, message: '请确认新密码', trigger: 'blur' },
        { validator: validateConfirmPassword, trigger: 'blur' }
      ]
    };

    // 通知设置表单
    const notificationForm = reactive({
      system_notify: ['web'],
      alert_notify: ['web', 'email']
    });

    onMounted(async () => {
      await loadUserInfo();
    });

    const loadUserInfo = async () => {
      try {
        const info = await userStore.getUserInfo();
        userInfo.value = info;
        Object.assign(basicForm, {
          username: info.username,
          phone: info.phone,
          bio: info.bio
        });
        Object.assign(notificationForm, info.notification_settings);
      } catch (error) {
        message.error('获取用户信息失败');
      }
    };

    const uploadAvatar: UploadProps['customRequest'] = async (options) => {
      try {
        const result = await userStore.uploadAvatar(options.file);
        userInfo.value.avatar = result.url;
        message.success('上传成功');
      } catch (error) {
        message.error('上传失败');
      }
    };

    const getRoleColor = (role: string) => {
      const colors = {
        admin: 'red',
        manager: 'blue',
        user: 'green'
      };
      return colors[role] || 'default';
    };

    const getRoleText = (role: string) => {
      const texts = {
        admin: '管理员',
        manager: '项目经理',
        user: '普通用户'
      };
      return texts[role] || role;
    };

    const onBasicFinish = async (values: any) => {
      try {
        await userStore.updateUserInfo(values);
        message.success('保存成功');
        await loadUserInfo();
      } catch (error) {
        message.error('保存失败');
      }
    };

    const onSecurityFinish = async (values: any) => {
      try {
        await userStore.changePassword(values);
        message.success('密码修改成功');
        securityForm.old_password = '';
        securityForm.new_password = '';
        securityForm.confirm_password = '';
      } catch (error) {
        message.error('密码修改失败');
      }
    };

    const onNotificationFinish = async (values: any) => {
      try {
        await userStore.updateNotificationSettings(values);
        message.success('设置保存成功');
      } catch (error) {
        message.error('设置保存失败');
      }
    };

    return {
      activeTab,
      userInfo,
      basicForm,
      basicRules,
      securityForm,
      securityRules,
      notificationForm,
      formatDate,
      uploadAvatar,
      getRoleColor,
      getRoleText,
      onBasicFinish,
      onSecurityFinish,
      onNotificationFinish
    };
  }
});
</script>

<style scoped>
.profile {
  padding: 24px;
  background: #f0f2f5;
}

.avatar-wrapper {
  padding: 24px;
  text-align: center;
  background: #fafafa;
}

.avatar-upload {
  margin-top: 8px;
}
</style> 