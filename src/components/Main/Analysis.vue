<script setup>
import FramePanel from '@/components/Main/FramePanel.vue' // 引入 FramePanel 子组件
import VideoComparator from "@/components/Main/VideoComparator.vue"; // 引入 VideoComparator 子组件
import axios from 'axios' // 引入 axios 用于请求数据

import { computed, ref, watch } from 'vue' // 引入 Vue 相关的函数
import { useHistoryStore } from '@/stores/history.js' // 引入 history store
import { useUserStore } from '@/stores/auth2' // 引入 auth store

const historyStore = useHistoryStore() // 实例化 historyStore，用于管理分析历史数据
const auth = useUserStore() // 实例化 auth，用于获取用户的认证信息
const originalUrl = ref('') // 原始视频的 URL
const processedUrl = ref('') // 处理后视频的 URL
const loading = ref(false) // 加载状态标志
const error = ref(null) // 错误信息
const currentVideoId = ref(null) // 当前视频 ID

// 计算属性：获取当前分析的历史项
const currentAnalysis = computed(() =>
  historyStore.historyItems.find(
    item => item.id === historyStore.currentAnalysisId
  )
)

// 计算属性：格式化时间
const formattedTime = computed(() =>
  currentAnalysis.value
    ? new Date(currentAnalysis.value.time).toLocaleString()
    : ''
)

// 异步函数：获取视频 URL
const fetchVideoUrls = async (videoId) => {
  try {
    loading.value = true // 设置加载状态为 true
    const token = auth.token // 获取用户的 token
    const response = await axios.get(`/api/video/${videoId}`, { // 发送请求获取视频 URL
      headers: {
        Authorization: `Bearer ${token}` // 使用 Bearer Token 进行身份认证
      }
    })

    // 如果请求成功，设置视频源 URL
    if (response.data.success) {
      originalUrl.value = response.data.data.original
      processedUrl.value = response.data.data.processed || '' // 如果没有处理后的视频，设置为空
    }
  } catch (err) {
    // 如果请求失败，设置错误信息
    error.value = err.response?.data?.message || '获取视频地址失败'
  } finally {
    loading.value = false // 请求完成，设置加载状态为 false
  }
}

// 监听 currentAnalysis 的变化，获取新的视频 ID 并调用 fetchVideoUrls 获取视频 URL
watch(() => currentAnalysis.value?.video_id, (newVideoId) => {
  if (newVideoId) {
    fetchVideoUrls(newVideoId) // 调用 fetchVideoUrls 方法
  }
}, { immediate: true }) // 初次执行时立即调用

// 监听 historyStore.currentAnalysisId 的变化，更新 currentVideoId
watch(() => historyStore.currentAnalysisId, (newId) => {
  const analysis = historyStore.historyItems.find(item => item.id === newId)
  currentVideoId.value = analysis?.video_id || null
}, { immediate: true }) // 初次执行时立即调用

// 监听 currentVideoId 的变化，获取新的视频 URL
watch(currentVideoId, (newId) => {
  if (newId) {
    fetchVideoUrls(newId) // 调用 fetchVideoUrls 方法
  }
})
</script>

<!-- Analysis.vue -->
<template>
  <div class="analysis-container">
    <h2 class="section-title">分析汇总界面 - {{ formattedTime }}</h2>
    <div class="content-wrapper">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">加载中...</div>

      <!-- 错误提示 -->
      <div v-if="error" class="error">{{ error }}</div>
      <!-- 视频对比组件，传递原始视频和处理后视频 URL -->
      <VideoComparator
        :original-src="originalUrl"
        :processed-src="processedUrl"
      />
      <!-- 帧面板组件 -->
      <FramePanel />
    </div>
  </div>
</template>

<style scoped>
/* 样式部分 */
.analysis-container {
  flex-direction: row; /* 设置为行布局 */
  max-width: 2000px; /* 最大宽度 */
  min-width: 1200px; /* 最小宽度 */
}

.section-title {
  white-space: nowrap; /* 防止标题换行 */
}

.content-wrapper {
  display: block; /* 设置为块级布局 */
}

/* 加载状态样式 */
.loading {
  color: #666;
  padding: 20px;
}

/* 错误提示样式 */
.error {
  color: #ff4444;
  padding: 10px;
}

/* 响应式设计，当屏幕宽度小于 768px 时 */
@media (max-width: 768px) {
  .analysis-container{
    font-size: 0.8rem;
  }
}
</style>
