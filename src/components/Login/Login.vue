<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {getCaptcha, password_loginUser, captcha_loginUser} from "@/api/api.ts"; // 引入loginUser接口
// Pinia 认证状态
import { useUserStore } from '@/stores/userStore.ts'
// 发送请求的库
import axios from 'axios'
// 应用 Logo 组件
import logo from '@/components/Home/Logo.vue'



// 路由实例，用于跳转页面
const router = useRouter()
// 登录方式：'password' 或 'sms'
const loginType = ref<'password' | 'sms'>('password')
// 表单输入项
const phone = ref('');              // 手机号
const password = ref('');           // 密码
const smsCode = ref('');            // 用户输入验证码
const captchaId = ref('');          // 验证码 ID
const captchaText = ref('');        // 验证码文本

// 获取验证码
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
    console.error('验证码报错:', error);  // 打印完整的错误信息
    alert('验证码报错');
  }
};


// 密码登录处理
const handlePasswordLogin = async () => {
  try {
  // 发送请求到后端登录接口
    const response = await password_loginUser(phone.value, password.value);
    console.log('完整响应：', response)           // 打印完整响应对象，直接就是个data了
    if (response.code === '0') {  // 后端返回登录成功
      const nickname = response.nickname || '默认昵称';
      const avatar = response.avatar || '默认头像';
      const userStore = useUserStore();
      const user_id = response.user_id || ''; // 获取用户 id


      userStore.setToken(response.token); // 存储 token 和更新登录状态
      userStore.setUserInfo(
        user_id,
        phone.value,
        nickname,
        avatar
      )
      // 打印存储的 token
      console.log(`登录成功111`,userStore.userInfo);
      console.log('登录成功，准备跳转到 /main');
      await router.push('/main')  // 登录成功后跳转到主页面
    } else {
      alert('登录失败111')  // 后端返回的错误信息
    }
  } catch (error: any) {
    alert(error || '登录失败111')  // 网络或其他请求失败时的错误信息
  }
}


// 验证码登录处理
const handleCaptchaLogin = async () => {
  try {
  // 发送请求到后端登录接口
    const response = await captcha_loginUser(phone.value, captchaId.value, smsCode.value);
    console.log('完整响应：', response)           // 打印完整响应对象，直接就是个data了
    if (response.code === '0') {  // 后端返回登录成功
      const nickname = response.nickname || '默认昵称';
      const avatar = response.avatar || '默认头像';
      const token = response.token ;
      const user_id = response.user_id ;
      const userStore = useUserStore();
      userStore.setToken(response.token); // 存储 token 和更新登录状态
      // 打印存储的 token
      console.log('登录成功，存储的 token:', userStore.token);

      console.log(`登录成功，用户名: ${nickname}, 头像: ${avatar}`);
      console.log('登录成功，准备跳转到 /main')

      await router.push('/main')  // 登录成功后跳转到主页面
    } else {
      alert('登录失败111')  // 后端返回的错误信息
    }
  } catch (error: any) {
    alert(error || '登录失败111')  // 网络或其他请求失败时的错误信息
  }
}

// 处理提交表单
const handleSubmit = async () => {
  if (loginType.value === 'password') {
    await handlePasswordLogin();
  } else {
    await handleCaptchaLogin();
  }
};

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
          <!-- 验证码按钮 -->
          <button type="button" class="sms-btn"  @click="getSmsCode">
            获取验证码
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
