<!-- VideoControls.vue -->
<template>
  <div class="video-controls">
    <!-- 播放/暂停按钮 -->
    <button @click="$emit('toggle-play')">
      <!-- 判断视频是否暂停，根据状态显示 ▶ 或 ⏸ -->
      {{ $parent.$refs[`${type}Video`]?.paused ? '▶' : '⏸' }}
    </button>

    <!-- 进度条 -->
    <input
      type="range"
      class="progress-bar"
      :value="progress"
      @input="$emit('seek', $event.target.value)"
      min="0"
      max="100"
      step="0.1"
    >

    <!-- 时间显示 -->
    <span class="time-display">
      {{ formatTime(currentTime) }} / {{ formatTime(duration) }} <!-- 格式化当前时间和总时长 -->
    </span>

    <!-- 全屏/退出全屏按钮 -->
    <button @click="$emit('toggle-zoom')">
      <!-- 判断视频是否全屏，根据状态显示 ⛶ 或 ✕ -->
      {{ isZoomed ? '✕' : '⛶' }}
    </button>
  </div>
</template>

<script>
export default {
  props: {
    // 控制类型（例如 'original' 或 'processed'），传递给父组件
    type: String,
    // 进度条当前值（0-100），表示视频播放进度
    progress: Number,
    // 当前播放时间
    currentTime: Number,
    // 视频总时长
    duration: Number,
    // 是否为全屏状态
    isZoomed: Boolean
  },
  methods: {
    // 格式化时间为 'hh:mm:ss' 形式
    formatTime(seconds) {
      const date = new Date(0); // 创建一个表示时间的Date对象
      date.setSeconds(seconds || 0); // 将传入的秒数转换为时间
      return date.toISOString().slice(11, 19); // 返回 'hh:mm:ss' 格式的时间
    }
  }
}
</script>

<style scoped>
/* 视频控制面板样式 */
.video-controls {
  display: flex; /* 使用弹性盒布局 */
  align-items: center; /* 垂直居中 */
  gap: 12px; /* 控件之间的间距 */
  padding: 12px 16px; /* 内边距 */
  background: #f8fafc; /* 背景色 */
  border-radius: 8px; /* 圆角 */
  margin-top: 10px; /* 上边距 */
}

/* 进度条样式 */
.progress-bar {
  flex: 1; /* 进度条填充父元素的剩余空间 */
  height: 4px; /* 高度 */
  background: #e0e6ed; /* 背景色 */
  border-radius: 2px; /* 圆角 */
}

/* 时间显示样式 */
.time-display {
  color: #5a6a85; /* 文本颜色 */
  font-size: 14px; /* 字体大小 */
  min-width: 120px; /* 最小宽度 */
  text-align: center; /* 居中对齐 */
}

/* 按钮样式 */
button {
  padding: 8px 12px; /* 内边距 */
  border-radius: 4px; /* 圆角 */
  border: 1px solid #e0e6ed; /* 边框 */
  background: white; /* 背景色 */
  cursor: pointer; /* 鼠标悬停时显示手指光标 */
  transition: all 0.2s; /* 过渡效果 */
}

/* 按钮悬停效果 */
button:hover {
  background: #f1f5f9; /* 鼠标悬停时改变背景色 */
}
</style>
