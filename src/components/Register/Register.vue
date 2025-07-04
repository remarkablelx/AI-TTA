<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { registerUser, getCaptcha } from '@/api/api';  // 引入 registerUser 方法
import logo from '@/components/Home/Logo.vue'

// 获取路由
const router = useRouter();

// 定义表单字段的响应式变量
const phone = ref('');              // 手机号
const password = ref('');           // 密码
const confirmPassword = ref('');    // 确认密码
const smsCode = ref('');            // 短信验证码
const captchaId = ref('');          // 验证码 ID
const captchaText = ref('');        // 验证码文本


// 获取短信验证码的逻辑
const getSmsCode = async () => {
  const phoneRegex = /^(?:(?:\+|00)86)?1[3-9]\d{9}$/;
  if (!phoneRegex.test(phone.value)) {
    alert('请输入有效的手机号码');
    return;
  }
  try {
    // 请求后端获取验证码 ID 和验证码文本
    const captchaResponse = await getCaptcha();  // 获取验证码
    console.log('验证码请求响应:', captchaResponse);  // 打印整个响应数据

    if (captchaResponse.code !== '0') {
      console.log('验证码获取失败');
      return;
    }
    else{
      alert('您的验证码是：'+captchaResponse.captcha_text)
    }
    // 存储获取到的 captcha_id 和 captcha_text
    captchaId.value = captchaResponse.captcha_id;
    captchaText.value = captchaResponse.captcha_text;
     // 获取短信验证码
  } catch (error) {
    console.error('验证码请求失败:', error);  // 打印完整的错误信息
    alert('验证码请求失败');
  }
};

// 注册提交处理逻辑
const handleRegister = async () => {
  // 检查两次密码是否一致
  if (password.value !== confirmPassword.value) {
    alert('两次输入的密码不一致');
    return;
  }
  // 检查验证码是否为空
  if (!smsCode.value) {
    alert('请输入验证码');
    return;
  }
  // 调用注册 API
  try {
    const response = await registerUser(phone.value, password.value, captchaId.value, smsCode.value);
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
          <input type="text" v-model="smsCode" placeholder="验证码" required />
          <button type="button" class="sms-btn" :disabled="countdown > 0" @click="getSmsCode">
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
