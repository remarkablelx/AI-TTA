<script>
import { computed, onMounted } from 'vue'
import logo from '@/components/Home/Logo.vue'
import { useUserStore } from '@/stores/auth2.js' // 导入身份验证
import { useHistoryStore } from '@/stores/history' // 导入历史记录
import axios from 'axios'
import { uploadVideo } from "@/api/api.js";
import { useVideoStore } from '@/stores/videoStore.js'; // 引入视频 store

export default {
  components: { logo },
  props: {
    activeTab: {
      type: String,
      required: true
    },
    isCollapsed: {
      type: Boolean,
      default: false //控制侧边栏是否折叠
    }
  },
  data() {
    return {
      showUploadDialog: false,
      selectedFile: null,
      uploadProgress: 0,
      uploadStatus: null, // null | 'uploading' | 'success' | 'error'
      tabs: [
        { id: 'analysis-view', label: '分析界面'},
        { id: 'analysis-history', label: '分析历史'},
        { id: 'user-information', label: '个人信息'}
      ]
    }
  },
  methods: {
    goHome() {
      this.$router.push('/')  // 跳转到主页
    },

    // 触发文件输入框点击事件
    triggerFileInput() {
      this.$refs.fileInput.click();  // 出发文件输入框点击事件
    },

    // 处理文件选择
    handleFileSelect(event) {
      const file = event.target.files[0]; // 获取选中文件
      if (!file) return; //没有文件就返回

      const allowedTypes = ['video/mp4', 'video/quicktime', 'video/x-msvideo'];
      if (!allowedTypes.includes(file.type)) {
        alert('仅支持 MP4、MOV 和 AVI 格式的视频');
        return;
      }
      if (file.size > 1024 * 1024 * 1024) {
        alert('文件大小不能超过1G');
        return;
      }

      this.selectedFile = file;
      this.showUploadDialog = true; // 打开上传对话框
      this.uploadStatus = null;
      this.uploadProgress = 0;
    },

    // 关闭上传对话框
    closeUploadDialog() {
      this.showUploadDialog = false;
      this.selectedFile = null;
      this.uploadProgress = 0;
      this.uploadStatus = null;
    },

    // 上传视频
    async performUpload() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append('video_file', this.selectedFile); // 添加视频文件
      const videoName = this.selectedFile.name; // 获取文件名


      this.uploadStatus = 'uploading'; // 开始上传
      try {
        // 调用 API 上传视频
        const response = await uploadVideo(this.selectedFile, videoName);
        console.log(response)
        if (response.code === "0") { // 判断上传成功

          const videoData = response.video_info;

          // 存储视频信息到全局状态管理
          const videoStore = useVideoStore();
          videoStore.setVideoInfo({
            video_id: videoData.video_id,
            video_name: videoData.video_name,
            video_path: videoData.video_path
          });
          console.log("现在的是video_id是"+videoStore.videoInfo.video_id)
          console.log("现在的是video_name是"+videoStore.videoInfo.video_name)
          console.log("现在的是video_path是"+videoStore.videoInfo.video_path)
          if (response.code === "0") {
            this.uploadStatus = 'success'; // 上传成功
            this.uploadProgress = 100; // 设置进度条满
          } else {
            this.uploadStatus = 'error'; // 上传失败
          }
        }
      }catch (error) {
        this.uploadStatus = 'error'; // 发生错误
        console.error(error);
      }
    },

    // 处理选项卡点击事件
    handleTabClick(tab) {
      if (tab.id === 'analysis-history') {
        this.$emit('toggle-view', 'history');
      } else if (tab.id === 'user-information') {
        this.$emit('toggle-view', 'userInfo');
      } else if (tab.id === 'analysis-view') {
        this.$emit('toggle-view', 'analysis');
      }
    }
  },

  setup() {
    const authStore = useUserStore() // 初始化身份验证
    const historyStore = useHistoryStore()  // 初始化历史记录

    onMounted(() => {
      if (authStore.isLoggedIn && !authStore.userInfo) {
        authStore.fetchUserInfo() // 如果已登录且没有用户信息，获取用户信息
      }
    })

    const hasHistory = computed(() => {
      return historyStore.historyItems?.length > 0 // 查看是否有历史记录
    })

    return {
      authStore,
      historyStore,
      hasHistory
    }
  },
}
</script>

<template>
  <!-- 当侧边栏折叠式，显示展开按钮 -->
  <transition name="button-fade">
    <button
        v-if="isCollapsed"
        class="expand-btn"
        @click="$emit('toggle-collapse')"
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
    <button class="collapse-btn" @click="$emit('toggle-collapse')">
      <img src="@/assets/photos/layout_left_bar_close_icon.png" alt="收起侧栏" />
    </button>
    <div class="sidebar-header">
      <div class="control-buttons">
          <input
        type="file"
        ref="fileInput"
        hidden
        accept="video/mp4,video/quicktime,video/x-msvideo"
        @change="handleFileSelect"
      >
        <button class="nav-item" @click="triggerFileInput">
          <span>上传视频</span>
        </button>
        <button class="nav-item" @click="goHome">
          <span>返回首页</span>
        </button>
      </div>
      <hr>
    </div>

    <ul class="sidebar-nav">
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

    <!-- 上传弹窗 -->
    <Teleport to="body">
      <div v-if="showUploadDialog" class="upload-modal">
        <div class="modal-content">
          <h3>确认上传视频</h3>

          <div class="file-info">
            <p>文件名: {{ selectedFile.name }}</p>
            <p>文件类型: {{ selectedFile.type }}</p>
            <p>文件大小: {{ (selectedFile.size / 1024 / 1024).toFixed(2) }}MB</p>
          </div>

          <!-- 上传进度条 -->
          <div v-if="uploadStatus === 'uploading'" class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: uploadProgress + '%' }"
            ></div>
            <span class="progress-text">{{ uploadProgress }}%</span>
          </div>

          <!-- 状态提示 -->
          <div v-if="uploadStatus === 'success'" class="status-success">
            上传成功
          </div>
          <div v-if="uploadStatus === 'error'" class="status-error">
            上传失败，请重试
          </div>

          <!-- 操作按钮 -->
          <div class="modal-actions">
            <button
              v-if="!uploadStatus"
              class="confirm-btn"
              @click="performUpload"
            >
              确认上传
            </button>
            <button
              class="cancel-btn"
              @click="closeUploadDialog"
              :disabled="uploadStatus === 'uploading'"
            >
              {{ uploadStatus === 'uploading' ? '上传中...' : '取消' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </nav>
</template>

<style scoped src="@/assets/styles/NavBar.css"></style>
