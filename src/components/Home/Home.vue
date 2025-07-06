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

// 跳转到管理员登录页面
const goToAdminLogin = () => {
  router.push('/adminlogin')
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
        <button class="btn admin-btn" @click="goToAdminLogin">管理员登录</button> <!-- 新增的按钮 -->
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 主容器设置 */
.welcome-container {
  min-height: 80vh;
  display: grid;
  justify-content: center;
  align-items: center;
  background: #ffffff;
}

/* 内容容器 */
.content-wrapper {
  text-align: center;
  padding: 2rem;
  max-width: 800px;
  width: 90%;
}

/* 主标题样式 */
.main-title {
  font-size: 5rem;  /* 增大主标题字体 */
  margin-bottom: 2rem;  /* 调整标题与副标题的间距 */
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
  animation-delay: 0.2s;
}

/* 副标题 */
.subtitle {
  font-size: 1.5rem;  /* 增大副标题字体 */
  color: #636e72;
  margin-bottom: 4rem;  /* 调整副标题与按钮的间距 */
  opacity: 0;
  animation: fadeIn 0.8s ease-out forwards;
  animation-delay: 0.4s;
}

/* 按钮容器 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 2rem;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
  animation-delay: 0.6s;
}

/* 基础按钮样式 */
.btn {
  position: relative;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  padding: 1rem 2rem;  /* 增大按钮内边距，调整为均衡的上下左右间距 */
  font-size: 1.1rem;  /* 调整按钮字体大小，确保按钮内文字不换行 */
  white-space: nowrap; /* 确保文字不会换行 */
  border: none;
  border-radius: 50px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  background: #2d3436;
  color: white;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}

.btn:hover::before {
  transform: scaleX(1);
  transform-origin: left;
}

.btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(45, 52, 54, 0.2);
}

.btn-content {
  position: relative;
  z-index: 1;
}

/* 注册按钮特殊样式 */
.register-btn {
  background: #636e72;
}

.abstract-section {
  display: block;
  width: 100%;
  float: none;
}

/* 动画定义 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }

  .main-title {
    font-size: 2rem;
  }

  .btn {
    padding: 0.8rem 1.5rem;
  }
}
</style>


