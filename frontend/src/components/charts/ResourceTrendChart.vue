<template>
  <div class="resource-trend-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <el-select v-model="timeRange" size="small">
        <el-option label="最近24小时" value="24h" />
        <el-option label="最近7天" value="7d" />
        <el-option label="最近30天" value="30d" />
      </el-select>
    </div>
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

const props = defineProps<{
  title: string
  data: {
    timestamps: string[]
    values: number[]
  }
}>()

const chartRef = ref<HTMLElement>()
const timeRange = ref('24h')
let chart: echarts.ECharts | null = null

// 初始化图表
function initChart() {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  updateChart()
  
  // 自适应大小
  window.addEventListener('resize', () => {
    chart?.resize()
  })
}

// 更新图表数据
function updateChart() {
  if (!chart) return
  
  const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>{a}: {c}%'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: props.data.timestamps
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: props.title,
        type: 'line',
        smooth: true,
        data: props.data.values,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  }
  
  chart.setOption(option)
}

// 监听数据变化
watch(() => props.data, () => {
  updateChart()
}, { deep: true })

// 监听时间范围变化
watch(timeRange, () => {
  // 这里可以触发数据重新加载
})

onMounted(() => {
  initChart()
})
</script>

<style scoped>
.resource-trend-chart {
  width: 100%;
  height: 100%;
}
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.chart-container {
  width: 100%;
  height: calc(100% - 40px);
}
</style> 