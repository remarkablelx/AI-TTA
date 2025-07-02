<template>
  <div class="main-container">
    <!-- 侧边栏组件 -->
    <NavBar @toggle-collapse="toggleCollapse" :is-collapsed="isCollapsed" />

    <!-- 主内容区，右侧区域根据侧边栏的折叠动态调整 -->
    <div class="content-area" :style="{ marginLeft: isCollapsed ? '0' : '220px' }">
      <!-- 用户信息组件，放在右侧上方 -->
      <div class="user-info-container">
        <UserInfo1
          :avatarUrl="'https://link-to-avatar.jpg'"
          :userName="'AI-TTA-User1'"
          :gender="'男'"
          :phonenumber="'19132050485'"
          :email="'822684749@qq.com'"
          :personal-note="'这是一个个性标签举例这是一个个性标签举例这是一个个性标签举例这是一个个性标签举例'"
        />
      </div>

      <!-- 第二部分：详细个人信息，包括表格和操作按钮 -->
      <div class="user-info-detail">
        <UserInfo2
          :avatarUrl="'https://link-to-avatar.jpg'"
          :userName="'AI-TTA-User1'"
          :gender="'男'"
          :height="175"
          :weight="70"
          :email="'822684749@qq.com'"
          :phonenumber="'19132050485'"
          :personalNote="'这是个人说明'"
          :registrationDate="'2022-01-26 16:29:44'"
        />
      </div>

      <!-- 这里是右侧下方的其他内容，稍后可以添加 -->
      <div class="other-content">
        <p>其他内容放在这里</p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/Main/NavBar.vue';  // 导入导航栏组件
import UserInfo1 from '@/components/Main/UserInfo1.vue';  // 导入用户信息组件
import UserInfo2 from '@/components/Main/UserInfo2.vue';  // 导入第二部分用户信息组件

export default {
  components: {
    NavBar,  // 注册 NavBar 组件
    UserInfo1,  // 注册 UserInfo1 组件
    UserInfo2  // 注册 UserInfo2 组件
  },
  data() {
    return {
      isCollapsed: false  // 控制侧边栏是否折叠
    };
  },
  methods: {
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;  // 切换侧边栏的折叠状态
    }
  }
};
</script>

<style scoped>
.main-container {
  display: flex; /* 使用 Flexbox 布局 */
  height: 100vh; /* 使主容器的高度占满整个视口 */
  width: 100vw; /* 横向撑满整个浏览器页面 */
}

/* 侧边栏样式 */
nav {
  width: 220px; /* 默认侧边栏宽度 */
  transition: width 0.3s; /* 平滑过渡效果 */
}

/* 右侧内容区域，包含用户信息和下方内容 */
.content-area {
  flex: 1; /* 使内容区自动填充剩余空间 */
  padding: 20px;
  transition: margin-left 0.3s ease; /* 平滑过渡效果 */
  overflow-y: auto; /* 如果内容过多，可以滚动 */
  height: 100vh; /* 确保内容区的高度填满视口 */
}

.user-info-container {
  margin-bottom: 20px; /* 设置与下方内容的间距 */
  max-width: 100%; /* 确保用户信息容器不超出右侧区域 */
}

.user-info-detail {
  margin-bottom: 20px;
}

.other-content {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-top: 20px;
}
</style>
