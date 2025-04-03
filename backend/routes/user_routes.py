from flask import Blueprint,jsonify,request
from models.models import Users
from extensions import db
user_bp = Blueprint("user_bp",__name__)


#1. lấy thông tin của toàn bộ người dùng:
@user_bp.route("/users", methods = ["GET"])
def get_users():
    users = Users.query.all()
    return jsonify([user.to_dict() for user in users])

#2. lấy thông tin chi tiết của 1 người dùng
@user_bp.route("/users/<int:user_id>", methods =["GET"])
def get_user_id(user_id):
    user = Users.query.get(user_id)
    return jsonify(user.to_dict())

#3. Thêm users
@user_bp.route("/users", methods=["POST"])
def post_user():
    data_list = request.get_json()

    if not isinstance(data_list, list):
        return jsonify({"error": "Input không phải list"}), 400

    users_created = []  # Lưu danh sách user được tạo
    users_not_created = []
    for data in data_list:
        if 'name' not in data or 'email_teams' not in data or "sdt" not in data or 'ten_nh' not in data or 'stk' not in data:
            users_not_created.append(data)
            continue  # Bỏ qua nếu thiếu thông tin

        try:
            new_user = Users(
                name=data['name'],
                email_teams=data['email_teams'],
                sdt=data['sdt'],
                ten_nh=data['ten_nh'],
                stk=data['stk']
            )
            db.session.add(new_user)
            users_created.append(new_user)
        except Exception as ex:
            print(f"Lỗi khi thêm user: {ex}")
            continue  # Bỏ qua user bị lỗi

    try:
        db.session.commit()
        return jsonify({
            "message": "Danh sách user đã thêm",
            "users": [user.to_dict() for user in users_created],
            "message_error": "Danh sách users chưa được thêm",
            "error_uesrs": [user for user in users_not_created]
        }), 201
    except Exception as ex:
        db.session.rollback()
        return jsonify({
            "error": str(ex),
            "users_created": [user.to_dict() for user in users_created],
            "error_users": users_not_created
        }), 500
#4. Xóa users
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error":"Không có user để xóa"})
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"Đã xóa thành công"})
    except Exception as ex:
        return jsonify({"error": str(ex)})
    
#5. Chỉnh sửa người dùng
@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def adjust_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error":"Không tồn tại user."})
    data = request.get_json()
    user.name=data.get('name',user.name)
    user.email_teams=data.get('email_teams',user.email_teams)
    user.sdt=data.get('sdt',user.sdt)
    user.ten_nh=data.get('ten_nh',user.ten_nh)
    user.stk=data.get('stk',user.stk)
    try:
        db.session.commit()
        return jsonify({"message": "Cập nhật thành công", "user": user.to_dict()}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 500