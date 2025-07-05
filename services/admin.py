from models.admin import db, Admin
from models.user import User
from models.video import Video
from models.record import Record
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, desc, asc, func


class AdminService:
    @staticmethod
    def login(account:str, password:str):
        """管理员登录验证
        :param account: 管理员账号
        :param password: 管理员密码
        :return: 包含登录结果的字典
        """
        # 根据账号查询管理员信息
        admin = Admin.query.filter_by(account=account).first()

        if not admin:
            return {'code': '-1', 'message': '管理员账号不存在'}

        # 验证密码是否正确
        if not check_password_hash(admin.password, password):
            return {'code': '-1', 'message': '密码错误'}

        return {
            'code': '0',
            'message': '登录成功',
            'admin_info': admin.to_dict()
        }

    @staticmethod
    def all_user(page_num: int = 1, page_size: int = 10):
        """获取所有用户信息（分页），并统计每个用户的记录数量
        :param page_num: 当前页码
        :param page_size: 每页显示数量
        :return: 包含用户列表和分页信息的字典
        """
        try:
            # 分页查询用户数据
            pagination = User.query.paginate(page=page_num, per_page=page_size, error_out=False)
            users = pagination.items

            user_ids = [user.user_id for user in users]

            # 查询每个用户的记录数量
            record_counts = db.session.query(
                Record.user_id,
                db.func.count(Record.record_id).label('record_count')
            ).filter(
                Record.user_id.in_(user_ids)
            ).group_by(Record.user_id).all()

            # 将记录数量转换为字典
            count_dict = {user_id: count for user_id, count in record_counts}

            # 构建结果列表，为每个用户添加记录数量
            result = []
            for user in users:
                user_dict = user.to_dict()
                # 添加记录数量，如果没有记录则为0
                user_dict['record_count'] = count_dict.get(user.user_id, 0)
                result.append(user_dict)

            return {
                'code': '0',
                'message': '用户获取成功',
                'records': result,
                'pagination': {
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'current_page': page_num,
                    'per_page': page_size
                }
            }
        except Exception as e:
            return {'code': '-1', 'message': f'用户获取失败{str(e)}'}

    @staticmethod
    def get_user_info(user_id: int):
        """获取指定用户的详细信息
        :param user_id: 用户ID
        :return: 用户信息字典
        """
        try:
            user = User.query.get(user_id)
            return user.to_dict()

        except Exception as e:
            return {'code': '-1', 'message': f'用户信息获取失败{str(e)}'}

    @staticmethod
    def delete_user(user_id):
        """删除指定用户及其相关记录
        :param user_id: 要删除的用户ID
        :return: 操作结果字典
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {'code': -1, 'message': '用户不存在'}

            # 删除用户相关记录
            Record.query.filter_by(user_id=user_id).delete()

            # 删除用户
            db.session.delete(user)
            db.session.commit()

            return {'code': 0, 'message': '用户删除成功', 'user_id': user_id}
        except Exception as e:
            db.session.rollback()
            return {'code': -1, 'message': f'用户删除失败: {str(e)}'}

    @staticmethod
    def filter_users(search = None, sort_field = 'user_id', sort_order = 'asc',sex = None, page_num = 1, page_size = 10):
        """多条件筛选用户列表
        :param search: 搜索关键字
        :param sort_field: 排序字段
        :param sort_order: 排序方向
        :param sex: 性别筛选条件
        :param page_num: 当前页码
        :param page_size: 每页数量
        :return: 包含筛选结果的字典
        """
        try:
            # 获取用户基础信息和记录数量
            query = db.session.query(
                User.user_id,
                User.nickname,
                User.account,
                User.sex,
                User.register_time,
                func.count(Record.record_id).label('record_count')
            ).outerjoin(Record, User.user_id == Record.user_id)

            # 模糊查询搜索内容
            if search:
                search_pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        User.nickname.ilike(search_pattern),
                        User.account.ilike(search_pattern)
                    )
                )

            # 性别筛选
            if sex in [0, 1]:
                query = query.filter(User.sex == sex)

            # 按用户分组
            query = query.group_by(
                User.user_id,
                User.nickname,
                User.account,
                User.sex,
                User.register_time
            )

            # 应用排序
            if sort_field == 'record_count':
                sort_column = func.count(Record.record_id)
            elif sort_field == 'register_time':
                sort_column = User.register_time
            else:  # 默认按user_id排序
                sort_column = User.user_id

            if sort_order.lower() == 'desc':
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # 执行分页查询
            pagination = query.paginate(page=page_num, per_page=page_size, error_out=False)
            records = pagination.items

            # 转换结果格式
            result = []
            for record in records:
                result.append({
                    'user_id': record.user_id,
                    'account': record.account,
                    'nickname': record.nickname,
                    'sex': record.sex,
                    'register_time': record.register_time.isoformat() if record.register_time else None,
                    'record_count': record.record_count
                })

            return {
                'code': 0,
                'message': '用户获取成功',
                'records': result,
                'pagination': {
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'current_page': page_num,
                    'per_page': page_size
                }
            }
        except Exception as e:
            return {
                'code': -1,
                'message': f'用户获取失败: {str(e)}'
            }

    @staticmethod
    def all_record(page_num: int = 1, page_size: int = 10):
        """获取所有分析记录（分页）
        :param page_num: 当前页码
        :param page_size: 每页数量
        :return: 包含记录列表的字典
        """
        try:
            # 查询记录并关联视频表获取视频名称
            query = db.session.query(
                Record,
                Video.video_name
            ).outerjoin(
                Video, Record.video_id == Video.video_id
            )

            pagination = query.paginate(page=page_num, per_page=page_size, error_out=False)
            records = pagination.items

            result = []
            for record, video_name in records:
                record_data = record.to_dict()
                record_data['video_name'] = video_name
                result.append(record_data)

            return {
                'code': '0',
                'message': '分析记录获取成功',
                'records': result,
                'pagination': {
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'current_page': page_num,
                    'per_page': page_size
                }
            }
        except Exception as e:
            return {'code': '-1', 'message': f'获取分析记录失败{str(e)}'}

    @staticmethod
    def delete_record(record_id):
        """删除指定分析记录
        :param record_id: 要删除的记录ID
        :return: 操作结果字典
        """
        try:
            record = Record.query.get(record_id)
            if not record_id:
                return {'code': -1, 'message': '用户不存在'}

            # 删除用户
            db.session.delete(record)
            db.session.commit()

            return {'code': 0, 'message': '分析记录删除成功', "record_id": record_id}
        except Exception as e:
            db.session.rollback()
            return {'code': -1, 'message': f'分析记录删除失败: {str(e)}'}

    @staticmethod
    def filter_record(search = None, order = 'asc',state = None, page_num = 1, page_size = 10):
        """多条件筛选分析记录
        :param search: 搜索关键字
        :param order: 排序方向
        :param state: 记录状态筛选
        :param page_num: 当前页码
        :param page_size: 每页数量
        :return: 包含筛选结果的字典
        """
        try:
            # 查询记录并关联视频表获取视频名称
            query = db.session.query(
                Record,
                Video.video_name
            ).outerjoin(
                Video, Record.video_id == Video.video_id
            )

            # 状态筛选
            if state is not None:
                query = query.filter(Record.state == state)

            # 关键字搜索
            if search:
                query = query.filter(
                    or_(
                        Record.time.ilike(f'%{search}%'),
                        Video.video_name.ilike(f'%{search}%')
                    )
                )

            # 应用排序
            if order.lower() == 'desc':
                query = query.order_by(desc('time'))
            else:
                query = query.order_by(asc('time'))

            # 分页
            pagination = query.paginate(page=page_num, per_page=page_size, error_out=False)
            records = pagination.items

            result = []
            for record, video_name in records:
                record_data = record.to_dict()
                record_data['video_name'] = video_name
                result.append(record_data)

            return {
                'code': '0',
                'message': '记录筛选成功',
                'records': result,
                'pagination': {
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'current_page': page_num,
                    'per_page': page_size
                }
            }
        except Exception as e:
            db.session.rollback()
            return {'code': '-1', 'message': f'记录筛选失败: {str(e)}'}


