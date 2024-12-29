import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import Register from '@/views/auth/Register.vue'
import { message } from 'ant-design-vue'

// Mock ant-design-vue message
jest.mock('ant-design-vue', () => ({
  message: {
    error: jest.fn(),
    success: jest.fn()
  }
}))

describe('Register.vue', () => {
  const wrapper = mount(Register, {
    global: {
      plugins: [createPinia()]
    }
  })

  it('renders register form', () => {
    expect(wrapper.find('.register-container').exists()).toBe(true)
    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
  })

  it('validates form fields', async () => {
    await wrapper.find('form').trigger('submit')
    expect(message.error).toHaveBeenCalled()
  })

  it('handles successful registration', async () => {
    await wrapper.setData({
      formState: {
        username: 'testuser',
        email: 'test@example.com',
        password: 'Test123456',
        confirmPassword: 'Test123456',
        captcha: '1234'
      }
    })
    await wrapper.find('form').trigger('submit')
    expect(message.success).toHaveBeenCalledWith('注册成功')
  })

  it('validates password requirements', async () => {
    await wrapper.setData({
      formState: {
        password: 'weak',
        confirmPassword: 'weak'
      }
    })
    await wrapper.find('form').trigger('submit')
    expect(message.error).toHaveBeenCalledWith('密码必须包含大小写字母和数字')
  })

  it('validates email format', async () => {
    await wrapper.setData({
      formState: {
        email: 'invalid-email'
      }
    })
    await wrapper.find('form').trigger('submit')
    expect(message.error).toHaveBeenCalledWith('请输入有效的邮箱地址')
  })

  it('handles captcha verification', async () => {
    // 测试获取验证码
    await wrapper.find('.captcha-button').trigger('click')
    expect(wrapper.vm.captchaImage).toBeTruthy()
    
    // 测试验证码刷新
    await wrapper.find('.refresh-captcha').trigger('click')
    expect(wrapper.vm.captchaImage).toBeTruthy()
  })

  it('handles network error', async () => {
    // 模拟网络错误
    jest.spyOn(global, 'fetch').mockRejectedValueOnce(new Error('Network error'))
    
    await wrapper.find('form').trigger('submit')
    expect(message.error).toHaveBeenCalledWith('网络错误，请稍后重试')
  })

  it('shows loading state during registration', async () => {
    const submitButton = wrapper.find('button[type="submit"]')
    await wrapper.setData({ loading: true })
    expect(submitButton.attributes('disabled')).toBeTruthy()
    expect(submitButton.find('.loading-icon').exists()).toBeTruthy()
  })

  it('validates username uniqueness', async () => {
    await wrapper.setData({
      formState: {
        username: 'existing_user'
      }
    })
    await wrapper.vm.checkUsername()
    expect(message.error).toHaveBeenCalledWith('用户名已存在')
  })

  it('handles password strength requirements', async () => {
    const testCases = [
      { password: 'short', message: '密码长度至少为8位' },
      { password: 'onlylowercase', message: '密码必须包含大写字母' },
      { password: 'ONLYUPPERCASE', message: '密码必须包含小写字母' },
      { password: 'NoNumbers', message: '密码必须包含数字' }
    ]

    for (const testCase of testCases) {
      await wrapper.setData({
        formState: {
          password: testCase.password
        }
      })
      await wrapper.vm.validatePassword()
      expect(message.error).toHaveBeenCalledWith(testCase.message)
    }
  })

  it('handles form reset', async () => {
    await wrapper.vm.resetForm()
    expect(wrapper.vm.formState).toEqual({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      captcha: ''
    })
  })

  it('supports i18n translations', async () => {
    // 切换语言
    await wrapper.vm.$i18n.locale = 'en'
    expect(wrapper.find('.title').text()).toBe('Register')
    expect(wrapper.find('.username-label').text()).toBe('Username')
    
    await wrapper.vm.$i18n.locale = 'zh-CN'
    expect(wrapper.find('.title').text()).toBe('注册')
    expect(wrapper.find('.username-label').text()).toBe('用户名')
  })

  it('adapts to theme changes', async () => {
    // 切换暗色主题
    await wrapper.vm.$theme.setTheme('dark')
    expect(wrapper.classes()).toContain('theme-dark')
    
    // 切换亮色主题
    await wrapper.vm.$theme.setTheme('light')
    expect(wrapper.classes()).toContain('theme-light')
  })

  it('handles responsive layout', async () => {
    // 模拟移动端视图
    Object.defineProperty(window, 'innerWidth', { value: 375 })
    window.dispatchEvent(new Event('resize'))
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.mobile-view').exists()).toBeTruthy()
    
    // 模拟桌面视图
    Object.defineProperty(window, 'innerWidth', { value: 1024 })
    window.dispatchEvent(new Event('resize'))
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.desktop-view').exists()).toBeTruthy()
  })

  it('handles password confirmation mismatch', async () => {
    await wrapper.setData({
      formState: {
        password: 'ValidPass123',
        confirmPassword: 'DifferentPass123'
      }
    })
    await wrapper.vm.validateConfirmPassword()
    expect(message.error).toHaveBeenCalledWith('两次输入的密码不一致')
  })

  it('handles server validation errors', async () => {
    // 模拟服务器返回的验证错误
    jest.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({
        errors: {
          username: ['用户名包含非法字符'],
          email: ['邮箱格式不正确']
        }
      })
    })
    
    await wrapper.find('form').trigger('submit')
    expect(wrapper.vm.formErrors).toEqual({
      username: ['用户名包含非法字符'],
      email: ['邮箱格式不正确']
    })
  })

  it('handles all form field validations', async () => {
    const fields = ['username', 'email', 'password', 'confirmPassword', 'captcha']
    for (const field of fields) {
      await wrapper.setData({
        formState: { [field]: '' }
      })
      await wrapper.vm.validateField(field)
      expect(wrapper.vm.formErrors[field]).toBeTruthy()
    }
  })

  it('handles captcha refresh failure', async () => {
    // 模拟验证码刷新失败
    jest.spyOn(global, 'fetch').mockRejectedValueOnce(new Error('Failed to refresh captcha'))
    
    await wrapper.find('.refresh-captcha').trigger('click')
    expect(message.error).toHaveBeenCalledWith('验证码刷新失败，请重试')
  })

  it('handles form submission with all possible states', async () => {
    // 测试所有可能的表单状态
    const testStates = [
      {
        state: { loading: true },
        expectation: 'should not submit when loading'
      },
      {
        state: { hasErrors: true },
        expectation: 'should not submit with errors'
      },
      {
        state: { isComplete: false },
        expectation: 'should not submit when incomplete'
      }
    ]

    for (const { state, expectation } of testStates) {
      await wrapper.setData(state)
      await wrapper.find('form').trigger('submit')
      expect(wrapper.vm.submitForm).not.toHaveBeenCalled()
    }
  })

  it('handles all theme variants', async () => {
    const themes = ['light', 'dark', 'custom']
    for (const theme of themes) {
      await wrapper.vm.$theme.setTheme(theme)
      expect(wrapper.classes()).toContain(`theme-${theme}`)
      
      // 验证所有主题相关的样式
      const elements = ['input', 'button', 'form']
      for (const el of elements) {
        expect(wrapper.find(el).classes()).toContain(`${theme}-element`)
      }
    }
  })

  it('handles all responsive breakpoints', async () => {
    const breakpoints = [
      { width: 320, expected: 'mobile' },
      { width: 768, expected: 'tablet' },
      { width: 1024, expected: 'desktop' },
      { width: 1440, expected: 'wide' }
    ]

    for (const { width, expected } of breakpoints) {
      Object.defineProperty(window, 'innerWidth', { value: width })
      window.dispatchEvent(new Event('resize'))
      await wrapper.vm.$nextTick()
      expect(wrapper.find(`.${expected}-view`).exists()).toBeTruthy()
    }
  })

  it('handles all i18n translations', async () => {
    const locales = ['zh-CN', 'en', 'ja']
    const elements = [
      { selector: '.title', key: 'register.title' },
      { selector: '.username-label', key: 'register.username' },
      { selector: '.submit-button', key: 'register.submit' }
    ]

    for (const locale of locales) {
      await wrapper.vm.$i18n.locale = locale
      for (const { selector, key } of elements) {
        expect(wrapper.find(selector).text()).toBe(wrapper.vm.$t(key))
      }
    }
  })

  it('handles all form interactions in sequence', async () => {
    // 测试完整的表单交互流程
    const interactions = [
      {
        action: () => wrapper.find('input[name="username"]').setValue('testuser'),
        expect: () => expect(wrapper.vm.formState.username).toBe('testuser')
      },
      {
        action: () => wrapper.find('input[name="email"]').setValue('test@example.com'),
        expect: () => expect(wrapper.vm.formState.email).toBe('test@example.com')
      },
      {
        action: () => wrapper.find('input[name="password"]').setValue('Test123456'),
        expect: () => expect(wrapper.vm.formState.password).toBe('Test123456')
      },
      {
        action: () => wrapper.find('input[name="confirmPassword"]').setValue('Test123456'),
        expect: () => expect(wrapper.vm.formState.confirmPassword).toBe('Test123456')
      },
      {
        action: () => wrapper.find('input[name="captcha"]').setValue('1234'),
        expect: () => expect(wrapper.vm.formState.captcha).toBe('1234')
      }
    ]

    for (const { action, expect } of interactions) {
      await action()
      expect()
      await wrapper.vm.$nextTick()
    }
  })

  describe('Event Handling', () => {
    it('emits register-success event on successful registration', async () => {
      await wrapper.setData({
        formState: {
          username: 'testuser',
          email: 'test@example.com',
          password: 'Test123456',
          confirmPassword: 'Test123456',
          captcha: '1234'
        }
      })

      // 模拟成功注册
      jest.spyOn(global, 'fetch').mockResolvedValueOnce({
        ok: true,
        json: async () => ({ token: 'test-token' })
      })

      await wrapper.vm.submitForm()
      expect(wrapper.emitted('register-success')).toBeTruthy()
      expect(wrapper.emitted('register-success')[0]).toEqual([{ token: 'test-token' }])
    })

    it('handles form field focus and blur events', async () => {
      const fields = ['username', 'email', 'password', 'confirmPassword']
      
      for (const field of fields) {
        const input = wrapper.find(`input[name="${field}"]`)
        
        // Focus event
        await input.trigger('focus')
        expect(wrapper.vm.focusedField).toBe(field)
        
        // Blur event with validation
        await input.trigger('blur')
        expect(wrapper.vm.validateField).toHaveBeenCalledWith(field)
      }
    })

    it('handles password visibility toggle', async () => {
      const passwordInput = wrapper.find('input[name="password"]')
      const toggleButton = wrapper.find('.password-toggle')
      
      await toggleButton.trigger('click')
      expect(passwordInput.attributes('type')).toBe('text')
      
      await toggleButton.trigger('click')
      expect(passwordInput.attributes('type')).toBe('password')
    })
  })

  describe('Form Validation States', () => {
    it('tracks field validation states correctly', async () => {
      const validationStates = {
        username: { value: 'test', isValid: true },
        email: { value: 'invalid', isValid: false },
        password: { value: 'weak', isValid: false },
        confirmPassword: { value: 'different', isValid: false }
      }

      for (const [field, state] of Object.entries(validationStates)) {
        await wrapper.setData({
          formState: { [field]: state.value }
        })
        await wrapper.vm.validateField(field)
        expect(wrapper.vm.fieldStates[field].isValid).toBe(state.isValid)
      }
    })

    it('updates form completion status correctly', async () => {
      // 初始状态
      expect(wrapper.vm.isFormComplete).toBe(false)

      // 填写所有必填字段
      await wrapper.setData({
        formState: {
          username: 'testuser',
          email: 'test@example.com',
          password: 'Test123456',
          confirmPassword: 'Test123456',
          captcha: '1234'
        }
      })

      expect(wrapper.vm.isFormComplete).toBe(true)

      // 清空一个字段
      await wrapper.setData({
        formState: {
          ...wrapper.vm.formState,
          email: ''
        }
      })

      expect(wrapper.vm.isFormComplete).toBe(false)
    })
  })

  describe('Accessibility Features', () => {
    it('supports keyboard navigation', async () => {
      const inputs = wrapper.findAll('input')
      
      // 测试Tab键导航
      for (let i = 0; i < inputs.length; i++) {
        await inputs[i].trigger('keydown.tab')
        expect(document.activeElement).toBe(inputs[i + 1]?.element || wrapper.find('button').element)
      }
    })

    it('provides proper ARIA attributes', () => {
      const form = wrapper.find('form')
      expect(form.attributes('aria-live')).toBe('polite')
      
      const errorMessages = wrapper.findAll('[aria-invalid="true"]')
      errorMessages.forEach(msg => {
        expect(msg.attributes('role')).toBe('alert')
      })
    })
  })

  describe('Performance Optimization', () => {
    it('debounces username availability check', async () => {
      jest.useFakeTimers()
      
      const usernameInput = wrapper.find('input[name="username"]')
      await usernameInput.setValue('t')
      await usernameInput.setValue('te')
      await usernameInput.setValue('tes')
      await usernameInput.setValue('test')
      
      expect(wrapper.vm.checkUsername).not.toHaveBeenCalled()
      
      jest.runAllTimers()
      expect(wrapper.vm.checkUsername).toHaveBeenCalledTimes(1)
      expect(wrapper.vm.checkUsername).toHaveBeenCalledWith('test')
    })

    it('optimizes form rerender performance', async () => {
      const renderSpy = jest.spyOn(wrapper.vm, '$forceUpdate')
      
      // 快速更新多个字段
      await wrapper.setData({
        formState: {
          username: 'test',
          email: 'test@example.com'
        }
      })
      
      expect(renderSpy).toHaveBeenCalledTimes(1)
    })
  })
}) 