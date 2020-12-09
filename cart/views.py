from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect

from shop.models import Category, Product
from cart.cart import Cart


class CartView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cart.html', context)


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart = Cart(request)
        cart.add_product(product=product)
        messages.add_message(request, messages.INFO, '{} добавлен в корзину'.format(product.title))
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart = Cart(request)
        cart.remove_product(product)
        messages.add_message(request, messages.INFO, '{} удалён из корзины'.format(product.title))
        return HttpResponseRedirect('/cart/')


class ChangeQuantityView(View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart = Cart(request)
        cart.change_product_quantity(product, int(request.GET.get('quantity')))
        messages.add_message(request, messages.INFO, 'Количество {} изменено'.format(product.title))
        return HttpResponseRedirect('/cart/')
