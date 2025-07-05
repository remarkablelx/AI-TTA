<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import logo from "@/components/Home/Logo.vue";
import { getCaptcha, set_password } from "@/api/api.js";
import { useUserStore } from '@/stores/userStore.js';  // 导入状态管理

const router = useRouter()
const newPassword = ref('')
const confirmPassword = ref('')
const phone = ref('');              // 手机号
const smsCode = ref('');            // 用户输入验证码
const captchaId = ref('');          // 验证码 ID
const captchaText = ref('');        // 验证码文本

// 获取用户 store 和 token
const userStore = useUserStore();
const token = userStore.token; // 获取 token

// 获取验证码
const getSmsCode = async () => {
  try {
    const captchaResponse = await getCaptcha();  // 请求验证码
    console.log('验证码请求响应:', captchaResponse);
    if (captchaResponse.code !== '0') {
      console.log('验证码获取失败');
      return;
    } else {
      alert('您的验证码是：' + captchaResponse.captcha_text);
    }
    // 存储验证码信息
    captchaId.value = captchaResponse.captcha_id;
    captchaText.value = captchaResponse.captcha_text;
  } catch (error) {
    console.error('验证码报错:', error);
    alert('验证码报错');
  }
};

// 重置密码请求
const handleReset = async () => {
  if (newPassword.value !== confirmPassword.value) {
    alert('两次输入的密码不一致')
    return
  }

  if (!newPassword.value || !confirmPassword.value || !phone.value || !smsCode.value) {
    alert('请填写所有必填项')
    return
  }

  // 调用后端接口修改密码
  try {
    const response = await set_password({
      token: token,
      captcha_id: captchaId.value,
      sms_code: smsCode.value,
    })

    if (response.code === '0') {
      alert('密码修改成功')
      await router.push('/login')
    } else {
      alert('密码修改失败: ' + response.message)
    }
  } catch (error) {
    console.error('修改密码错误:', error)
    alert('修改密码失败，请重试')
  }
}
</script>





<template>
  <div class="login-container">
    <div class="login-header">
      <h1><logo /></h1>
    </div>
    <div class="login-header">
      <h2>重置密码</h2>
    </div>

    <form @submit.prevent="handleReset">
      <div class="form-group">
        <input
          type="tel"
          v-model="phone"
          placeholder="请输入注册手机号"
          required
        >
      </div>

      <div class="form-group">
        <div class="sms-input">
          <input
            type="text"
            v-model="smsCode"
            placeholder="验证码"
            required
          >
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

      <div class="form-group">
        <input
          type="password"
          v-model="newPassword"
          placeholder="设置新密码"
          required
        >
      </div>

      <div class="form-group">
        <input
          type="password"
          v-model="confirmPassword"
          placeholder="确认新密码"
          required
        >
      </div>

      <button type="submit" class="submit-btn">重置密码</button>
    </form>

    <div class="footer-links">
      <router-link to="/login">返回登录</router-link>
    </div>
  </div>
</template>

<style scoped src="@/assets/styles/login.css"></style>