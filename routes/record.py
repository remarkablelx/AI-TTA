import json

from  flask import  Blueprint, request, jsonify
record = Blueprint('record',__name__)
from services.record import RecordService

@record.route('/all_record', methods=["POST"])
def all_record():
    data=json.loads(request.data)
    user_id=data.get("user_id")
    page_num = data.get("page_num")
    page_size = data.get("page_size")
    result = RecordService.all_record(user_id, page_num, page_size)
    return result

@record.route('/add_record', methods=["POST"])
def add_record():
    data = json.loads(request.data)
    video_id = data.get("video_id")
    user_id = data.get("user_id")
    result = RecordService.all_record(video_id, user_id)
    return result

@record.route('/select_record', methods=["POST"])
def select_record():
    return

@record.route('/select_record', methods=["POST"])
def select_record():
    return