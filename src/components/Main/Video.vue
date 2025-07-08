<template>
  <div class="video-comparator-container">
    <!-- 视频比较组件 -->
    <video-comparator
      :originalSrc="originalSrc"
      :processedSrc="processedSrc"
    />
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, watch} from 'vue';
import VideoComparator from '@/components/Main/VideoComparator.vue'; // 引入子组件
import { get_video,get_result,get_json} from '@/api/api'; // 引入获取视频的 API
import VisualizationPanel from '@/components/Main/Visualization.vue';
// 直接在定义 props 时声明
const props = defineProps({
  result_id: {
    type: Number,
    required: true // 改为 required，确保必须传递
  },
  originalPath: String,
  processedPath: String
});


// 添加 watch 监听 result_id 变化
watch(() => props.result_id, (newVal) => {
  console.log("result_id 变化:", newVal);
  if (newVal) {
    loadVideos(); // 当 result_id 变化时重新加载视频
  }
});

// 使用 result_id
console.log("传过来的result_id"+props.result_id); // 访问传递的 result_id

// 结果数据的接口定义
interface resultData {
  annotated_video_path: string;
  ball_json_path: string;
  ball_video_path: string;
  pose_json_path: string;
  pose_video_path: string;
  recognition_json_path: string;
  result_id: number;
  segment_json_path: string;
  video_id: number;
  video_path: string;
}

// 响应式数据
const originalSrc = ref('');
const processedSrc = ref('');
const showVisualization = ref(false);
const resultData = ref<resultData | null>(null);
const ballData = ref<any[]>([]);
const actionData = ref<any[]>([]);
const segmentData = ref<any[]>([]);


// 获取视频分析结果的函数
const loadAnalysisResult = async (result_id: number) => {
  try {
    // 获取视频分析结果
    const response = await get_result(result_id);
    console.log('分析结果:', response);
    return response.result; // 返回 result 部分的数据
  } catch (error) {
    console.error('加载视频分析结果失败:', error);
    throw new Error('加载视频分析结果失败');
  }
};



// 加载所有数据（视频和JSON）
const loadAllData = async () => {
  try {
    showVisualization.value = false;

    // 1. 加载视频分析结果
    resultData.value = await get_result(props.result_id);
    console.log('分析结果:', resultData.value);

    // 2. 并行加载视频和JSON数据
    await Promise.all([
      loadVideos(),
      loadJsonData()
    ]);

    showVisualization.value = true;
  } catch (error) {
    console.error('加载数据失败:', error);
    showVisualization.value = false;
  }
};

// 获取视频数据的函数
const loadVideos = async () => {
  try {
    // 1. 获取视频分析结果
    const resultData = await loadAnalysisResult(props.result_id);

    // 2. 获取原视频的 Blob 数据并转换为 URL
    const originalBlob = await get_video(resultData.video_path);
    originalSrc.value = URL.createObjectURL(originalBlob);
    console.log('Original Video Source:', originalSrc.value);

    // 3. 获取处理后视频的 Blob 数据并转换为 URL
    const processedBlob = await get_video(resultData.annotated_video_path);
    processedSrc.value = URL.createObjectURL(processedBlob);
    console.log('Processed Video Source:', processedSrc.value);

  } catch (error) {
    console.error('加载视频失败:', error);
  }
};

// 加载JSON数据
const loadJsonData = async () => {
  try {
    // 检查resultData是否存在
    if (!resultData.value) {
      console.log('resultData is not loaded yet');
    }
    // 并行加载所有JSON数据
    const [ballJson, actionJson, segmentJson] = await Promise.all([
      get_json(resultData.value.ball_json_path),
      get_json(resultData.value.pose_json_path), // 假设动作数据在pose_json_path
      get_json(resultData.value.segment_json_path)
    ]);

    ballData.value = ballJson;
    actionData.value = actionJson;
    segmentData.value = segmentJson;

    console.log('JSON数据加载完成:', {
      ballData: ballData.value,
      actionData: actionData.value,
      segmentData: segmentData.value
    });
  } catch (error) {
    console.error('加载JSON数据失败:', error);
    throw error;
  }
};

// 在组件挂载后获取视频
onMounted(() => {
  if (props.result_id) {
    loadAllData();
  }
});
</script>

<style scoped>
.video-comparator-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
