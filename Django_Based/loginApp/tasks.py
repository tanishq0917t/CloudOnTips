from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task
import time

@shared_task
def send_html_email(otp,email):
    subject = "Verify your OTP"
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    message = EmailMessage(subject=subject,body="",from_email=from_email,to=to_email)
    message.content_subtype = "html"
    message.body = f"<h1>Hello!</h1><p>Your OTP is: <b>{otp}</b></p>"
    message.send()