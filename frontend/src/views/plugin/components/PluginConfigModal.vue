<template>
  <a-modal
    :title="`配置插件 - ${plugin?.name}`"
    :visible="visible"
    :confirm-loading="loading"
    @ok="onSubmit"
    @cancel="onCancel"
  >
    <template v-if="configSchema">
      <a-form
        :model="formState"
        :rules="rules"
        layout="vertical"
      >
        <template v-for="field in configSchema.fields" :key="field.name">
          <!-- 文本输入 -->
          <a-form-item
            v-if="field.type === 'string'"
            :label="field.label"
            :name="field.name"
          >
            <a-input
              v-model:value="formState[field.name]"
              :placeholder="field.placeholder"
            />
          </a-form-item>

          <!-- 数字输入 -->
          <a-form-item
            v-else-if="field.type === 'number'"
            :label="field.label"
            :name="field.name"
          >
            <a-input-number
              v-model:value="formState[field.name]"
              :min="field.min"
              :max="field.max"
              :step="field.step"
            />
          </a-form-item>

          <!-- 开关 -->
          <a-form-item
            v-else-if="field.type === 'boolean'"
            :label="field.label"
            :name="field.name"
          >
            <a-switch v-model:checked="formState[field.name]" />
          </a-form-item>

          <!-- 选择器 -->
          <a-form-item
            v-else-if="field.type === 'select'"
            :label="field.label"
            :name="field.name"
          >
            <a-select
              v-model:value="formState[field.name]"
              :placeholder="field.placeholder"
            >
              <a-select-option
                v-for="option in field.options"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </a-select-option>
            </a-select>
          </a-form-item>

          <!-- JSON编辑器 -->
          <a-form-item
            v-else-if="field.type === 'json'"
            :label="field.label"
            :name="field.name"
          >
            <json-editor
              v-model:value="formState[field.name]"
              :height="200"
            />
          </a-form-item>
        </template>
      </a-form>
    </template>
    <template v-else>
      <a-empty description="该插件暂无配置项" />
    </template>
  </a-modal>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, watch } from 'vue';
import { message } from 'ant-design-vue';
import { usePluginStore } from '@/stores/plugin';
import type { Plugin, PluginConfigSchema } from '@/types/plugin';
import JsonEditor from '@/components/JsonEditor.vue';

export default defineComponent({
  name: 'PluginConfigModal',

  components: {
    JsonEditor
  },

  props: {
    visible: {
      type: Boolean,
      required: true
    },
    plugin: {
      type: Object as () => Plugin,
      required: true
    }
  },

  emits: ['update:visible', 'success'],

  setup(props, { emit }) {
    const pluginStore = usePluginStore();
    const loading = ref(false);
    const configSchema = ref<PluginConfigSchema | null>(null);
    const formState = reactive<Record<string, any>>({});
    const rules = reactive<Record<string, any>>({});

    watch(() => props.visible, async (visible) => {
      if (visible && props.plugin) {
        await loadPluginConfig();
      }
    });

    const loadPluginConfig = async () => {
      try {
        // 获取插件配置模式
        configSchema.value = await pluginStore.getPluginConfigSchema(props.plugin.id);
        
        // 获取当前配置
        const config = await pluginStore.getPluginConfig(props.plugin.id);
        
        // 初始化表单状态
        Object.keys(formState).forEach(key => delete formState[key]);
        Object.assign(formState, config);

        // 生成验证规则
        Object.keys(rules).forEach(key => delete rules[key]);
        configSchema.value?.fields.forEach(field => {
          if (field.required) {
            rules[field.name] = [{
              required: true,
              message: `请输入${field.label}`,
              trigger: field.type === 'select' ? 'change' : 'blur'
            }];
          }
        });
      } catch (error) {
        message.error('加载插件配置失败');
      }
    };

    const onSubmit = async () => {
      loading.value = true;
      try {
        await pluginStore.updatePluginConfig(props.plugin.id, formState);
        message.success('保存成功');
        emit('success');
        onCancel();
      } catch (error) {
        message.error('保存失败');
      } finally {
        loading.value = false;
      }
    };

    const onCancel = () => {
      emit('update:visible', false);
    };

    return {
      loading,
      configSchema,
      formState,
      rules,
      onSubmit,
      onCancel
    };
  }
});
</script> 