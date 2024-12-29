import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import MonitorDashboard from '@/views/monitor/MonitorDashboard.vue'
import { message } from 'ant-design-vue'
import dayjs from 'dayjs'

jest.mock('ant-design-vue', () => ({
  message: {
    error: jest.fn(),
    success: jest.fn(),
    warning: jest.fn()
  }
}))

describe('MonitorDashboard.vue', () => {
  let wrapper: any

  beforeEach(() => {
    wrapper = mount(MonitorDashboard, {
      global: {
        plugins: [createPinia()]
      }
    })
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  // 基础渲染测试
  describe('Component Rendering', () => {
    it('renders dashboard layout', () => {
      expect(wrapper.find('.monitor-dashboard').exists()).toBe(true)
      expect(wrapper.find('.metric-cards').exists()).toBe(true)
      expect(wrapper.find('.chart-container').exists()).toBe(true)
      expect(wrapper.find('.alert-list').exists()).toBe(true)
    })

    it('renders metric cards with correct data', async () => {
      const metrics = [
        { name: 'CPU使用率', value: '45%', status: 'normal' },
        { name: '内存使用率', value: '60%', status: 'warning' },
        { name: '磁盘使用率', value: '85%', status: 'critical' }
      ]
      
      await wrapper.setData({ metrics })
      const cards = wrapper.findAll('.metric-card')
      expect(cards.length).toBe(metrics.length)
      expect(cards[0].text()).toContain('CPU使用率')
      expect(cards[0].classes()).toContain('status-normal')
    })
  })

  // 图表功能测试
  describe('Chart Features', () => {
    it('initializes charts correctly', () => {
      expect(wrapper.vm.cpuChart).toBeTruthy()
      expect(wrapper.vm.memoryChart).toBeTruthy()
      expect(wrapper.vm.diskChart).toBeTruthy()
    })

    it('updates chart data', async () => {
      const chartData = {
        timestamps: ['2024-01-01 00:00:00', '2024-01-01 00:01:00'],
        values: [45, 50]
      }
      
      await wrapper.vm.updateChartData('cpu', chartData)
      expect(wrapper.vm.cpuChart.data.labels).toEqual(chartData.timestamps)
      expect(wrapper.vm.cpuChart.data.datasets[0].data).toEqual(chartData.values)
    })

    it('handles chart type switching', async () => {
      const chartTypes = ['line', 'bar', 'area']
      for (const type of chartTypes) {
        await wrapper.find(`.chart-type-${type}`).trigger('click')
        expect(wrapper.vm.chartType).toBe(type)
        expect(wrapper.vm.updateChartType).toHaveBeenCalledWith(type)
      }
    })
  })

  // 时间范围测试
  describe('Time Range Features', () => {
    it('handles time range selection', async () => {
      const timeRange = [
        dayjs().subtract(1, 'hour'),
        dayjs()
      ]
      await wrapper.find('.time-range-picker').trigger('change', timeRange)
      expect(wrapper.vm.startTime).toBe(timeRange[0].format('YYYY-MM-DD HH:mm:ss'))
      expect(wrapper.vm.endTime).toBe(timeRange[1].format('YYYY-MM-DD HH:mm:ss'))
    })

    it('supports quick time range selection', async () => {
      const ranges = [
        { key: '1h', label: '最近1小时' },
        { key: '6h', label: '最近6小时' },
        { key: '24h', label: '最近24小时' },
        { key: '7d', label: '最近7天' }
      ]

      for (const range of ranges) {
        await wrapper.find(`.quick-range-${range.key}`).trigger('click')
        expect(wrapper.vm.fetchMetricData).toHaveBeenCalled()
      }
    })
  })

  // 告警功能测试
  describe('Alert Features', () => {
    it('displays active alerts', async () => {
      const alerts = [
        { id: 1, level: 'critical', message: 'CPU使用率过高' },
        { id: 2, level: 'warning', message: '内存使用率较高' }
      ]
      
      await wrapper.setData({ activeAlerts: alerts })
      const alertElements = wrapper.findAll('.alert-item')
      expect(alertElements.length).toBe(alerts.length)
      expect(alertElements[0].classes()).toContain('level-critical')
    })

    it('handles alert acknowledgment', async () => {
      await wrapper.find('.acknowledge-alert-button').trigger('click')
      expect(wrapper.vm.acknowledgeAlert).toHaveBeenCalled()
      expect(message.success).toHaveBeenCalledWith('告警已确认')
    })
  })

  // 实时更新测试
  describe('Real-time Updates', () => {
    it('handles metric updates via WebSocket', async () => {
      const newMetric = {
        type: 'cpu',
        value: 75,
        timestamp: '2024-01-01 00:00:00'
      }
      
      await wrapper.vm.handleMetricUpdate(newMetric)
      expect(wrapper.vm.metrics.find(m => m.type === 'cpu').value).toBe(75)
      expect(wrapper.vm.updateChartData).toHaveBeenCalledWith('cpu', expect.any(Object))
    })

    it('handles WebSocket reconnection', async () => {
      await wrapper.vm.wsConnection.close()
      expect(wrapper.vm.reconnectWebSocket).toHaveBeenCalled()
      expect(wrapper.vm.wsConnection).toBeTruthy()
    })
  })

  // 导出功能测试
  describe('Export Features', () => {
    it('exports metric data', async () => {
      await wrapper.find('.export-metrics-button').trigger('click')
      expect(wrapper.vm.exportMetricData).toHaveBeenCalled()
    })

    it('exports chart as image', async () => {
      await wrapper.find('.export-chart-button').trigger('click')
      expect(wrapper.vm.exportChartImage).toHaveBeenCalled()
    })
  })

  // 错误处理测试
  describe('Error Handling', () => {
    it('handles API errors', async () => {
      jest.spyOn(global, 'fetch').mockRejectedValueOnce(new Error('API Error'))
      await wrapper.vm.fetchMetricData()
      expect(message.error).toHaveBeenCalledWith('获取监控数据失败：API Error')
    })

    it('handles WebSocket errors', async () => {
      wrapper.vm.handleWebSocketError(new Error('WebSocket Error'))
      expect(message.error).toHaveBeenCalledWith('实时数据连接失败：WebSocket Error')
    })
  })

  // 性能优化测试
  describe('Performance Optimizations', () => {
    it('throttles real-time updates', async () => {
      jest.useFakeTimers()
      
      for (let i = 0; i < 10; i++) {
        wrapper.vm.handleMetricUpdate({ type: 'cpu', value: i })
      }
      
      expect(wrapper.vm.updateChartData).toHaveBeenCalledTimes(1)
      jest.runAllTimers()
      expect(wrapper.vm.updateChartData).toHaveBeenCalledTimes(2)
    })

    it('implements chart data point limiting', async () => {
      const largeDataset = Array(1000).fill(null).map((_, i) => ({
        timestamp: `2024-01-01 00:${i}:00`,
        value: i
      }))
      
      await wrapper.vm.updateChartData('cpu', largeDataset)
      expect(wrapper.vm.cpuChart.data.labels.length).toBeLessThanOrEqual(500)
    })
  })
}) 