from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomerManager


class Address(models.Model):

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Покупатель')
    title = models.CharField(max_length=64, verbose_name='Название', null=True, blank=True)
    address = models.CharField(max_length=256, verbose_name='Адрес', null=True, blank=True)
    apartment_number = models.PositiveIntegerField(verbose_name='Квартира', null=True, blank=True)
    porch_number = models.PositiveIntegerField(verbose_name='Подъезд', null=True, blank=True)
    floor_number = models.PositiveIntegerField(verbose_name='Этаж', null=True, blank=True)
    intercom = models.CharField(max_length=256, verbose_name='Код домофона', null=True, blank=True)


class Customer(AbstractUser):

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    username = None
    phone = models.CharField(max_length=11, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    activation_code = models.PositiveIntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomerManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
