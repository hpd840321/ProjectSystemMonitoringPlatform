<template>
  <div class="log-search">
    <a-card>
      <template #title>
        <a-space>
          <span>日志搜索</span>
          <a-radio-group v-model:value="timeRange" @change="onTimeRangeChange">
            <a-radio-button value="1h">1小时</a-radio-button>
            <a-radio-button value="6h">6小时</a-radio-button>
            <a-radio-button value="1d">1天</a-radio-button>
            <a-radio-button value="7d">7天</a-radio-button>
            <a-radio-button value="custom">自定义</a-radio-button>
          </a-radio-group>
          <a-range-picker
            v-if="timeRange === 'custom'"
            v-model:value="customTimeRange"
            show-time
            @change="onCustomTimeRangeChange"
          />
        </a-space>
      </template>

      <a-form layout="inline" class="search-form">
        <a-form-item label="关键词">
          <a-input
            v-model:value="searchParams.keyword"
            placeholder="请输入关键词"
            allow-clear
            @pressEnter="onSearch"
          />
        </a-form-item>

        <a-form-item label="日志级别">
          <a-select
            v-model:value="searchParams.level"
            placeholder="请选择日志级别"
            style="width: 120px"
            allow-clear
          >
            <a-select-option value="debug">DEBUG</a-select-option>
            <a-select-option value="info">INFO</a-select-option>
            <a-select-option value="warning">WARNING</a-select-option>
            <a-select-option value="error">ERROR</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="服务器">
          <a-select
            v-model:value="searchParams.server_id"
            placeholder="请选择服务器"
            style="width: 200px"
            allow-clear
          >
            <a-select-option
              v-for="server in servers"
              :key="server.id"
              :value="server.id"
            >
              {{ server.name }}
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item>
          <a-button type="primary" @click="onSearch">搜索</a-button>
        </a-form-item>
      </a-form>

      <a-table
        :columns="columns"
        :data-source="logs"
        :loading="loading"
        :pagination="pagination"
        @change="onTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'level'">
            <a-tag :color="getLevelColor(record.level)">
              {{ record.level.toUpperCase() }}
            </a-tag>
          </template>

          <template v-if="column.key === 'content'">
            <a-typography-paragraph
              :ellipsis="{ rows: 2, expandable: true }"
            >
              {{ record.content }}
            </a-typography-paragraph>
          </template>

          <template v-if="column.key === 'action'">
            <a-button type="link" @click="onViewDetail(record)">
              详情
            </a-button>
          </template>
        </template>
      </a-table>
    </a-card>

    <log-detail-modal
      v-model:visible="detailModalVisible"
      :log="selectedLog"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue';
import { useLogStore } from '@/stores/log';
import { useServerStore } from '@/stores/server';
import type { Log } from '@/types/log';
import LogDetailModal from './components/LogDetailModal.vue';

export default defineComponent({
  name: 'LogSearch',

  components: {
    LogDetailModal
  },

  setup() {
    const logStore = useLogStore();
    const serverStore = useServerStore();

    const loading = ref(false);
    const logs = ref<Log[]>([]);
    const servers = ref([]);
    const timeRange = ref('1h');
    const customTimeRange = ref<[moment.Moment, moment.Moment]>([]);
    const detailModalVisible = ref(false);
    const selectedLog = ref<Log | null>(null);

    const searchParams = reactive({
      keyword: '',
      level: undefined,
      server_id: undefined,
      start_time: undefined,
      end_time: undefined
    });

    const pagination = reactive({
      current: 1,
      pageSize: 20,
      total: 0
    });

    const columns = [
      {
        title: '时间',
        dataIndex: 'timestamp',
        key: 'timestamp',
        width: 180
      },
      {
        title: '级别',
        dataIndex: 'level',
        key: 'level',
        width: 100
      },
      {
        title: '服务器',
        dataIndex: 'server_name',
        key: 'server_name',
        width: 150
      },
      {
        title: '内容',
        dataIndex: 'content',
        key: 'content'
      },
      {
        title: '操作',
        key: 'action',
        width: 80
      }
    ];

    onMounted(async () => {
      await fetchServers();
      setTimeRange('1h');
      fetchLogs();
    });

    const fetchServers = async () => {
      try {
        const { items } = await serverStore.fetchServers();
        servers.value = items;
      } catch (error) {
        console.error('获取服务器列表失败:', error);
      }
    };

    const fetchLogs = async () => {
      loading.value = true;
      try {
        const { items, total } = await logStore.searchLogs({
          ...searchParams,
          page: pagination.current,
          pageSize: pagination.pageSize
        });
        logs.value = items;
        pagination.total = total;
      } catch (error) {
        console.error('搜索日志失败:', error);
      } finally {
        loading.value = false;
      }
    };

    const setTimeRange = (range: string) => {
      const now = moment();
      let startTime;

      switch (range) {
        case '1h':
          startTime = now.clone().subtract(1, 'hour');
          break;
        case '6h':
          startTime = now.clone().subtract(6, 'hours');
          break;
        case '1d':
          startTime = now.clone().subtract(1, 'day');
          break;
        case '7d':
          startTime = now.clone().subtract(7, 'days');
          break;
        default:
          return;
      }

      searchParams.start_time = startTime.toISOString();
      searchParams.end_time = now.toISOString();
    };

    const onTimeRangeChange = (e: any) => {
      if (e.target.value !== 'custom') {
        setTimeRange(e.target.value);
        fetchLogs();
      }
    };

    const onCustomTimeRangeChange = (dates: [moment.Moment, moment.Moment]) => {
      if (dates) {
        searchParams.start_time = dates[0].toISOString();
        searchParams.end_time = dates[1].toISOString();
        fetchLogs();
      }
    };

    const onSearch = () => {
      pagination.current = 1;
      fetchLogs();
    };

    const onTableChange = (pag: any) => {
      pagination.current = pag.current;
      pagination.pageSize = pag.pageSize;
      fetchLogs();
    };

    const getLevelColor = (level: string) => {
      const colors = {
        debug: 'default',
        info: 'success',
        warning: 'warning',
        error: 'error'
      };
      return colors[level] || 'default';
    };

    const onViewDetail = (log: Log) => {
      selectedLog.value = log;
      detailModalVisible.value = true;
    };

    return {
      loading,
      logs,
      servers,
      timeRange,
      customTimeRange,
      searchParams,
      pagination,
      columns,
      detailModalVisible,
      selectedLog,
      getLevelColor,
      onTimeRangeChange,
      onCustomTimeRangeChange,
      onSearch,
      onTableChange,
      onViewDetail
    };
  }
});
</script>

<style scoped>
.log-search {
  padding: 24px;
  background: #f0f2f5;
}

.search-form {
  margin-bottom: 24px;
}
</style> 