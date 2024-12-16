import os
from random import randrange
from django.core.mail import send_mail
from redis import Redis

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
    r=Redis(decode_responses=True)
    r.set('code', code)
    r.expire('code', 300)
    print(r.get('code'))
    return code


