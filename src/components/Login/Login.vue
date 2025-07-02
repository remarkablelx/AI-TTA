<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Pinia 认证状态
import { useAuthStore } from '@/stores/auth'

// 发送请求的库
import axios from 'axios'

// 应用 Logo 组件
import logo from '@/components/Home/Logo.vue'

// 路由实例，用于跳转页面
const router = useRouter()

// 登录方式：'password' 或 'sms'
const loginType = ref<'password' | 'sms'>('password')

// 表单输入项
const phone = ref('')       // 手机号
const password = ref('')    // 密码
const smsCode = ref('')     // 验证码

// 验证码倒计时（秒）
const countdown = ref(0)

//发送短信验证码
const getSmsCode = async () => {
  try {
    const response = await axios.post('/api/send_sms', { phone: phone.value })
    if (response.data.success) {
      // 启动倒计时 60 秒
      countdown.value = 60
      const timer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) clearInterval(timer)
      }, 1000)
    }
  } catch (error: any) {
    alert(error.response?.data.message || '发送验证码失败')
  }
}

// 登录提交处理（根据登录方式处理密码或验证码）

const handleSubmit = async () => {
  // ✅ 写死测试账号和密码（开发阶段使用）
  const TEST_PHONE = '1'
  const TEST_PASSWORD = '1'

  if (
    loginType.value === 'password' &&
    phone.value === TEST_PHONE &&
    password.value === TEST_PASSWORD
  ) {
    // 模拟后端返回 token
    const fakeToken = 'fake.jwt.token'

    const authStore = useAuthStore()
    await authStore.login(fakeToken)
    // 登录后跳转到main界面
    console.log('登录成功，准备跳转到 /main')
    await router.push('/main')
    console.log('router.currentRoute:', router.currentRoute.value)
    return
  }

  // ⛔ 其他情况调用真实接口
  try {
    const payload: any = {
      phone: phone.value,
      type: loginType.value
    }

    if (loginType.value === 'password') {
      payload.password = password.value
    } else {
      payload.sms_code = smsCode.value
    }

    const response = await axios.post('/api/password_login', payload)

    if (response.data.success) {
      const authStore = useAuthStore()
      await authStore.login(response.data.token)
      await router.push('/main')
    } else {
      alert(response.data.message)
    }
  } catch (error: any) {
    alert(error.response?.data.message || '登录失败')
  }
}
</script>

<template>
  <div class="login-container">
    <!-- 顶部 Logo 区域 -->
    <div class="login-header">
      <h1>
        <logo />
      </h1>
    </div>
    <div class="login-header">
      <h2>用户登录</h2>
    </div>

    <!-- 登录方式切换 -->
    <div class="login-tabs">
      <button
        class="tab"
        :class="{ active: loginType === 'password' }"
        @click="loginType = 'password'"
      >
        密码登录
      </button>
      <button
        class="tab"
        :class="{ active: loginType === 'sms' }"
        @click="loginType = 'sms'"
      >
        验证码登录
      </button>
    </div>

    <!-- 登录表单 -->
    <form @submit.prevent="handleSubmit">
      <!-- 手机号输入 -->
      <div class="form-group">
        <input
          type="tel"
          v-model="phone"
          placeholder="请输入手机号"
          required
        >
      </div>

      <!-- 密码输入 -->
      <div class="form-group" v-if="loginType === 'password'">
        <input
          type="password"
          v-model="password"
          placeholder="请输入密码"
          required
        >
      </div>

      <!-- 验证码输入 -->
      <div class="form-group" v-if="loginType === 'sms'">
        <div class="sms-input">
          <input
            type="text"
            v-model="smsCode"
            placeholder="验证码"
            required
          >
          <!-- 验证码按钮，倒计时期间禁用 -->
          <button
            type="button"
            class="sms-btn"
            :disabled="countdown > 0"
            @click="getSmsCode"
          >
            {{ countdown ? `${countdown}s` : '获取验证码' }}
          </button>
        </div>
      </div>

      <!-- 登录按钮 -->
      <button type="submit" class="submit-btn">立即登录</button>
    </form>

    <!-- 底部链接：忘记密码 / 注册 -->
    <div class="footer-links">
      <router-link to="/change">忘记密码</router-link>
      <router-link to="/register">注册账号</router-link>
    </div>
  </div>
</template>

<style src="@/assets/styles/Login.css"></style>
