<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { adminLogin} from "@/api/api.ts"; // 引入loginUser接口
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
const admin_id = ref('');


// 密码登录处理
const handlePasswordLogin = async () => {
  try {
  // 发送请求到后端登录接口
    const response = await adminLogin(phone.value, password.value);
    console.log('完整响应：', response)           // 打印完整响应对象，直接就是个data了
    if (response.code === '0') {  // 后端返回登录成功
      const admin_id =  response.admin_id ;
      await router.push('/admin')  // 登录成功后跳转到主页面
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
      <h2>管理员登录</h2>
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


      <!-- 登录按钮 -->
      <button type="submit" class="submit-btn">立即登录</button>
    </form>

  </div>
</template>

<style src="@/assets/styles/Login.css"></style>
