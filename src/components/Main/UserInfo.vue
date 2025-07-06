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
        <UserInfo3  form=""/>
      </h1>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUserStore } from "@/stores/userStore.js";
import { get_personalInfo } from "@/api/api.js";
import UserInfo1 from './UserInfo1.vue';
import UserInfo2 from './UserInfo2.vue';
import UserInfo3 from "./UserInfo3.vue";

// 获取用户信息
const userStore = useUserStore();
const token = userStore.token;
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


// 更新用户信息
const updateUserInfo = (updatedData: any) => {
  UserInfo.value.avatarUrl = updatedData.avatar || '';
  UserInfo.value.userName = updatedData.nickname || '';
  UserInfo.value.gender = updatedData.sex === 1 ? '男' : '女';
  UserInfo.value.email = updatedData.email || '';
  UserInfo.value.personalNote = updatedData.note || '';
  UserInfo.value.height = updatedData.height || '';
  UserInfo.value.weight = updatedData.weight || '';
  UserInfo.value.registrationDate = updatedData.register_time || '';
  UserInfo.value.location = updatedData.location || '';
};

// 在组件挂载后获取个人信息
onMounted(async () => {
  try {
    const personalInfo = await get_personalInfo(user_id); // 获取个人信息
    console.log(personalInfo.user_info)
    updateUserInfo(personalInfo.user_info);  // 更新用户信息
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
