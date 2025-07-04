import json

from  flask import  Blueprint, request, jsonify
video = Blueprint('video',__name__)
from services.video import VideoService

@video.route('/upload_video', methods=["POST"])
def upload_video():
    #获取前端传入的json数据
    data=json.loads(request.data)
    #提取字段
    video_path = data.get("video_path")
    video_name = data.get("video_name")
    result = VideoService.upload_video(video_path, video_path)

    return result

