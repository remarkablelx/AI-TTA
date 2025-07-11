import json
import os

from  flask import  Blueprint, request, jsonify, send_file, abort
result = Blueprint('result',__name__)
from services.result import ResultService

@result.route('/generate_result',methods=["POST"])
def generate_result():
    """生成分析结果"""
    # 获取请求JSON数据：分析记录编号
    data = json.loads(request.data)
    record_id = data.get('record_id')
    res = ResultService.generate_result(record_id)
    return jsonify(res)

@result.route('/get_result',methods=["POST"])
def get_result():
    """获取分析结果"""
    # 获取请求JSON数据：分析结果编号
    data = json.loads(request.data)
    result_id = data.get('result_id')
    res = ResultService.get_result(result_id)
    return jsonify(res)

@result.route('/set_result',methods=["POST"])
def set_result():
    """更新分析结果"""
    #定义可修改的字段
    info = {
        'ball_json_path',
        'pose_json_path',
        'ball_video_path',
        'pose_video_path',
        'segment_json_path',
        'annotated_video_path',
        'recognition_json_path'
    }
    # 获取请求JSON数据：分析结果编号，更新字典
    data = json.loads(request.data)
    result_id = data.get('result_id')
    # 根据更新字典提取要修改的信息
    update_data = {}
    for field in info:
        if field in data:
            update_data[field] = data[field]

    res = ResultService.set_result(result_id, update_data)
    return jsonify(res)


@result.route('/get_video',methods=["POST"])
def get_video():
    """根据视频路径上传视频"""
    data = json.loads(request.data)
    video_path = data.get('video_path')

    if not video_path or not os.path.exists(video_path):
        return {'code':'-1', 'message': '视频路径不存在'}

    ext = os.path.splitext(video_path)[1].lower()
    mime_types = {
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime',
        '.avi': 'video/x-msvideo',
        '.mkv': 'video/x-matroska',
        '.webm': 'video/webm'
    }
    mime_type = mime_types.get(ext, 'application/octet-stream')

    return send_file(
        video_path,
        mimetype=mime_type,
        conditional=True,
        etag=True
    )

@result.route('/get_json',methods=["POST"])
def get_json():
    """根据视频路径上传视频"""
    data = json.loads(request.data)
    json_path = data.get('json_path')

    if not json_path or not os.path.exists(json_path):
        return {'code':'-1', 'message': '文件路径不存在'}

    with open(json_path, 'r', encoding='utf-8') as file:
        json_text = json.load(file)

    return {'code':'0', 'message': '文件获取成功', 'json': json_text}
