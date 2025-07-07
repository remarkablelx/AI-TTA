from config.db_config import db_init as db

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='管理员ID')
    account = db.Column(db.String(11), nullable=True, comment='管理员账号')
    password = db.Column(db.String(45), nullable=True, comment='密码')

    def __repr__(self):
        return f'<Admin {self.admin_id}>'

    def to_dict(self):
        return {
            'admin_id': self.admin_id,
            'account': self.account,
            'password': self.password
        }