import json

from  flask import  Blueprint, request, jsonify
result = Blueprint('result',__name__)
from services.result import ResultService

@result.route('/generate_result',methods=["POST"])
def generate_result():
    """生成分析结果"""
    # 获取请求JSON数据：视频编号
    data = json.loads(request.data)
    video_id = data.get('video_id')
    res = ResultService.generate_result(video_id)
    return res

@result.route('/get_result',methods=["POST"])
def get_result():
    """获取分析结果"""
    # 获取请求JSON数据：分析结果编号
    data = json.loads(request.data)
    result_id = data.get('result_id')
    res = ResultService.get_result(result_id)
    return res

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
    return res