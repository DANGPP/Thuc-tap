from functools import wraps
from flask import request, jsonify
from utils.jwt_utils import decode_token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Thiếu hoặc sai định dạng token"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if "error" in payload:
            return jsonify(payload), 401

        request.user_id = payload["user_id"]
        return f(*args, **kwargs)

    return decorated_function
