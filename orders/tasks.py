from django.core.mail import send_mail

from base.celery import app
from base.settings import EMAIL_HOST_USER


@app.task
def send_registration_code_email(email):
    print('sending registration code to {}'.format(email))


@app.task
def send_order_created_email(email, details):
    ''' Send order details to customer email '''
    send_mail(
        'Детали заказа',
        'Детали заказа: {}'.format(details),
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
