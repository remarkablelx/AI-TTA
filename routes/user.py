import json
import os

from  flask import  Blueprint, request, jsonify, send_file

user = Blueprint('user',__name__)
from services.user import UserService

@user.route('/captcha', methods=["POST"])
def captcha():
    """生成验证码"""
    result = UserService.create_captcha()
    return jsonify(result)

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
    return jsonify(result)

@user.route('/password_login', methods=["POST"])
def password_login():
    """用户使用密码登录"""
    # 获取请求JSON数据：用户账号，用户密码
    data = json.loads(request.data)
    account = data.get('account')
    password = data.get('password')
    result = UserService.password_login(account, password)
    return jsonify(result)

@user.route('/captcha_login', methods=["POST"])
def captcha_login():
    """用户使用密码登录"""
    # 获取请求JSON数据：用户账号，验证码编号，验证码内容
    data = json.loads(request.data)
    account = data.get('account')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')
    result = UserService.captcha_login(account, captcha_id, captcha_text)
    return jsonify(result)


@user.route('/cancel_account', methods=["POST"])
def cancel_account():
    """注销账号"""
    # 获取请求JSON数据：用户编号，验证码编号，验证码内容
    data = json.loads(request.data)
    user_id = data.get('user_id')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')
    result = UserService.cancel_account(user_id, captcha_id, captcha_text)
    return jsonify(result)

@user.route('/set_password', methods=["POST"])
def set_password():
    """重新设置密码"""
    # 获取请求JSON数据：用户账号，新密码，验证码编号，验证码内容
    data = json.loads(request.data)
    user_id = data.get('user_id')
    new_password = data.get('new_password')
    captcha_id = data.get('captcha_id')
    captcha_text = data.get('captcha_text')
    result = UserService.set_password(user_id, new_password, captcha_id, captcha_text)
    return jsonify(result)

@user.route('/set_personal_info', methods=["POST"])
def set_personal_info():
    """更新个人信息"""
    # 定义可修改的字段
    info={'nickname', 'sex', 'email', 'note', 'height', 'weight', 'location', 'birth'}
    # 获取请求JSON数据：用户编号，更新字典
    data = json.loads(request.data)
    user_id=data.get('user_id')
    # 根据更新字典提取要修改的个人信息
    update_data={}
    for field in info:
        if field in data:
            update_data[field]=data[field]

    result = UserService.update_personal_info(user_id, update_data)
    return jsonify(result)

@user.route('/get_personal_info', methods=["POST"])
def get_personal_info():
    """获取个人详细信息"""
    # 获取请求JSON数据：用户编号
    data = json.loads(request.data)
    user_id = data.get('user_id')
    result = UserService.get_user_info(user_id)
    return jsonify(result)

@user.route('/set_avatar', methods=["POST"])
def set_avatar():
    """设置用户头像"""
    if 'avatar_file' not in request.files:
        return {'code': '-1', 'message': '未上传文件'}
    file = request.files['avatar_file']

    user_id = request.form.get('user_id')

    filename = file.filename
    avatar_name = os.path.splitext(file.filename)[0]
    file_ext = os.path.splitext(filename)[1].lower()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    avatar_dir = os.path.join(project_root, 'avatar', f"{avatar_name}{file_ext}")
    result = UserService.set_avatar(file, user_id, avatar_dir)
    return jsonify(result)


@user.route('/get_avatar', methods=["POST"])
def get_avatar():
    """获取用户头像"""
    data = json.loads(request.data)
    avatar = data.get('avatar')

    return send_file(
        avatar,
        conditional=True,
        etag=True
    )


