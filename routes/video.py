import json

from  flask import  Blueprint, request, jsonify
video = Blueprint('video',__name__)
from services.video import VideoService

@video.route('/upload_video', methods=["POST"])
def upload_video():
    """上传视频"""
    # 获取请求JSON数据：视频路径，视频名称
    data=json.loads(request.data)
    video_path = data.get("video_path")
    video_name = data.get("video_name")
    result = VideoService.upload_video(video_path, video_name)
    return result

@video.route('/get_video_info', methods=["POST"])
def get_video_info():
    """获取视频信息"""
    # 获取请求JSON数据：视频编号
    data=json.loads(request.data)
    video_id = data.get("video_id")
    result = VideoService.get_video_info(video_id)
    return result

@video.route('/set_name', methods=["POST"])
def set_name():
    """设置视频名称"""
    # 获取请求JSON数据：视频编号，新名称
    data=json.loads(request.data)
    video_id = data.get("video_id")
    new_name = data.get("new_name")
    result = VideoService.set_name(video_id, new_name)
    return result

@video.route('/set_path', methods=["POST"])
def set_path():
    """设置视频路径"""
    # 获取请求JSON数据：视频编号，新路径
    data=json.loads(request.data)
    video_id = data.get("video_id")
    new_path = data.get("new_path")
    result = VideoService.set_path(video_id, new_path)
    return result

