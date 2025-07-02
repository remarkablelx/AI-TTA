<script setup lang="ts">
import { useRouter } from 'vue-router'
import Logo from '@/components/Home/Logo.vue'

// 获取路由实例
const router = useRouter()

// 跳转到主页面
const goToAnalysis = () => {
  router.push('/main')
}

// 跳转到登录或注册页面
const goToLogin = () => {
  router.push('/login')
}
</script>

<template>
  <div class="welcome-container">
    <!-- 内容容器 -->
    <div class="content-wrapper">
      <!-- 主标题 -->
      <h1 class="main-title">
        <logo />
      </h1>
      <!-- 副标题 -->
      <p class="subtitle">智能乒乓球运动分析与可视化系统</p>

      <!-- 操作按钮组 -->
      <div class="action-buttons">
       <button class="btn analysis-btn" @click="goToAnalysis">开 始 分 析</button>
        <button class="btn login-btn" @click="goToLogin">登录 / 注册</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
@import "@/assets/styles/Home.css";
</style>