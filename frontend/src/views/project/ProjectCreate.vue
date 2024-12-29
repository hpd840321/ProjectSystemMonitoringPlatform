<template>
  <div class="project-create">
    <a-card title="创建项目">
      <a-form 
        :model="formState"
        :rules="rules"
        @finish="onFinish"
        layout="vertical"
      >
        <a-form-item label="项目名称" name="name">
          <a-input v-model:value="formState.name" placeholder="请输入项目名称" />
        </a-form-item>

        <a-form-item label="项目代码" name="code">
          <a-input v-model:value="formState.code" placeholder="请输入项目代码" />
        </a-form-item>

        <a-form-item label="项目描述" name="description">
          <a-textarea 
            v-model:value="formState.description"
            placeholder="请输入项目描述"
            :rows="4"
          />
        </a-form-item>

        <a-form-item label="所属租户" name="tenant_id" v-if="isSuperAdmin">
          <a-select
            v-model:value="formState.tenant_id"
            placeholder="请选择所属租户"
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

        <a-form-item>
          <a-space>
            <a-button type="primary" html-type="submit">创建</a-button>
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
import { useUserStore } from '@/stores/user';
import { useTenantStore } from '@/stores/tenant';
import type { Project } from '@/types/project';

export default defineComponent({
  name: 'ProjectCreate',
  
  setup() {
    const router = useRouter();
    const userStore = useUserStore();
    const tenantStore = useTenantStore();
    
    const formState = reactive<Partial<Project>>({
      name: '',
      code: '',
      description: '',
      tenant_id: undefined
    });

    const rules = {
      name: [
        { required: true, message: '请输入项目名称', trigger: 'blur' },
        { min: 3, max: 50, message: '长度应为3-50个字符', trigger: 'blur' }
      ],
      code: [
        { required: true, message: '请输入项目代码', trigger: 'blur' },
        { pattern: /^[a-z0-9-]+$/, message: '只能包含小写字母、数字和连字符', trigger: 'blur' }
      ],
      tenant_id: [
        { required: true, message: '请选择所属租户', trigger: 'change' }
      ]
    };

    const tenants = ref([]);
    const isSuperAdmin = computed(() => userStore.isSuperAdmin);

    onMounted(async () => {
      if (isSuperAdmin.value) {
        await tenantStore.fetchTenants();
        tenants.value = tenantStore.tenants;
      }
    });

    const onFinish = async (values: any) => {
      try {
        await projectStore.createProject(values);
        message.success('创建项目成功');
        router.push('/projects');
      } catch (error) {
        message.error('创建项目失败');
      }
    };

    const onCancel = () => {
      router.back();
    };

    return {
      formState,
      rules,
      tenants,
      isSuperAdmin,
      onFinish,
      onCancel
    };
  }
});
</script>

<style scoped>
.project-create {
  padding: 24px;
  background: #f0f2f5;
}
</style> 