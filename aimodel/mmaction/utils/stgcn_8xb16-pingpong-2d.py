# mmaction2/configs/skeleton/stgcn/stgcn_improved_config_fixed.py

custom_imports = dict(imports=['mmaction.datasets.transforms'], allow_failed_imports=False)

_base_ = ['default_runtime.py']

# 使用预训练模型作为起点
load_from = r'stgcn_8xb16-joint-u100-80e_ntu60-xsub-keypoint-2d_20221129-484a394a.pth'

# 模型配置
model = dict(
    type='RecognizerGCN',
    backbone=dict(
        type='STGCN',
        graph_cfg=dict(layout='coco'),
        gcn_adaptive='init',
        gcn_with_res=True,
        tcn_type='mstcn'),
    cls_head=dict(
        type='GCNHead',
        num_classes=5,
        in_channels=256,
        loss_cls=dict(type='CrossEntropyLoss')))

# 数据集配置
dataset_type = 'PoseDataset'
data_root = 'data/'
ann_file_train = data_root + 'pingpong_train.pkl'
ann_file_val = data_root + 'pingpong_val.pkl'
ann_file_test = data_root + 'pingpong_val.pkl' # 测试时也使用验证集

# 训练数据管道
clip_len = 64
train_pipeline = [
    dict(type='PoseDecode'),
    dict(type='UniformSampleFrames', clip_len=clip_len),
    dict(type='Flip', flip_ratio=0.5, left_kp=[1, 3, 5, 7, 9, 11, 13, 15], right_kp=[2, 4, 6, 8, 10, 12, 14, 16]),
    dict(type='RandomResizedCrop', area_range=(0.56, 1.0)),
    dict(type='FormatGCNInput'),
    dict(type='PackActionInputs')
]

# 验证管道
val_pipeline = [
    dict(type='PoseDecode'),
    dict(type='UniformSampleFrames', clip_len=clip_len, num_clips=1, test_mode=True),
    dict(type='FormatGCNInput'),
    dict(type='PackActionInputs')
]

# 测试管道
test_pipeline = [
    dict(type='PoseDecode'),
    dict(type='UniformSampleFrames', clip_len=clip_len, num_clips=1, test_mode=True),
    dict(type='FormatGCNInput'),
    dict(type='PackActionInputs')
]

# 数据加载器配置
train_dataloader = dict(
    batch_size=8,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        split='pingpong_train',
        pipeline=train_pipeline))

# 验证和测试的数据加载器
val_dataloader = dict(
    batch_size=8,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        split='pingpong_val',
        pipeline=val_pipeline,
        test_mode=True))

test_dataloader = dict(
    batch_size=1,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_test,
        split='pingpong_val',
        pipeline=test_pipeline,
        test_mode=True))

# 评估器配置
val_evaluator = dict(type='AccMetric')
test_evaluator = val_evaluator

# 训练策略配置
train_cfg = dict(by_epoch=True, max_epochs=200, val_interval=5)
val_cfg = dict()
test_cfg = dict()

# 优化器和学习率配置
optim_wrapper = dict(
    optimizer=dict(type='AdamW', lr=0.0001, weight_decay=0.0005),
    clip_grad=dict(max_norm=40, norm_type=2))

# 学习率调度器
param_scheduler = [
    dict(type='CosineAnnealingLR', T_max=200, eta_min=0, by_epoch=True)
]
