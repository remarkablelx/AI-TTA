<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { registerUser } from '@/api/api';  // 引入 registerUser 方法

// 获取路由
const router = useRouter();

// 定义表单字段的响应式变量
const phone = ref('');              // 手机号
const password = ref('');           // 密码
const confirmPassword = ref('');    // 确认密码
const smsCode = ref('');            // 短信验证码
const captchaId = ref('');          // 验证码 ID
const captchaText = ref('');        // 验证码文本
const countdown = ref(0);           // 倒计时，用于验证码按钮的冷却时间

// 获取短信验证码的逻辑
const getSmsCode = async () => {
  const phoneRegex = /^(?:(?:\+|00)86)?1[3-9]\d{9}$/;
  if (!phoneRegex.test(phone.value)) {
    alert('请输入有效的手机号码');
    return;
  }

  // 假设你已经通过后端获取到验证码 ID 和验证码文本
  // 示例：
  captchaId.value = 'some-captcha-id';
  captchaText.value = 'some-captcha-text';

  // 设置倒计时 60 秒
  countdown.value = 60;
  const timer = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) clearInterval(timer);  // 倒计时结束后清除定时器
  }, 1000);
};

// 注册提交处理逻辑
const handleRegister = async () => {
  // 检查两次密码是否一致
  if (password.value !== confirmPassword.value) {
    alert('两次输入的密码不一致');
    return;
  }

  // 调用注册 API
  try {
    const response = await registerUser(phone.value, password.value, captchaId.value, captchaText.value);
    if (response.code === '0') {
      alert('注册成功');
      await router.push('/login'); // 注册成功后跳转到登录页面
    } else {
      alert(`注册失败: ${response.message}`);
    }
  } catch (error) {
    console.error('注册请求失败', error);
    alert('注册请求失败');
  }
};
</script>

<template>
  <div class="login-container">
    <!-- 页面顶部 Logo 区域 -->
    <div class="login-header">
      <h1><logo /></h1>
    </div>

    <!-- 注册标题 -->
    <div class="login-header">
      <h2>用户注册</h2>
    </div>

    <!-- 注册表单 -->
    <form @submit.prevent="handleRegister">
      <!-- 手机号输入框 -->
      <div class="form-group">
        <input
          type="tel"
          v-model="phone"
          placeholder="请输入手机号"
          required
        />
      </div>

      <!-- 设置密码输入框 -->
      <div class="form-group">
        <input
          type="password"
          v-model="password"
          placeholder="设置登录密码"
          required
        />
      </div>

      <!-- 确认密码输入框 -->
      <div class="form-group">
        <input
          type="password"
          v-model="confirmPassword"
          placeholder="确认登录密码"
          required
        />
      </div>

      <!-- 验证码输入和获取按钮 -->
      <div class="form-group">
        <div class="sms-input">
          <input
            type="text"
            v-model="smsCode"
            placeholder="验证码"
            required
          />
          <!-- 验证码按钮：在倒计时期间禁用 -->
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

      <!-- 注册提交按钮 -->
      <button type="submit" class="submit-btn">立即注册</button>
    </form>

    <!-- 跳转到登录页面的链接 -->
    <div class="footer-links">
      <router-link to="/login">已有账号 ? 立即登录</router-link>
    </div>
  </div>
</template>

<style scoped src="@/assets/styles/login.css"></style>
