<!-- VideoComparator.vue -->
<template>
  <div class="video-comparator">
    <!-- 全局控制按钮 -->
    <div class="global-controls">
      <h2>视频分析（原视频 / 处理视频）</h2>
      <!-- 同步播放按钮 -->
      <button class="sync-button" @click="toggleSync">
        {{ isSyncing ? '断开同步' : '同步播放' }}
      </button>
    </div>
    <div class="comparison-container">
      <!-- 原始视频 -->
      <div
        class="video-panel"
        :class="{ 'fullscreen-mode': isZoomed.original }"
        ref="originalPanel"
      >
        <div class="video-wrapper">
          <div class="video-frame">
            <!-- 原始视频播放组件 -->
            <video
              ref="originalVideo"
              :src="originalSrc"
              @play="handlePlay('original')"
              @pause="handlePause('original')"
              @timeupdate="e => updateProgress(e, 'original')"
            ></video>
          </div>
          <!-- 原视频控制 -->
          <video-controls
            type="original"
            :progress="progress.original"
            :currentTime="currentTime.original"
            :duration="duration.original"
            :is-zoomed="isZoomed.original"
            @toggle-play="togglePlay('original')"
            @seek="handleSeek($event, 'original')"
            @toggle-zoom="toggleZoom('original')"
          />
        </div>
      </div>

      <!-- 处理后视频 -->
      <div
        class="video-panel"
        :class="{ 'fullscreen-mode': isZoomed.processed }"
        ref="processedPanel"
      >
        <div class="video-wrapper">
          <div class="video-frame">
            <!-- 处理后视频播放组件 -->
            <video
              ref="processedVideo"
              :src="processedSrc"
              @play="handlePlay('processed')"
              @pause="handlePause('processed')"
              @timeupdate="e => updateProgress(e, 'processed')"
            ></video>
          </div>
          <!-- 处理后视频控制 -->
          <video-controls
            type="processed"
            :progress="progress.processed"
            :currentTime="currentTime.processed"
            :duration="duration.processed"
            :is-zoomed="isZoomed.processed"
            @toggle-play="togglePlay('processed')"
            @seek="handleSeek($event, 'processed')"
            @toggle-zoom="toggleZoom('processed')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VideoControls from "@/components/Main/VideoControls.vue";

export default {
  components: { VideoControls },
  props: {
    // 原始视频源和处理后视频源
    originalSrc: String,
    processedSrc: String
  },
  data() {
    return {
      // 同步播放状态
      isSyncing: false,
      // 视频播放进度
      progress: { original: 0, processed: 0 },
      // 当前播放时间
      currentTime: { original: 0, processed: 0 },
      // 视频时长
      duration: { original: 0, processed: 0 },
      // 视频是否全屏
      isZoomed: { original: false, processed: false }
    };
  },
  mounted() {
    // 监听全屏事件
    document.addEventListener('fullscreenchange', this.handleFullscreenChange);
  },
  beforeDestroy() {
    // 组件销毁时移除事件监听
    document.removeEventListener('fullscreenchange', this.handleFullscreenChange);
  },
  methods: {
    // 切换播放/暂停
    togglePlay(type) {
      const video = this.$refs[`${type}Video`];
      video.paused ? video.play() : video.pause();
    },
    // 更新视频播放进度
    updateProgress(event, type) {
      const video = event.target;
      this.currentTime[type] = video.currentTime;
      this.duration[type] = video.duration;
      this.progress[type] = (video.currentTime / video.duration) * 100 || 0;

      // 如果开启同步播放，保持两个视频同步
      if (this.isSyncing && type === "original") {
        this.$refs.processedVideo.currentTime = video.currentTime;
      }
    },
    // 处理视频进度条拖动
    handleSeek(value, type) {
      const video = this.$refs[`${type}Video`];
      video.currentTime = (value * video.duration) / 100;
    },
    // 切换同步播放状态
    toggleSync() {
      this.isSyncing = !this.isSyncing;
      if (this.isSyncing) {
        this.syncVideos();
      }
    },
    // 同步播放两个视频
    async syncVideos() {
      await Promise.all([
        this.$refs.originalVideo.play(),
        this.$refs.processedVideo.play()
      ]);
    },
    // 处理播放事件
    handlePlay() {
      if (this.isSyncing) this.syncVideos();
    },
    // 处理暂停事件
    handlePause() {
      if (this.isSyncing) {
        this.$refs.originalVideo.pause();
        this.$refs.processedVideo.pause();
      }
    },

    // 全屏控制方法
    async toggleZoom(type) {
      const panel = this.$refs[`${type}Panel`];
      if (!this.isZoomed[type]) {
        await this.enterFullscreen(panel);
        this.isZoomed = { ...this.isZoomed, [type]: true };
      } else {
        await this.exitFullscreen();
        this.isZoomed = { ...this.isZoomed, [type]: false };
      }
    },
    // 进入全屏模式
    async enterFullscreen(element) {
      if (element.requestFullscreen) {
        return element.requestFullscreen();
      } else if (element.webkitRequestFullscreen) { /* Safari */
        return element.webkitRequestFullscreen();
      } else if (element.msRequestFullscreen) { /* IE11 */
        return element.msRequestFullscreen();
      }
      console.warn('Fullscreen API is not supported');
    },
    // 退出全屏模式
    async exitFullscreen() {
      if (document.exitFullscreen) {
        await document.exitFullscreen();
      } else if (document.webkitExitFullscreen) { /* Safari */
        await document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) { /* IE11 */
        await document.msExitFullscreen();
      }
    },
    // 监听全屏变化事件
    handleFullscreenChange() {
      if (!document.fullscreenElement) {
        this.isZoomed = { original: false, processed: false };
      }
    }
  }
};
</script>

<style scoped>
.video-comparator {
  padding: 10px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(32, 62, 92, 0.12);
  margin-bottom: 20px;
}

.comparison-container {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
}

.video-panel {
  background: white;
  border-radius: 12px;
}

.video-panel.fullscreen-mode {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
  background: #000;
  border-radius: 0;
}

.video-wrapper {
  margin: 20px;
}

.video-frame {
  position: relative;
  aspect-ratio: 16/9;
  border-radius: 8px;
  overflow: hidden;
  background: #000;
}

.fullscreen-mode .video-frame {
  height: calc(100vh - 120px);
  width: calc(100vw - 40px);
  margin: 20px auto;
}

video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.global-controls {
  display: flex;
  gap: 6px;
  margin-bottom: 1rem;
  z-index: 1;
}

.global-controls h2{
  margin: 10px 0 0 20px;
}

.sync-button {
  background: #2c3e50;
  margin: 6px 0 0 20px ;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
}

.sync-button:hover {
  background: #34495e;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(44, 62, 80, 0.2);
}

@media (max-width: 768px) {
  .comparison-container {
    grid-template-columns: 1fr;
  }

  .video-wrapper {
    margin: 10px;
  }

  .fullscreen-mode .video-frame {
    height: calc(100vh - 80px);
    margin: 10px auto;
  }
}
</style>
