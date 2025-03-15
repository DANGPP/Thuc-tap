from flask import Flask

from configs.config import Config
from extensions import db
from models.models import User
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

# Khởi tạo database, liên kết với flask app
db.init_app(app)

# Đăng ký routes
register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
