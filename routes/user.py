import json

from  flask import  Blueprint, request, jsonify
user = Blueprint('user',__name__)
from services.user import UserService

@user.route('/captcha', methods=["POST"])
def captcha():
    """生成验证码"""
    result = UserService.create_captcha()
    return result

@user.route('/register', methods=["POST"])
def register():
    """用户注册"""
    # 获取请求JSON数据：用户账号，用户密码，验证码编号，验证码内容
    data = json.loads(request.data)
    account = data.get('account')
    password = data.get('password')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')
    result = UserService.register(account, password, captcha_id, captcha_text)
    return result

@user.route('/password_login', methods=["POST"])
def password_login():
    """用户使用密码登录"""
    # 获取请求JSON数据：用户账号，用户密码
    data = json.loads(request.data)
    account = data.get('account')
    password = data.get('password')
    result = UserService.password_login(account, password)
    return result

@user.route('/captcha_login', methods=["POST"])
def captcha_login():
    """用户使用密码登录"""
    # 获取请求JSON数据：用户账号，验证码编号，验证码内容
    data = json.loads(request.data)
    account = data.get('account')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')
    result = UserService.captcha_login(account, captcha_id, captcha_text)
    return result


@user.route('/cancel_account', methods=["POST"])
def cancel_account():
    """注销账号"""
    # 获取请求JSON数据：用户编号，验证码编号，验证码内容
    data = json.loads(request.data)
    user_id = data.get('user_id')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')
    result = UserService.cancel_account(user_id, captcha_id, captcha_text)
    return result

@user.route('/set_password', methods=["POST"])
def set_password():
    """重新设置密码"""
    # 获取请求JSON数据：用户账号，新密码，验证码编号，验证码内容
    data = json.loads(request.data)
    account = data.get('account')
    new_password = data.get('new_password')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')
    result = UserService.set_password(account, new_password, captcha_id, captcha_text)
    return result

@user.route('/set_personal_info', methods=["POST"])
def set_personal_info():
    """更新个人信息"""
    # 定义可修改的字段
    info={'nickname', 'avatar', 'sex', 'email', 'note', 'height', 'weight', 'location', 'birth'}
    # 获取请求JSON数据：用户令牌，更新字典
    data = json.loads(request.data)
    token=data.get('token')
    # 根据更新字典提取要修改的个人信息
    update_data={}
    for field in info:
        if field in data:
            update_data[field]=data[field]

    result = UserService.update_personal_info(token, update_data)
    return result

@user.route('/get_personal_info', methods=["POST"])
def get_personal_info():
    """获取个人详细信息"""
    # 获取请求JSON数据：用户令牌
    data = json.loads(request.data)
    token = data.get('token')
    result = UserService.get_user_info(token)
    return result




