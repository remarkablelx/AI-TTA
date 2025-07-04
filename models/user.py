from config.db_config import db_init as db

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    account = db.Column(db.String(11), unique=True, nullable=False, comment='账号')
    password = db.Column(db.String(45), nullable=False, comment='密码')
    nickname = db.Column(db.String(45), comment='昵称')
    avatar = db.Column(db.String(45), comment='头像路径')
    register_time = db.Column(db.DateTime, comment='注册时间')
    sex = db.Column(db.SmallInteger, comment='性别')
    email = db.Column(db.String(45), comment='邮箱')
    note = db.Column(db.Text, comment='备注信息')
    height = db.Column(db.Float, comment='身高')
    weight = db.Column(db.Float, comment='体重')
    location = db.Column(db.String(45), comment='地区')
    birth = db.Column(db.DateTime, comment='出生日期')

    def __repr__(self):
        return f'<User {self.user_id}>'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'register_time': self.register_time,
            'sex': self.sex,
            'email': self.email,
            'note': self.note,
            'height': self.height,
            'weight': self.weight,
            'location':self.location,
            'birth': self.birth
        }