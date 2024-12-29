<template>
  <div class="tenant-list">
    <a-card>
      <template #title>
        <a-space>
          <span>租户管理</span>
          <a-button
            v-if="hasPermission('tenant:create')"
            type="primary"
            @click="onCreate"
          >
            创建租户
          </a-button>
        </a-space>
      </template>

      <a-table
        :columns="columns"
        :data-source="tenants"
        :loading="loading"
        :pagination="pagination"
        @change="onTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)">
              {{ getStatusText(record.status) }}
            </a-tag>
          </template>

          <template v-if="column.key === 'resource_usage'">
            <a-progress
              :percent="getResourceUsagePercent(record)"
              :status="getResourceUsageStatus(record)"
            />
          </template>

          <template v-if="column.key === 'action'">
            <a-space>
              <a-button
                v-if="hasPermission('tenant:edit')"
                type="link"
                @click="onEdit(record)"
              >
                编辑
              </a-button>
              <a-button
                v-if="hasPermission('tenant:delete')"
                type="link"
                danger
                @click="onDelete(record)"
              >
                删除
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <tenant-create-modal
      v-model:visible="createModalVisible"
      @success="onCreateSuccess"
    />

    <tenant-edit-modal
      v-model:visible="editModalVisible"
      :tenant="selectedTenant"
      @success="onEditSuccess"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { useTenantStore } from '@/stores/tenant';
import { usePermissionStore } from '@/stores/permission';
import type { Tenant } from '@/types/tenant';
import TenantCreateModal from './components/TenantCreateModal.vue';
import TenantEditModal from './components/TenantEditModal.vue';

export default defineComponent({
  name: 'TenantList',

  components: {
    TenantCreateModal,
    TenantEditModal
  },

  setup() {
    const router = useRouter();
    const tenantStore = useTenantStore();
    const permissionStore = usePermissionStore();

    const loading = ref(false);
    const tenants = ref<Tenant[]>([]);
    const pagination = ref({
      current: 1,
      pageSize: 10,
      total: 0
    });

    const createModalVisible = ref(false);
    const editModalVisible = ref(false);
    const selectedTenant = ref<Tenant | null>(null);

    const columns = [
      {
        title: '租户名称',
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: '租户代码',
        dataIndex: 'code',
        key: 'code'
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status'
      },
      {
        title: '资源使用',
        key: 'resource_usage'
      },
      {
        title: '创建时间',
        dataIndex: 'created_at',
        key: 'created_at'
      },
      {
        title: '操作',
        key: 'action'
      }
    ];

    const fetchTenants = async () => {
      loading.value = true;
      try {
        const { items, total } = await tenantStore.fetchTenants({
          page: pagination.value.current,
          pageSize: pagination.value.pageSize
        });
        tenants.value = items;
        pagination.value.total = total;
      } catch (error) {
        message.error('获取租户列表失败');
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchTenants();
    });

    const hasPermission = (permission: string) => {
      return permissionStore.hasPermission(permission);
    };

    const getStatusColor = (status: string) => {
      const colors = {
        active: 'success',
        suspended: 'warning',
        deleted: 'error'
      };
      return colors[status] || 'default';
    };

    const getStatusText = (status: string) => {
      const texts = {
        active: '正常',
        suspended: '已暂停',
        deleted: '已删除'
      };
      return texts[status] || status;
    };

    const getResourceUsagePercent = (tenant: Tenant) => {
      const { users_percent, projects_percent, servers_percent } = tenant.resource_usage;
      return Math.max(users_percent, projects_percent, servers_percent);
    };

    const getResourceUsageStatus = (tenant: Tenant) => {
      const percent = getResourceUsagePercent(tenant);
      if (percent >= 90) return 'exception';
      if (percent >= 70) return 'warning';
      return 'normal';
    };

    const onTableChange = (pagination: any) => {
      pagination.value = pagination;
      fetchTenants();
    };

    const onCreate = () => {
      createModalVisible.value = true;
    };

    const onEdit = (tenant: Tenant) => {
      selectedTenant.value = tenant;
      editModalVisible.value = true;
    };

    const onDelete = async (tenant: Tenant) => {
      try {
        await tenantStore.deleteTenant(tenant.id);
        message.success('删除租户成功');
        fetchTenants();
      } catch (error) {
        message.error('删除租户失败');
      }
    };

    const onCreateSuccess = () => {
      createModalVisible.value = false;
      fetchTenants();
    };

    const onEditSuccess = () => {
      editModalVisible.value = false;
      fetchTenants();
    };

    return {
      loading,
      tenants,
      pagination,
      columns,
      createModalVisible,
      editModalVisible,
      selectedTenant,
      hasPermission,
      getStatusColor,
      getStatusText,
      getResourceUsagePercent,
      getResourceUsageStatus,
      onTableChange,
      onCreate,
      onEdit,
      onDelete,
      onCreateSuccess,
      onEditSuccess
    };
  }
});
</script>

<style scoped>
.tenant-list {
  padding: 24px;
  background: #f0f2f5;
}
</style> 