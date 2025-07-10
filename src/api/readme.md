# API 文档

## 概述

这个文件包含了与后端服务交互的所有 API 请求方法，使用 axios 作为 HTTP 客户端。API 主要分为用户相关、记录相关、管理员相关、视频分析和报告相关等功能模块。

## 基础配置

使用时修改个人基础配置

```javascript
const api = axios.create({
  baseURL: 'http://192.168.223.250:5000', // 后端接口基础 URL
});
```

## 用户相关 API

### 验证码
- `getCaptcha()`: 获取验证码 ID 和验证码文本

### 注册与登录
- `registerUser()`: 用户注册
- `password_loginUser()`: 用户密码登录
- `captcha_loginUser()`: 用户验证码登录

### 个人信息管理
- `get_personalInfo()`: 获取个人信息
- `update_personalInfo()`: 修改个人信息
- `cancel_account()`: 注销账户
- `set_password()`: 修改密码
- `set_avatar()`: 上传设置头像
- `get_avatar()`: 获取头像

## 记录相关 API

### 记录管理
- `get_allRecord()`: 获取所有历史记录
- `add_record()`: 新增历史记录
- `get_record()`: 查看单个分析记录
- `set_record()`: 修改分析记录
- `delete_record()`: 删除分析记录
- `search_record()`: 筛选分析记录

## 管理员相关 API

### 管理员功能
- `adminLogin()`: 管理员登录

### 用户管理
- `get_allUser()`: 查看用户列表
- `get_user_info()`: 查看用户详细信息
- `delete_user()`: 删除用户
- `filter_user()`: 筛选用户

### 记录管理
- `AdminGetAllRecord()`: 查看所有分析记录列表
- `AdminDeleteRecord()`: 删除记录
- `filter_record()`: 筛选所有用户的分析记录

## 视频分析相关 API

### 视频处理
- `uploadVideo()`: 上传视频
- `get_video()`: 获取视频文件
- `get_json()`: 获取JSON文件

### 分析结果
- `generate_result()`: 生成分析结果
- `get_result()`: 查看视频分析结果

## 报告相关 API

- `create_report()`: 生成分析报告
- `view_report()`: 查看分析报告
- `delete_report()`: 删除分析报告

## 错误处理

所有 API 都包含 try-catch 块，捕获错误时会抛出带有描述性信息的 Error 对象。

## 使用示例

```javascript
import { getCaptcha, registerUser } from './api';

// 获取验证码
const captcha = await getCaptcha();

// 用户注册
const registerResult = await registerUser('username', 'password', 'captcha_id', 'smsCode');
```

## 注意事项

1. 部分 API 需要身份验证，请确保在调用前已登录
2. 文件上传 API 需要使用 FormData 格式
3. 所有 API 都返回 Promise，建议使用 async/await 或 .then() 处理响应