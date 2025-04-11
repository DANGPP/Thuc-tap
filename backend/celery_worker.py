from tasks.send_mail_task import celery  # import celery app

# Khi chạy celery, sử dụng worker này
if __name__ == '__main__':
    celery.start()
