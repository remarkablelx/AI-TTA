import json

from  flask import  Blueprint, request, jsonify
admin = Blueprint('admin',__name__)
from services.admin import AdminService

@admin.route('/login', methods=["POST"])
def login():
    """管理员登录"""
    # 获取JSON数据：管理员账号，管理员密码
    data = json.loads(request.data)
    account = data.get('account')
    password = data.get('password')
    result = AdminService.login(account, password)
    return jsonify(result)

@admin.route('/all_user', methods=["POST"])
def all_user():
    """获取所有用户列表(分页)"""
    # 获取JSON数据：分页号，分页大小
    data = json.loads(request.data)
    page_num = data.get('page_num', 1)
    page_size = data.get('page_size', 10)
    result = AdminService.all_user(page_num, page_size)
    return jsonify(result)

@admin.route('/get_user_info', methods=["POST"])
def get_user_info():
    """获取用户详细信息"""
    #获取请求JSON数据：用户id
    data = json.loads(request.data)
    user_id = data.get('user_id')
    result = AdminService.get_user_info(user_id)
    return jsonify(result)

@admin.route('/delete_user', methods=["POST"])
def delete_user():
    """删除用户"""
    # 获取请求JSON数据：用户id
    data = json.loads(request.data)
    user_id = data.get('user_id')
    result = AdminService.delete_user(user_id)
    return jsonify(result)


@admin.route('/filter_user', methods=["POST"])
def filter_user():
    """根据条件筛选用户"""
    # 获取请求JSON数据：搜索内容，排序字段，排序方式，性别，分页号，分页大小
    data = json.loads(request.data)
    search = data.get('search', None)
    sort_field = data.get('sort', 'user_id')
    sort_order = data.get('order', 'asc')
    sex = data.get('sex', None)
    page_num = data.get('page_num', 1)
    page_size = data.get('page_size', 10)
    result = AdminService.filter_users(search, sort_field, sort_order, sex, page_num, page_size)
    return jsonify(result)


@admin.route('/all_record', methods=["POST"])
def all_record():
    """获取所有分析记录"""
    # 获取JSON数据：分页号，分页大小
    data = json.loads(request.data)
    page_num = data.get('page_num')
    page_size = data.get('page_size')
    result = AdminService.all_record(page_num, page_size)
    return jsonify(result)

@admin.route('/delete_record', methods=["POST"])
def delete_record():
    """"删除分析记录"""
    # 获取JSON数据：分析记录编号
    data = json.loads(request.data)
    record_id = data.get('record_id')
    result = AdminService.delete_record(record_id)
    return jsonify(result)

@admin.route('/filter_record', methods=["POST"])
def filter_record():
    """根据条件筛选用户"""
    # 获取请求JSON数据：搜索内容，排序方式，分析记录状态，分页号，分页大小
    data = json.loads(request.data)
    search = data.get('search', None)
    order = data.get('order', 'asc')
    state = data.get('state', None)
    page_num = data.get('page_num', 1)
    page_size = data.get('page_size', 10)

    result = AdminService.filter_record(search, order, state, page_num, page_size)

    return jsonify(result)
