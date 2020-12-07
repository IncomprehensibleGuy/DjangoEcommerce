from django.views import View
from django.shortcuts import render
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import CreateOrderForm
from cart.mixins import CartMixin


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = CreateOrderForm(request.POST or None)

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
        form = CreateOrderForm(request.POST or None)
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
