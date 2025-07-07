// src/stores/videoStore.js
import { defineStore } from 'pinia';

// 定义 videoData 的类型
interface VideoData {
  video_id: number;
  video_name: string;
  video_path: string;
}

export const useVideoStore = defineStore('video', {
  state: () => ({
    videoInfo: {
      video_id: 0,
      video_name: '',
      video_path: '',
    }
  }),

  actions: {
    // 设置视频信息
    setVideoInfo(videoData: VideoData) { // 使用 VideoData 类型
      this.videoInfo.video_id = videoData.video_id;
      this.videoInfo.video_name = videoData.video_name;
      this.videoInfo.video_path = videoData.video_path;
    },

    // 清空视频信息
    clearVideoInfo() {
      this.videoInfo.video_id = 0;
      this.videoInfo.video_name = '';
      this.videoInfo.video_path = '';
    }
  }
});
