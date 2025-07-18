<template>
  <div>
    <!-- 四个按钮容器 -->
    <div class="button-container">
      <button class="action-button" @click="handleLogout">注销账号</button>
      <button class="action-button" @click="handleChangePassword">修改密码</button>
      <button class="action-button" @click="handleEdit">编辑信息</button>
      <button class="action-button" @click="handleCancel">退出登录</button>
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
          <button @click="getSmsCode" class="action-button1">获取验证码</button>
        </div>
        <div class="popup-footer">
          <button @click="confirmLogout" class="action-button">确认注销</button>
          <button @click="closeLogoutModal" class="action-button">取消注销</button>
        </div>
      </div>
    </div>

    <!-- 编辑表单弹窗 -->
    <div v-if="showEditModal" class="overlay">
      <div class="popup2">
        <div class="popup-header2">
            <Logo />
          <button class="close" @click="closeModal">&times;</button>
        </div>
        <div class="popup-body2">
          <form @submit.prevent="handleSubmit">
            <table class="user-info-table">
              <tbody>
                <tr>
                  <td>头像</td>
                  <td>
                    <img :src="form.avatarUrl" alt="用户头像" class="user-avatar" @click="triggerAvatarInput"/>
                    <input
                      type="file"
                      ref="avatarInput"
                      style="display: none;"
                      @change="handleAvatarUpload"
                      accept="image/*"
                    />
                  </td>
                  <td>昵称</td>
                  <td><input type="text" v-model="form.userName" /></td>
                </tr>
                <tr>
                  <td>性别</td>
                  <td><input type="text" v-model="form.gender" /></td>
                  <td>位置</td>
                  <td><input type="text" v-model="form.location" /></td>
                </tr>
                <tr>
                  <td>身高 (cm)</td>
                  <td><input type="number" v-model="form.height" min="0" /></td>
                  <td>体重 (kg)</td>
                  <td><input type="number" v-model="form.weight" min="0" /></td>
                </tr>
                <tr>
                  <td>邮箱</td>
                  <td><input type="email" v-model="form.email" /></td>
                  <td>电话号码</td>
                  <td><input type="text" v-model="form.phonenumber" /></td>
                </tr>
                <tr>
                  <td>个人说明</td>
                  <td colspan="3"><input type="text" v-model="form.personalNote" /></td>
                </tr>
                <tr>
                  <td>注册时间</td>
                  <td colspan="3"><input type="text" v-model="form.registrationDate" disabled /></td>
                </tr>
              </tbody>
            </table>
            <div class="form-actions">
              <button class = action-button2 type="submit">提交</button>
              <button class = action-button2 type="button" @click="closeModal">关闭</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import {getCaptcha, cancel_account, update_personalInfo, get_personalInfo, set_avatar,get_avatar} from "@/api/api.ts";
import { useUserStore } from '@/stores/userStore.ts';  // 导入状态管理
import { useRouter } from 'vue-router';  // 引入 Vue Router
import Logo from "@/components/Home/Logo.vue";

const props = defineProps({
  userInfo: {
    type: Object,
    required: true,
  },
});

// 路由实例，用于跳转页面
const router = useRouter();

// 获取用户 store 和 token
const userStore = useUserStore();
const userInfo = userStore.userInfo
const user_id = userInfo.user_id;


// 状态管理
const showLogoutModal = ref(false); // 控制注销弹窗显示
const showEditModal = ref(false);   // 控制编辑弹窗显示
const captchaInput = ref('');       // 验证码输入
const captchaId = ref('');          // 用于存储验证码 ID
const captchaText = ref('');        // 用于存储验证码文本


// 独立的头像上传 ref
const avatarInput = ref<HTMLInputElement | null>(null);

// 触发头像上传
const triggerAvatarInput = () => {
  avatarInput.value?.click();
};

// 头像上传处理
const handleAvatarUpload = async (event: Event) => {
  const fileInput = event.target as HTMLInputElement;
  if (fileInput.files && fileInput.files[0]) {
    const file = fileInput.files[0];

    try {
      // 1. 上传头像到后端
      const uploadResponse = await set_avatar(file, user_id);

      if (uploadResponse.code === '0') {
        // 2. 获取新头像
        const avatarResponse = await get_avatar(uploadResponse.avatar);

        // 3. 更新表单中的头像URL
        form.value.avatarUrl = URL.createObjectURL(avatarResponse);

        // 4. 可选：更新全局用户信息
        userStore.userInfo.avatarUrl = form.value.avatarUrl;
        alert('头像更新成功');
      } else {
        alert('头像上传失败: ' + uploadResponse.message);
      }
    } catch (error) {
      console.error('头像处理失败:', error);
      alert('头像处理失败');
    }
  }
};

// 定义表单数据类型
interface Form {
  avatarUrl: string;
  userName: string;
  gender: number;
  location: string;
  height: string;
  weight: string;
  email: string;
  phonenumber: string;
  personalNote: string;
  registrationDate: string;
}

// 创建表单数据的响应式变量
const form = ref({ ...props.userInfo });

// 提交编辑表单
const handleSubmit = async () => {
  // 验证手机号
  if (!/^\d{11}$/.test(form.value.phonenumber)) {
    alert("电话号码必须是11位数字");
    return;
  }

  // // 验证性别
  // if (form.value.gender !== 0 && form.value.gender !== 1) {  // 数字验证
  //   alert("性别必须是0（男）或1（女）");
  //   return;
  // }

  // 验证邮箱
  if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$/.test(form.value.email)) {
    alert("邮箱格式必须为 xxx@xxx.com");
    return;
  }

  try {
    // 调用修改个人信息的 API
    const response = await update_personalInfo(
        user_id,
        form.value.userName,
        form.value.avatarUrl,
        form.value.gender,
        form.value.email,
        form.value.personalNote,
        form.value.height,
        form.value.weight,
        form.value.location
    );
    console.log("正在更新个人信息, user_id:", user_id);

    if (response.code === '1') {
      alert('信息更新成功');
      closeModal(); // 关闭编辑弹窗

    } else {
      alert('信息更新失败: ' + response.message);
    }
  } catch (error) {
    console.error('提交失败:', error);
    alert('提交失败');
  }
};

// 关闭编辑弹窗
const closeModal = () => {
  showEditModal.value = false;
};

// 显示编辑模态框并填充数据
const handleEdit = () => {
  // 填充表单数据
  form.value = { ...props.userInfo };
  showEditModal.value = true; // 打开编辑弹窗
};




// 退出登录处理
const handleCancel = () => {
  userStore.token = ''; // 清除 token
  userStore.userInfo = {
    user_id: -1,               // 用户 ID
    account: '',              // 用户账号
    nickname: '',             // 用户昵称
    avatarUrl: '',            // 用户头像 URL
    userName: '',             // 用户姓名
    gender: -1,                // 用户性别，0为女，1为男
    height: '',               // 用户身高
    weight: '',               // 用户体重
    email: '',                // 用户邮箱
    location: '',             // 用户位置
    personalNote: '',         // 用户个人说明
    registrationDate: '',     // 用户注册日期
  };
  // 清除本地存储中的用户信息
  localStorage.removeItem('token');
  localStorage.removeItem('userInfo');

  // 跳转到登录页面
  router.push('/login');
};

// 获取验证码
const getSmsCode = async () => {
  try {
    const captchaResponse = await getCaptcha();  // 请求验证码
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
  try {
    const response = await cancel_account(user_id, captchaId.value, captchaInput.value); // 假设注销接口是 cancel_account
    if (response.code === '0') {
      alert('注销成功');
      closeLogoutModal(); // 关闭模态框
      await router.push('/login');
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
  border-radius: 8px;
  width: 400px; /* 调整为较小的宽度 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
  position: relative;
  margin: auto;
}

.popup-header {
  display: flex;
  justify-content: center; /* 居中标题 */
  align-items: center;
  font-size: 16px; /* 字体稍小 */
  margin-bottom: 15px;
}

.popup-header h2 {
  font-size: 18px; /* 标题字体稍微小一点 */
  margin: 0;
}

.popup2 {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 800px; /* 增加弹窗宽度 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards; /* 弹窗上滑动画 */
  position: relative;
}

/* 弹窗正文 */
.popup-body {
  margin: 20px 0;
}

/* 自定义关闭按钮样式 */
.close {
  font-size: 20px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  background: transparent;
  color: #e74c3c;
  transition: color 0.3s ease;
}

.close:hover {
  color: #c0392b;
}

/* 弹窗底部按钮 */
.popup-footer {
  display: flex;
  justify-content: center; /* 居中按钮 */
  gap: 15px; /* 增加按钮间距 */
  margin-top: 20px;
}

.action-button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background-color: #3498db;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 120px; /* 固定按钮宽度 */
}

.action-button:hover {
  background-color: #2980b9;
  transform: scale(1.05); /* 放大效果 */
}

/* 主按钮容器样式 */
.button-container {
  display: flex;
  justify-content: space-between; /* 水平排列按钮 */
  gap: 20px; /* 按钮间距，可以修改为你希望的大小 */
  background-color: white; /* 背景色设置为白色 */
  padding: 20px; /* 增加内边距 */
  border-radius: 10px; /* 圆角 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 轻微阴影 */
}

/* 按钮样式 */
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

.form-actions {
  display: flex;             /* 使用 Flexbox 来进行布局 */
  justify-content: center;   /* 水平居中按钮 */
  align-items: center;       /* 垂直居中按钮 */
  gap: 10px;                 /* 按钮之间的间距 */
}

.action-button2 {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background-color: black;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 120px; /* 固定按钮宽度 */
}

.action-button2:hover {
  background-color: black;
  transform: scale(1.05); /* 放大效果 */
}
.captcha-input {
  width: 68%; /* 输入框占70%宽度 */
  padding: 10px;
  font-size: 14px; /* 输入框字体小一些 */
  margin-right: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.action-button1 {
  width: 28%; /* 按钮占28%宽度 */
  padding: 10px;
  font-size: 14px; /* 按钮字体小一些 */
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}


.popup-header2 {
  display: flex;           /* 使用 flexbox 来进行布局 */
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
}

.popup-header2 img {
  width: 150px;   /* 设置Logo的宽度 */
  height: auto;   /* 高度自适应 */
}

.user-avatar {
  width: 80px;          /* 设置宽度 */
  height: 80px;         /* 设置高度，与宽度相同 */
  border-radius: 50%;   /* 圆形效果 */
  object-fit: cover;    /* 确保图片填充但不失真 */
  cursor: pointer;      /* 鼠标悬停时显示手型指针 */
  border: 2px solid #ddd; /* 添加边框 */
  transition: all 0.3s ease; /* 平滑过渡效果 */
}

.user-avatar:hover {
  transform: scale(1.05); /* 悬停时轻微放大 */
  box-shadow: 0 0 10px rgba(0,0,0,0.2); /* 添加阴影效果 */
}

</style>
