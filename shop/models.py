from django.db import models
from django.urls import reverse


class Category(models.Model):

    title = models.CharField(max_length=64, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class ProductPhoto(models.Model):

    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    image = models.ImageField(verbose_name='Фото')
    title = models.CharField(max_length=64, verbose_name='Название')

    class Meta:
        ordering = ('product',)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.title


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество на складе')
    available = models.BooleanField(default=True, verbose_name='Доступен для покупок')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})
