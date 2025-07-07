<template>
  <div class="video-comparator">
    <div class="global-controls">
      <h2>视频分析（原视频 / 处理视频）</h2>
      <button class="sync-button" @click="toggleSync">
        {{ isSyncing ? '断开同步' : '同步播放' }}
      </button>
    </div>
    <div class="comparison-container">
      <!-- 原始视频 -->
      <div class="video-panel" :class="{ 'fullscreen-mode': isZoomed.original }">
        <div class="video-wrapper">
          <div class="video-frame">
            <video
              ref="originalVideo"
              :src="props.originalSrc"
              @play="handlePlay('original')"
              @pause="handlePause('original')"
              @timeupdate="e => updateProgress(e, 'original')"
            ></video>
          </div>
        </div>
      </div>

      <!-- 处理后视频 -->
      <div class="video-panel" :class="{ 'fullscreen-mode': isZoomed.processed }">
        <div class="video-wrapper">
          <div class="video-frame">
            <video
              ref="processedVideo"
              :src="props.processedSrc"
              @play="handlePlay('processed')"
              @pause="handlePause('processed')"
              @timeupdate="e => updateProgress(e, 'processed')"
            ></video>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// 在 script setup 中解构 props
const props = defineProps({
  originalSrc: String,
  processedSrc: String
});

// 视频同步控制
const isSyncing = ref(false);
const progress = ref({ original: 0, processed: 0 });
const currentTime = ref({ original: 0, processed: 0 });
const duration = ref({ original: 0, processed: 0 });
const isZoomed = ref({ original: false, processed: false });

// 切换播放/暂停
const togglePlay = (type: 'original' | 'processed') => {
  const video = document.querySelector(`video[src="${type === 'original' ? props.originalSrc : props.processedSrc}"]`) as HTMLVideoElement;
  video.paused ? video.play() : video.pause();
};

// 更新视频播放进度
const updateProgress = (event: Event, type: 'original' | 'processed') => {
  const video = event.target as HTMLVideoElement;
  currentTime.value[type] = video.currentTime;
  duration.value[type] = video.duration;
  progress.value[type] = (video.currentTime / video.duration) * 100 || 0;

  // 如果同步播放，保持两个视频同步
  if (isSyncing.value && type === 'original') {
    const processedVideo = document.querySelector(`video[src="${props.processedSrc}"]`) as HTMLVideoElement;
    processedVideo.currentTime = video.currentTime;
  }
};

// 切换同步播放状态
const toggleSync = () => {
  isSyncing.value = !isSyncing.value;
  if (isSyncing.value) {
    syncVideos();
  }
};

// 同步播放两个视频
const syncVideos = () => {
  const originalVideo = document.querySelector(`video[src="${props.originalSrc}"]`) as HTMLVideoElement;
  const processedVideo = document.querySelector(`video[src="${props.processedSrc}"]`) as HTMLVideoElement;

  Promise.all([originalVideo.play(), processedVideo.play()]);
};

// 处理播放事件
const handlePlay = (type: 'original' | 'processed') => {
  if (isSyncing.value) syncVideos();
};

// 处理暂停事件
const handlePause = (type: 'original' | 'processed') => {
  if (isSyncing.value) {
    const originalVideo = document.querySelector(`video[src="${props.originalSrc}"]`) as HTMLVideoElement;
    const processedVideo = document.querySelector(`video[src="${props.processedSrc}"]`) as HTMLVideoElement;

    originalVideo.pause();
    processedVideo.pause();
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

.global-controls h2 {
  margin: 10px 0 0 20px;
}

.sync-button {
  background: #2c3e50;
  margin: 6px 0 0 20px;
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
