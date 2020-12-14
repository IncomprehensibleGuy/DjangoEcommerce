from django.core.mail import send_mail

from base.celery import app
from base.settings import EMAIL_HOST_USER


@app.task
def send_registration_code_email(email, activation_code):
    ''' Send order details to customer email '''

    send_mail(
        'Код активации на сайте',
        'Код: {}'.format(activation_code),
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
