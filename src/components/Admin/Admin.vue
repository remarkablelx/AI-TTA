<template>
  <div class="admin-container">
    <AdminBar
      @toggle-collapse="toggleCollapse"
      :is-collapsed="isCollapsed"
      @toggle-view="toggleView"
      :activeTab="activeTab"
    />

    <!-- 右侧内容区域 -->
    <div class="admin-main" :class="{ 'collapsed': isCollapsed }">
      <!-- 添加 transition 动画包裹 UserManagement 和 RecordManagement -->
      <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
        <UserManagement v-if="isUserManagementVisible" />
      </transition>
      <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
        <RecordManagement v-if="isRecordManagementVisible" />
      </transition>
    </div>
  </div>
</template>

<script>
import AdminBar from '@/components/Admin/AdminBar.vue';
import UserManagement from '@/components/Admin/UserManagement.vue';  // New component for User Management
import RecordManagement from '@/components/Admin/RecordManagement.vue';

export default {
  components: {
    AdminBar,
    UserManagement,
    RecordManagement,
  },
  data() {
    return {
      isCollapsed: false,
      isUserManagementVisible: false,
      isRecordManagementVisible: false,
      activeTab: 'user-list',  // Ensure that the active tab state is set correctly
    };
  },
  methods: {
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
    },
    toggleView(view) {
      // Ensure that the correct tab visibility is toggled
      if (view === 'userList') {
        this.isRecordManagementVisible = false;  // Hide the record management
        this.isUserManagementVisible = !this.isUserManagementVisible;  // Toggle the user management visibility
      } else if (view === 'recordList') {
        this.isUserManagementVisible = false;  // Hide the user management
        this.isRecordManagementVisible = !this.isRecordManagementVisible;  // Toggle the record management visibility
      }
    },
    // 过渡钩子
    beforeEnter(el) {
      el.style.opacity = 0;
      el.style.transform = 'translateY(10px)';
    },
    enter(el, done) {
      el.offsetHeight;  // Force reflow
      el.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      el.style.opacity = 1;
      el.style.transform = 'translateY(0px)';
      done();
    },
    leave(el, done) {
      el.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      el.style.opacity = 0;
      el.style.transform = 'translateY(10px)';
      done();
    },
  },
};
</script>


<style scoped>
.admin-container {
  display: block;
  min-height: 100vh;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

.admin-main {
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
  .admin-main {
    margin-left: 0 !important;
    padding: 2rem 10px;
  }
}

.admin-main.collapsed {
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