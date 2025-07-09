from flask import Blueprint,jsonify,request
from models.models import Users
from extensions import db
from utils.jwt_utils import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ( 'email_teams', 'mk')):
        return jsonify({'message': 'Thiếu thông tin bắt buộc'}), 400
    email_teams = data.get('email_teams')
    mk = data.get('mk')
    user = Users.query.filter_by(email_teams=email_teams).first()
    if not user:
        return jsonify({'message': 'Người dùng không tồn tại'}), 404
    if not user.check_mk(mk):
        return jsonify({'message': 'Mật khẩu không đúng'}), 401
    token = generate_token(user.id)
    return jsonify({
        'message': 'Đăng nhập thành công',
        "token": token,
        'user': user.to_dict()
    }), 200 
    