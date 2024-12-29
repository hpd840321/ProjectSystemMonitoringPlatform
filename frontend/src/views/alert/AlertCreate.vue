<template>
  <div class="alert-create">
    <a-card title="创建告警规则">
      <a-form
        :model="formState"
        :rules="rules"
        @finish="onFinish"
        layout="vertical"
      >
        <a-form-item label="规则名称" name="name">
          <a-input v-model:value="formState.name" placeholder="请输入规则名称" />
        </a-form-item>

        <a-form-item label="监控指标" name="metric">
          <a-select v-model:value="formState.metric" placeholder="请选择监控指标">
            <a-select-option value="cpu_usage">CPU使用率</a-select-option>
            <a-select-option value="memory_usage">内存使用率</a-select-option>
            <a-select-option value="disk_usage">磁盘使用率</a-select-option>
            <a-select-option value="network_in">网络入流量</a-select-option>
            <a-select-option value="network_out">网络出流量</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="告警条件" name="condition">
          <a-input-group compact>
            <a-select v-model:value="formState.operator" style="width: 20%">
              <a-select-option value=">">&gt;</a-select-option>
              <a-select-option value=">=">&gt;=</a-select-option>
              <a-select-option value="<">&lt;</a-select-option>
              <a-select-option value="<=">&lt;=</a-select-option>
              <a-select-option value="==">==</a-select-option>
            </a-select>
            <a-input-number
              v-model:value="formState.threshold"
              style="width: 30%"
              placeholder="阈值"
            />
            <a-select v-model:value="formState.duration" style="width: 30%">
              <a-select-option value="5m">持续5分钟</a-select-option>
              <a-select-option value="10m">持续10分钟</a-select-option>
              <a-select-option value="30m">持续30分钟</a-select-option>
              <a-select-option value="1h">持续1小时</a-select-option>
            </a-select>
          </a-input-group>
        </a-form-item>

        <a-form-item label="告警级别" name="level">
          <a-select v-model:value="formState.level" placeholder="请选择告警级别">
            <a-select-option value="info">提示</a-select-option>
            <a-select-option value="warning">警告</a-select-option>
            <a-select-option value="error">错误</a-select-option>
            <a-select-option value="critical">严重</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="通知渠道" name="channels">
          <a-checkbox-group v-model:value="formState.channels">
            <a-checkbox value="email">邮件</a-checkbox>
            <a-checkbox value="sms">短信</a-checkbox>
            <a-checkbox value="webhook">Webhook</a-checkbox>
          </a-checkbox-group>
        </a-form-item>

        <a-form-item label="通知模板" name="template">
          <a-textarea
            v-model:value="formState.template"
            :rows="4"
            placeholder="支持变量: ${metric}, ${value}, ${threshold}, ${duration}"
          />
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
import { defineComponent, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { useAlertStore } from '@/stores/alert';
import type { AlertRule } from '@/types/alert';

export default defineComponent({
  name: 'AlertCreate',

  setup() {
    const router = useRouter();
    const alertStore = useAlertStore();

    const formState = reactive<Partial<AlertRule>>({
      name: '',
      metric: undefined,
      operator: '>',
      threshold: undefined,
      duration: '5m',
      level: 'warning',
      channels: ['email'],
      template: '${metric}指标值为${value},超过阈值${threshold},持续时间${duration}'
    });

    const rules = {
      name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
      metric: [{ required: true, message: '请选择监控指标', trigger: 'change' }],
      threshold: [{ required: true, message: '请输入阈值', trigger: 'blur' }],
      level: [{ required: true, message: '请选择告警级别', trigger: 'change' }],
      channels: [{ required: true, message: '请选择通知渠道', trigger: 'change' }]
    };

    const onFinish = async (values: any) => {
      try {
        await alertStore.createAlertRule(values);
        message.success('创建告警规则成功');
        router.push('/alerts');
      } catch (error) {
        message.error('创建告警规则失败');
      }
    };

    const onCancel = () => {
      router.back();
    };

    return {
      formState,
      rules,
      onFinish,
      onCancel
    };
  }
});
</script>

<style scoped>
.alert-create {
  padding: 24px;
  background: #f0f2f5;
}
</style> 