import json

from  flask import  Blueprint, request, jsonify
record = Blueprint('record',__name__)
from services.record import RecordService

@record.route('/all_record', methods=["POST"])
def all_record():
    """获取用户所有记录（分页）"""
    # 获取JSON数据：用户编号，分页号，分页大小
    data=json.loads(request.data)
    user_id=data.get("user_id")
    page_num = data.get("page_num")
    page_size = data.get("page_size")
    result = RecordService.all_record(user_id, page_num, page_size)
    return jsonify(result)

@record.route('/add_record', methods=["POST"])
def add_record():
    """添加新记录"""
    # 获取JSON数据：视频编号，用户编号
    data = json.loads(request.data)
    video_id = data.get("video_id")
    user_id = data.get("user_id")
    result = RecordService.add_record(video_id, user_id)
    return jsonify(result)

@record.route('/get_record', methods=["POST"])
def get_record():
    """根据记录ID获取记录"""
    # 获取JSON数据：分析记录编号
    data = json.loads(request.data)
    record_id = data.get("record_id")
    result = RecordService.get_record(record_id)
    return jsonify(result)

@record.route('/set_record', methods=["POST"])
def set_record():
    """更新记录信息"""
    # 获取JSON数据：分析记录编号，更新字典
    data = json.loads(request.data)
    record_id = data.get("record_id")
    # 提取更新字典中的更新数据
    update_data = {k: v for k, v in data.items() if k != 'record_id'}
    result = RecordService.set_record(record_id, update_data)
    return jsonify(result)

@record.route('/delete_record', methods=["POST"])
def delete_record():
    """删除记录"""
    # 获取JSON数据：分析记录编号
    data = json.loads(request.data)
    record_id = data.get("record_id")
    result = RecordService.delete_record(record_id)
    return jsonify(result)

@record.route('/search_record', methods=["POST"])
def search_record():
    """筛选记录"""
    # 获取请求JSON数据：用户编号，搜索内容，排序方式，分析记录状态，分页号，分页大小
    data = json.loads(request.data)
    user_id = data.get("user_id")
    search = data.get("search")
    state = data.get("state")
    sort = data.get("sort")
    page_num = data.get("page_num")
    page_size = data.get("page_size")

    result = RecordService.search_record(
        user_id=user_id,
        search=search,
        state=state,
        sort=sort,
        page_num=page_num,
        page_size=page_size
    )
    return jsonify(result)