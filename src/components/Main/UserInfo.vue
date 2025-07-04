<template>
  <div class="user-info-container">
    <!-- 显示 UserInfo1 组件 -->
    <UserInfo1
      class="user-info-1"
      :avatarUrl="avatarUrl"
      :userName="userName"
      :gender="gender"
      :phonenumber="phonenumber"
      :email="email"
      :personalNote="personalNote"
    />

    <!-- 显示 UserInfo2 组件 -->
    <UserInfo2
      class="user-info-2"
      :avatarUrl="avatarUrl"
      :userName="userName"
      :gender="gender"
      :height="height"
      :weight="weight"
      :email="email"
      :location="location"
      :phonenumber="phonenumber"
      :personalNote="personalNote"
      :registrationDate="registrationDate"
      @update-user="updateUserInfo"
    />
  </div>
</template>


<script>
// 导入 UserInfo1 和 UserInfo2 组件
import UserInfo1 from './UserInfo1.vue';
import UserInfo2 from './UserInfo2.vue';


export default {
  name: 'UserInfo',
  components: {
    UserInfo1,
    UserInfo2
  },
  data() {
    return {
      avatarUrl: '',
      userName: '',
      gender: '',
      phonenumber: '',
      email: '',
      personalNote: '',
      height:'',
      weight:'',
      registrationDate: '',
      location:'',
    };
  },
  methods: {
    // 更新用户信息的函数
    updateUserInfo(updatedData) {
      this.avatarUrl = updatedData.avatarUrl;
      this.userName = updatedData.userName;
      this.gender = updatedData.gender;
      this.phonenumber = updatedData.phonenumber;
      this.email = updatedData.email;
      this.personalNote = updatedData.personalNote;
      this.height = updatedData.height;
      this.weight = updatedData.weight;
      this.registrationDate = updatedData.registrationDate;
      this.location = updatedData.location;
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
  width: 100%; /* 使其宽度自适应父容器 */
  max-width: 2000px; /* 设置最大宽度，可以调整 */
  min-width: 1200px;  /* 设置最小宽度，可以调整 */
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin: 0 auto; /* 使组件居中 */
}


</style>


我这里怎么调用呢？