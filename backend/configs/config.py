import os
class Config:
    # Lấy DATABASE_URL từ biến môi trường (ưu tiên nếu có)
    db_host = os.getenv('DB_HOST', 'host.docker.internal')  # Dùng host.docker.internal trên Windows/macOS
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD','1')
    db_name = os.getenv('DB_NAME', 'postgres')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT   = 587
    MAIL_USE_TLS   = True
    MAIL_USERNAME   = 'maitiandewd@gmail.com'
    MAIL_PASSWORD   = 'brzo hedf veiy jksi'  # App password
    MAIL_DEFAULT_SENDER   = 'maitiandewd@gmail.com'
    
    # Chỉ cần đặt Redis URL một lần
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND","redis://localhost:6379/1")
    CELERY_CONFIG = {
        'task_serializer': 'json',
        'accept_content': ['json'],
        'result_serializer': 'json'
    }