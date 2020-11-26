import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone


#-------------------------------
# Address
# Customer +
# Category +
# Product +
# Smartphone extends Product + / delete at refactoring
# Notebook extends Product + / delete at refactoring
# CartProduct +
# Cart +
# Order +
#-------------------------------


User = get_user_model()


class Address(models.Model):

    title = models.CharField(max_length=64, verbose_name='Название', null=True, blank=True)
    address = models.CharField(max_length=256, verbose_name='Адрес', null=True, blank=True)
    apartment_number = models.PositiveIntegerField(verbose_name='Квартира', null=True, blank=True)
    porch_number = models.PositiveIntegerField(verbose_name='Подъезд', null=True, blank=True)
    floor_number = models.PositiveIntegerField(verbose_name='Этаж', null=True, blank=True)
    intercom = models.CharField(max_length=256, verbose_name='Код домофона', null=True, blank=True)


class Customer(models.Model):

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(max_length=63, verbose_name='Электронная почта', blank=True)
    orders = models.ManyToManyField('Order', verbose_name='История заказов', related_name='related_customer')
    addresses = models.ForeignKey(Address, verbose_name='Адреса', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.__str__()


class Category(models.Model):

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(max_length=64, verbose_name="Категория")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Product(models.Model):

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    title = models.CharField(max_length=255, verbose_name="Название")
    image1 = models.ImageField(verbose_name="Фото 1", blank=True)
    image2 = models.ImageField(verbose_name="Фото 2", blank=True)
    image3 = models.ImageField(verbose_name="Фото 3", blank=True)
    image4 = models.ImageField(verbose_name="Фото 4", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name="Цена")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})


class Cart(models.Model):

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    owner = models.ForeignKey(Customer, verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField("CartProduct", blank=True, related_name="related_products")
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name="Общая стоимость", default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartProduct(models.Model):

    class Meta:
        verbose_name = "Товар корзины"
        verbose_name_plural = "Товары корзины"

    user = models.ForeignKey(Customer, verbose_name="Клиент", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=7, decimal_places=0, default=0, verbose_name="Общая стоимость")

    def __str__(self):
        return "Товар: {}".format(self.product.title)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)


class ReceiveMethod(models.Model):

    title = models.CharField(max_length=64, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Стоимость', default=0)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Способ доставки"
        verbose_name_plural = "Способы доставки"


class Order(models.Model):

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_IS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_IS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    PAYMENT_METHOD_CARD_ONLINE = 'card_online'
    PAYMENT_METHOD_CASH = 'cash'

    PAYMENT_METHOD_CHOICES = (
        (PAYMENT_METHOD_CARD_ONLINE, 'Картой онлайн'),
        (PAYMENT_METHOD_CASH, 'Наличныйми при получении'),
    )

    # Form fields
    city = models.CharField(max_length=255, verbose_name='Населённый пункт')
    receive_method = models.ForeignKey(
        ReceiveMethod,
        on_delete=models.CASCADE,
        verbose_name='Способ получения',
        default='Самовывоз',
    )

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
    customer = models.ForeignKey(
        Customer,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
        related_name='related_order'
    )
    cart = models.ForeignKey(Cart, verbose_name='корзина', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=63,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    creation_datetime = models.DateTimeField(auto_now=True, verbose_name='Дата и время создания заказа')

    def __str__(self):
        return str('Заказ №{} от {}'.format(self.id, self.customer.__str__()))

    def get_payment_method_display(self):
        return Order.PAYMENT_METHOD_CARD_ONLINE
