<template>
  <div class="user-container">
    <NavBar
      @toggle-collapse="toggleCollapse"
      :is-collapsed="isCollapsed"
      @toggle-view="toggleView"
    />

    <!-- 右侧内容区域 -->
    <div class="user-main" :class="{ 'collapsed': isCollapsed }">
      <!-- 恢复原始transition动画 -->
      <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
        <UserInfo v-if="isUserInfoVisible" />
      </transition>
      <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
        <History
          v-if="isHistoryVisible"
          @toggle-view="handleViewToggle"
        />
      </transition>
      <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
        <Video
          v-if="isAnalysisVisible"
          :result_id="currentResultId"
        />
      </transition>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import NavBar from '@/components/Main/NavBar.vue'
import UserInfo from '@/components/Main/UserInfo/UserInfo.vue'
import History from '@/components/Main/History/History.vue'
import Video from "@/components/Main/Analysis/Video.vue"

export default {
  components: { NavBar, UserInfo, History, Video },
  setup() {
    const isCollapsed = ref(false)
    const isUserInfoVisible = ref(false)
    const isHistoryVisible = ref(false)
    const isAnalysisVisible = ref(false)
    const currentResultId = ref(0)

    const toggleCollapse = () => {
      isCollapsed.value = !isCollapsed.value
    }

    const toggleView = (view) => {
      isUserInfoVisible.value = false
      isHistoryVisible.value = false
      isAnalysisVisible.value = false

      if (view === 'history') {
        isHistoryVisible.value = true
      } else if (view === 'userInfo') {
        isUserInfoVisible.value = true
      } else if (view === 'analysis') {
        isAnalysisVisible.value = true
      }
    }

    const handleViewToggle = (view, resultId = null) => {
      if (resultId) {
        console.log("接收到切换视图请求:", view, "resultId:", resultId)
        currentResultId.value = resultId
      }
      toggleView(view)
    }

    // 恢复原始动画方法
    const beforeEnter = (el) => {
      el.style.opacity = 0
      el.style.transform = 'translateY(10px)'
    }

    const enter = (el, done) => {
      el.offsetHeight
      el.style.transition = 'opacity 0.3s ease, transform 0.3s ease'
      el.style.opacity = 1
      el.style.transform = 'translateY(0px)'
      done()
    }

    const leave = (el, done) => {
      el.style.transition = 'opacity 0.3s ease, transform 0.3s ease'
      el.style.opacity = 0
      el.style.transform = 'translateY(10px)'
      done()
    }

    return {
      isCollapsed,
      isUserInfoVisible,
      isHistoryVisible,
      isAnalysisVisible,
      currentResultId,
      toggleCollapse,
      toggleView,
      handleViewToggle,
      beforeEnter,
      enter,
      leave
    }
  }
}
</script>

<style scoped>
/* 保持原有样式不变 */
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
.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>