import jwt
import datetime

SECRET_KEY = "hello"  # tốt nhất đọc từ biến môi trường

def generate_token(user_id, expires_in=2):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expires_in)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token đã hết hạn"}
    except jwt.InvalidTokenError:
        return {"error": "Token không hợp lệ"}
