# infer.py
import argparse
import json
import os
from collections import defaultdict
from tqdm import tqdm

import cv2
import mmengine
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from mmengine.runner import load_checkpoint

from mmaction.apis import init_recognizer, inference_recognizer
from mmaction.datasets.transforms import PackActionInputs

PERSON_COLORS_BGR = [
    (34, 139, 34), (255, 0, 0), (0, 0, 255),
    (0, 255, 255), (255, 255, 0), (255, 0, 255)
]


def parse_args():
    parser = argparse.ArgumentParser(description='Multi-person, Segment-based Action Recognition with Video Annotation')
    parser.add_argument(
        '--config',
        help='模型配置文件的路径'
    )
    parser.add_argument(
        '--checkpoint',
        help='模型权重文件的路径'
    )
    parser.add_argument(
        '--pose-json',
        help='包含完整视频骨骼点数据的JSON文件路径'
    )
    parser.add_argument(
        '--segments-json',
        help='包含视频分段信息的JSON文件路径'
    )
    parser.add_argument(
        '--class-names-file',
        help='类别名称文件的路径'
    )
    # --- 视频标注相关参数 ---
    parser.add_argument(
        '--video-input',
        help='输入视频文件的路径'
    )
    parser.add_argument(
        '--video-output',
        help='输出标注视频的路径'
    )
    parser.add_argument(
        '--device',
        type=str,
        default='cuda:0',
        help='使用的设备 (例如 "cuda:0" 或 "cpu")'
    )
    parser.add_argument(
        '--iou-threshold',
        type=float,
        default=0.4,
        help='用于追踪的IoU阈值'
    )
    args = parser.parse_args()
    return args


def calculate_iou(boxA, boxB):
    # 计算两个边界框的交并比(IoU)
    if not isinstance(boxA, (list, np.ndarray)) or len(boxA) < 4 or not isinstance(boxB, (list, np.ndarray)) or len(
            boxB) < 4:
        return 0.0
    xA, yA, xB, yB = max(boxA[0], boxB[0]), max(boxA[1], boxB[1]), min(boxA[2], boxB[2]), min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea, boxBArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1]), (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    denominator = float(boxAArea + boxBArea - interArea)
    return interArea / denominator if denominator != 0 else 0.0


def track_people_by_iou(frame_data_map, total_frames, iou_threshold=0.4):
    # 使用IoU对检测到的人进行追踪
    print("正在通过IoU追踪人员...")
    tracks, next_person_id, person_tracks = [], 0, defaultdict(dict)
    for frame_id in tqdm(range(total_frames), desc="追踪进度"):
        instances = frame_data_map.get(frame_id, [])
        if not instances: continue
        matched_indices = set()
        if not tracks:
            for inst in instances:
                tracks.append({'id': next_person_id, 'bbox': inst['bbox'][0], 'last_frame': frame_id})
                person_tracks[next_person_id][frame_id] = inst
                next_person_id += 1
            continue
        iou_matrix = np.zeros((len(tracks), len(instances)))
        for i, track in enumerate(tracks):
            for j, inst in enumerate(instances):
                iou_matrix[i, j] = calculate_iou(track['bbox'], inst['bbox'][0])
        for _ in range(len(tracks)):
            if iou_matrix.size == 0 or np.max(iou_matrix) < iou_threshold: break
            track_idx, inst_idx = np.unravel_index(np.argmax(iou_matrix), iou_matrix.shape)
            track, instance = tracks[track_idx], instances[inst_idx]
            person_tracks[track['id']][frame_id], track['bbox'], track['last_frame'] = instance, instance['bbox'][
                0], frame_id
            matched_indices.add(inst_idx)
            iou_matrix[track_idx, :], iou_matrix[:, inst_idx] = -1, -1
        for i, inst in enumerate(instances):
            if i not in matched_indices:
                tracks.append({'id': next_person_id, 'bbox': inst['bbox'][0], 'last_frame': frame_id})
                person_tracks[next_person_id][frame_id] = inst
                next_person_id += 1
        tracks = [t for t in tracks if frame_id - t['last_frame'] < 5]
    print(f"追踪完成，共发现 {len(person_tracks)} 条独立轨迹。")
    return person_tracks


def visualize_and_save(video_path, output_path, person_tracks, recognition_results):
    # 将识别结果绘制到视频上并保存
    print(f"开始生成标注视频: {output_path}")

    # 1. 加载视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"错误: 无法打开视频文件 {video_path}")
        return
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 2. 设置视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 3. 准备字体
    try:
        # 尝试使用常见的黑体，如果找不到，Pillow会使用默认字体
        font = ImageFont.truetype("simhei.ttf", 20)
    except IOError:
        print("警告: 未找到'simhei.ttf'字体，将使用Pillow的默认字体，中文可能无法显示。")
        font = ImageFont.load_default()

    # 4. 重构识别结果为按帧查找的格式，并解决重叠问题
    action_timeline = defaultdict(dict)
    for res in recognition_results:
        person_id = res['person_id']
        start_frame, end_frame = res['segment_frames']
        confidence = res['confidence_score']
        label = f"{res['predicted_label']} ({confidence:.2f})"

        for i in range(start_frame, end_frame + 1):
            # 如果该帧还没有这个人的标签，或者新标签的置信度更高，则更新
            if person_id not in action_timeline[i] or confidence > action_timeline[i][person_id][1]:
                action_timeline[i][person_id] = (label, confidence)

    # 5. 逐帧处理并绘制
    for frame_idx in tqdm(range(total_frames), desc="视频生成进度"):
        ret, frame = cap.read()
        if not ret:
            break

        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)

        # 绘制当前帧的所有人员
        for person_id, track_data in person_tracks.items():
            if frame_idx in track_data:
                instance = track_data[frame_idx]
                bbox = instance['bbox'][0]
                x1, y1, x2, y2 = map(int, bbox)

                color = PERSON_COLORS_BGR[person_id % len(PERSON_COLORS_BGR)]
                color_rgb = (color[2], color[1], color[0])

                # 绘制边界框
                draw.rectangle([(x1, y1), (x2, y2)], outline=color_rgb, width=3)

                # 检查并绘制动作标签
                if frame_idx in action_timeline and person_id in action_timeline[frame_idx]:
                    # 从元组中获取最终要显示的文本
                    display_text, _ = action_timeline[frame_idx][person_id]

                    text_bbox = draw.textbbox((0, 0), display_text, font=font)
                    text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

                    # 绘制文字背景
                    draw.rectangle([(x1, y1 - text_h - 10), (x1 + text_w + 8, y1 - 5)], fill=color_rgb)
                    # 绘制文字
                    draw.text((x1 + 4, y1 - text_h - 10), display_text, font=font, fill=(255, 255, 255))

        processed_frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        writer.write(processed_frame)

    # 6. 释放资源
    cap.release()
    writer.release()
    print("视频生成完成！")


def main():
    args = parse_args()

    # 初始化模型和加载数据
    print("正在初始化模型...")
    model = init_recognizer(args.config, args.checkpoint, device=args.device)
    print("正在加载数据...")
    with open(args.pose_json, 'r') as f:
        full_pose_data = json.load(f)
    with open(args.segments_json, 'r') as f:
        segments_data = json.load(f)

    frame_data_map = {item['frame_id']: item['instances'] for item in full_pose_data['instance_info']}
    total_frames = max(frame_data_map.keys()) + 1 if frame_data_map else 0
    img_height, img_width = 1080, 1920
    if 'meta_info' in full_pose_data and 'video_info' in full_pose_data['meta_info']:
        video_info = full_pose_data['meta_info']['video_info']
        img_height, img_width = video_info.get('height', 1080), video_info.get('width', 1920)

    # 人员追踪
    person_tracks = track_people_by_iou(frame_data_map, total_frames, args.iou_threshold)

    # 对每个人的每个分段进行推理
    all_results = []
    print(f"开始对 {len(segments_data)} 个分段和 {len(person_tracks)} 个人员进行推理...")
    with open(args.class_names_file, 'r', encoding='utf-8') as f:
        class_names = [line.strip().split(':')[1] for line in f]

    for segment in tqdm(segments_data, desc="分段推理进度"):
        start_frame, end_frame = segment['start_frame'], segment['end_frame']
        for person_id, track_data in person_tracks.items():
            keypoints_segment, scores_segment = [], []
            for frame_id in range(start_frame, end_frame + 1):
                instance = track_data.get(frame_id)
                if instance:
                    keypoints_segment.append(instance['keypoints'])
                    scores_segment.append(instance['keypoint_scores'])
                else:
                    keypoints_segment.append(np.zeros((17, 2)).tolist())
                    scores_segment.append(np.zeros(17).tolist())

            if np.all(np.array(scores_segment) == 0): continue

            data_info = {
                'keypoint': np.array(keypoints_segment, dtype=np.float32).reshape(1, -1, 17, 2),
                'keypoint_score': np.array(scores_segment, dtype=np.float32).reshape(1, -1, 17),
                'total_frames': len(keypoints_segment), 'img_shape': (img_height, img_width),
                'frame_inds': np.arange(len(keypoints_segment))
            }
            result = inference_recognizer(model, data_info)
            pred_scores = result.pred_score.cpu().numpy()
            top1_idx = pred_scores.argmax()
            all_results.append({
                "person_id": person_id, "segment_frames": [start_frame, end_frame],
                "predicted_label": class_names[top1_idx],
                "confidence_score": float(pred_scores[top1_idx]),
            })

    # 将结果保存为JSON文件
    output_json_path = os.path.join(os.path.dirname(args.video_output), 'multi_person_recognition_results.json')
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    print(f"\n推理JSON结果已保存至: {output_json_path}")

    # 将结果绘制到视频上并保存
    visualize_and_save(args.video_input, args.video_output, person_tracks, all_results)


if __name__ == '__main__':
    main()
