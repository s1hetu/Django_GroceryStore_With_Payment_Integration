import os

from celery import shared_task
from django.core.mail import send_mail

@shared_task()
def send_email_when_quantity_available(subject, message, receiver):
    if receiver:
        recipient_list = [receiver, ]
    else:
        recipient_list = ['shahhetu.hs@gmail.com']
    send_mail(
        subject,
        message,
        os.environ.get('EMAIL_USER'),
        recipient_list,
        fail_silently = False
    )

@shared_task()
def eee():
    for i in range(1,9):
        print(i)
    return "done"
