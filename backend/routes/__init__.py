from flask import Blueprint
from routes.user_routes import user_bp
from routes.event_routes import event_bp 
from routes.auth import auth_bp

# Đăng ký Blueprint cho routes
def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(event_bp)  # Đăng ký routes cho sự kiện
    app.register_blueprint(auth_bp)  # Đăng ký routes cho xác thực
