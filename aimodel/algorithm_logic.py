import os
import subprocess
import sys
from typing import Dict, Any, Tuple


def ball_detect(video_path: str) -> Tuple[bool, Dict[str, Any]]:
    """
    输入视频路径，在内部按 "_ball_detect" 格式生成输出路径，并调用脚本。
    """
    print("--- [1/4] 启动球体跟踪任务 ---")
    try:
        if not os.path.exists(video_path):
            return False, {"error": f"输入视频文件不存在: {video_path}"}

        video_name = os.path.splitext(os.path.basename(video_path))[0]
        video_out_path = os.path.join('video_output', f'{video_name}_ball_detect.mp4')
        json_out_path = os.path.join('json', f'{video_name}_ball_detect.json')

        os.makedirs(os.path.dirname(video_out_path), exist_ok=True)
        os.makedirs(os.path.dirname(json_out_path), exist_ok=True)

        command = [
            sys.executable, 'balldetect_pos_vel/ball_detect.py',
            '--video_path', video_path,
            '--model_path', 'balldetect_pos_vel/ball_detect.pt',
            '--video_out_path', video_out_path,
            '--json_out_path', json_out_path,
            '--extrapolation'
        ]

        process = subprocess.run(
            command, capture_output=True, text=True, check=False, encoding='utf-8')

        if process.returncode == 0:
            print("--- 球体跟踪成功 ---")
            return True, {
                "video_out_path": os.path.abspath(video_out_path),
                "json_out_path": os.path.abspath(json_out_path)
            }
        else:
            return False, {"error": process.stderr if process.stderr else process.stdout}

    except Exception as e:
        return False, {"error": f"调用脚本时发生意外错误: {str(e)}"}


def pose_detect(video_path: str) -> Tuple[bool, Dict[str, Any]]:
    """
    输入视频路径，在内部按 "_pose_detect" 格式生成输出路径，并调用脚本。
    """
    print("--- [2/4] 启动骨骼点检测任务 ---")
    try:
        if not os.path.exists(video_path):
            return False, {"error": f"输入文件不存在: {video_path}"}

        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_dir_for_video = 'video_output'
        # 这是我们期望的最终JSON路径
        final_json_out_path = os.path.join('json', f'{video_name}_pose_detect.json')

        os.makedirs(output_dir_for_video, exist_ok=True)
        os.makedirs('json', exist_ok=True)

        command = [
            sys.executable, 'mmpose/predict.py',
            'mmpose/utils/coco_person.py',
            'mmpose/utils/model1.pth',
            'mmpose/utils/config.py',
            'mmpose/utils/model2.pth',
            '--input', video_path,
            '--output-root', output_dir_for_video,  # 底层脚本会把所有东西输出到这里
            '--save-predictions',
            '--draw-bbox'
        ]

        process = subprocess.run(
            command, capture_output=True, text=True, check=False, encoding='utf-8')

        if process.returncode == 0:
            # pose_detect.py 会生成一个 'results_....json' 文件，我们必须重命名它
            generated_json = os.path.join(output_dir_for_video, f'results_{video_name}.json')
            if os.path.exists(generated_json):
                if os.path.exists(final_json_out_path):
                    os.remove(final_json_out_path)
                os.rename(generated_json, final_json_out_path)

            if not os.path.exists(final_json_out_path):
                return False, {
                    "error": f"错误: pose_detect.py 成功运行但未能找到或重命名JSON文件至: {final_json_out_path}"}
            print("--- 骨骼点检测成功 ---")
            return True, {"json_out_path": os.path.abspath(final_json_out_path)}
        else:
            return False, {"error": process.stderr if process.stderr else process.stdout}

    except Exception as e:
        return False, {"error": f"调用脚本时发生意外错误: {str(e)}"}


def action_split(ball_json_path: str) -> Tuple[bool, Dict[str, Any]]:
    """
    输入球轨迹JSON路径，在内部生成固定的 "segments_from_ball.json" 输出。
    """
    print("--- [3/4] 启动动作片段切分任务 ---")
    try:
        if not os.path.exists(ball_json_path):
            return False, {"error": f"球轨迹JSON文件不存在: {ball_json_path}"}

        # 使用您偏好的固定文件名
        output_segment_json_path = os.path.join('json', 'test_ball_detect_segments.json')
        os.makedirs(os.path.dirname(output_segment_json_path), exist_ok=True)

        command = [
            sys.executable, 'mmaction/segment.py',
            '--ball-trajectory-json', ball_json_path,
            '--output-json', output_segment_json_path,
        ]

        process = subprocess.run(
            command, capture_output=True, text=True, check=False, encoding='utf-8')

        if process.returncode == 0:
            print("--- 动作片段切分成功 ---")
            return True, {"segment_json_path": os.path.abspath(output_segment_json_path)}
        else:
            return False, {"error": process.stderr if process.stderr else process.stdout}

    except Exception as e:
        return False, {"error": f"调用脚本时发生意外错误: {str(e)}"}


def action_detect(video_input_path: str, pose_json_path: str, segment_json_path: str) -> Tuple[bool, Dict[str, Any]]:
    """
    输入必要的路径，在内部生成固定的 "final_annotated_video.mp4" 等输出。
    """
    print("--- [4/4] 启动动作识别任务 ---")
    try:
        # 使用您偏好的固定文件名
        output_video_path = os.path.join('video_output', 'test_action.mp4')
        recognition_json_path = os.path.join('json', 'test_action.json')

        config_path = 'mmaction/utils/stgcn_8xb16-pingpong-2d.py'
        checkpoint_path = 'mmaction/utils/best_acc_top1_epoch_65.pth'
        class_names_path = 'mmaction/utils/action.txt'

        required_files = [video_input_path, pose_json_path, segment_json_path,
                          config_path, checkpoint_path, class_names_path]
        for file_path in required_files:
            if not os.path.exists(file_path):
                return False, {"error": f"输入文件不存在: {file_path}"}

        os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

        command = [
            sys.executable, 'mmaction/infer.py',
            '--video-input', video_input_path,
            '--video-output', output_video_path,
            '--pose-json', pose_json_path,
            '--segments-json', segment_json_path,
            '--config', config_path,
            '--checkpoint', checkpoint_path,
            '--class-names-file', class_names_path,
        ]

        process = subprocess.run(
            command, capture_output=True, text=True, check=False, encoding='utf-8')

        if process.returncode == 0:
            # action_detect.py 会在视频同目录下生成 'multi_person_recognition_results.json'
            generated_json = os.path.join(os.path.dirname(output_video_path), 'multi_person_recognition_results.json')
            if os.path.exists(generated_json):
                if os.path.exists(recognition_json_path):
                    os.remove(recognition_json_path)
                os.rename(generated_json, recognition_json_path)

            print("--- 动作识别成功 ---")
            return True, {
                "annotated_video_path": os.path.abspath(output_video_path),
                "recognition_json_path": os.path.abspath(recognition_json_path)
            }
        else:
            return False, {"error": process.stderr if process.stderr else process.stdout}

    except Exception as e:
        return False, {"error": f"调用脚本时发生意外错误: {str(e)}"}


if __name__ == '__main__':
    INPUT_VIDEO = 'video/test.mp4'

    if not os.path.exists(INPUT_VIDEO):
        print(f"错误: 初始输入视频不存在: {INPUT_VIDEO}")
        exit(1)

    print("=" * 25 + " 开始执行端到端视频分析流水线 " + "=" * 25)

    # 创建一个主字典来收集所有路径
    pipeline_results = {}

    # --- 步骤 1: 球体轨迹跟踪 ---
    success, ball_result = ball_detect(video_path=INPUT_VIDEO)
    if not success:
        print(f"流程终止于【球体跟踪】。错误: {ball_result.get('error')}")
        exit(1)
    # 将此步骤的结果合并到主字典中
    pipeline_results.update(ball_result)
    print("步骤 1/4 完成。")


    # --- 步骤 2: 人体骨骼点检测 ---
    success, pose_result = pose_detect(video_path=INPUT_VIDEO)
    if not success:
        print(f"流程终止于【骨骼点检测】。错误: {pose_result.get('error')}")
        exit(1)
    # 将此步骤的结果合并到主字典中
    pipeline_results.update(pose_result)
    print("步骤 2/4 完成。")


    # --- 步骤 3: 基于球轨迹的动作切分 ---
    success, segment_result = action_split(ball_json_path=pipeline_results["json_out_path"])
    if not success:
        print(f"流程终止于【动作片段切分】。错误: {segment_result.get('error')}")
        exit(1)
    # 将此步骤的结果合并到主字典中
    pipeline_results.update(segment_result)
    print("步骤 3/4 完成。")


    # --- 步骤 4: 动作识别与视频生成 ---
    success, final_result = action_detect(
        video_input_path=INPUT_VIDEO,
        pose_json_path=pipeline_results["json_out_path"],
        segment_json_path=pipeline_results["segment_json_path"],
    )
    if not success:
        print(f"流程终止于【动作识别】。错误: {final_result.get('error')}")
        exit(1)
    # 将此步骤的结果合并到主字典中
    pipeline_results.update(final_result)
    print("步骤 4/4 完成。")


    print("\n" + "=" * 25 + " 端到端视频分析流程全部成功完成! " + "=" * 25)
    print("\n所有生成的中间及最终文件路径:")
    # 打印包含所有路径的主字典
    for key, value in pipeline_results.items():
        # 确保路径存在才打印，对于像pose_detect可能不生成视频的情况
        if value:
            # 通过格式化输出，让键（key）对齐，看起来更整洁
            print(f"  - {key:<25}: {value}")