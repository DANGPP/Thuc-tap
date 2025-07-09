from flask import Flask
from flask_cors import CORS
from configs.config import Config
from extensions import db
from routes import register_routes
from models import models
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",  # hoặc giới hạn domain: "http://localhost:3000"
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
app.config.from_object(Config)

# Khởi tạo database, liên kết với flask app
db.init_app(app)
with app.app_context():
    db.create_all()
# Đăng ký routes
register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
