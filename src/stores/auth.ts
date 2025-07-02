import { defineStore } from 'pinia'
import { ref } from 'vue'

// 定义用户信息接口（根据实际后端返回结构调整字段）
interface UserInfo {
  id: number
  username: string
  email: string
  registration_date: string
  days?: number // 计算出的注册天数
}

// 定义 Store
export const useAuthStore = defineStore('auth', () => {
  // 登录状态，初始化时根据 localStorage 判断是否存在 JWT
  const isLoggedIn = ref<boolean>(!!localStorage.getItem('jwt'))

  // JWT 令牌
  const token = ref<string | null>(localStorage.getItem('jwt'))

  // 用户信息
  const userInfo = ref<UserInfo | null>(null)

  /**
   * 登录方法，传入 JWT 并尝试获取用户信息
   * @param jwt - 登录成功后获取的 JWT 字符串
   */
  const login = async (jwt: string): Promise<void> => {
  // 开发阶段的测试 token 直接放行，不 fetch
  if (jwt === 'fake.jwt.token') {
    isLoggedIn.value = true
    token.value = jwt
    localStorage.setItem('jwt', jwt)
    userInfo.value = {
      id: 0,
      username: '测试用户',
      email: 'test@example.com',
      registration_date: new Date().toISOString(),
      days: 0
    }
    return
  }
  // 正常 JWT 处理逻辑
  if (typeof jwt !== 'string' || jwt.split('.').length !== 3) {
    console.error('无效的令牌格式')
    logout()
    return
  }

  isLoggedIn.value = true
  token.value = jwt
  localStorage.setItem('jwt', jwt)

  try {
    await fetchUserInfo()
  } catch (error) {
    console.error('登录后验证失败:', error)
    logout()
  }
}


  /**
   * 登出方法，清除本地存储和状态
   */
  const logout = (): void => {
    isLoggedIn.value = false
    token.value = null
    userInfo.value = null
    localStorage.removeItem('jwt')
  }

  /**
   * 从本地存储初始化 token 和登录状态（页面刷新时自动调用）
   */
  const initialize = (): void => {
    const savedToken = localStorage.getItem('jwt')
    if (savedToken) {
      token.value = savedToken
      isLoggedIn.value = true
    }
  }

  /**
   * 获取用户信息（请求需携带 Authorization 头）
   */
  const fetchUserInfo = async (): Promise<void> => {
    try {
      const response = await fetch('/api/user-info', {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })

      if (!response.ok) {
        console.error('请求失败，状态码:', response.status)
        logout()
        return
      }

      const { data }: { data: UserInfo } = await response.json()

      // 添加注册天数字段
      const registrationDate = new Date(data.registration_date)
      const today = new Date()
      const diffTime = today.getTime() - registrationDate.getTime()
      data.days = Math.floor(diffTime / (1000 * 60 * 60 * 24))

      userInfo.value = data
    } catch (error) {
      console.error('用户信息获取失败:', error)
      logout()
    }
  }

  // 模块加载时自动初始化
  initialize()

  // 返回状态和方法
  return {
    isLoggedIn,
    token,
    userInfo,
    login,
    logout,
    fetchUserInfo
  }
})
