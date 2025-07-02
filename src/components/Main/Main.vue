<template>
  <div class="user-container">
    <!-- 侧边栏组件 -->
    <NavBar @toggle-collapse="toggleCollapse" :is-collapsed="isCollapsed" @toggle-user-panel="toggleUserInfo" />

    <!-- 右侧内容区域 -->
    <div class="user-main" :class="{ 'collapsed': isCollapsed }">
      <!-- 将 UserInfo 组件挂载在这里 -->
      <UserInfo v-if="isUserInfoVisible" />
    </div>
  </div>
</template>

<script>
// 导入 NavBar 和 UserInfo 组件
import NavBar from '@/components/Main/NavBar.vue';
import UserInfo from '@/components/Main/UserInfo.vue';
export default {
  components: {
    NavBar,  // 注册 NavBar 组件
    UserInfo  // 注册 UserInfo 组件
  },
  data() {
    return {
      isCollapsed: false,  // 控制侧边栏是否折叠
      isUserInfoVisible: false,  // 控制用户信息界面的显示与隐藏
    };
  },
  methods: {
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;  // 切换侧边栏的折叠状态
    },
    toggleUserInfo() {
      this.isUserInfoVisible = !this.isUserInfoVisible;  // 切换用户信息界面的显示与隐藏
    }
  }
};
</script>

<style scoped>
.user-container {
  display: block;
  min-height: 100vh;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

.user-main {
  margin-left: 260px;
  padding: 2rem;
  min-height: 80vh;
  transition: margin-left 0.3s ease;
}

.sidebar-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  z-index: 999;
  transition: opacity 0.3s;
}

@media (max-width: 768px) {
  .user-main {
    margin-left: 0 !important;
    padding: 2rem 10px;
  }
}

.user-main.collapsed {
  margin-left: 0 !important;  /* 当侧边栏折叠时，右侧内容区不再有左边距 */
}
</style>
