from config.db_config import db_init as db

class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='报告ID')
    video_result_path = db.Column(db.String(45), nullable=True, comment='视频结果路径')
    pose_estimate = db.Column(db.Text, nullable=True, comment='姿势评估结果')
    exercise_advice = db.Column(db.Text, nullable=True, comment='锻炼建议')
    train_advice = db.Column(db.Text, nullable=True, comment='训练建议')

    def __repr__(self):
        return f'<Report {self.report_id}>'

    def to_dict(self):
        return {
            'report_id': self.report_id,
            'video_result_path': self.video_result_path,
            'pose_estimate': self.pose_estimate,
            'exercise_advice': self.exercise_advice,
            'train_advice': self.train_advice
        }