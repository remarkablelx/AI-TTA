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
      <div class="video-panel" :class="{ 'fullscreen-mode': isFullscreen.original }">
        <div class="video-wrapper">
          <div class="video-frame">
            <video
              ref="originalVideo"
              :src="props.originalSrc"
              @play="handlePlay('original')"
              @pause="handlePause('original')"
              @timeupdate="e => updateProgress(e, 'original')"
              @loadedmetadata="e => setDuration(e, 'original')"
            ></video>
            <div class="video-controls">
              <div class="controls-top">
                <button @click="togglePlay('original')">
                  {{ isPlaying.original ? '❚❚' : '▶' }}
                </button>
                <span class="time-display">
                  {{ formatTime(currentTime.original) }} / {{ formatTime(duration.original) }}
                </span>
                <button @click="toggleFullscreen('original')">
                  {{ isFullscreen.original ? '退出全屏' : '全屏' }}
                </button>
              </div>
              <input
                type="range"
                class="progress-bar"
                v-model="currentTime.original"
                :max="duration.original"
                @input="seekVideo('original')"
                step="0.1"
              >
            </div>
          </div>
        </div>
      </div>

      <!-- 处理后视频 -->
      <div class="video-panel" :class="{ 'fullscreen-mode': isFullscreen.processed }">
        <div class="video-wrapper">
          <div class="video-frame">
            <video
              ref="processedVideo"
              :src="props.processedSrc"
              @play="handlePlay('processed')"
              @pause="handlePause('processed')"
              @timeupdate="e => updateProgress(e, 'processed')"
              @loadedmetadata="e => setDuration(e, 'processed')"
            ></video>
            <div class="video-controls">
              <div class="controls-top">
                <button @click="togglePlay('processed')">
                  {{ isPlaying.processed ? '❚❚' : '▶' }}
                </button>
                <span class="time-display">
                  {{ formatTime(currentTime.processed) }} / {{ formatTime(duration.processed) }}
                </span>
                <button @click="toggleFullscreen('processed')">
                  {{ isFullscreen.processed ? '退出全屏' : '全屏' }}
                </button>
              </div>
              <input
                type="range"
                class="progress-bar"
                v-model="currentTime.processed"
                :max="duration.processed"
                @input="seekVideo('processed')"
                step="0.1"
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const props = defineProps({
  originalSrc: String,
  processedSrc: String
});

// 视频状态
const isSyncing = ref(false);
const currentTime = ref({ original: 0, processed: 0 });
const duration = ref({ original: 0, processed: 0 });
const isPlaying = ref({ original: false, processed: false });
const isFullscreen = ref({ original: false, processed: false });

// 获取视频元素引用
const originalVideo = ref<HTMLVideoElement | null>(null);
const processedVideo = ref<HTMLVideoElement | null>(null);

// 设置视频时长
const setDuration = (event: Event, type: 'original' | 'processed') => {
  const video = event.target as HTMLVideoElement;
  duration.value[type] = video.duration;
};

// 格式化时间显示
const formatTime = (time: number) => {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60);
  return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
};

// 切换播放/暂停
const togglePlay = (type: 'original' | 'processed') => {
  const video = type === 'original' ? originalVideo.value : processedVideo.value;
  if (!video) return;

  if (video.paused) {
    video.play().then(() => {
      isPlaying.value[type] = true;
      if (isSyncing.value && type === 'original') {
        processedVideo.value?.play();
      }
    });
  } else {
    video.pause();
    isPlaying.value[type] = false;
    if (isSyncing.value && type === 'original') {
      processedVideo.value?.pause();
    }
  }
};

// 更新进度条
const updateProgress = (event: Event, type: 'original' | 'processed') => {
  const video = event.target as HTMLVideoElement;
  currentTime.value[type] = video.currentTime;

  // 同步状态下，原视频控制处理视频
  if (isSyncing.value && type === 'original' && processedVideo.value) {
    processedVideo.value.currentTime = video.currentTime;
    currentTime.value.processed = video.currentTime;
  }
};

// 跳转视频
const seekVideo = (type: 'original' | 'processed') => {
  const video = type === 'original' ? originalVideo.value : processedVideo.value;
  if (!video) return;

  video.currentTime = currentTime.value[type];

  // 同步状态下，原视频跳转时也跳转处理视频
  if (isSyncing.value && type === 'original' && processedVideo.value) {
    processedVideo.value.currentTime = currentTime.value[type];
    currentTime.value.processed = currentTime.value[type];
  }
};

// 处理播放事件
const handlePlay = (type: 'original' | 'processed') => {
  isPlaying.value[type] = true;
  if (isSyncing.value && type === 'original' && processedVideo.value) {
    processedVideo.value.play();
  }
};

// 处理暂停事件
const handlePause = (type: 'original' | 'processed') => {
  isPlaying.value[type] = false;
  if (isSyncing.value && type === 'original' && processedVideo.value) {
    processedVideo.value.pause();
  }
};

// 切换同步状态
const toggleSync = () => {
  isSyncing.value = !isSyncing.value;
  if (isSyncing.value && originalVideo.value && processedVideo.value) {
    // 同步时，将处理视频同步到原视频的状态
    processedVideo.value.currentTime = originalVideo.value.currentTime;
    currentTime.value.processed = originalVideo.value.currentTime;
    if (!originalVideo.value.paused) {
      processedVideo.value.play();
    } else {
      processedVideo.value.pause();
    }
  }
};

// 切换全屏
const toggleFullscreen = (type: 'original' | 'processed') => {
  isFullscreen.value[type] = !isFullscreen.value[type];
};

// 初始化视频元素引用
onMounted(() => {
  originalVideo.value = document.querySelector(`video[src="${props.originalSrc}"]`) as HTMLVideoElement;
  processedVideo.value = document.querySelector(`video[src="${props.processedSrc}"]`) as HTMLVideoElement;
});
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
  position: relative;
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

.video-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.controls-top {
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-display {
  color: white;
  font-family: monospace;
  flex-grow: 1;
}

.progress-bar {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: #555;
  outline: none;
  -webkit-appearance: none;
}

.progress-bar::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
}

button {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.global-controls {
  display: flex;
  gap: 6px;
  margin-bottom: 1rem;
  z-index: 1;
}

.global-controls h2 {
  margin: 10px 0 0 20px;
  color: #333;
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