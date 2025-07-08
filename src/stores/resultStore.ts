import { defineStore } from 'pinia'

export const useResultStore = defineStore('resultStore', {
  state: () => ({
    result: {
      annotated_video_path: '',   // 标注后的视频路径
      ball_json_out_path: '',     // 球检测的 JSON 路径
      ball_video_out_path: '',    // 球检测后的视频路径
      pose_json_out_path: '',     // 姿势检测的 JSON 路径
      pose_video_out_path: '',    // 姿势检测后的视频路径
      recognition_json_path: '',  // 识别结果的 JSON 路径
      result_id: 0,               // 结果ID
      segment_json_path: '',      // 分段 JSON 路径
      video_path: '',             // 视频原始路径
    },
  }),

  actions: {
    setResult(result: any) {
      // 设置结果数据
      this.result = result;
    },
  },
});
