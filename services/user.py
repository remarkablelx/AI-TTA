from models.user import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import time
import string
import jwt
import os

# 验证码存储
captcha_storage = {}
CAPTCHA_EXPIRATION = 300  # 验证码有效期5分钟

# 获取JWT密钥
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
JWT_ALGORITHM = 'HS256'

class UserService:
    @staticmethod
    def generate_captcha(length=4):
        """生成验证码文本
        :param length: 验证码长度
        :return: 验证码文本
        """
        # 生成随机字符:数字+大写字母
        characters = string.digits + string.ascii_uppercase
        captcha_text = ''.join(random.choices(characters, k=length))

        return captcha_text

    @staticmethod
    def create_captcha():
        """创建验证码并存储
        :return: 包含验证码ID和文本的字典
        """
        captcha_id = f"captcha_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        captcha_text = UserService.generate_captcha()
        # 存储验证码
        captcha_storage[captcha_id] = {
            'text': captcha_text,
            'expire_at': datetime.now() + timedelta(seconds=CAPTCHA_EXPIRATION)
        }
        return  {'code':'0', 'captcha_id': captcha_id, 'captcha_text': captcha_text}

    @staticmethod
    def verify_captcha(captcha_id, user_input):
        """验证用户输入的验证码
        :param captcha_id: 验证码ID
        :param user_input: 用户输入的验证码
        :return: 验证是否通过
        """
        if not captcha_id or not user_input:
            return False
        captcha_data = captcha_storage.get(captcha_id)
        if not captcha_data:
            return False
        # 检查是否过期
        if datetime.now() > captcha_data['expire_at']:
            # 清理过期验证码
            del captcha_storage[captcha_id]
            return False
        # 验证用户输入
        is_valid = user_input.upper() == captcha_data['text'].upper()
        # 无论是否匹配都删除已使用的验证码
        del captcha_storage[captcha_id]
        return is_valid

    @staticmethod
    def register(account: str, password: str, captcha_id: str, captcha_input: str) -> dict:
        """
        用户注册（需要图形验证码）
        :param account: 手机号/账号
        :param password: 密码
        :param captcha_id: 验证码ID
        :param captcha_input: 用户输入的验证码
        :return: 操作结果
        """
        # 验证图形验证码
        if not UserService.verify_captcha(captcha_id, captcha_input):
            return {'code': '-1', 'message': '图形验证码错误或已过期'}

        # 检查账号是否已存在
        if User.query.filter_by(account=account).first():
            return {'code': '-1', 'message': '账号已存在'}

        try:
            # 创建新用户
            new_user = User(
                account=account,
                password=generate_password_hash(password),
                register_time=datetime.now(),
            )

            db.session.add(new_user)
            db.session.commit()

            return {
                'code': '0',
                'message': '注册成功',
                'user_id': new_user.user_id,
                'register_time': new_user.register_time
            }
        except Exception as e:
            db.session.rollback()
            return {'code': '-1', 'message': f'注册失败: {str(e)}'}

    @staticmethod
    def password_login(account: str, password: str) -> dict:
        """密码登录
        :param account: 账号
        :param password: 密码
        :return: 登录结果字典
        """
        user = User.query.filter_by(account=account).first()

        if not user:
            return {'code': '-1', 'message': '账号不存在'}

        if not check_password_hash(user.password, password):
            return {'code': '-1', 'message': '密码错误'}

        token = UserService.generate_jwt(user.user_id)

        return {
            'code': '0',
            'message': '登录成功',
            'user_id': user.user_id,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'token': token
        }

    @staticmethod
    def captcha_login(account: str, captcha_id: str, captcha_text: str) -> dict:
        """验证码登录
        :param account: 账号
        :param captcha_id: 验证码ID
        :param captcha_text: 验证码文本
        :return: 登录结果字典
        """
        # 验证验证码
        if not UserService.verify_captcha(captcha_id, captcha_text):
            return {'code': '-1', 'message': '短信验证码错误或已过期'}

        user = User.query.filter_by(account=account).first()
        if not user:
            return {'code': '-1', 'message': '账号不存在'}

        token = UserService.generate_jwt(user.user_id)

        return {
            'code': '0',
            'message': '登录成功',
            'user_id': user.user_id,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'token': token
        }

    @staticmethod
    def cancel_account(token: str, captcha_id: str, captcha_input: str) -> dict:
        """
        注销账号
        :param token: 用户令牌
        :param captcha_id: 验证码ID
        :param captcha_input: 用户输入的验证码
        :return: 操作结果
        """
        user_info = UserService.get_user_info(token)
        # 验证图形验证码
        if not UserService.verify_captcha(captcha_id, captcha_input):
            return {'code': '-1', 'message': '验证码错误或已过期'}

        user_id = user_info['user_id']

        user = User.query.get(user_id)
        if not user:
            return {'code': '-1', 'message': '用户不存在'}

        try:
            account = user.account
            db.session.delete(user)
            db.session.commit()

            return {'code': '0', 'message': '账号注销成功'}
        except Exception as e:
            db.session.rollback()
            return {'code': '-1', 'message': f'账号注销失败: {str(e)}'}

    @staticmethod
    def set_password(token: str, new_password: str, captcha_id: str, captcha_input: str) -> dict:
        """
        修改密码
        :param token: 用户令牌
        :param new_password: 新密码
        :param captcha_id: 图形验证码ID
        :param captcha_input: 用户输入的图形验证码
        :return: 操作结果
        """
        user_info = UserService.get_user_info(token)
        # 验证验证码
        if not UserService.verify_captcha(captcha_id, captcha_input):
            return {'code': '-1', 'message': '图形验证码错误或已过期'}

        user_id = user_info['user_id']

        user = User.query.get(user_id)

        if not user:
            return {'code': '-1', 'message': '用户不存在'}

        try:
            user.password = generate_password_hash(new_password)
            db.session.commit()

            return {'code': '0', 'message': '密码修改成功'}
        except Exception as e:
            db.session.rollback()
            return {'code': '-1', 'message': f'密码修改失败: {str(e)}'}

    @staticmethod
    def update_personal_info(token, update_data):
        """更新用户个人信息
        :param token: 用户令牌
        :param update_data: 更新数据字典
        :return: 操作结果字典
        """
        try:
            user_info = UserService.get_user_info(token)
            user_id = user_info['user_id']
            user = User.query.get(user_id)
            if not user:
                return {'code': '-1', 'message': '用户不存在'}

            # 遍历更新字段
            for field, value in update_data.items():
                setattr(user, field, value)

            # 保存到数据库
            db.session.commit()

            return {
                'code': '1',
                'message': '个人信息更新成功',
                'updated_fields': { f"{field}": value for field, value in update_data.items() }
            }

        except Exception as e:
            db.session.rollback()
            return {
                'code': '-1',
                'message': f'更新个人信息失败: {str(e)}'
            }



    @staticmethod
    def generate_jwt(user_id: int) -> str:
        """生成JWT令牌
        :param user_id:用户编号
        :return jwt令牌
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.now() + timedelta(days=30)
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


    @staticmethod
    def verify_jwt(token: str) -> dict:
        """验证JWT令牌并
        :param token:用户令牌
        :return payload
        """
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return {'code':'-1','message': 'Token已过期'}
        except jwt.InvalidTokenError:
            return {'code':'-1','message': 'Token不合法'}


    @staticmethod
    def get_user_info(token: str) -> dict:
        """验证JWT令牌并
        :param token:用户令牌
        :return 用户信息
        """
        payload = UserService.verify_jwt(token)
        if 'code' in payload and payload.get('code') == -1:
            return payload

        user_id = payload['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'code':'-1','message': '用户不存在'}

        return user.to_dict()