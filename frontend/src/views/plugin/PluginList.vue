<template>
  <div class="plugin-list">
    <a-card>
      <template #title>
        <a-space>
          <span>插件管理</span>
          <a-button
            v-if="hasPermission('plugin:install')"
            type="primary"
            @click="onInstall"
          >
            安装插件
          </a-button>
        </a-space>
      </template>

      <a-table
        :columns="columns"
        :data-source="plugins"
        :loading="loading"
        :pagination="false"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-badge
              :status="getPluginStatus(record.status).type"
              :text="getPluginStatus(record.status).text"
            />
          </template>

          <template v-if="column.key === 'action'">
            <a-space>
              <a-button
                v-if="record.status === 'installed' && !record.enabled"
                type="link"
                @click="onEnable(record)"
              >
                启用
              </a-button>
              <a-button
                v-if="record.enabled"
                type="link"
                @click="onDisable(record)"
              >
                禁用
              </a-button>
              <a-button
                type="link"
                @click="onConfigure(record)"
              >
                配置
              </a-button>
              <a-button
                type="link"
                danger
                @click="onUninstall(record)"
              >
                卸载
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <plugin-install-modal
      v-model:visible="installModalVisible"
      @success="onInstallSuccess"
    />

    <plugin-config-modal
      v-model:visible="configModalVisible"
      :plugin="selectedPlugin"
      @success="onConfigSuccess"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { usePluginStore } from '@/stores/plugin';
import { usePermissionStore } from '@/stores/permission';
import type { Plugin } from '@/types/plugin';
import PluginInstallModal from './components/PluginInstallModal.vue';
import PluginConfigModal from './components/PluginConfigModal.vue';

export default defineComponent({
  name: 'PluginList',

  components: {
    PluginInstallModal,
    PluginConfigModal
  },

  setup() {
    const pluginStore = usePluginStore();
    const permissionStore = usePermissionStore();

    const loading = ref(false);
    const plugins = ref<Plugin[]>([]);
    const installModalVisible = ref(false);
    const configModalVisible = ref(false);
    const selectedPlugin = ref<Plugin | null>(null);

    const columns = [
      {
        title: '插件名称',
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: '版本',
        dataIndex: 'version',
        key: 'version',
        width: 100
      },
      {
        title: '描述',
        dataIndex: 'description',
        key: 'description'
      },
      {
        title: '状态',
        key: 'status',
        width: 120
      },
      {
        title: '操作',
        key: 'action',
        width: 200
      }
    ];

    onMounted(() => {
      fetchPlugins();
    });

    const fetchPlugins = async () => {
      loading.value = true;
      try {
        plugins.value = await pluginStore.getPlugins();
      } catch (error) {
        message.error('获取插件列表失败');
      } finally {
        loading.value = false;
      }
    };

    const hasPermission = (permission: string) => {
      return permissionStore.hasPermission(permission);
    };

    const getPluginStatus = (status: string) => {
      const statusMap = {
        installed: { type: 'default', text: '已安装' },
        enabled: { type: 'success', text: '已启用' },
        disabled: { type: 'warning', text: '已禁用' },
        error: { type: 'error', text: '异常' }
      };
      return statusMap[status] || { type: 'default', text: status };
    };

    const onInstall = () => {
      installModalVisible.value = true;
    };

    const onInstallSuccess = () => {
      installModalVisible.value = false;
      fetchPlugins();
    };

    const onEnable = async (plugin: Plugin) => {
      try {
        await pluginStore.enablePlugin(plugin.id);
        message.success('启用成功');
        fetchPlugins();
      } catch (error) {
        message.error('启用失败');
      }
    };

    const onDisable = async (plugin: Plugin) => {
      try {
        await pluginStore.disablePlugin(plugin.id);
        message.success('禁用成功');
        fetchPlugins();
      } catch (error) {
        message.error('禁用失败');
      }
    };

    const onConfigure = (plugin: Plugin) => {
      selectedPlugin.value = plugin;
      configModalVisible.value = true;
    };

    const onConfigSuccess = () => {
      configModalVisible.value = false;
      fetchPlugins();
    };

    const onUninstall = async (plugin: Plugin) => {
      try {
        await pluginStore.uninstallPlugin(plugin.id);
        message.success('卸载成功');
        fetchPlugins();
      } catch (error) {
        message.error('卸载失败');
      }
    };

    return {
      loading,
      plugins,
      columns,
      installModalVisible,
      configModalVisible,
      selectedPlugin,
      hasPermission,
      getPluginStatus,
      onInstall,
      onInstallSuccess,
      onEnable,
      onDisable,
      onConfigure,
      onConfigSuccess,
      onUninstall
    };
  }
});
</script>

<style scoped>
.plugin-list {
  padding: 24px;
  background: #f0f2f5;
}
</style> 