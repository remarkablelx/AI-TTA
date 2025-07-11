# `mmaction`文件夹
- 包含了用于动作识别的Python脚本。
- 该脚本使用MMAction2库来处理视频流，并通过深度学习模型来识别视频中的动作。

---
```
.
└── mmaction/
    ├── infer.py      # 对包含动作片段的视频进行动作识别
    ├── segment.py    # 判断包含动作片段的内容并输出json文件
    └── utils/
        ├── action.txt                                          # 动作类别
        ├── best_acc_top1_epoch_65.pth                          # ST-GCN模型的最佳准确率检查点
        ├── default_runtime.py                                  # 配置文件
        ├── stgcn_8xb16-joint-u100-80e_ntu60-xsub-keypoint-2d...pth # 预训练模型
        └── stgcn_8xb16-pingpong-2d.py                          # 配置文件
```