<template>
  <div class="user-info-container">
    <!-- 显示 UserInfo1 组件 -->
    <UserInfo1
      class="user-info-1"
      :avatarUrl="userInfo.avatarUrl"
      :userName="userInfo.userName"
      :gender="userInfo.gender"
      :phonenumber="userInfo.phonenumber"
      :email="userInfo.email"
      :personalNote="userInfo.personalNote"
    />

    <!-- 显示 UserInfo2 组件 -->
    <UserInfo2
      class="user-info-2"
      :avatarUrl="userInfo.avatarUrl"
      :userName="userInfo.userName"
      :gender="userInfo.gender"
      :height="userInfo.height"
      :weight="userInfo.weight"
      :email="userInfo.email"
      :location="userInfo.location"
      :phonenumber="userInfo.phonenumber"
      :personalNote="userInfo.personalNote"
      :registrationDate="userInfo.registrationDate"
    />
      <h1>
        <UserInfo3  form=""/>
      </h1>
  </div>
</template>

<script>
// 导入 UserInfo1 和 UserInfo2 组件
import UserInfo1 from './UserInfo1.vue';
import UserInfo2 from './UserInfo2.vue';
import UserInfo3 from "./UserInfo3.vue";
import { useUserStore } from "@/stores/userStore.js";
import { get_personalInfo } from "@/api/api.js";

export default {
  name: 'UserInfo',
  components: {
    UserInfo1,
    UserInfo2,
    UserInfo3,
  },
  data() {
    return {
      userInfo: {
        avatarUrl: '',
        userName: '',
        gender: '',
        phonenumber: '',
        email: '',
        personalNote: '',
        height: '',
        weight: '',
        registrationDate: '',
        location: ''
      }
    };
  },
  async created() {
    // 获取 token
    const userStore = useUserStore();
    const token = userStore.token;

    // 调用 API 获取个人信息
    try {
      const personalInfo = await get_personalInfo(token); // 获取个人信息
      // 更新组件的状态
      this.updateUserInfo(personalInfo);
    } catch (error) {
      console.error('获取个人信息失败:', error);
    }
  },
  methods: {
    // 更新用户信息的函数
    updateUserInfo(updatedData) {
      // 根据返回的数据字段更新组件的状态
      this.userInfo.avatarUrl = updatedData.avatar || '';
      this.userInfo.userName = updatedData.nickname || '';
      this.userInfo.gender = updatedData.sex === 1 ? '男' : '女';
      this.userInfo.phonenumber = updatedData.account || '';
      this.userInfo.email = updatedData.email || '';
      this.userInfo.personalNote = updatedData.note || '';
      this.userInfo.height = updatedData.height || '';
      this.userInfo.weight = updatedData.weight || '';
      this.userInfo.registrationDate = updatedData.register_time || '';
      this.userInfo.location = updatedData.location || '';
    }
  }
};
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
