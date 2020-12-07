import datetime

from django.db import models
from django.utils import timezone

from shop.models import Product


class ReceiveMethod(models.Model):

    title = models.CharField(max_length=64, verbose_name='Название')
    price = models.PositiveIntegerField(default=0, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'

    def __str__(self):
        return str(self.title)


class Order(models.Model):

    STATUS_NEW                  = 'new'
    STATUS_IN_PROGRESS          = 'in_progress'
    STATUS_IS_READY             = 'is_ready'
    STATUS_IN_DELIVERY          = 'in_delivery'
    STATUS_DELIVERED            = 'delivered'
    STATUS_COMPLETED            = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ находится в обработке'),
        (STATUS_IS_READY, 'Заказ готов'),
        (STATUS_IN_DELIVERY, 'Передан в службу доставки'),
        (STATUS_DELIVERED, 'Заказ доставлен'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    PAYMENT_METHOD_CARD_ONLINE  = 'card_online'
    PAYMENT_METHOD_CASH         = 'cash'

    PAYMENT_METHOD_CHOICES = (
        (PAYMENT_METHOD_CARD_ONLINE, 'Картой онлайн'),
        (PAYMENT_METHOD_CASH, 'Наличными при получении'),
    )

    # Form fields
    city = models.CharField(max_length=255, verbose_name='Населённый пункт')
    receive_method = models.ForeignKey(ReceiveMethod, on_delete=models.CASCADE, verbose_name='Способ получения')
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    apartment_number = models.PositiveIntegerField(verbose_name='Квартира', null=True, blank=True)
    porch_number = models.PositiveIntegerField(verbose_name='Подъезд', null=True, blank=True)
    floor_number = models.PositiveIntegerField(verbose_name='Этаж', null=True, blank=True)
    intercom = models.CharField(max_length=255, verbose_name='Код домофона', null=True, blank=True)
    full_passport_name = models.CharField(max_length=255, verbose_name='Фамилия и Имя по паспорту')
    phone = models.CharField(max_length=11, verbose_name='Номер телефона')
    email = models.EmailField(max_length=63, verbose_name='Электронная почта')
    delivery_date = models.DateField(verbose_name='Дата доставки', default=timezone.now)
    delivery_time = models.TimeField(verbose_name='Время доставки', default=datetime.time(12, 00))
    payment_method = models.CharField(
        max_length=255,
        verbose_name='Способ оплаты',
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_CARD_ONLINE,
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    # Others
    status = models.CharField(
        max_length=63,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания заказа')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления заказа')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str('Заказ №{}'.format(self.id))

    def get_payment_method_display(self):
        return Order.PAYMENT_METHOD_CARD_ONLINE


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
