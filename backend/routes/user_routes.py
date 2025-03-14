from flask import Blueprint, jsonify, request, make_response
from extensions import db
from models import User
from sqlalchemy.sql import text

user_bp = Blueprint("user_b", __name__) # Tên Blueprint:"user_bp"

# Kiểm tra kết nối database
@user_bp.route("/health", methods=["GET"])
def health_check():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": f"not connected: {str(e)}"}), 500

# Lấy danh sách users
@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Lấy thông tin chi tiết của một user theo ID
@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User không tồn tại"}), 404

    return jsonify(user.to_dict()), 200

# Thêm user mới
@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "name" not in data or "email_teams" not in data:
        return make_response(jsonify({"error": "Thiếu thông tin name hoặc email_teams"}), 400)

    new_user = User(name=data["name"], email_teams=data["email_teams"], sdt=data.get("sdt"))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

# Cập nhật user
@user_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User không tồn tại"}), 404

    data = request.get_json()
    if "name" in data:
        user.name = data["name"]
    if "email_teams" in data:
        user.email_teams = data["email_teams"]
    if "sdt" in data:
        user.sdt = data["sdt"]

    db.session.commit()
    return jsonify(user.to_dict()), 200

# Xóa user
@user_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User không tồn tại"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User đã bị xóa"}), 200
