<template>
  <div class="user-info-container">
    <!-- 显示 UserInfo1 组件 -->
    <UserInfo1
      class="user-info-1"
      :avatarUrl="UserInfo.avatarUrl"
      :userName="UserInfo.userName"
      :gender="UserInfo.gender"
      :phonenumber="UserInfo.phonenumber"
      :email="UserInfo.email"
      :personalNote="UserInfo.personalNote"
    />

    <!-- 显示 UserInfo2 组件 -->
    <UserInfo2
      class="user-info-2"
      :avatarUrl="UserInfo.avatarUrl"
      :userName="UserInfo.userName"
      :gender="UserInfo.gender"
      :height="UserInfo.height"
      :weight="UserInfo.weight"
      :email="UserInfo.email"
      :location="UserInfo.location"
      :phonenumber="UserInfo.phonenumber"
      :personalNote="UserInfo.personalNote"
      :registrationDate="UserInfo.registrationDate"
    />
      <h1>
        <UserInfo3 :userInfo="UserInfo" />
      </h1>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUserStore } from "@/stores/userStore.ts";
import {get_avatar, get_personalInfo} from "@/api/api.ts";
import UserInfo1 from './UserInfo1.vue';
import UserInfo2 from './UserInfo2.vue';
import UserInfo3 from "./UserInfo3.vue";

// 获取用户信息
const userStore = useUserStore();
const user_id = userStore.userInfo.user_id
const account = userStore.userInfo.account

// 创建响应式数据
const UserInfo = ref({
  avatarUrl: '',
  userName: '',
  gender: '',
  phonenumber: account,
  email: '',
  personalNote: '',
  height: '',
  weight: '',
  registrationDate: '',
  location: ''
});


// 新增：获取头像 URL
const fetchAvatarUrl = async (avatarPath: string) => {
  if (!avatarPath) return '';

  try {
    const blob = await get_avatar(avatarPath);
    return URL.createObjectURL(blob); // 创建 blob URL
  } catch (error) {
    console.error('获取头像失败:', error);
    return ''; // 返回空字符串或默认头像
  }
};

// 新增时间格式化函数
const formatDate = (dateString: string) => {
  if (!dateString) return '';

  try {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    }).replace(/\//g, '-');
  } catch (e) {
    return dateString; // 如果解析失败，返回原始字符串
  }
};

// 更新用户信息（修改后）
const updateUserInfo = async (updatedData: any) => {
  const avatarUrl = await fetchAvatarUrl(updatedData.avatar || '');

  UserInfo.value = {
    avatarUrl,
    userName: updatedData.nickname || '',
    gender: updatedData.sex === 1 ? '男' : '女',
    phonenumber: account,
    email: updatedData.email || '',
    personalNote: updatedData.note || '',
    height: updatedData.height || '',
    weight: updatedData.weight || '',
    registrationDate: formatDate(updatedData.register_time) || '',
    location: updatedData.location || ''
  };
};

// 在组件挂载后获取个人信息
onMounted(async () => {
  try {
    const personalInfo = await get_personalInfo(user_id); // 获取个人信息
    console.log(personalInfo.user_info)
    await updateUserInfo(personalInfo.user_info); // 注意这里加了 await
  } catch (error) {
    console.error('获取个人信息失败:', error);
  }
});
</script>


<style scoped>
.user-info-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.user-info-container > div {
  margin-bottom: 20px;
}

.user-info-1, .user-info-2 {
  width: 100%;
  max-width: 2000px;
  min-width: 1200px;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
}
h1 {
  margin-top: 30px; /* 增加UserInfo3上方的间距 */
}
</style>
