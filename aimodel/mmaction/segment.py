# segment_by_ball_trajectory.py
import argparse
import json
import numpy as np


# (在 mmaction/segment.py 文件中)

def segment_by_reversals(input_path, output_path, pre_frames=15, post_frames=10, cooldown=20):
    """
    根据乒乓球轨迹在X轴和Y轴上的方向反转来切分动作片段。
    """
    print("正在加载乒乓球轨迹数据...")
    try:
        with open(input_path, 'r') as f:
            ball_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"错误: 处理文件失败 - {e}")
        return

    # --- 已修正的部分 开始 ---
    # 1. 从加载的JSON数据中获取 'trajectory' 列表
    trajectory_list = ball_data.get('trajectory')
    if trajectory_list is None:
        print("错误: JSON文件中未找到 'trajectory' 键。")
        return

    # 2. 从 trajectory_list 中构建 pos_map，并使用 'frame_index' 作为键
    pos_map = {item['frame_index']: (item['position']['x'], item['position']['y'])
               for item in trajectory_list if item.get('position') is not None}
    # --- 已修正的部分 结束 ---

    if not pos_map:
        print("警告: 未找到任何有效的球位置信息。")
        return

    # 1. 计算每一帧的速度向量 (vx, vy)
    velocities = {}
    sorted_frames = sorted(pos_map.keys())
    for i in range(len(sorted_frames) - 1):
        f1, f2 = sorted_frames[i], sorted_frames[i + 1]
        if f2 - f1 == 1:
            p1 = np.array(pos_map[f1])
            p2 = np.array(pos_map[f2])
            velocities[f1] = p2 - p1

    # 2. 分别检测X轴和Y轴上的方向反转事件
    event_frames = set()
    last_x_rev_frame = -float('inf')
    last_y_rev_frame = -float('inf')

    print("\n" + "=" * 50)
    print("--- 开始检测X轴(击球)和Y轴(轨迹顶点/发球)的反转事件 ---")
    print("=" * 50)

    sorted_v_frames = sorted(velocities.keys())
    for i in range(len(sorted_v_frames) - 1):
        f1, f2 = sorted_v_frames[i], sorted_v_frames[i + 1]
        if f2 - f1 == 1:
            v1 = velocities[f1]
            v2 = velocities[f2]
            vx1, vy1 = v1
            vx2, vy2 = v2

            if vx1 * vx2 < 0 and abs(vx1) + abs(vx2) > 5:
                if f1 - last_x_rev_frame > cooldown:
                    print(f"帧 {f1:03d}: 检测到 X轴反转 (击球). vx: {vx1:+.1f} -> {vx2:+.1f}")
                    event_frames.add(f1)
                    last_x_rev_frame = f1

            if vy1 * vy2 < 0 and abs(vy1) + abs(vy2) > 4:
                if f1 - last_y_rev_frame > cooldown:
                    print(f"帧 {f1:03d}: 检测到 Y轴反转 (顶点). vy: {vy1:+.1f} -> {vy2:+.1f}")
                    event_frames.add(f1)
                    last_y_rev_frame = f1

    sorted_event_frames = sorted(list(event_frames))
    print("\n" + "=" * 50)
    print(f"检测到 {len(sorted_event_frames)} 个独立的事件点: {sorted_event_frames}")
    print("=" * 50 + "\n")

    # 3. 根据事件点生成片段 (不合并)
    final_segments = []
    if not sorted_event_frames:
        print("未生成任何片段。")
    else:
        for frame in sorted_event_frames:
            start = max(0, frame - pre_frames)
            end = frame + post_frames
            final_segments.append({'start_frame': start, 'end_frame': end})
        print(f"已生成 {len(final_segments)} 个独立的动作片段。")

    # 4. 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_segments, f, indent=4)
    print(f"分段结果已成功保存至: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Automatically segment actions based on ball trajectory analysis.")
    parser.add_argument(
        '--ball-trajectory-json',
        default='E:/fwwb/mmaction2-main/data/test/valid1_dealt.json',
        help='包含乒乓球轨迹跟踪信息的JSON文件路径。'
    )
    parser.add_argument(
        '--output-json',
        default='E:/fwwb/mmaction2-main/data/inference_input_from_ball_reversal.json',
        help='输出的自动分段JSON文件路径。'
    )
    # --- 可调参数 ---
    parser.add_argument('--pre-frames', type=int, default=15, help='在事件点前截取的帧数。')
    parser.add_argument('--post-frames', type=int, default=10, help='在事件点后截取的帧数。')
    parser.add_argument('--cooldown', type=int, default=15, help='两次同类型事件之间的最小冷却帧数。')

    args = parser.parse_args()

    segment_by_reversals(
        args.ball_trajectory_json,
        args.output_json,
        pre_frames=args.pre_frames,
        post_frames=args.post_frames,
        cooldown=args.cooldown
    )


if __name__ == '__main__':
    main()
