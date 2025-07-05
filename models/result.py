from config.db_config import db_init as db

class Result(db.Model):
    __tablename__ = 'result'
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='结果ID')
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), nullable=True, comment='视频ID')
    ball_json_path = db.Column(db.String(100), nullable=True, comment='球轨迹文件路径')
    pose_json_path = db.Column(db.String(100), nullable=True, comment='骨骼标签文件路径')
    ball_video_path = db.Column(db.String(100), nullable=True, comment='球轨迹标注视频路径')
    pose_video_path = db.Column(db.String(100), nullable=True, comment='骨骼点标注视频路径')
    segment_json_path = db.Column(db.String(100), nullable=True, comment='动作时间戳路径')
    annotated_video_path = db.Column(db.String(100), nullable=True, comment='动作视频路径')
    recognition_json_path = db.Column(db.String(100), nullable=True, comment='动作标签文件路径')
    __table_args__ = (
        db.Index('video_idx', 'video_id'),
    )

    def __repr__(self):
        return f'<Result {self.result_id}>'

    def to_dict(self):
        return {
            'result_id': self.result_id,
            'video_id': self.video_id,
            'ball_json_path': self.ball_json_path,
            'pose_json_path': self.pose_json_path,
            'ball_video_path': self.ball_video_path,
            'pose_video_path': self.pose_video_path,
            'segment_json_path': self.segment_json_path,
            'annotated_video_path': self.annotated_video_path,
            'recognition_json_path': self.recognition_json_path
        }