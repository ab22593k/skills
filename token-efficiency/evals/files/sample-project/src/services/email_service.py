import smtplib
from email.mime.text import MIMEText

class EmailService:
    def __init__(self, smtp_host="localhost", smtp_port=25):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send_welcome_email(self, user_email, username):
        msg = MIMEText(f"Welcome {username}!")
        msg["Subject"] = "Welcome to our platform"
        msg["To"] = user_email
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.send_message(msg)

    def send_password_reset(self, user_email, token):
        msg = MIMEText(f"Reset your password using token: {token}")
        msg["Subject"] = "Password Reset Request"
        msg["To"] = user_email
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.send_message(msg)
