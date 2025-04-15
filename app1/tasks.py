from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_new_show_email(subject, message, recipient_list):
    send_mail(subject, message, None, recipient_list)
