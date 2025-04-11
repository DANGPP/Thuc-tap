from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configs.config import Config

# Cấu hình Celery
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

@celery.task
def send_email_background(subject, recipient, body):
    sender_email = "maitiandewd@gmail.com"
    sender_password = "brzo hedf veiy jksi"  # App password

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())

        print(f"Email đã được gửi đến {recipient}")
        return f"Email sent to {recipient}"

    except Exception as e:
        print(f"Lỗi khi gửi email: {str(e)}")
        raise e
