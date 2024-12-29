<template>
  <div class="server-create">
    <a-card title="添加服务器">
      <a-form
        :model="formState"
        :rules="rules"
        @finish="onFinish"
        layout="vertical"
      >
        <a-form-item label="服务器名称" name="name">
          <a-input v-model:value="formState.name" placeholder="请输入服务器名称" />
        </a-form-item>

        <a-form-item label="主机地址" name="host">
          <a-input v-model:value="formState.host" placeholder="请输入IP地址或域名" />
        </a-form-item>

        <a-form-item label="SSH端口" name="port">
          <a-input-number
            v-model:value="formState.port"
            :min="1"
            :max="65535"
            placeholder="SSH端口"
          />
        </a-form-item>

        <a-form-item label="认证方式" name="auth_type">
          <a-radio-group v-model:value="formState.auth_type">
            <a-radio value="password">密码认证</a-radio>
            <a-radio value="key">密钥认证</a-radio>
          </a-radio-group>
        </a-form-item>

        <template v-if="formState.auth_type === 'password'">
          <a-form-item label="用户名" name="username">
            <a-input v-model:value="formState.username" placeholder="请输入用户名" />
          </a-form-item>

          <a-form-item label="密码" name="password">
            <a-input-password
              v-model:value="formState.password"
              placeholder="请输入密码"
            />
          </a-form-item>
        </template>

        <template v-else>
          <a-form-item label="用户名" name="username">
            <a-input v-model:value="formState.username" placeholder="请输入用户名" />
          </a-form-item>

          <a-form-item label="私钥" name="private_key">
            <a-textarea
              v-model:value="formState.private_key"
              placeholder="请输入私钥内容"
              :rows="6"
            />
          </a-form-item>

          <a-form-item label="私钥密码" name="key_password">
            <a-input-password
              v-model:value="formState.key_password"
              placeholder="如果私钥有密码保护，请输入密码"
            />
          </a-form-item>
        </template>

        <a-form-item label="所属项目" name="project_id">
          <a-select
            v-model:value="formState.project_id"
            placeholder="请选择所属项目"
          >
            <a-select-option
              v-for="project in projects"
              :key="project.id"
              :value="project.id"
            >
              {{ project.name }}
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="标签" name="tags">
          <a-select
            v-model:value="formState.tags"
            mode="tags"
            placeholder="请输入标签"
            :token-separators="[',']"
          />
        </a-form-item>

        <a-form-item>
          <a-space>
            <a-button type="primary" html-type="submit">添加</a-button>
            <a-button @click="onTest">测试连接</a-button>
            <a-button @click="onCancel">取消</a-button>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { useProjectStore } from '@/stores/project';
import { useServerStore } from '@/stores/server';
import type { Server } from '@/types/server';

export default defineComponent({
  name: 'ServerCreate',

  setup() {
    const router = useRouter();
    const projectStore = useProjectStore();
    const serverStore = useServerStore();

    const formState = reactive<Partial<Server>>({
      name: '',
      host: '',
      port: 22,
      auth_type: 'password',
      username: '',
      password: '',
      private_key: '',
      key_password: '',
      project_id: undefined,
      tags: []
    });

    const rules = {
      name: [
        { required: true, message: '请输入服务器名称', trigger: 'blur' }
      ],
      host: [
        { required: true, message: '请输入主机地址', trigger: 'blur' }
      ],
      port: [
        { required: true, message: '请输入SSH端口', trigger: 'blur' }
      ],
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ],
      project_id: [
        { required: true, message: '请选择所属项目', trigger: 'change' }
      ]
    };

    const projects = ref([]);

    onMounted(async () => {
      await projectStore.fetchProjects();
      projects.value = projectStore.projects;
    });

    const onFinish = async (values: any) => {
      try {
        await serverStore.createServer(values);
        message.success('添加服务器成功');
        router.push('/servers');
      } catch (error) {
        message.error('添加服务器失败');
      }
    };

    const onTest = async () => {
      try {
        await serverStore.testConnection(formState);
        message.success('连接测试成功');
      } catch (error) {
        message.error('连接测试失败');
      }
    };

    const onCancel = () => {
      router.back();
    };

    return {
      formState,
      rules,
      projects,
      onFinish,
      onTest,
      onCancel
    };
  }
});
</script>

<style scoped>
.server-create {
  padding: 24px;
  background: #f0f2f5;
}
</style> 