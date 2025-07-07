from config.db_config import db_init as db


class Video(db.Model):
    __tablename__ = 'video'  # 数据库表名

    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='视频ID')
    video_path = db.Column(db.String(100), nullable=True, comment='视频存储路径')
    video_name = db.Column(db.String(45), nullable=True, comment='视频名称')
    video_size = db.Column(db.DECIMAL(5, 2), nullable=True, comment='视频文件大小')
    video_duration = db.Column(db.String(45), nullable=True, comment='视频时长')
    video_format = db.Column(db.String(45), nullable=True, comment='文件格式')
    video_resolution = db.Column(db.String(45), nullable=True, comment='视频分辨率')
    video_frame_rate = db.Column(db.DECIMAL(5, 2), nullable=True, comment='视频帧率(FPS)')

    def __repr__(self):
        return f'<Video {self.video_id}>'

    def to_dict(self):
        return {
            'video_id': self.video_id,
            'video_name': self.video_name,
            'video_size': self.video_size,
            'video_path': self.video_path,
            'video_duration': self.video_duration,
            'video_resolution': self.video_resolution,
            'video_frame_rate': self.video_frame_rate,
            'video_format': self.video_format
        }