import os
import subprocess
import sys
from typing import Dict, Any, Tuple


# 球轨迹检测算法调用
def ball_detect(video_path: str) -> Tuple[bool, Dict[str, Any]]:
    print("--- [1/4] 启动球体跟踪任务 ---")
    try:
        if not os.path.exists(video_path):
            return False, {"error": f"输入视频文件不存在: {video_path}"}

        video_name = os.path.splitext(os.path.basename(video_path))[0]
        video_out_path = os.path.join('aimodel','video_output', f'{video_name}_ball_detect.mp4')
        json_out_path = os.path.join('aimodel','json', f'{video_name}_ball_detect.json')

        os.makedirs(os.path.dirname(video_out_path), exist_ok=True)
        os.makedirs(os.path.dirname(json_out_path), exist_ok=True)

        command = [
            sys.executable, 'aimodel/balldetect_pos_vel/ball_detect.py',
            '--video_path', video_path,
            '--model_path', 'aimodel/balldetect_pos_vel/ball_detect.pt',
            '--video_out_path', video_out_path,
            '--json_out_path', json_out_path,
            '--extrapolation'
        ]

        process = subprocess.run(
            command, capture_output=True, text=True, check=False, encoding='utf-8')

        if process.returncode == 0:
            print("--- 球体跟踪成功 ---")
            return True, {
                "ball_video_out_path": os.path.abspath(video_out_path),
                "ball_json_out_path": os.path.abspath(json_out_path)
            }
        else:
            return False, {"error": process.stderr if process.stderr else process.stdout}

    except Exception as e:
        return False, {"error": f"调用脚本时发生意外错误: {str(e)}"}


# 骨骼点检测算法调用
def pose_detect(video_path: str) -> Tuple[bool, Dict[str, Any]]:
    print("--- [2/4] 启动骨骼点检测任务 ---")
    try:
        if not os.path.exists(video_path):
            return False, {"error": f"输入文件不存在: {video_path}"}

        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_dir_for_video = os.path.join('aimodel','video_output')
        final_json_out_path = os.path.join('aimodel','json', f'{video_name}_pose_detect.json')

        os.makedirs(output_dir_for_video, exist_ok=True)
        os.makedirs(os.path.dirname(final_json_out_path), exist_ok=True)

        command = [
            sys.executable, 'aimodel/mmpose/predict.py',
            'aimodel/mmpose/utils/coco_person.py',
            'aimodel/mmpose/utils/model1.pth',
            'aimodel/mmpose/utils/config.py',
            'aimodel/mmpose/utils/model2.pth',
            '--input', video_path,
            '--output-root', output_dir_for_video,
            '--save-predictions',
            '--draw-bbox'
        ]

        process = subprocess.run(
            command, capture_output=True, text=True, check=False, encoding='utf-8')

        output_file = os.path.join(output_dir_for_video, f'{video_name}_pose_detect.mp4')

        if process.returncode == 0:
            generated_json = os.path.join(output_dir_for_video, f'results_{video_name}.json')
            if os.path.exists(generated_json):
                if os.path.exists(final_json_out_path):
                    os.remove(final_json_out_path)
                os.rename(generated_json, final_json_out_path)

            if not os.path.exists(final_json_out_path):
                return False, {
                    "error": f"错误: pose_detect.py 成功运行但未能找到或重命名JSON文件至: {final_json_out_path}"}
            print("--- 骨骼点检测成功 ---")
            return True, {
                "pose_json_out_path": os.path.abspath(final_json_out_path),
                "pose_video_out_path": os.path.abspath(output_file)
            }
        else:
            return False, {"error": process.stderr if process.stderr else process.stdout}

    except Exception as e:
        return False, {"error": f"调用脚本时发生意外错误: {str(e)}"}


# 基于球轨迹json文件进行动作片段的分割
def action_split(ball_json_path: str) -> Tuple[bool, Dict[str, Any]]:
    print("--- [3/4] 启动动作片段切分任务 ---")
    try:
        if not os.path.exists(ball_json_path):
            return False, {"error": f"球轨迹JSON文件不存在: {ball_json_path}"}
        ball_json_name = os.path.splitext(os.path.basename(ball_json_path))[0]
        output_segment_json_path = os.path.join('aimodel','json', f"{ball_json_name}_segments.json")
        os.makedirs(os.path.dirname(output_segment_json_path), exist_ok=True)

        command = [
            sys.executable, 'aimodel/mmaction/segment.py',
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


# 根据分割的片段进行动作识别
def action_detect(video_input_path: str, pose_json_path: str, segment_json_path: str) -> Tuple[bool, Dict[str, Any]]:
    print("--- [4/4] 启动动作识别任务 ---")
    try:
        video_path = os.path.splitext(os.path.basename(video_input_path))[0]
        output_video_path = os.path.join('video_output', f"{video_path}_action.mp4")
        recognition_json_path = os.path.join('json', f"{video_path}_action.json")

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
            generated_json = os.path.join(os.path.dirname(output_video_path), 'multi_person_recognition_results.json')
            if os.path.exists(generated_json):
                if os.path.exists(recognition_json_path):
                    os.remove(recognition_json_path)
                os.rename(generated_json, recognition_json_path)

            print("--- 动作识别成功 ---")
            print(f"输出视频路径: {output_video_path}")
            print(f"识别结果JSON路径: {recognition_json_path}")
            return True, {
                "annotated_video_path": os.path.abspath(output_video_path),
                "recognition_json_path": os.path.abspath(recognition_json_path)
            }
        else:
            return False, {"error": process.stderr if process.stderr else process.stdout}

    except Exception as e:
        return False, {"error": f"调用脚本时发生意外错误: {str(e)}"}


# 生成个性化报告
def report_generate(pose_json_path: str) -> Tuple[bool, Dict[str, Any]]:
    """
    通过命令行调用 report.py 脚本，为输入的骨骼点数据生成分析报告。

    :param pose_json_path: 包含骨骼点信息的JSON文件路径。
    :return: 一个元组 (success, result_dict)。
             - success: 布尔值，表示是否成功。
             - result_dict: 包含输出报告路径或错误信息的字典。
    """
    print("--- 启动个性化报告生成任务 ---")
    try:
        if not os.path.exists(pose_json_path):
            return False, {"error": f"错误: 骨骼点JSON文件不存在: {pose_json_path}"}

        input_basename = os.path.splitext(os.path.basename(pose_json_path))[0]
        output_report_path = os.path.join('aimodel', 'report', f"{input_basename}_report.md")
        os.makedirs(os.path.dirname(output_report_path), exist_ok=True)

        command = [
            sys.executable,
            'aimodel/report_gen/report.py',  # report.py 的路径
            '--input',
            pose_json_path
        ]

        print(f"执行命令: {' '.join(command)}")

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            encoding='utf-8',
            timeout=600  # 10分钟超时，防止进程卡死
        )

        if process.returncode == 0:
            if not os.path.exists(output_report_path):
                return False, {
                    "error": f"脚本成功运行但未在预期位置找到报告文件: {output_report_path}\n"
                             f"子进程输出: {process.stdout}\n"
                             f"子进程错误: {process.stderr}"
                }
            print("--- 个性化报告生成成功 ---")
            return True, {"report_path": os.path.abspath(output_report_path)}
        else:
            error_message = process.stderr if process.stderr else process.stdout
            print(f"--- 个性化报告生成失败 ---\n{error_message}")
            return False, {"error": error_message}

    except subprocess.TimeoutExpired:
        return False, {"error": "错误：报告生成超时。任务可能过于复杂或网络延迟较高。"}
    except Exception as e:
        return False, {"error": f"调用脚本时发生意外错误: {str(e)}"}


if __name__ == "__main__":
    # INPUT_VIDEO = 'video/test.mp4'
    #
    # if not os.path.exists(INPUT_VIDEO):
    #     print(f"错误: 初始输入视频不存在: {INPUT_VIDEO}")
    #     exit(1)
    #
    # print("=" * 25 + " 开始执行端到端视频分析流水线 " + "=" * 25)
    #
    # # 创建一个主字典来收集所有路径
    # pipeline_results = {}

    # # --- 步骤 1: 球体轨迹跟踪 ---
    # success, ball_result = ball_detect(video_path=INPUT_VIDEO)
    # if not success:
    #     print(f"流程终止于【球体跟踪】。错误: {ball_result.get('error')}")
    #     exit(1)
    # # 将此步骤的结果合并到主字典中
    # pipeline_results.update(ball_result)
    # print("步骤 1/4 完成。")


    # # --- 步骤 2: 人体骨骼点检测 ---
    # success, pose_result = pose_detect(video_path=INPUT_VIDEO)
    # if not success:
    #     print(f"流程终止于【骨骼点检测】。错误: {pose_result.get('error')}")
    #     exit(1)
    # # 将此步骤的结果合并到主字典中
    # pipeline_results.update(pose_result)
    # print("步骤 2/4 完成。")


    # # --- 步骤 3: 基于球轨迹的动作切分 ---
    # success, segment_result = action_split(ball_json_path=pipeline_results["json_out_path"])
    # if not success:
    #     print(f"流程终止于【动作片段切分】。错误: {segment_result.get('error')}")
    #     exit(1)
    # # 将此步骤的结果合并到主字典中
    # pipeline_results.update(segment_result)
    # print("步骤 3/4 完成。")


    # --- 步骤 4: 动作识别与视频生成 ---
    # success, final_result = action_detect(
    #     video_input_path=INPUT_VIDEO,
    #     pose_json_path=pipeline_results["json_out_path"],
    #     segment_json_path=pipeline_results["segment_json_path"],
    # )
    success, final_result = action_detect(
        video_input_path=r"E:\fwwb\shixun\aimodel\video_output\val3_ball_detect_pose_detect.mp4",
        pose_json_path=r"E:\fwwb\shixun\aimodel\json\val3.mp4_ball_detect_pose_detect.json",
        segment_json_path=r"E:\fwwb\shixun\aimodel\json\val3.mp4_ball_detect_segments.json",
    )
    if not success:
        print(f"流程终止于【动作识别】。错误: {final_result.get('error')}")
        exit(1)
    # 将此步骤的结果合并到主字典中
    # pipeline_results.update(final_result)
    print("步骤 4/4 完成。")


    print("\n" + "=" * 25 + " 端到端视频分析流程全部成功完成! " + "=" * 25)
    print("\n所有生成的中间及最终文件路径:")
    # 打印包含所有路径的主字典
    # for key, value in pipeline_results.items():
    #     if value:
    #         print(f"  - {key:<25}: {value}")

    # # 报告生成测试
    # POSE_JSON_INPUT = os.path.join('aimodel', 'json', 'test_pose_detect.json')
    #
    # if not os.path.exists(POSE_JSON_INPUT):
    #     print(f"\n!!! 错误: 必需的输入文件不存在 !!!")
    #     print(f"测试 `report_generate` 需要一个骨骼点JSON文件。")
    #     print(f"请确保路径 '{POSE_JSON_INPUT}' 是一个有效的文件路径。")
    #     print(f"您可能需要先运行 `pose_detect` 函数来生成它。")
    # else:
    #     print("\n" + "=" * 25 + " 开始测试 'report_generate' 函数 " + "=" * 25)
    #
    #     success, result = report_generate(pose_json_path=POSE_JSON_INPUT)
    #
    #     print("\n----------- 调用结果 -----------")
    #     if success:
    #         print("状态: \033[92m成功\033[0m")  # 绿色
    #         print("输出文件路径:")
    #         for key, value in result.items():
    #             print(f"  - {key}: {value}")
    #     else:
    #         print("状态: \033[91m失败\033[0m")  # 红色
    #         print("错误信息:", result.get('error', '未知错误'))
    #     print("---------------------------------")