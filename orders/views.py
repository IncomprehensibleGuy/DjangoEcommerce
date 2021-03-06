from django.views import View
from django.shortcuts import render
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect

from shop.models import Category
from cart.cart import Cart

from .models import ReceiveMethod, OrderItem
from .forms import CreateOrderForm
from .tasks import send_order_created_email


class CheckoutView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = CreateOrderForm(request.POST or None)

        context = {
            'categories': categories,
            'form': form,
            'receive_methods': ReceiveMethod.objects.all(),
        }

        return render(request, 'checkout.html', context)


class CreateOrderView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = CreateOrderForm(request.POST or None)
        cart = Cart(request)
        #customer = Customer.objects.get(user=request.user)

        if form.is_valid():
            order = form.save(commit=False)
            # order.customer = customer
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
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

            # Celery email task
            send_str = 'Вы закази {} товаров на сумму {} руб.'.format(cart.__len__(), cart.get_total_price())
            send_order_created_email.delay(form.cleaned_data['email'], send_str)

            cart.clear()

            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с вами свяжется в течение 5 минут.')
            return HttpResponseRedirect('/')

        return HttpResponseRedirect('/orders/checkout/')
