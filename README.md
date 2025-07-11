# AI-TTA

## 核心框架

[![Flask](https://img.shields.io/badge/Flask-2.0.x-blue)](https://flask.palletsprojects.com/)
[![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen)](https://vuejs.org/)

## 相关技术栈

**后端服务**  
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0.x-blue?logo=flask)
![Flask-CORS](https://img.shields.io/badge/Flask--CORS-3.0.x-lightgrey)

**前端服务**  
![Vue3](https://img.shields.io/badge/Vue-3.x-brightgreen?logo=vue.js)
![Pinia](https://img.shields.io/badge/Pinia-2.x-orange?logo=vue.js)
![Vue Router](https://img.shields.io/badge/vue_router-4.x-green?logo=vue.js)
![Vite](https://img.shields.io/badge/Vite-4.x-purple?logo=vite)
![Axios](https://img.shields.io/badge/Axios-1.x-blueviolet)
![piESLint](https://img.shields.io/badge/ESLint-8.x-red?logo=eslint)
![ECharts](https://img.shields.io/badge/ECharts-5.6.x-red?logo=ECharts)

## 项目结构
```
/AI-TTA
├── /aimodel            # AI算法模型
├── /avatar             # 头像图片
├── /config             # 数据库配置
├── /models             # 模型层，存放数据模型类
├── /routes             # 路由层，存放路由处理函数
├── /services           # 服务层，存放业务逻辑处理函数
├── /setup              # 数据库文件和需要修改的库包
├── /vue                # 前端代码
├── app.py              # Flask应用入口
└── requirements.txt    # Python依赖包列表
```

## 🌐 使用方法
### 克隆仓库
```bash
git clone https://github.com/remarkablelx/AI-TTA
```
---
## 后端部署
### 创建虚拟环境
```bash
conda create -n your_env_name python=3.10
conda activate your_env_name
```
### 安装依赖
```bash
pip install -r requirements.txt
```
### 特殊环境安装（一定要再次安装确定环境正确配置）
```bash
# CUDA 11.8 + Torch 2.0.1
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
```
```bash
# NumPy 1.23.5
pip install numpy==1.23.5
```
```bash
# mmcv 2.0.0
pip install mmcv==2.0.0 -f https://download.openmmlab.com/mmcv/dist/cu118/torch2.0/index.html
```
### 还有一个MMAction本身库的一个文件缺失，需要把`setup/drn.rar`
### 解压到`"你的环境\Lib\site-packages\mmaction\models\localizers"`下
![1.png](setup%2F1.png)
![2.png](setup%2F2.png)

### 修改`aimodel/report_gen/.env`的`QIANFAN_API_KEY`配置，使用自己的API
![3.png](setup%2F3.png)

### 然后导入数据库，修改`setup/shixun.sql`的账密配置并导入到本机数据库中
![4.png](setup%2F4.png)

### 启动后端服务
```bash
python app.py
```
---
## 前端部署
### 启动前端服务（确保安装了node.js）
```bash
cd vue
npm install
```
### 修改本机路由`vue/src/api/api.ts`
![5.png](setup%2F5.png)
### 打包
```bash
npm run build
```
### 启动前端服务
```bash
npm run preview
```


