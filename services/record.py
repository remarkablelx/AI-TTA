from models.record import db, Record
from models.video import Video
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import or_

class RecordService:
    @staticmethod
    def all_record(user_id:int, page_num:int = 1, page_size:int = 10):
        """获取指定用户的所有分析记录（分页）
        :param user_id: 用户ID
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
            ).filter(
                Record.user_id == user_id
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
                'message': '记录获取成功',
                'records': result,
                'total_records': pagination.total,
                'total_pages': pagination.pages,
                'current_page': page_num
            }
        except Exception as e:
            return {'code': '-1', 'message': f'获取分析记录失败{str(e)}'}

    @staticmethod
    def add_record(video_id:int, user_id:int):
        """创建新的分析记录
        :param video_id: 视频ID
        :param user_id: 用户ID
        :return: 操作结果字典
        """
        try:
            # 创建新记录对象
            new_record = Record(
                video_id = video_id,
                user_id = user_id,
                state = 0, #初始为0，未处理
                time = datetime.now(),
                expiration_time = datetime.now()+timedelta(days=30) # 默认30天后过期
            )
            db.session.add(new_record)
            db.session.commit()
            return  {'code':'0','message':'记录添加成功','record':new_record.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'code': '-1', 'message': f'记录添加失败: {str(e)}'}

    @staticmethod
    def get_record(record_id):
        """根据记录ID获取分析记录详情
        :param record_id: 记录ID
        :return: 包含记录详情的字典
        """
        try:
            record = db.session.execute(
                db.select(Record).filter_by(record_id=record_id)
            ).scalar_one()

            video_name = None
            if record.video_id:
                try:
                    video = db.session.execute(
                        db.select(Video).filter_by(video_id=record.video_id)
                    ).scalar_one()
                    video_name = video.video_name
                except NoResultFound:
                    video_name = None

            record_data = record.to_dict()
            record_data['video_name'] = video_name
            return {'code': '0','message': '记录获取成功','record':record_data}
        except Exception as e:
            return {'code': '-1', 'message': f'记录获取失败: {str(e)}'}

    @staticmethod
    def set_record(record_id, data):
        """更新记录信息
        :param record_id: 记录ID
        :param data: 更新数据字典
        :return: 操作结果字典
        """
        try:
            # 获取记录
            record = Record.query.get(record_id)
            # 更新记录字段
            if 'state' in data:
                record.state = data['state']
            if 'expiration_time' in data:
                record.expiration_time = data['expiration_time']

            # 更新关联视频名称
            if 'video_name' in data and record.video_id:
                try:
                    video = Video.query.get(record.video_id)
                    video.video_name = data['video_name']
                except Exception as e:
                    return {'code': '-1', 'message': f'视频不存在: {str(e)}'}

            db.session.commit()
            return {'code': '0', 'message': '记录更新成功', 'record': record.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'code': '-1', 'message': f'记录更新失败: {str(e)}'}

    @staticmethod
    def delete_record(record_id):
        """删除分析记录
        :param record_id: 记录ID
        :return: 操作结果字典
        """
        try:
            # 获取记录
            record = Record.query.get(record_id)

            db.session.delete(record)
            db.session.commit()
            return {'code': '0', 'message': '记录删除成功', 'record_id': record_id}
        except Exception as e:
            db.session.rollback()
            return {'code': '-1', 'message': f'记录删除失败: {str(e)}'}

    @staticmethod
    def search_record(user_id, search='', state=None, sort='time_desc', page_num=1, page_size=10):
        """多条件筛选分析记录
        :param user_id: 用户ID
        :param search: 搜索关键字
        :param state: 记录状态筛选
        :param sort: 排序方式
        :param page_num: 当前页码
        :param page_size: 每页数量
        :return: 包含筛选结果的字典
        """
        try:
            query = db.session.query(
                Record,
                Video.video_name
            ).outerjoin(
                Video, Record.video_id == Video.video_id
            ).filter(
                Record.user_id == user_id
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

            # 排序处理
            sort_mapping = {
                'time_asc': Record.time.asc(),
                'time_desc': Record.time.desc()
            }
            query = query.order_by(sort_mapping.get(sort, Record.time.desc()))

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
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page_num
            }
        except Exception as e:
            db.session.rollback()
            return {'code': '-1', 'message': f'记录筛选失败: {str(e)}'}