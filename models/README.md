# Models层架构说明

该文件夹包含系统核心数据模型的Flask-SQLAlchemy定义，共六个主要实体类，每个类对应数据库中的一个数据库表。

## 📂 模型文件结构
```plaintext
models/
├── Admin.py        # 管理员模型
├── Record.py       # 观看记录模型
├── Report.py       # 分析报告模型
├── Result.py       # 分析结果模型
├── User.py         # 用户模型
└── Video.py        # 视频模型
```

# 具体模型类说明

## 1️⃣ 管理员模型 (Admin)
**表名**: `admin`

### 字段
- `admin_id` (主键)：管理员ID
- `account`：管理员账号
- `password`：密码

### 功能
存储后台管理员账户信息

---

## 2️⃣ 分析记录模型 (Record)
**表名**: `record`

### 字段
- `record_id` (主键)：记录ID
- `video_id` (外键)：关联视频ID
- `user_id` (外键)：关联用户ID
- `state`：观看状态
- `time`：生成时间
- `expiration_time`：过期时间

### 索引
- `video_id_idx`: 视频ID索引
- `user_id_idx`: 用户ID索引

### 功能
储存分析记录

---

## 3️⃣ 分析报告模型 (Report)
**表名**: `report`

### 字段
- `report_id` (主键)：报告ID
- `pose_estimate`：姿势评估报告(JSON格式)
- `result_id`：关联的分析结果ID

### 索引
- `result_id_idx`: 分析结果ID索引

### 功能
存储动作分析的报告

---

## 4️⃣ 分析结果模型 (Result)
**表名**: `result`

### 字段
- `result_id` (主键)：结果ID
- `video_id` (外键)：关联视频ID
- `ball_json_path`：球轨迹文件路径
- `pose_json_path`：骨骼点文件路径
- `ball_video_path`：球视频路径
- `pose_video_path`：姿态视频路径
- `segment_json_path`：动作分段路径
- `annotated_video_path`：标注视频路径
- `recognition_json_path`：动作标签路径

### 索引
- `video_idx`: 视频ID索引

### 功能
存储视频分析生成的各类结果文件路径

---

## 5️⃣ 用户模型 (User)
**表名**: `user`

### 字段
- `user_id` (主键)：用户ID
- `account` (唯一)：用户账号
- `password`：密码
- `nickname`：昵称
- `avatar`：头像
- `height`：身高
- `weight`：体重
- `sex`：性别
- `birth`：出生日期
- `location`：地理位置
- `email`：电子邮箱
- `register_time`：注册时间

### 功能
存储用户账户信息和用户画像数据

---

## 6️⃣ 视频模型 (Video)
**表名**: `video`

### 字段
- `video_id` (主键)：视频ID
- `video_path`：存储路径
- `video_name`：视频名称
- `video_size`：文件大小
- `video_duration`：时长
- `video_format`：格式
- `video_resolution`：分辨率
- `video_frame_rate`：帧率

### 功能
存储物理视频文件和视频元数据信息



