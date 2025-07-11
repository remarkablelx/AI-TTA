import json
import os

from  flask import  Blueprint, request, jsonify
video = Blueprint('video',__name__)
from services.video import VideoService
from werkzeug.utils import secure_filename

@video.route('/upload_video', methods=["POST"])
def upload_video():
    """上传视频"""
    # 检查请求中是否包含文件
    if 'video_file' not in request.files:
        return {'code': '-1', 'message': '未上传文件'}
    file = request.files['video_file']
    filename = file.filename
    file_ext = os.path.splitext(filename)[1].lower()

    video_name = request.form.get('video_name', '未命名视频')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    video_dir = os.path.join(project_root, 'aimodel', 'video',f"{video_name}")

    # 调用服务层
    result = VideoService.upload_video(file, video_dir, video_name)
    return jsonify(result)

@video.route('/get_video_info', methods=["POST"])
def get_video_info():
    """获取视频信息"""
    # 获取请求JSON数据：视频编号
    data=json.loads(request.data)
    video_id = data.get("video_id")
    result = VideoService.get_video_info(video_id)
    return jsonify(result)

@video.route('/set_name', methods=["POST"])
def set_name():
    """设置视频名称"""
    # 获取请求JSON数据：视频编号，新名称
    data=json.loads(request.data)
    video_id = data.get("video_id")
    new_name = data.get("new_name")
    result = VideoService.set_name(video_id, new_name)
    return jsonify(result)

@video.route('/set_path', methods=["POST"])
def set_path():
    """设置视频路径"""
    # 获取请求JSON数据：视频编号，新路径
    data=json.loads(request.data)
    video_id = data.get("video_id")
    new_path = data.get("new_path")
    result = VideoService.set_path(video_id, new_path)
    return jsonify(result)

