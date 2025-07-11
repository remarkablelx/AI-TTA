# `balldetect_pos_vel`文件夹
- 包含了用于检测乒乓球位置和速度的Python脚本。
- 该脚本使用OpenCV库来处理视频流，并通过图像处理技术来识别乒乓球的位置和速度。

---
```
.
└── balldetect_pos_vel/
    ├── ball_detect.py      # 进行乒乓球轨迹跟踪和速度计算
    ├── ball_detect.pt      # 基于TrackNet训练的模型文件
    └── utils/
        ├── general_back.py # 包含推理和后处理
        └── model.py        # 定义了TrackNet模型的结构
```