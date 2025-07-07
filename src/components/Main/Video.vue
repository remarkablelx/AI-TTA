<template>
  <div class="video-comparator-container">
    <!-- 将视频源传递给子组件 -->
    <video-comparator
      :originalSrc="originalSrc"
      :processedSrc="processedSrc"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import VideoComparator from '@/components/Main/VideoComparator.vue'; // 引入子组件
import { get_video } from '@/api/api'; // 引入获取视频的 API
import { useVideoStore } from "@/stores/videoStore.ts"



// 父组件传递的视频路径
defineProps({
  originalPath: String,
  processedPath: String
});

// 用来保存转换后的视频 URL
const originalSrc = ref('');
const processedSrc = ref('');

const videoStore = useVideoStore();
const video_id = videoStore.videoInfo.video_id;
console.log(video_id)
const video_path = "F:\\download\\shixun\\aimodel\\video\\testupload.mp4"



// 获取视频数据的函数
const loadVideos = async () => {
  try {
    // 获取原视频的 Blob 数据并转换为 URL
    const originalBlob = await get_video(video_path);
    originalSrc.value = URL.createObjectURL(originalBlob);
    console.log(originalSrc);
    // 获取处理后视频的 Blob 数据并转换为 URL
    const processedBlob = await get_video(video_path);
    processedSrc.value = URL.createObjectURL(processedBlob);
    console.log(processedSrc);
  } catch (error) {
    console.error('加载视频失败:', error);
  }
};

// 在组件挂载后获取视频
onMounted(() => {
  loadVideos();
});
</script>

<style scoped>
.video-comparator-container {
  padding: 20px;
}
</style>
