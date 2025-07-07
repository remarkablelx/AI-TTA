from config.db_config import db_init as db

class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='报告ID')
    pose_estimate = db.Column(db.Text, nullable=True, comment='姿势评估结果')
    technical_analysis = db.Column(db.Text, nullable=True, comment='技术分析')
    train_advice = db.Column(db.Text, nullable=True, comment='训练建议')

    def __repr__(self):
        return f'<Report {self.report_id}>'

    def to_dict(self):
        return {
            'report_id': self.report_id,
            'pose_estimate': self.pose_estimate,
            'technical_analysis': self.technical_analysis,
            'train_advice': self.train_advice
        }