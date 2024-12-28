<template>
  <div class="dashboard">
    <!-- 系统状态概览 -->
    <SystemOverview />
    
    <!-- 其他仪表盘内容 -->
  </div>
</template>

<script setup lang="ts">
import SystemOverview from '@/components/dashboard/SystemOverview.vue'
</script>

<style scoped>
.dashboard {
  min-height: 100%;
  background-color: #f5f7fa;
}
</style> 