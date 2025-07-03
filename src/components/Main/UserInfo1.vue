<template>
  <div class="user-info-container">
    <!-- 用户头像部分 -->
    <div class="user-avatar">
      <img :src="avatarUrl" alt="用户头像" />
      <!-- 用户名 -->
      <h3 class="username">{{ userName }}</h3>
    </div>
    <!-- 用户详细信息部分 -->
    <div class="user-details">

      <!-- 性别、手机号、邮箱：放在同一行并固定位置 -->
      <div class="additional-info">
        <span class="info-item">性别: <strong>{{ gender }}</strong></span>
        <span class="info-item">手机号: <strong>{{ phonenumber }}</strong></span>
        <span class="info-item">邮箱: <strong>{{ email }}</strong></span>
      </div>
      <!-- 个人说明 -->
      <div class="personal-note">
        <span>个人说明: <strong>{{ personalNote }}</strong></span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserInfo1',
  props: {
    avatarUrl: String,
    userName: String,
    gender: String,
    phonenumber: String,
    email: String,
    personalNote: String
  }
};
</script>

<style scoped src="@/assets/styles/UserInfo1.css"></style>