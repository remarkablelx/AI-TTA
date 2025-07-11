# `mmpose`文件夹
- 包含了用于人体姿态估计的Python脚本。
- 该脚本使用MMPose库来处理视频流，并通过深度学习模型来识别人体关键点。

---
```
.
└── mmpose/
    ├── predict.py      # 对视频进行人体骨骼点的识别，并保存json文件和视频文件
    └── utils/
        ├── coco_person.py        # 配置文件
        ├── config.py             # 配置文件
        ├── default_runtime.py    # 配置文件
        ├── model1.pth            # 识别预训练模型文件
        └── model2.pth            # 骨骼预训练模型文件
```