from config.db_config import db_init as db

class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='报告ID')
    pose_estimate = db.Column(db.Text, nullable=True, comment='分析报告结果')
    result_id = db.Column(db.Integer, nullable=True, comment='分析结果ID')
    __table_args__ = (
        db.Index('result_id_idx', 'result_id'),
    )

    def __repr__(self):
        return f'<Report {self.report_id}>'

    def to_dict(self):
        return {
            'report_id': self.report_id,
            'pose_estimate': self.pose_estimate,
            'result_id': self.result_id
        }