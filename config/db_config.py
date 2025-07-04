from flask import  Flask
from flask_sqlalchemy import  SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/shixun'

db_init = SQLAlchemy(app)