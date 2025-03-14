# Sử dụng Python 3.11 
FROM python:3.11

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file requirements.txt vào container
COPY requirements.txt .

# Cài đặt thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Mở cổng Flask
EXPOSE 5000

# Chạy ứng dụng Flask
CMD ["python", "app.py"]
