<template>
  <div>
    <!-- 四个按钮容器 -->
    <div class="button-container">
      <button class="action-button" @click="handleLogout">注销账号</button>
      <button class="action-button" @click="handleChangePassword">修改密码</button>
      <button class="action-button" @click="showEditModal = true">编辑信息</button>
      <button class="action-button" @click="handleLogout">退出登录</button>
    </div>

    <!-- 弹窗：注销账号 -->
    <div v-if="showLogoutModal" class="overlay">
      <div class="popup">
        <div class="popup-header">
          <h2>注销账号</h2>
          <button class="close" @click="closeLogoutModal">&times;</button>
        </div>
        <div class="popup-body">
          <!-- 验证码输入框和按钮 -->
          <input
            type="text"
            v-model="captchaInput"
            placeholder="请输入验证码"
            class="captcha-input"
          />
          <button @click="getSmsCode" class="action-button">获取验证码</button>
        </div>
        <div class="popup-footer">
          <button @click="confirmLogout" class="action-button">确认注销</button>
          <button @click="closeLogoutModal" class="action-button">取消注销</button>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import { ref } from 'vue';
import { getCaptcha, cancel_account } from "@/api/api.ts";
import { useUserStore } from '@/stores/userStore.js';  // 导入状态管理
import { useRouter } from 'vue-router';  // 引入 Vue Router
// 路由实例，用于跳转页面

export default {
  setup() {
    const router = useRouter()
    // 获取用户 store 和 token
    const userStore = useUserStore();
    const token = userStore.token; // 获取 token

    // 状态管理
    const showLogoutModal = ref(false);  // 控制弹窗显示
    const captchaInput = ref('');        // 验证码输入
    const captchaId = ref('');           // 用于存储验证码 ID
    const captchaText = ref('');         // 用于存储验证码文本

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

    // 注销账号
    const confirmLogout = async () => {
      // 在此进行注销账号的实际操作
      try {
        const response = await cancel_account(token,captchaId.value, captchaInput.value);  // 假设注销接口是 cancel_account
        if (response.code === '0') {
          alert('注销成功');
          closeLogoutModal(); // 关闭模态框
        } else {
          alert('注销失败');
        }
      } catch (error) {
        console.error('注销失败:', error);
        alert('注销失败');
      }
    };

    // 关闭模态框
    const closeLogoutModal = () => {
      showLogoutModal.value = false;
      captchaInput.value = ''; // 清空验证码输入框
    };

    // 显示注销模态框
    const handleLogout = () => {
      showLogoutModal.value = true;
    };

    // 处理修改密码按钮点击事件，跳转到修改密码页面
    const handleChangePassword = () => {
      router.push('/change');  // 路由跳转到修改密码页面
    };

    return {
      showLogoutModal,
      captchaInput,
      getSmsCode,
      confirmLogout,
      closeLogoutModal,
      handleLogout,
      handleChangePassword,
    };
  },
};
</script>



<style scoped>
/* 遮罩层 */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);  /* 半透明黑色背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 使遮罩层位于最上层 */
}

/* 弹窗样式 */
.popup {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards; /* 弹窗上滑动画 */
  position: relative;
}

/* 弹窗头部 */
.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.popup-header h2 {
  margin: 0;
  color: #2c3e50;
  font-weight: 600;
}

/* 验证码输入区域（验证码 + 按钮并排） */
.sms-input {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* 验证码输入框样式 */
.captcha-input {
  flex: 1;
  padding: 12px;
  border: 2px solid #ecf0f1;
  border-radius: 8px;
  font-size: 15px;
  transition: border-color 0.3s ease, transform 0.3s ease;
}

.captcha-input:focus {
  outline: none;
  border-color: #2c3e50;
  transform: translateY(-1px); /* 向上微动 */
}

/* 获取验证码按钮样式 */
.sms-btn {
  padding: 10px 14px;
  background: #2d3436;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  font-size: 14px;
}

.close {
  font-size: 25px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  background: transparent;
}

/* 弹窗正文 */
.popup-body {
  margin: 20px 0;
}

.captcha-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* 弹窗底部按钮 */
.popup-footer {
  display: flex;
  justify-content: space-between;
}

.action-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: black;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-button:hover {
  background-color: #333;
}

.button-container {
  display: flex;
  justify-content: space-between; /* 水平排列按钮 */
  gap: 20px; /* 按钮间距，可以修改为你希望的大小 */
  background-color: white; /* 背景色设置为白色 */
  padding: 20px; /* 增加内边距 */
  border-radius: 10px; /* 圆角 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 轻微阴影 */
}

.action-button {
  padding: 12px 24px; /* 可以根据需要调整按钮的大小 */
  border: none;
  border-radius: 20px; /* 按钮圆角 */
  background-color: black; /* 按钮背景色设置为黑色 */
  color: white; /* 文字颜色为白色 */
  font-size: 16px; /* 字体大小 */
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease; /* 添加平滑过渡效果 */
}

.action-button:hover {
  background-color: #333; /* 鼠标悬停时背景颜色 */
  transform: translateY(-5px); /* 鼠标悬停时轻微上浮 */
}
</style>


