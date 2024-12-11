from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_password_reset_email(user_email):
    send_mail(
        'Password Reset Request',
        'Please follow the instructions to reset your password.',
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
