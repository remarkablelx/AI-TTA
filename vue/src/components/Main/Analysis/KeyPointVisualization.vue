<template>
  <div class="keypoint-visualization">
    <!-- 标题和人员切换 -->
    <div class="header">
      <h3>运动员姿态分析 (ID: {{ currentPersonIndex + 1 }})</h3>
      <div class="person-switcher">
        <button
          @click="prevPerson"
          :disabled="currentPersonIndex === 0"
          class="switch-btn"
        >← 上一位</button>
        <span class="person-count">{{ currentPersonIndex + 1 }} / {{ personCount }}</span>
        <button
          @click="nextPerson"
          :disabled="currentPersonIndex === personCount - 1"
          class="switch-btn"
        >下一位 →</button>
      </div>
    </div>

    <!-- 当前帧信息 -->
    <div class="frame-info">
      <div class="frame-count">当前帧: {{ currentFrameDisplay }} / {{ totalFrames }}</div>
      <div class="bbox-info">边界框: ({{ currentBbox[0].toFixed(1) }}, {{ currentBbox[1].toFixed(1) }}) →
            ({{ currentBbox[2].toFixed(1) }}, {{ currentBbox[3].toFixed(1) }})</div>
    </div>

    <!-- 关键点表格 -->
    <div class="keypoint-table-container">
      <table class="keypoint-table">
        <thead>
          <tr>
            <th class="col-keypoint">关键点</th>
            <th class="col-coord">X坐标</th>
            <th class="col-coord">Y坐标</th>
            <th class="col-confidence">置信度</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(kp, index) in filteredKeypoints" :key="index">
            <td class="keypoint-name">{{ kpNames[index] }}</td>
            <td class="coord-value">{{ kp[0].toFixed(1) }}</td>
            <td class="coord-value">{{ kp[1].toFixed(1) }}</td>
            <td class="confidence-cell">
              <div class="confidence-container">
                <div class="confidence-bar" :style="{ width: `${currentScores[index] * 100}%` }"></div>
                <span class="confidence-text">{{ (currentScores[index] * 100).toFixed(0) }}%</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 帧滑动条 -->
    <div class="slider-container">
      <input
        type="range"
        v-model="currentFrame"
        min="0"
        :max="totalFrames - 1"
        @input="handleSliderInput"
        class="frame-slider"
      >
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface KeypointInstance {
  bbox: number[][];
  bbox_score: number;
  keypoints: number[][];
  keypoint_scores: number[];
}

interface FrameData {
  frame_id: number;
  instances: KeypointInstance[];
}

// COCO关键点名称（17个点）
const kpNames = [
  'nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
  'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
  'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
  'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
]

// 定义props接收actionDataInstanceInfo
const props = defineProps({
  instanceData: {
    type: Array as () => FrameData[], // Correct the data structure
    required: true
  }
});

// 当前显示的人员索引
const currentPersonIndex = ref(0)
// 当前显示的帧索引
const currentFrame = ref(0)
// 滑动条值（用于解决直接v-model绑定时的跳帧问题）
const sliderValue = ref(0)

// 计算属性
const personCount = computed(() => {
  return props.instanceData.length > 0 ? props.instanceData[0].instances.length : 0
})

const totalFrames = computed(() => {
  return props.instanceData.length
})

const currentFrameDisplay = computed(() => {
  return (currentFrame.value + 1).toString().padStart(3, '0')
})

const currentPersonData = computed(() => {
  if (!props.instanceData[currentFrame.value]) return null
  return props.instanceData[currentFrame.value].instances[currentPersonIndex.value]
})

const currentBbox = computed(() => {
  return currentPersonData.value?.bbox[0] || [0, 0, 0, 0]
})

const currentKeypoints = computed(() => {
  return currentPersonData.value?.keypoints || Array(17).fill([0, 0])
})

const currentScores = computed(() => {
  return currentPersonData.value?.keypoint_scores || Array(17).fill(0)
})

// 只显示置信度大于30%的关键点
const filteredKeypoints = computed(() => {
  // Assuming keypoints are [x, y] tuples
  return currentKeypoints.value.filter((_: [number, number], index: number) => currentScores.value[index] > 0.3)
})

// 切换人员
const prevPerson = () => {
  if (currentPersonIndex.value > 0) {
    currentPersonIndex.value--
  }
}

const nextPerson = () => {
  if (currentPersonIndex.value < personCount.value - 1) {
    currentPersonIndex.value++
  }
}

// 处理滑动条输入
const handleSliderInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  sliderValue.value = parseInt(target.value)
  currentFrame.value = sliderValue.value
}

// 监听外部数据变化
watch(() => props.instanceData, (newVal) => {
  if (newVal && newVal.length > 0) {
    currentFrame.value = 0
    currentPersonIndex.value = 0
    sliderValue.value = 0
  }
}, { immediate: true })
</script>

<style scoped>
.keypoint-visualization {
  font-family: 'Segoe UI', Arial, sans-serif;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: none;
  display: flex;
  flex-direction: column;
  height: 70vh; /* 限制整体高度 */
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.header h3 {
  margin: 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.person-switcher {
  display: flex;
  align-items: center;
  gap: 12px;
}

.switch-btn {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #f5f5f5;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.switch-btn:hover:not(:disabled) {
  background: #e0e0e0;
}

.switch-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.person-count {
  font-weight: bold;
  min-width: 50px;
  text-align: center;
  font-size: 14px;
}

.frame-info {
  margin-bottom: 16px;
  font-size: 14px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.frame-count, .bbox-info {
  background: #f8f8f8;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 500;
  white-space: nowrap;
}

.keypoint-table-container {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  max-height: calc(70vh - 200px); /* 自动计算表格最大高度 */
}

.keypoint-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.keypoint-table th {
  position: sticky;
  top: 0;
  background-color: #2c3e50;
  color: white;
  padding: 10px 12px;
  text-align: left;
  font-weight: 500;
}

.keypoint-table td {
  padding: 8px 12px;
  border-bottom: 1px solid #eee;
}

.col-keypoint {
  width: 100px;
  min-width: 100px;
}

.col-coord {
  width: 80px;
  min-width: 80px;
}

.col-confidence {
  width: 120px;
  min-width: 120px;
}

.keypoint-name {
  font-weight: 500;
  color: #333;
}

.coord-value {
  font-family: 'Courier New', monospace;
  color: #555;
}

.confidence-cell {
  padding: 8px 12px !important;
}

.confidence-container {
  display: flex;
  align-items: center;
  height: 20px;
}

.confidence-bar {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  border-radius: 4px;
  transition: width 0.3s ease-out;
}

.confidence-text {
  margin-left: 8px;
  min-width: 30px;
  text-align: right;
  font-weight: 500;
}

.slider-container {
  margin-top: 16px;
  padding: 0 10px;
}

.frame-slider {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: #e0e0e0;
  outline: none;
  -webkit-appearance: none;
}

.frame-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #2c3e50;
  cursor: pointer;
}

/* 奇数行背景色 */
.keypoint-table tr:nth-child(odd) {
  background-color: #fafafa;
}

/* 悬停效果 */
.keypoint-table tr:hover {
  background-color: #f5f5f5;
}

/* 滚动条样式 */
.keypoint-table-container::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.keypoint-table-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.keypoint-table-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.keypoint-table-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>