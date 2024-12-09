import os
from random import randrange

from django.core.mail import send_mail

from config.celery import app


@app.task
def send_email(email):
    code = randrange(100000, 999999)
    send_mail(
        "Verification Code for Your Email",
        f"Your verification code is: {code}",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=[email],
    )
    with open("detail.txt", "a") as f:
        f.write(f"\nYuborilgan email:{email} uning kodi:{code}\n")
        f.close()
    with open("code.txt", "x") as f:
        f.write(f"{code}")
        f.close()
    return code
