from config.db_config import db_init as db

class Result(db.Model):
    __tablename__ = 'result'
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='结果ID')
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), nullable=True, comment='视频ID')
    ball_trace_path = db.Column(db.String(45), nullable=True, comment='球轨迹文件路径')
    bone_label_path = db.Column(db.String(45), nullable=True, comment='骨骼标签文件路径')
    report_id = db.Column(db.Integer, db.ForeignKey('report.report_id'), nullable=True, comment='报告ID')
    video_with_ball_trace = db.Column(db.String(45), nullable=True, comment='球轨迹标注视频路径')
    video_with_bone_label = db.Column(db.String(45), nullable=True, comment='骨骼点标注视频路径')
    action_timestamp_path = db.Column(db.String(45), nullable=True, comment='动作时间戳路径')
    __table_args__ = (
        db.Index('report_id_idx', 'report_id'),
        db.Index('video_idx', 'video_id'),
    )

    def __repr__(self):
        return f'<Result {self.result_id}>'

    def to_dict(self):
        return {
            'result_id': self.result_id,
            'video_id': self.video_id,
            'ball_trace_path': self.ball_trace_path,
            'bone_label_path': self.bone_label_path,
            'report_id': self.report_id,
            'video_with_ball_trace': self.video_with_ball_trace,
            'video_with_bone_label': self.video_with_bone_label,
            'action_timestamp_path': self.action_timestamp_path
        }