import json

from  flask import  Blueprint, request, jsonify
user = Blueprint('user',__name__)
from services.user import UserService

@user.route('/captcha', methods=["POST"])
def captcha():
    result = UserService.create_captcha()
    return result

@user.route('/register', methods=["POST"])
def register():
    # 获取前端传入的 JSON 数据
    data = json.loads(request.data)
    #提取各个字段
    account = data.get('account')
    password = data.get('password')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')

    result = UserService.register(account, password, captcha_id, captcha_text)
    return result

@user.route('/password_login', methods=["POST"])
def password_login():
    # 获取前端传入的 JSON 数据
    data = json.loads(request.data)
    # 提取各个字段
    account = data.get('account')
    password = data.get('password')

    result = UserService.password_login(account, password)
    return jsonify(result)

@user.route('/captcha_login', methods=["POST"])
def captcha_login():
    # 获取前端传入的 JSON 数据
    data = json.loads(request.data)
    # 提取各个字段
    account = data.get('account')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')

    result = UserService.captcha_login(account, captcha_id, captcha_text)
    return result


@user.route('/cancel', methods=["POST"])
def cancel():
    # 获取前端传入的 JSON 数据
    data = json.loads(request.data)
    # 提取各个字段
    user_id = data.get('user_id')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')

    result = UserService.cancel_account(user_id, captcha_id, captcha_text)
    return result

@user.route('/update_password', methods=["POST"])
def update_password():
    # 获取前端传入的 JSON 数据
    data = json.loads(request.data)
    # 提取各个字段
    account = data.get('account')
    new_password = data.get('new_password')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')

    result = UserService.update_password(account, new_password, captcha_id, captcha_text)
    return result

@user.route('/set_personal_info', methods=["POST"])
def set_personal_info():
    info={'nickname', 'avatar', 'sex', 'email', 'note'}
    # 获取前端传入的 JSON 数据
    data = json.loads(request.data)
    # 提取用户id
    user_id=data.get('user_id')
    # 提取要修改的个人信息
    update_data={}
    for field in info:
        if field in data:
            update_data[field]=data[field]

    result = UserService.update_personal_info(user_id, update_data)
    return result





