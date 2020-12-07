# from django.db import models
#
# from customers.models import Customer
# from shop.models import Product
#
#
# class Cart(models.Model):
#
#     class Meta:
#         verbose_name = "Корзина"
#         verbose_name_plural = "Корзины"
#
#     owner = models.ForeignKey(Customer, verbose_name="Владелец", on_delete=models.CASCADE)
#     products = models.ManyToManyField("CartProduct", blank=True, related_name="related_products")
#     total_products = models.PositiveIntegerField(default=0)
#     total_price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name="Общая стоимость", default=0)
#     in_order = models.BooleanField(default=False)
#     for_anonymous_user = models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.id)
#
#
# class CartProduct(models.Model):
#
#     class Meta:
#         verbose_name = "Товар корзины"
#         verbose_name_plural = "Товары корзины"
#
#     user = models.ForeignKey(Customer, verbose_name="Клиент", on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_cart")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     total_price = models.DecimalField(max_digits=7, decimal_places=0, default=0, verbose_name="Общая стоимость")
#
#     def __str__(self):
#         return "Товар: {}".format(self.product.title)
#
#     def save(self, *args, **kwargs):
#         self.total_price = self.product.price * self.quantity
#         super().save(*args, **kwargs)
