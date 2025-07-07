from flask import  Flask, request, Response
from routes.user import user
from routes.video import video
from routes.record import record
from routes.admin import admin
from routes.result import result
from config.db_config import app
from flask_cors import  CORS
CORS(app)

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(video, url_prefix="/video")
app.register_blueprint(record, url_prefix="/record")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(result, url_prefix="/result")

@app.route('/')
def ping():
    return  'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
