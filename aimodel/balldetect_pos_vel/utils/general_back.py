import torch
import time
import numpy as np
import torch.nn as nn
import cv2
from scipy.spatial import distance

def train(model, train_loader, optimizer, device, epoch, max_iters=200):
    """
        模型训练函数，用于执行一个epoch的训练。

        :param model: 要训练的模型
        :param train_loader: 训练数据的DataLoader
        :param optimizer: 优化器
        :param device: 'cpu' 或 'cuda'
        :param epoch: 当前的epoch数
        :param max_iters: 每个epoch的最大迭代次数
        :return: 当前epoch的平均损失
    """
    start_time = time.time()
    losses = []
    criterion = nn.CrossEntropyLoss()
    for iter_id, batch in enumerate(train_loader):
        optimizer.zero_grad()
        model.train()

        out = model(batch[0].float().to(device))
        gt = torch.tensor(batch[1], dtype=torch.long, device=device)
        loss = criterion(out, gt)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        end_time = time.time()
        duration = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))
        print('train | epoch = {}, iter = [{}|{}], loss = {}, time = {}'.format(epoch, iter_id, max_iters,
                                                                                round(loss.item(), 6), duration))
        losses.append(loss.item())

        if iter_id > max_iters - 1:
            break

    return np.mean(losses)

def validate(model, val_loader, device, epoch, min_dist=5):
    """
        模型验证函数，用于评估模型在验证集上的性能。

        :param model: 要验证的模型
        :param val_loader: 验证数据的DataLoader
        :param device: 'cpu' 或 'cuda'
        :param epoch: 当前的epoch数
        :param min_dist: 判断为真阳性(TP)的最大像素距离
        :return: 平均损失, 准确率, 召回率, F1分数
    """
    height = 360
    width = 640
    orig_height = 1080
    orig_width = 1920
    # 计算坐标缩放比例
    scale_x = orig_width / width  # 宽度缩放因子
    scale_y = orig_height / height  # 高度缩放因子

    losses = []
    tp = [0, 0, 0, 0]
    fp = [0, 0, 0, 0]
    tn = [0, 0, 0, 0]
    fn = [0, 0, 0, 0]
    criterion = nn.CrossEntropyLoss()
    model.eval()
    for iter_id, batch in enumerate(val_loader):
        with torch.no_grad():
            out = model(batch[0].float().to(device))
            gt = torch.tensor(batch[1], dtype=torch.long, device=device)
            loss = criterion(out, gt)
            losses.append(loss.item())
            # metrics
            output = out.argmax(dim=1).detach().cpu().numpy()
            for i in range(len(output)):
                x_pred, y_pred = postprocess(output[i],scale_x, scale_y)
                x_gt = batch[2][i]
                y_gt = batch[3][i]
                vis = batch[4][i]
                if x_pred:
                    if vis != 0:
                        dst = distance.euclidean((x_pred, y_pred), (x_gt, y_gt))
                        if dst < min_dist:
                            tp[vis] += 1
                        else:
                            fp[vis] += 1
                    else:
                        fp[vis] += 1
                if not x_pred:
                    if vis != 0:
                        fn[vis] += 1
                    else:
                        tn[vis] += 1
            print('val | epoch = {}, iter = [{}|{}], loss = {}, tp = {}, tn = {}, fp = {}, fn = {} '.format(epoch,
                                                                                                            iter_id,
                                                                                                            len(val_loader),
                                                                                                            round(np.mean(losses), 6),
                                                                                                            sum(tp),
                                                                                                            sum(tn),
                                                                                                            sum(fp),
                                                                                                            sum(fn)))
    eps = 1e-15
    precision = sum(tp) / (sum(tp) + sum(fp) + eps)
    vc1 = tp[1] + fp[1] + tn[1] + fn[1]
    vc2 = tp[2] + fp[2] + tn[2] + fn[2]
    vc3 = tp[3] + fp[3] + tn[3] + fn[3]
    recall = sum(tp) / (vc1 + vc2 + vc3 + eps)
    f1 = 2 * precision * recall / (precision + recall + eps)
    print('precision = {}'.format(precision))
    print('recall = {}'.format(recall))
    print('f1 = {}'.format(f1))

    return np.mean(losses), precision, recall, f1


def postprocess(feature_map, scale_x, scale_y):
    """
    后处理函数，将模型的输出热力图转换为球的坐标。

    :param feature_map: 模型输出的单通道特征图
    :param scale_x: 宽度方向的缩放因子
    :param scale_y: 高度方向的缩放因子
    :return: x, y: 球在原始图像尺寸下的坐标，如果未检测到则为None
    """
    feature_map *= 255
    feature_map = feature_map.reshape((360, 640))
    feature_map = feature_map.astype(np.uint8)
    ret, heatmap = cv2.threshold(feature_map, 127, 255, cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(heatmap, cv2.HOUGH_GRADIENT, dp=1, minDist=1, param1=50, param2=2, minRadius=2,
                               maxRadius=7)
    x,y = None, None
    if circles is not None:
        if len(circles) == 1:
            x = circles[0][0][0] * scale_x
            y = circles[0][0][1] * scale_y
    return x, y



