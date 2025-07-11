<template>
  <div class="video-comparator-container">
    <!-- 视频比较组件 -->
    <video-comparator
      :originalSrc="originalSrc"
      :processedSrc="processedSrc"
    />
    <!-- 报告操作按钮区域 -->
    <div class="report-actions">
      <button class="generate" @click="generateReport">获取分析报告</button>
      <button class="view" @click="viewReport" :disabled="!report_id">查看分析报告</button>
      <button class="delete" @click="deleteReport" :disabled="!report_id">删除分析报告</button>
    </div>

    <!-- 报告显示区域 -->
    <div class="report-display" v-if="reportContent">
      <h3>分析报告内容：</h3>
      <pre>{{ reportContent }}</pre>
    </div>
    <!-- 球可视化组件 -->
    <BallVisualization
        v-if="showVisualization && ballData.length > 0"
        :ballData="ballData"
    />
    <!-- 挥拍识别可视化组件 -->
    <RecognitionVisualization
        v-if="showVisualization && recognitionData.length > 0"
        :recognitionData="recognitionData"
    />
    <!-- 关键点可视化组件 -->
    <KeyPointVisualization
      v-if="showVisualization && actionDataInstanceInfo.length > 0"
      :instanceData="actionDataInstanceInfo"
    />

  </div>
</template>

<script setup lang="ts">
import {onMounted, ref, watch} from 'vue';
import VideoComparator from '@/components/Main/Analysis/VideoComparator.vue';
import {create_report, delete_report, get_json, get_result, get_video, view_report} from '@/api/api.ts';
import BallVisualization from '@/components/Main/Analysis/BallVisualization.vue';
import RecognitionVisualization from "@/components/Main/Analysis/RecognitionVisualization.vue";
import {ElMessage, ElMessageBox} from 'element-plus';
import KeyPointVisualization from "@/components/Main/Analysis/KeyPointVisualization.vue";
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
const actionDataInstanceInfo = ref<any[]>([]);
const actionDataMetaInfo = ref<any[]>([]);
const segmentData = ref<any[]>([]);
const recognitionData = ref<any[]>([]);
const report_id = ref<number>(0);  // 默认值为0，类型为number
const reportContent = ref<string>('');

// 生成分析报告
const generateReport = async () => {
  try {
    alert('正在分析报告')
    console.log("正在分析报告")
    const response = await create_report(props.result_id);
    report_id.value = response.report.report_id;
    alert('分析报告完成，您的report_id是'+report_id)
    console.log("分析报告完成，report_id是"+report_id)
  } catch (error) {
    console.error('生成分析报告失败:', error);
  }
};

// 查看分析报告
const viewReport = async () => {
  if (!report_id.value) return;

  try {
    reportContent.value = await view_report(report_id.value)
    console.log("当前的reportContent是"+reportContent.value)
  } catch (error) {
    console.error('查看分析报告失败:', error);
    ElMessage.error('查看分析报告失败');
  }
};

// 删除函数
const deleteReport = async () => {
  if (!report_id.value) return;

  try {
    alert('正在删除')
    console.log("正在删除")
    await delete_report(report_id.value);
    report_id.value = 0;
    reportContent.value = '';
    alert('删除成功')
    console.log("删除成功")
  } catch (error) {
    console.error('删除分析报告失败:', error);
    ElMessage.error('删除分析报告失败');
  }
};

// 获取视频分析结果的函数
const loadAnalysisResult = async (result_id: number) => {
  try {
    // 获取视频分析结果
    const response = await get_result(result_id);
    console.log('分析结果:', response.result);
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
    resultData.value = await loadAnalysisResult(props.result_id);
    console.log("完整 resultData:", JSON.parse(JSON.stringify(resultData.value)));

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
    console.log("完整 resultData:",resultData);

    // 2. 获取原视频的 Blob 数据并转换为 URL
    const originalBlob = await get_video(resultData.video_path);
    originalSrc.value = URL.createObjectURL(originalBlob);
    console.log('Original Video Source:', originalSrc.value);

    // 3. 获取处理后视频的 Blob 数据并转换为 URL
    const processedBlob = await get_video(resultData.annotated_video_path);
    processedSrc.value = URL.createObjectURL(processedBlob);
    console.log('Processed Video Source:', processedSrc.value);

    // 4.加入report_id
    report_id.value = resultData.report_id;
    console.log("现在的report_id是+"+report_id.value)

  } catch (error) {
    console.error('加载视频失败:', error);
  }
};

// 加载JSON数据
const loadJsonData = async () => {
  try {
    const resultData = await loadAnalysisResult(props.result_id);
    console.log("完整 resultData:",resultData);
    console.log("开始")
    console.log(resultData.ball_json_path)
    console.log(resultData.pose_json_path)
    console.log(resultData.segment_json_path)
    console.log(resultData.recognition_json_path)
    console.log("结束")
    // 并行加载所有JSON数据
    const [ballJson, actionJson, segmentJson,recognitionJson] = await Promise.all([
      get_json(resultData.ball_json_path),
      get_json(resultData.pose_json_path), // 假设动作数据在pose_json_path
      get_json(resultData.segment_json_path),
      get_json(resultData.recognition_json_path)
    ]);
    console.log(ballJson)
    console.log(actionJson)
    console.log(segmentJson)
    console.log(recognitionJson)
    ballData.value = ballJson.json;
    actionData.value = actionJson.json;
    actionDataInstanceInfo.value = actionJson.json.instance_info;
    actionDataMetaInfo.value = actionJson.json.meta_info;
    segmentData.value = segmentJson.json;
    recognitionData.value = recognitionJson.json
    console.log("Json数据加载如下")
    console.log("完整 ballData:", JSON.parse(JSON.stringify(ballData.value)));
    console.log("完整 actionData:", JSON.parse(JSON.stringify(actionData.value)));
    console.log("完整 actionDataInstanceInfo:", JSON.parse(JSON.stringify(actionDataInstanceInfo.value)));
    console.log("完整 actionDataMetaInfo:", JSON.parse(JSON.stringify(actionDataMetaInfo.value)));
    console.log("完整 segmentData:", JSON.parse(JSON.stringify(segmentData.value)));
    console.log("完整 recognitionData:", JSON.parse(JSON.stringify(recognitionData.value)));
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

.report-actions {
  display: flex;
  justify-content: center; /* 使按钮居中 */
  gap: 20px; /* 增加按钮间距 */
  margin: 20px 0;
  padding: 10px 0;
}

.report-actions button {
  padding: 10px 20px; /* 稍微加大按钮内边距 */
  border: none;
  border-radius: 6px; /* 稍微增加圆角 */
  cursor: pointer;
  font-size: 14px;
  min-width: 120px; /* 设置最小宽度使按钮大小一致 */
  transition: all 0.3s ease; /* 添加过渡效果 */
}

.report-actions button.generate {
  background-color: #2c3e50;
  color: white;
}

.report-actions button.view {
  background-color: #409eff;
  color: white;
}

.report-actions button.delete {
  background-color: #f56c6c;
  color: white;
}

.report-actions button:disabled {
  background-color: #c0c4cc;
  cursor: not-allowed;
  opacity: 0.7; /* 禁用时降低透明度 */
}

.report-actions button:not(:disabled):hover {
  transform: translateY(-2px); /* 悬停时轻微上浮 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}

.report-display {
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}

.report-display h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

.report-display pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
  font-family: monospace;
}
</style>
