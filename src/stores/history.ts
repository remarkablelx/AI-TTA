import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'

// 定义历史记录项的类型
interface HistoryItem {
  id: number
  user_id: number
  video_id: number
  time: string
  status: string
  expiry: string
}

// 模拟数据生成器
const generateMockData = (): HistoryItem[] => {
  const baseTime = Date.now();
  return Array.from({ length: 5 }, (_, i) => ({
    id: i + 1,
    time: new Date(baseTime + i * 1000).toLocaleString(),
    status: i === 0 ? 'expired' : (i === 4 ? 'processing' : 'completed'),
    expiry: "2024-03-20",
    user_id: 1,  // 示例字段
    video_id: 101  // 示例字段
  }));
}

export const useHistoryStore = defineStore('history', () => {
  const auth = useAuthStore()

  // 状态变量
  const historyItems = ref<HistoryItem[]>([])  // 历史记录数组
  const currentAnalysisId = ref<number | null>(null)  // 当前分析ID
  const isLoading = ref<boolean>(false)  // 加载状态
  const error = ref<string | null>(null)  // 错误信息

  // 设置当前分析ID
  const setCurrentAnalysisId = (id: number | null): void => {
    currentAnalysisId.value = id
  }

  // 获取历史记录数据（开发环境使用模拟数据，生产环境使用真实数据）
  const fetchHistory = async (): Promise<void> => {
    try {
      isLoading.value = true

      // 开发环境：使用模拟数据
      if (import.meta.env.MODE === 'development') {
        await new Promise(resolve => setTimeout(resolve, 500))
        historyItems.value = generateMockData()

        // 设置默认选择最新的非 processing 状态的记录
        if (historyItems.value.length > 0) {
          const validRecords = historyItems.value
            .filter(item => item.status !== 'processing')
            .sort((a, b) => b.id - a.id)

          currentAnalysisId.value = validRecords[0]?.id || null
        }

        error.value = null
        return
      }

      // 生产环境：通过 API 获取历史记录
      const response = await fetch('/api/history', {
        headers: {
          Authorization: `Bearer ${auth.token}`
        }
      })

      if (!response.ok) {
        const { message } = await response.json()
        error.value = message || '获取历史记录失败'
        return
      }

      const { data } = await response.json()
      historyItems.value = data.map((item: HistoryItem) => ({
        id: item.id,
        user_id: item.user_id,
        video_id: item.video_id,  // 新增字段映射
        time: item.time,
        status: item.status,
        expiry: item.expiry
      }))

      // 设置默认选择第一条记录
      if (historyItems.value.length > 0) {
        currentAnalysisId.value = historyItems.value[0].id
      }

      error.value = null
    } catch (err) {
      // 错误处理
      if (err instanceof Error) {
        error.value = err.message || '请求失败，请检查网络连接'
      } else {
        error.value = '未知错误，请检查网络连接'
      }
      console.error('获取历史记录失败:', err)
    } finally {
      isLoading.value = false
    }
  }

  // 删除历史记录项
  const deleteItem = async (id: number): Promise<void> => {
    try {
      const targetId = Number(id)

      // 开发环境：模拟删除操作
      if (import.meta.env.MODE === 'development') {
        historyItems.value = historyItems.value.filter(
          item => item.id !== targetId
        )

        // 如果删除的是当前选中的记录，清除选中状态
        if (currentAnalysisId.value === targetId) {
          currentAnalysisId.value = null
        }

        error.value = null
        return
      }

      // 生产环境：发送删除请求
      const response = await fetch(`/api/history/${targetId}`, {  // 修改URL，添加路径参数
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${auth.token}`
        }
      })

      if (!response.ok) {
        let errorMessage = '删除项目失败'
        try {
          // 尝试解析 JSON 错误信息
          const errorData = await response.json()
          errorMessage = errorData.message || errorMessage
        } catch (e) {
          // 当响应不是 JSON 时使用状态文本
          errorMessage = `${response.status} ${response.statusText}`
        }
        error.value = errorMessage
        return
      }

      historyItems.value = historyItems.value.filter(
        item => item.id !== targetId
      )

      // 如果删除的是当前选中的记录，清除选中状态
      if (currentAnalysisId.value === targetId) {
        currentAnalysisId.value = null
      }

      error.value = null
    } catch (err) {
      // 错误处理
      if (err instanceof Error) {
        error.value = err.message || '删除请求失败，请检查网络连接'
      } else {
        error.value = '未知错误，请检查网络连接'
      }
      console.error('删除操作失败:', err)
    }
  }

  return {
    historyItems,
    currentAnalysisId,
    isLoading,
    error,
    setCurrentAnalysisId,
    fetchHistory,
    deleteItem
  }
})
