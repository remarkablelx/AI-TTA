<template>
  <div class="user-container">
    <NavBar
      @toggle-collapse="toggleCollapse"
      :is-collapsed="isCollapsed"
      @toggle-view="toggleView"
    />

    <!-- 右侧内容区域 -->
    <div class="user-main" :class="{ 'collapsed': isCollapsed }">
      <!-- 添加 transition 动画包裹 UserInfo 和 History -->
      <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
        <UserInfo v-if="isUserInfoVisible" />
      </transition>
      <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
        <History v-if="isHistoryVisible" />
      </transition>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/Main/NavBar.vue';
import UserInfo from '@/components/Main/UserInfo.vue';
import History from '@/components/Main/History.vue';

export default {
  components: {
    NavBar,
    UserInfo,
    History,
  },
  data() {
    return {
      isCollapsed: false,
      isUserInfoVisible: false,
      isHistoryVisible: false,
    };
  },
  methods: {
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
    },
    toggleView(view) {
      if (view === 'history') {
        this.isUserInfoVisible = false;
        this.isHistoryVisible = !this.isHistoryVisible;
      } else if (view === 'userInfo') {
        this.isHistoryVisible = false;
        this.isUserInfoVisible = !this.isUserInfoVisible;
      }
    },
    // 过渡钩子
    beforeEnter(el) {
      el.style.opacity = 0;  // 初始状态
      el.style.transform = 'translateY(10px)';  // 初始位置
    },
    enter(el, done) {
      el.offsetHeight; // 强制重排
      el.style.transition = 'opacity 0.3s ease, transform 0.3s ease';  // 设置动画属性
      el.style.opacity = 1;
      el.style.transform = 'translateY(0px)';
      done();
    },
    leave(el, done) {
      el.style.transition = 'opacity 0.3s ease, transform 0.3s ease';  // 设置动画属性
      el.style.opacity = 0;
      el.style.transform = 'translateY(10px)';
      done();
    },
  },
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
  margin-left: 0 !important;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
  transform: translateY(10px);
}
</style>
