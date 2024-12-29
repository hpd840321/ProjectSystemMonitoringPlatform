import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import LogSearch from '@/views/log/LogSearch.vue'
import { message } from 'ant-design-vue'
import dayjs from 'dayjs'

jest.mock('ant-design-vue', () => ({
  message: {
    error: jest.fn(),
    success: jest.fn(),
    warning: jest.fn()
  }
}))

describe('LogSearch.vue', () => {
  let wrapper: any

  beforeEach(() => {
    wrapper = mount(LogSearch, {
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
    it('renders all search form elements', () => {
      expect(wrapper.find('.search-form').exists()).toBe(true)
      expect(wrapper.find('.keyword-input').exists()).toBe(true)
      expect(wrapper.find('.time-range-picker').exists()).toBe(true)
      expect(wrapper.find('.log-level-select').exists()).toBe(true)
      expect(wrapper.find('.search-button').exists()).toBe(true)
    })

    it('renders log table with correct columns', () => {
      const columns = wrapper.findAll('.ant-table-column')
      expect(columns.length).toBe(6) // 时间、级别、来源、消息、追踪ID、操作
      expect(columns[0].text()).toBe('时间')
      expect(columns[1].text()).toBe('级别')
    })
  })

  // 搜索功能测试
  describe('Search Functionality', () => {
    it('updates search form values', async () => {
      const keyword = wrapper.find('.keyword-input')
      await keyword.setValue('error')
      expect(wrapper.vm.searchForm.keyword).toBe('error')

      const levelSelect = wrapper.find('.log-level-select')
      await levelSelect.trigger('change', 'ERROR')
      expect(wrapper.vm.searchForm.level).toBe('ERROR')
    })

    it('handles time range selection', async () => {
      const timeRange = [
        dayjs().subtract(1, 'day'),
        dayjs()
      ]
      await wrapper.find('.time-range-picker').trigger('change', timeRange)
      expect(wrapper.vm.searchForm.startTime).toBe(timeRange[0].format('YYYY-MM-DD HH:mm:ss'))
      expect(wrapper.vm.searchForm.endTime).toBe(timeRange[1].format('YYYY-MM-DD HH:mm:ss'))
    })

    it('validates search form before submission', async () => {
      // 清空必填字段
      await wrapper.setData({
        searchForm: {
          startTime: '',
          endTime: ''
        }
      })
      await wrapper.find('.search-button').trigger('click')
      expect(message.warning).toHaveBeenCalledWith('请选择时间范围')
    })

    it('handles search with all parameters', async () => {
      const searchParams = {
        keyword: 'test error',
        level: 'ERROR',
        source: 'backend',
        startTime: '2024-01-01 00:00:00',
        endTime: '2024-01-02 00:00:00',
        traceId: '123456',
        userId: '789'
      }

      await wrapper.setData({ searchForm: searchParams })
      await wrapper.vm.handleSearch()

      expect(wrapper.vm.loading).toBe(true)
      // 验证API调用参数
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/logs/search'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(searchParams)
        })
      )
    })
  })

  // 高级功能测试
  describe('Advanced Features', () => {
    it('handles log level filtering', async () => {
      const levels = ['ERROR', 'WARN', 'INFO', 'DEBUG']
      for (const level of levels) {
        await wrapper.find('.log-level-select').trigger('change', level)
        expect(wrapper.vm.searchForm.level).toBe(level)
        expect(wrapper.vm.handleSearch).toHaveBeenCalled()
      }
    })

    it('supports quick time range selection', async () => {
      const ranges = [
        { key: 'last15mins', label: '最近15分钟' },
        { key: 'last1hour', label: '最近1小时' },
        { key: 'last24hours', label: '最近24小时' },
        { key: 'last7days', label: '最近7天' }
      ]

      for (const range of ranges) {
        await wrapper.find(`.quick-range-${range.key}`).trigger('click')
        expect(wrapper.vm.searchForm.startTime).toBeTruthy()
        expect(wrapper.vm.searchForm.endTime).toBeTruthy()
      }
    })

    it('handles log detail view with syntax highlighting', async () => {
      const logItem = {
        id: '1',
        timestamp: '2024-01-01 00:00:00',
        level: 'ERROR',
        message: '{"error": "Test error message"}',
        stack: 'Error: Test error\n    at Test.func (/app/test.js:1:1)'
      }

      await wrapper.setData({ selectedLog: logItem })
      await wrapper.vm.$nextTick()

      const detailModal = wrapper.find('.log-detail-modal')
      expect(detailModal.exists()).toBe(true)
      expect(detailModal.find('.json-viewer').exists()).toBe(true)
      expect(detailModal.find('.stack-trace').exists()).toBe(true)
    })

    it('supports log context viewing', async () => {
      await wrapper.find('.view-context-button').trigger('click')
      expect(wrapper.vm.loadingContext).toBe(true)
      expect(wrapper.vm.contextLogs.length).toBeGreaterThan(0)
      expect(wrapper.find('.context-logs-modal').exists()).toBe(true)
    })
  })

  // 实时功能测试
  describe('Real-time Features', () => {
    it('handles websocket connection for real-time logs', async () => {
      await wrapper.find('.real-time-toggle').trigger('click')
      expect(wrapper.vm.realTimeEnabled).toBe(true)
      expect(wrapper.vm.wsConnection).toBeTruthy()

      // 模拟接收新日志
      const newLog = {
        timestamp: '2024-01-01 00:00:00',
        level: 'ERROR',
        message: 'New error message'
      }
      wrapper.vm.handleNewLog(newLog)
      expect(wrapper.vm.logData[0]).toEqual(newLog)
    })

    it('handles websocket reconnection', async () => {
      wrapper.vm.wsConnection = null
      await wrapper.vm.connectWebSocket()
      expect(wrapper.vm.wsConnection).toBeTruthy()
      expect(wrapper.vm.reconnectAttempts).toBe(0)
    })
  })

  // 导出功能测试
  describe('Export Features', () => {
    it('supports multiple export formats', async () => {
      const formats = ['csv', 'json', 'txt']
      for (const format of formats) {
        await wrapper.find(`.export-${format}-button`).trigger('click')
        expect(wrapper.vm.exportLogs).toHaveBeenCalledWith(format)
      }
    })

    it('handles large dataset export', async () => {
      await wrapper.setData({ total: 10000 })
      await wrapper.find('.export-button').trigger('click')
      expect(message.warning).toHaveBeenCalledWith('导出数据量较大，请稍候...')
    })
  })

  // 性能优化测试
  describe('Performance Optimizations', () => {
    it('implements virtual scrolling for large datasets', async () => {
      const largeDataset = Array(1000).fill(null).map((_, i) => ({
        id: i,
        timestamp: '2024-01-01 00:00:00',
        level: 'INFO',
        message: `Log message ${i}`
      }))

      await wrapper.setData({ logData: largeDataset })
      expect(wrapper.find('.virtual-scroll-container').exists()).toBe(true)
      expect(wrapper.vm.visibleLogs.length).toBeLessThan(largeDataset.length)
    })

    it('debounces search input', async () => {
      jest.useFakeTimers()
      const searchInput = wrapper.find('.keyword-input')
      
      await searchInput.setValue('t')
      await searchInput.setValue('te')
      await searchInput.setValue('tes')
      await searchInput.setValue('test')

      expect(wrapper.vm.handleSearch).not.toHaveBeenCalled()
      jest.runAllTimers()
      expect(wrapper.vm.handleSearch).toHaveBeenCalledTimes(1)
    })
  })
}) 