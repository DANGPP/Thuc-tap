import os
class Config:
    # Lấy DATABASE_URL từ biến môi trường (ưu tiên nếu có)
    db_host = os.getenv('DB_HOST', 'host.docker.internal')  # Dùng host.docker.internal trên Windows/macOS
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '1')
    db_name = os.getenv('DB_NAME', 'postgres')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False