<template>
  <div ref="chartRef" class="chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps<{
  data: Array<{ time: number; value: number }>
}>()

const chartRef = ref(null)
let chart = null

const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart) return
  
  const option = {
    grid: {
      top: 10,
      right: 10,
      bottom: 20,
      left: 40
    },
    xAxis: {
      type: 'time',
      splitLine: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: [
      {
        type: 'line',
        data: props.data.map(item => [item.time, item.value]),
        smooth: true,
        showSymbol: false,
        lineStyle: {
          width: 2
        },
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  }
  
  chart.setOption(option)
}

watch(() => props.data, updateChart, { deep: true })

onMounted(() => {
  initChart()
  
  window.addEventListener('resize', () => {
    chart?.resize()
  })
})

onUnmounted(() => {
  chart?.dispose()
  window.removeEventListener('resize', () => {
    chart?.resize()
  })
})
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
}
</style> 