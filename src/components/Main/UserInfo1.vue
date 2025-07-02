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

<style scoped>
/* 用户信息整体容器 */
.user-info-container {
  display: flex; /* 使用 Flexbox 布局 */
  align-items: flex-start;
  padding: 25px;
  border-radius: 12px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 20px auto;
  font-family: 'Arial', sans-serif; /* 使用黑体 */
  position: relative; /* 保证定位不受其他元素影响 */
}

/* 用户头像样式 */
.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;  /* 确保图片填充满容器并保持比例 */
  object-position: center;  /* 确保图片居中对齐 */
  max-width: 100px;  /* 限制最大宽度为100px */
  max-height: 100px;  /* 限制最大高度为100px */
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 用户详细信息部分的样式 */
.user-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-size: 0.95em; /* 调整字体大小 */
  width: 100%; /* 确保详细信息区域占满剩余空间 */
}

/* 用户名样式 */
.username {
  font-size: 1.3em; /* 字体适当增大 */
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

/* 信息样式（性别、手机号、邮箱）放在一行并固定位置 */
.additional-info {
  font-size: 1em;
  color: #555;
  display: flex; /* 使用 Flexbox 排版 */
  justify-content: space-between; /* 分散对齐 */
  gap: 20px; /* 设置每项之间的间距 */
  margin-bottom: 10px; /* 增加底部间距 */
}

.info-item {
  flex-basis: 30%; /* 确保每项占据一定宽度 */
  white-space: nowrap; /* 防止内容换行 */
}

/* 个人说明样式 */
.personal-note {
  font-size: 1em;
  color: #444;
  margin-top: 15px;
}

.personal-note span {
  display: block;
}
</style>
