from models.video import db, Video

class VideoService:
    @staticmethod
    def upload_video(video_path:str, video_name:str):

        try:
            # 创建新用户
            new_video = Video(
                video_name=video_name,
                video_path=video_path,
            )
            db.session.add(new_video)
            db.session.commit()

            return {
                'code': '0',
                'message': '视频上传成功',
                'user_id': new_video.user_id
            }
        except Exception as e:
            db.session.rollback()
            return {'code': '-1', 'message': f'视频上传失败: {str(e)}'}

    @staticmethod
    def select_video(video_id:int):
        return

    @staticmethod
    def delete_video(video_id:int):
        return

    @staticmethod
    def update_name(video_id:int):
        return



