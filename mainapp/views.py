from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, DetailView
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from .models import (
    Customer,
    Category,
    Product,
    CartProduct,
    ReceiveMethod,
)
from .mixins import CartMixin
from .forms import OrderForm
from .utils import recalculate_cart


class CatalogView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart,
        }
        return render(request, 'catalog.html', context)


class CategoryView(CartMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class ProductView(CartMixin, DetailView):

    context_object_name = 'product'
    template_name = 'product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories,
        }
        return render(request, 'cart.html', context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, is_created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if is_created:
            self.cart.products.add(cart_product)
        recalculate_cart(self.cart)
        messages.add_message(request, messages.INFO, '{} добавлен в корзину'.format(product.title))
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalculate_cart(self.cart)
        messages.add_message(request, messages.INFO, '{} удалён из корзины'.format(product.title))
        return HttpResponseRedirect('/cart/')


class ChangeQuantityView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        cart_product.quantity = int(request.POST.get('quantity'))
        cart_product.save()
        recalculate_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Количество {} изменено'.format(product.title))
        return HttpResponseRedirect('/cart/')


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)

        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form,
            'total_order_price': self.cart.total_price,
            'receive_methods': ReceiveMethod.objects.all(),
        }

        return render(request, 'checkout.html', context)


class CreateOrderView(CartMixin, View):

    def fill_order_info(self, order, form, customer):
        order.customer = customer
        order.city = form.cleaned_data['city']
        order.receive_method = form.cleaned_data['receive_method']
        order.address = form.cleaned_data['address']
        order.apartment_number = form.cleaned_data['apartment_number']
        order.porch_number = form.cleaned_data['porch_number']
        order.floor_number = form.cleaned_data['floor_number']
        order.intercom = form.cleaned_data['intercom']
        order.full_passport_name = form.cleaned_data['full_passport_name']
        order.phone = form.cleaned_data['phone']
        order.email = form.cleaned_data['email']
        order.delivery_date = form.cleaned_data['delivery_date']
        order.delivery_time = form.cleaned_data['delivery_time']
        order.payment_method = form.cleaned_data['payment_method']
        order.comment = form.cleaned_data['comment']
        order.cart = self.cart
        order.save()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)

        if form.is_valid():
            self.cart.in_order = True
            self.cart.save()

            new_order = form.save(commit=False)
            self.fill_order_info(new_order, form, customer)

            customer.phone = form.cleaned_data['phone']
            customer.email = form.cleaned_data['email']
            # customer.addresses.add(
            #     Address(
            #         address=form.cleaned_data['address'],
            #         apartment_number=form.cleaned_data['apartment_number'],
            #         porch_number=form.cleaned_data['porch_number'],
            #         floor_number=form.cleaned_data['floor_number'],
            #         intercom=form.cleaned_data['intercom']
            #     )
            # )
            customer.orders.add(new_order)
            customer.save()

            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с вами свяжется в течение 5 минут.')
            return HttpResponseRedirect('/')

        return HttpResponseRedirect('/checkout/')
