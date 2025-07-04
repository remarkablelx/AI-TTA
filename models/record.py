from config.db_config import db_init as db

class Record(db.Model):
    __tablename__ = 'record'
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='记录ID')
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), nullable=True, comment='视频ID')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True, comment='用户ID')
    state = db.Column(db.Integer, nullable=True, comment='状态')
    time = db.Column(db.DateTime, nullable=True, comment='生成时间')
    expiration_time = db.Column(db.DateTime, nullable=True, comment='过期时间')
    __table_args__ = (
        db.Index('video_id_idx', 'video_id'),
        db.Index('uesr_id_idx', 'user_id'),
    )

    def __repr__(self):
        return f'<Record {self.record_id}>'

    def to_dict(self):
        return {
            'record_id': self.record_id,
            'video_id': self.video_id,
            'user_id': self.user_id,
            'state': self.state,
            'time': self.time,
            'expiration_time': self.expiration_time
        }