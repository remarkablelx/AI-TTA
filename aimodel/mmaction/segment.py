# segment.py
import argparse
import json
import numpy as np


def segment_by_reversals(input_path, output_path, pre_frames=15, post_frames=10, cooldown=20):
    """
    根据乒乓球轨迹在X轴和Y轴上的方向反转来切分动作片段。

    Args:
        input_path (str): 包含球轨迹的JSON文件路径。
        output_path (str): 输出分段信息的JSON文件路径。
        pre_frames (int): 在事件点前截取的帧数。
        post_frames (int): 在事件点后截取的帧数。
        cooldown (int): 两次同类型事件之间的最小帧数（冷却时间）。
    """
    print("正在加载乒乓球轨迹数据...")
    try:
        with open(input_path, 'r') as f:
            ball_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"错误: 处理文件失败 - {e}")
        return

    # 检查并处理不同格式的数据
    try:
        # 如果ball_data是字典且包含轨迹数据
        if isinstance(ball_data, dict) and 'trajectory' in ball_data:
            trajectory_data = ball_data['trajectory']
        # 如果ball_data本身就是轨迹数据列表
        elif isinstance(ball_data, list):
            trajectory_data = ball_data
        else:
            # 尝试解析可能嵌套的JSON字符串
            if isinstance(ball_data, str):
                try:
                    trajectory_data = json.loads(ball_data)
                    if isinstance(trajectory_data, dict) and 'trajectory' in trajectory_data:
                        trajectory_data = trajectory_data['trajectory']
                except:
                    print(f"错误: 无法解析JSON字符串: {ball_data[:100]}...")
                    return
            else:
                print(f"错误: 不支持的数据格式: {type(ball_data)}")
                print(f"数据示例: {str(ball_data)[:100]}...")
                return

        # 构建pos_map，更健壮地处理字段名
        pos_map = {}
        for item in trajectory_data:
            if not isinstance(item, dict):
                continue

            frame_idx = item.get('frame', item.get('frame_index'))
            if frame_idx is None:
                continue

            position = item.get('position')
            if not position or not isinstance(position, dict):
                continue

            x = position.get('x')
            y = position.get('y')
            if x is not None and y is not None:
                pos_map[frame_idx] = (x, y)

    except Exception as e:
        print(f"错误: 处理球轨迹数据时发生异常 - {e}")
        return

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

            # --- 检测X轴反转 (击球) ---
            if vx1 * vx2 < 0 and abs(vx1) + abs(vx2) > 5:  # 增加速度幅度判断
                if f1 - last_x_rev_frame > cooldown:
                    print(f"帧 {f1:03d}: 检测到 X轴反转 (击球). vx: {vx1:+.1f} -> {vx2:+.1f}")
                    event_frames.add(f1)
                    last_x_rev_frame = f1

            # --- 检测Y轴反转 (轨迹顶点/抛球) ---
            if vy1 * vy2 < 0 and abs(vy1) + abs(vy2) > 4:  # Y轴速度阈值可以低一些
                if f1 - last_y_rev_frame > cooldown:
                    print(f"帧 {f1:03d}: 检测到 Y轴反转 (顶点). vy: {vy1:+.1f} -> {vy2:+.1f}")
                    event_frames.add(f1)
                    last_y_rev_frame = f1

    sorted_event_frames = sorted(list(event_frames))
    print("\n" + "=" * 50)
    print(f"检测到 {len(sorted_event_frames)} 个独立的事件点: {sorted_event_frames}")
    print("=" * 50 + "\n")

    # 3. 根据事件点生成片段
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
        help='包含乒乓球轨迹跟踪信息的JSON文件路径。'
    )
    parser.add_argument(
        '--output-json',
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
