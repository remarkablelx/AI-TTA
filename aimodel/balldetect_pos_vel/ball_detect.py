import json
from utils.model import BallTrackerNet
import torch
import cv2
from utils.general_back import postprocess
from tqdm import tqdm
import numpy as np
import argparse
from itertools import groupby
from scipy.spatial import distance


def read_video(path_video):
    """
    读取视频文件。

    :param path_video: 视频文件的路径
    :return:
        frames: 视频帧的列表
        fps: 视频的帧率
    """
    cap = cv2.VideoCapture(path_video)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
        else:
            break
    cap.release()
    return frames, fps


def infer_model(frames, model):
    """
    在一系列连续的视频帧上运行预训练模型。

    :param frames: 连续视频帧的列表
    :param model: 预训练好的模型
    :return:
        ball_track: 检测到的球点坐标列表
        dists: 相邻球点之间的欧氏距离列表
        output_video: 带有实时检测效果的帧列表
    """

    #cv2.namedWindow("Processing Preview", cv2.WINDOW_NORMAL)
    # 定义模型输入的图像尺寸
    height = 360
    width = 640

    # 初始化距离和轨迹列表，前两帧没有检测结果
    dists = [-1] * 2
    ball_track = [(None, None)] * 2

    # 添加视频写入准备
    output_video = []
    for num in tqdm(range(2, len(frames))):
        # 获取原始帧尺寸
        original_frame = frames[num]
        orig_height, orig_width = original_frame.shape[:2]

        img = cv2.resize(frames[num], (width, height))
        img_prev = cv2.resize(frames[num - 1], (width, height))
        img_preprev = cv2.resize(frames[num - 2], (width, height))
        imgs = np.concatenate((img, img_prev, img_preprev), axis=2)
        imgs = imgs.astype(np.float32) / 255.0
        imgs = np.rollaxis(imgs, 2, 0)
        inp = np.expand_dims(imgs, axis=0)
        out = model(torch.from_numpy(inp).float().to(device))
        output = out.argmax(dim=1).detach().cpu().numpy()
        # 计算坐标缩放比例
        scale_x = orig_width / width  # 宽度缩放因子
        scale_y = orig_height / height  # 高度缩放因子

        x_pred, y_pred = postprocess(output, scale_x, scale_y)
        ball_track.append((x_pred, y_pred))

        if ball_track[-1][0] and ball_track[-2][0]:
            dist = distance.euclidean(ball_track[-1], ball_track[-2])
        else:
            dist = -1
        dists.append(dist)
        # 创建实时预览帧
        preview_frame = frames[num].copy()
        # 添加坐标显示
        # 获取当前帧坐标
        current_x, current_y = x_pred, y_pred

        # 坐标文本格式化
        coord_text = f"X: {current_x:.1f}" if current_x else "X: NaN"
        coord_text += f"  Y: {current_y:.1f}" if current_y else "  Y: NaN"

        # 绘制坐标信息
        text_scale = 1.2
        text_thickness = 2
        text_color = (255, 255, 255)
        bg_color = (40, 40, 40)

        # 计算文字区域尺寸
        (text_width, text_height), _ = cv2.getTextSize(
            coord_text, cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_thickness)

        # 绘制背景矩形
        cv2.rectangle(preview_frame,
                      (10, 10),
                      (20 + text_width, 20 + text_height * 2),
                      bg_color, -1)

        # 绘制坐标文字
        cv2.putText(preview_frame, coord_text,
                    (20, 20 + text_height),
                    cv2.FONT_HERSHEY_SIMPLEX, text_scale,
                    text_color, text_thickness)

        # 绘制实时轨迹（最近3帧）
        for i in range(10):
            idx = num - i
            if idx >= 0 and ball_track[idx][0]:
                color = (0, 0, 255) if i == 0 else (0, 255, 0)
                cv2.circle(preview_frame,
                           (int(ball_track[idx][0]), int(ball_track[idx][1])),
                           radius=3, color=color, thickness=-1)

        # 实时显示
        # cv2.imshow("Processing Preview", cv2.resize(preview_frame, (orig_width, orig_height)))
        output_video.append(preview_frame)

        # 按ESC可提前终止
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    return ball_track, dists, output_video  # 修改返回值


def remove_outliers(ball_track, dists, max_dist=100):
    """
    从模型预测中移除离群点。
    如果一个点与前一个点的距离超过阈值，则视为离群点。

    :param ball_track: 检测到的球点坐标列表
    :param dists: 相邻球点之间的欧氏距离列表
    :param max_dist: 两个相邻球点之间的最大允许距离
    :return: 清理后的球点坐标列表
    """
    outliers = list(np.where(np.array(dists) > max_dist)[0])
    # 简单的离群点判断逻辑：如果当前点和后一个点的距离都很大，则将当前点移除
    for i in outliers:
        if (dists[i + 1] > max_dist) | (dists[i + 1] == -1):
            ball_track[i] = (None, None)
            outliers.remove(i)
        elif dists[i - 1] == -1:
            ball_track[i - 1] = (None, None)
    return ball_track


def split_track(ball_track, max_gap=4, max_dist_gap=80, min_track=5):
    """
    将完整的球轨迹分割成多个子轨迹，用于后续的插值处理。
    分割的依据是连续未检测到球的帧数（gap）或两段轨迹间的距离。

    :param ball_track: 球点坐标列表
    :param max_gap: 允许插值的最大连续None值数量
    :param max_dist_gap: 两个子轨迹端点之间的最大平均距离
    :param min_track: 一个有效子轨迹所需的最短帧数
    :return: result: 一个包含每个子轨迹起始和结束索引的列表
    """

    # 0表示检测到，1表示未检测到(None)
    list_det = [0 if x[0] else 1 for x in ball_track]
    groups = [(k, sum(1 for _ in g)) for k, g in groupby(list_det)]

    cursor = 0
    min_value = 0
    result = []
    for i, (k, l) in enumerate(groups):
        if (k == 1) & (i > 0) & (i < len(groups) - 1):
            dist = distance.euclidean(ball_track[cursor - 1], ball_track[cursor + l])
            if (l >= max_gap) | (dist / l > max_dist_gap):
                if cursor - min_value > min_track:
                    result.append([min_value, cursor])
                    min_value = cursor + l - 1
        cursor += l
    if len(list_det) - min_value > min_track:
        result.append([min_value, len(list_det)])
    return result


def interpolation(coords):
    """
    在一个子轨迹内部进行线性插值，填补缺失的球坐标。

    :param coords: 一个子轨迹的球坐标列表（包含None值）
    :return: track: 插值后的球坐标列表
    """

    def nan_helper(y):
        return np.isnan(y), lambda z: z.nonzero()[0]

    x = np.array([x[0] if x[0] is not None else np.nan for x in coords])
    y = np.array([x[1] if x[1] is not None else np.nan for x in coords])

    nons, yy = nan_helper(x)
    x[nons] = np.interp(yy(nons), yy(~nons), x[~nons])
    nans, xx = nan_helper(y)
    y[nans] = np.interp(xx(nans), xx(~nans), y[~nans])

    track = [*zip(x, y)]
    return track


def write_track(frames, ball_track, path_output_video, fps, trace=7):
    """
    将带有检测轨迹的帧写入一个新的.avi视频文件。
    注意：在这个版本中，输入的`frames`已经是带有轨迹预览的帧了。
    这个函数可以直接将这些处理过的帧写入视频。

    :param frames: 带有轨迹的视频帧列表
    :param ball_track: 球坐标列表 (在此实现中未使用，因为轨迹已绘制在frames上)
    :param path_output_video: 输出视频的路径
    :param fps: 视频的帧率
    :param trace: 轨迹的长度 (在此实现中未使用)
    """

    height, width = frames[0].shape[:2]
    out = cv2.VideoWriter(path_output_video, cv2.VideoWriter_fourcc(*'DIVX'),
                          fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=2, help='batch size')
    parser.add_argument('--model_path', type=str, help='path to model')
    parser.add_argument('--video_path', type=str, help='path to input video')
    parser.add_argument('--video_out_path', type=str, help='path to output video')
    parser.add_argument('--extrapolation', action='store_true', help='whether to use ball track extrapolation')
    parser.add_argument('--json_out_path', type=str, help='path to output JSON file for ball trajectory')

    args = parser.parse_args()

    model = BallTrackerNet()
    device = 'cuda'
    model.load_state_dict(torch.load(args.model_path, map_location=device))
    model = model.to(device)
    model.eval()

    frames, fps = read_video(args.video_path)
    ball_track, dists, processed_frames = infer_model(frames, model)  # 获取处理后的帧
    ball_track = remove_outliers(ball_track, dists)

    if args.extrapolation:
        subtracks = split_track(ball_track)
        for r in subtracks:
            ball_subtrack = ball_track[r[0]:r[1]]
            ball_subtrack = interpolation(ball_subtrack)
            ball_track[r[0]:r[1]] = ball_subtrack
    # 如果指定了JSON输出路径，将轨迹保存为JSON
    if args.json_out_path:
        # 创建轨迹数据结构
        trajectory_data = []
        for i, (x, y) in enumerate(ball_track):
            if i < 2:  # 跳过初始化的两个点
                continue

            frame_data = {
                "frame": i,
                "position": {"x": x, "y": y} if x is not None else None,
                "distance": dists[i] if i < len(dists) else None
            }
            trajectory_data.append(frame_data)

        # 将数据写入JSON文件
        with open(args.json_out_path, 'w') as f:
            json.dump(trajectory_data, f, indent=4)
        print(f"Ball trajectory saved to {args.json_out_path}")

    write_track(processed_frames, ball_track, args.video_out_path, fps)
