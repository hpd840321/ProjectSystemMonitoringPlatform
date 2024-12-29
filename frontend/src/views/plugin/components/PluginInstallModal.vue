<template>
  <a-modal
    title="安装插件"
    :visible="visible"
    :confirm-loading="loading"
    @ok="onSubmit"
    @cancel="onCancel"
  >
    <a-form :model="formState" :rules="rules" layout="vertical">
      <a-form-item label="上传插件包" name="file">
        <a-upload
          v-model:fileList="fileList"
          :beforeUpload="beforeUpload"
          :maxCount="1"
        >
          <a-button>
            <upload-outlined />
            选择文件
          </a-button>
        </a-upload>
      </a-form-item>

      <a-form-item label="插件来源" name="source">
        <a-radio-group v-model:value="formState.source">
          <a-radio value="local">本地上传</a-radio>
          <a-radio value="market">插件市场</a-radio>
        </a-radio-group>
      </a-form-item>

      <template v-if="formState.source === 'market'">
        <a-form-item label="插件市场" name="market_plugin">
          <a-select
            v-model:value="formState.market_plugin"
            placeholder="请选择插件"
            :loading="marketLoading"
          >
            <a-select-option
              v-for="plugin in marketPlugins"
              :key="plugin.id"
              :value="plugin.id"
            >
              {{ plugin.name }} ({{ plugin.version }})
            </a-select-option>
          </a-select>
        </a-form-item>
      </template>
    </a-form>
  </a-modal>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, watch } from 'vue';
import { message } from 'ant-design-vue';
import { UploadOutlined } from '@ant-design/icons-vue';
import { usePluginStore } from '@/stores/plugin';
import type { UploadProps } from 'ant-design-vue';

export default defineComponent({
  name: 'PluginInstallModal',

  components: {
    UploadOutlined
  },

  props: {
    visible: {
      type: Boolean,
      required: true
    }
  },

  emits: ['update:visible', 'success'],

  setup(props, { emit }) {
    const pluginStore = usePluginStore();
    const loading = ref(false);
    const marketLoading = ref(false);
    const fileList = ref([]);
    const marketPlugins = ref([]);

    const formState = reactive({
      source: 'local',
      file: undefined,
      market_plugin: undefined
    });

    const rules = {
      file: [
        { 
          required: true,
          message: '请上传插件包',
          trigger: 'change',
          validator: (_rule: any, value: any) => {
            if (formState.source === 'local' && !fileList.value.length) {
              return Promise.reject();
            }
            return Promise.resolve();
          }
        }
      ],
      market_plugin: [
        {
          required: true,
          message: '请选择插件',
          trigger: 'change',
          validator: (_rule: any, value: any) => {
            if (formState.source === 'market' && !value) {
              return Promise.reject();
            }
            return Promise.resolve();
          }
        }
      ]
    };

    watch(() => props.visible, async (visible) => {
      if (visible) {
        await fetchMarketPlugins();
      }
    });

    const fetchMarketPlugins = async () => {
      marketLoading.value = true;
      try {
        marketPlugins.value = await pluginStore.getMarketPlugins();
      } catch (error) {
        message.error('获取插件市场数据失败');
      } finally {
        marketLoading.value = false;
      }
    };

    const beforeUpload: UploadProps['beforeUpload'] = (file) => {
      const isZip = file.type === 'application/zip';
      if (!isZip) {
        message.error('只能上传ZIP格式的插件包');
        return false;
      }
      formState.file = file;
      return false;
    };

    const onSubmit = async () => {
      loading.value = true;
      try {
        if (formState.source === 'local') {
          await pluginStore.installLocalPlugin(formState.file);
        } else {
          await pluginStore.installMarketPlugin(formState.market_plugin);
        }
        message.success('安装成功');
        emit('success');
        onCancel();
      } catch (error) {
        message.error('安装失败');
      } finally {
        loading.value = false;
      }
    };

    const onCancel = () => {
      formState.source = 'local';
      formState.file = undefined;
      formState.market_plugin = undefined;
      fileList.value = [];
      emit('update:visible', false);
    };

    return {
      loading,
      marketLoading,
      fileList,
      marketPlugins,
      formState,
      rules,
      beforeUpload,
      onSubmit,
      onCancel
    };
  }
});
</script> 