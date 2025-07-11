from models.video import db, Video
from datetime import timedelta
import os
import cv2

class VideoService:
    @staticmethod
    def upload_video(file_stream, video_path, video_name):
        """上传视频文件并保存到数据库
        :param file_stream: 文件流
        :param video_path: 视频文件存储路径
        :param video_name: 视频名称
        :return: 包含操作结果和视频信息的字典
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(video_path), exist_ok=True)

            # 保存文件到本地
            file_stream.save(video_path)

            # 获取视频元数据
            video_info = VideoService.get_info(video_path)

            # 创建新视频记录
            new_video = Video(
                video_name=video_name,
                video_path=video_path,
                video_size=os.path.getsize(video_path),
                video_format=video_info.get('format'),
                video_duration=video_info.get('duration'),
                video_resolution=video_info.get('resolution'),
                video_frame_rate=video_info.get('frame_rate')
            )

            db.session.add(new_video)
            db.session.commit()

            return {
                'code': '0',
                'message': '视频上传成功',
                'video_info': new_video.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'code': '-1',
                'message': f'视频上传失败: {str(e)}'
            }

    @staticmethod
    def get_info(video_path):
        """
        获取视频基本信息
        :param video_path: 视频文件路径
        :return: 包含视频信息的字典
        """
        if not os.path.exists(video_path):
            return {
                'code':'-1',
                'message': "视频文件不存在"
            }

        try:
            # 使用 OpenCV 获取视频基础信息
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                return {
                    'code':'-1',
                    'message': "无法打开视频文件"
                }

            # 获取基本信息
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # 计算时长
            duration_seconds = int(frame_count / fps) if fps > 0 else 0
            duration = str(timedelta(seconds=duration_seconds))

            cap.release()

            # 获取文件大小，转换为MB
            file_size = os.path.getsize(video_path)
            file_size_mb = round(file_size / (1024 * 1024), 2)

            # 获取视频格式
            _, file_extension = os.path.splitext(video_path)
            video_format = file_extension[1:].upper()

            return {
                'code': '0',
                'format': video_format,
                'duration': duration,
                'resolution': f"{width}x{height}",
                'frame_rate': round(fps, 2),
                'video_size': f"{file_size_mb}MB"
            }
        except Exception as e:
            return {
                'code': '-1',
                'message': f'视频信息获取失败: {str(e)}'
            }


    @staticmethod
    def get_video_info(video_id):
        """根据视频ID获取视频信息
        :param video_id: 视频ID
        :return: 包含视频信息的字典
        """
        try:
            # 从数据库获取视频
            video = Video.query.get(video_id)
            if not video:
                return {
                    'code': '-1',
                    'message': '视频不存在'
                }

            return {
                'code': '0',
                'message': '视频信息获取成功',
                'video_info': video.to_dict()
            }
        except Exception as e:
            return {
                'code': '-1',
                'message': f'获取视频信息失败: {str(e)}'
            }

    @staticmethod
    def set_name(video_id, new_name):
        """更新视频名称
        :param video_id: 视频ID
        :param new_name: 新的视频名称
        :return: 操作结果字典
        """
        try:
            # 从数据库获取视频
            video = Video.query.get(video_id)
            if not video:
                return {
                    'code': '-1',
                    'message': '视频不存在'
                }

            # 更新名称
            video.video_name = new_name
            db.session.commit()

            return {
                'code': '0',
                'message': '视频名称更新成功'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'code': '-1',
                'message': f'更新视频名称失败: {str(e)}'
            }

    @staticmethod
    def set_path(video_id, new_path):
        """更新视频存储路径并刷新视频信息
        :param video_id: 视频ID
        :param new_path: 新的视频存储路径
        :return: 操作结果和新视频信息的字典
        """
        try:
            # 从数据库获取视频
            video = Video.query.get(video_id)
            if not video:
                return {
                    'code': '-1',
                    'message': '视频不存在'
                }

            # 检查新路径是否存在
            if not os.path.exists(new_path):
                return {
                    'code': '-1',
                    'message': '新视频文件不存在'
                }

            # 更新路径
            video.video_path = new_path

            # 获取新的视频信息
            video_info = VideoService.get_info(new_path)
            if video_info.get('code') != '-1':
                video.video_size = video_info.get('video_size')
                video.video_format = video_info.get('format')
                video.video_duration = video_info.get('duration')
                video.video_resolution = video_info.get('resolution')
                video.video_frame_rate = video_info.get('frame_rate')

            db.session.commit()

            return {
                'code': '0',
                'message': '视频路径更新成功',
                'new_video_info': video.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'code': '-1',
                'message': f'更新视频路径失败: {str(e)}'
            }