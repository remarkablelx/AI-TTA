<template>
  <!-- 当侧边栏折叠式，显示展开按钮 -->
  <transition name="button-fade">
    <button
        v-if="isCollapsed"
        class="expand-btn"
        @click="toggleCollapse"
    >
      <img src="@/assets/photos/layout_left_bar_open_icon.png" alt="打开侧栏" />
    </button>
  </transition>

   <!-- 侧边栏导航菜单 -->
  <nav
    class="user-sidebar"
    :class="{ collapsed: isCollapsed }"
  >

    <h3 class="logo">
      <logo />
    </h3>

    <!-- 收起侧边栏按钮 -->
    <button class="collapse-btn" @click="toggleCollapse">
      <img src="@/assets/photos/layout_left_bar_close_icon.png" alt="收起侧栏" />
    </button>
    <div class="sidebar-header">
      <div class="control-buttons">
        <!-- 仅返回首页按钮 -->
        <button class="nav-item" @click="goHome">
          <span>返回首页</span>
        </button>
      </div>
      <hr>
    </div>

    <ul class="sidebar-nav">
      <!-- 替换为管理员的用户列表和记录列表 -->
      <li
        v-for="tab in tabs"
        :key="tab.id"
        class="nav-item"
        :class="{
          active: activeTab === tab.id,
        }"
        @click="handleTabClick(tab)"
      >
        <span>{{ tab.label }}</span>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import logo from '@/components/Home/Logo.vue'
// Define component props
const props = defineProps({
  activeTab: {
    type: String,
    required: true,
  },
  isCollapsed: {
    type: Boolean,
    default: false,
  },
})

// Define component emits
const emit = defineEmits<{
  (e: 'toggle-collapse'): void;
  (e: 'toggle-view', view: string): void;
}>()

// Tabs definition
const tabs = [
  { id: 'user-list', label: '用户列表' },
  { id: 'record-list', label: '记录列表' },
]

// Method to go to the homepage
const goHome = () => {
  // Navigate to the homepage (router logic assumed)
  window.location.href = '/'
}

// Handle tab clicks
const handleTabClick = (tab: { id: string }) => {
  if (tab.id === 'user-list') {
    emit('toggle-view', 'userList')
  } else if (tab.id === 'record-list') {
    emit('toggle-view', 'recordList')
  }
}

// Method to toggle the sidebar collapse
const toggleCollapse = () => {
  emit('toggle-collapse')
}
</script>

<style scoped src="@/assets/styles/NavBar.css"></style>
