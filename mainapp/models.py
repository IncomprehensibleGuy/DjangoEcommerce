import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone

#-------------------------------
# 1  Category +
# 2  Product +
# 3  Smartphone extends Product +
# 4  Notebook extends Product +
# 5  CartProduct +
# 6  Cart +
# 7  Customer +
# 8  Order +
#-------------------------------


User = get_user_model()


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by("-id")[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager


class CategoryManager(models.Manager):

    CATEGORY_TITLE_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфоны': 'smartphone__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_sidebar_categories(self):
        models = get_models_for_count('notebook','smartphone')
        queryset = self.get_queryset().annotate(*models)
        data = [
            dict(
                title=category.title,
                url=category.get_absolute_url(),
                count=getattr(category, self.CATEGORY_TITLE_COUNT_NAME[category.title])
            ) for category in queryset
        ]
        return data


class Category(models.Model):

    title = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (2000, 2000)

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

    class Meta:
        abstract = True



class Smartphone(Product):

    class Meta:
        verbose_name = "Смартфон"
        verbose_name_plural = "Смартфоны"

    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    display_type = models.CharField(max_length=255, verbose_name="Матрица")
    resolution = models.CharField(max_length=255, verbose_name="Разрешение экрана")
    accumulator_volume = models.CharField(max_length=255, verbose_name="Ёмкость аккумулятора")
    sd_volume_max = models.CharField(max_length=255, verbose_name="Объём встроенной памяти")
    ram = models.CharField(max_length=255,
                           choices=[ (str(x)+' ГБ', str(x)+' ГБ') for x in [2, 3, 4, 6, 8, 16, 32]],
                           verbose_name="Объём оперативной памяти")
    sd = models.BooleanField(default=True, verbose_name="SD карта")
    main_camera_mp = models.CharField(max_length=255, verbose_name="Основная камера")
    frontal_camera_mp = models.CharField(max_length=255, verbose_name="Фронтальная камера")

    def __str__(self):
        return "{}: {}".format(self.category.title, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product')


class Notebook(Product):

    class Meta:
        verbose_name = "Ноутбук"
        verbose_name_plural = "Ноутбуки"

    diagonal = models.FloatField(verbose_name="Диагональ")
    display_type = models.CharField(max_length=255, verbose_name="Матрица")
    processor = models.CharField(max_length=255, verbose_name="Процессор")
    processor_frequency = models.CharField(max_length=255, verbose_name="Частота процессора")
    total_memory = models.CharField(max_length=255, verbose_name="Общий объём памяти")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    video = models.CharField(max_length=255, verbose_name="Видеокарта")
    time_without_charge = models.CharField(max_length=255, verbose_name="Время работы аккумулятора")

    def __str__(self):
        return "{}: {}".format(self.category.title, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product')


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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=7, decimal_places=0, default=0, verbose_name="Общая стоимость")

    def __str__(self):
        return "Товар: {}".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.total_price = self.content_object.price * self.quantity
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
