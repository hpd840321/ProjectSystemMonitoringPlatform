<template>
  <div class="register">
    <div class="register-container">
      <h2>注册账号</h2>
      <a-form
        :model="formState"
        :rules="rules"
        @finish="onFinish"
        layout="vertical"
      >
        <a-form-item label="用户名" name="username">
          <a-input 
            v-model:value="formState.username"
            placeholder="请输入用户名"
          />
        </a-form-item>

        <a-form-item label="邮箱" name="email">
          <a-input 
            v-model:value="formState.email"
            placeholder="请输入邮箱"
          />
        </a-form-item>

        <a-form-item label="密码" name="password">
          <a-input-password
            v-model:value="formState.password"
            placeholder="请输入密码"
          />
        </a-form-item>

        <a-form-item label="确认密码" name="confirmPassword">
          <a-input-password
            v-model:value="formState.confirmPassword"
            placeholder="请再次输入密码"
          />
        </a-form-item>

        <a-form-item label="所属租户" name="tenantId">
          <a-select
            v-model:value="formState.tenantId"
            placeholder="请选择租户"
            :loading="tenantsLoading"
          >
            <a-select-option 
              v-for="tenant in tenants"
              :key="tenant.id"
              :value="tenant.id"
            >
              {{ tenant.name }}
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="验证码" name="captcha">
          <a-row :gutter="8">
            <a-col :span="16">
              <a-input
                v-model:value="formState.captcha"
                placeholder="请输入验证码"
              />
            </a-col>
            <a-col :span="8">
              <img 
                :src="captchaUrl"
                @click="refreshCaptcha"
                class="captcha-img"
                alt="验证码"
              />
            </a-col>
          </a-row>
        </a-form-item>

        <a-form-item>
          <a-button 
            type="primary" 
            html-type="submit" 
            :loading="loading"
            block
          >
            注册
          </a-button>
        </a-form-item>

        <div class="form-footer">
          已有账号? <router-link to="/login">立即登录</router-link>
        </div>
      </a-form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { useTenantStore } from '@/stores/tenant';
import { useUserStore } from '@/stores/user';
import type { Rule } from 'ant-design-vue/es/form';

export default defineComponent({
  name: 'Register',

  setup() {
    const router = useRouter();
    const tenantStore = useTenantStore();
    const userStore = useUserStore();

    const loading = ref(false);
    const tenantsLoading = ref(false);
    const tenants = ref([]);
    const captchaUrl = ref('');

    const formState = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      tenantId: undefined,
      captcha: ''
    });

    const rules: Record<string, Rule[]> = {
      username: [
        { required: true, message: '请输入用户名' },
        { min: 3, max: 20, message: '用户名长度为3-20个字符' },
        { pattern: /^[a-zA-Z0-9_-]+$/, message: '用户名只能包含字母、数字、下划线和中划线' }
      ],
      email: [
        { required: true, message: '请输入邮箱' },
        { type: 'email', message: '请输入正确的邮箱格式' }
      ],
      password: [
        { required: true, message: '请输入密码' },
        { min: 8, message: '密码长度不能小于8个字符' },
        { 
          pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/,
          message: '密码必须包含大小写字母和数字'
        }
      ],
      confirmPassword: [
        { required: true, message: '请再次输入密码' },
        {
          validator: async (_rule: Rule, value: string) => {
            if (value !== formState.password) {
              return Promise.reject('两次输入的密码不一致');
            }
            return Promise.resolve();
          }
        }
      ],
      tenantId: [
        { required: true, message: '请选择所属租户' }
      ],
      captcha: [
        { required: true, message: '请输入验证码' },
        { len: 6, message: '验证码长度为6位' }
      ]
    };

    const fetchTenants = async () => {
      tenantsLoading.value = true;
      try {
        tenants.value = await tenantStore.getTenants();
      } catch (error) {
        message.error('获取租户列表失败');
      } finally {
        tenantsLoading.value = false;
      }
    };

    const refreshCaptcha = () => {
      captchaUrl.value = `/api/v1/captcha?t=${Date.now()}`;
    };

    const onFinish = async (values: any) => {
      loading.value = true;
      try {
        await userStore.register({
          ...values,
          captcha: formState.captcha
        });
        message.success('注册成功，请登录');
        router.push('/login');
      } catch (error: any) {
        message.error(error.message || '注册失败');
        refreshCaptcha();
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchTenants();
      refreshCaptcha();
    });

    return {
      loading,
      tenantsLoading,
      tenants,
      captchaUrl,
      formState,
      rules,
      refreshCaptcha,
      onFinish
    };
  }
});
</script>

<style scoped>
.register {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f2f5;
}

.register-container {
  width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  color: rgba(0, 0, 0, 0.85);
}

.captcha-img {
  width: 100%;
  height: 32px;
  cursor: pointer;
}

.form-footer {
  text-align: center;
  margin-top: 16px;
}
</style> 