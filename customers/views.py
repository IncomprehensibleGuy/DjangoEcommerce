'''
Issues:
* admin and user login conflict (csrf)
* incorrect work with passwords
'''
from random import randint

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login

from .forms import LoginForm, RegistrationForm, ConfirmEmailForm
from .models import Customer
from .tasks import send_registration_code_email


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            customer = authenticate(email=email, password=password)
            if customer:
                login(request, customer)
                return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'login.html', context)


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            activation_code = randint(10000, 99999)

            customer = form.save(commit=False)
            customer.email = form.cleaned_data['email']
            customer.set_password(form.cleaned_data['password1'])
            customer.activation_code = activation_code
            customer.is_active = False
            customer.save()
            authenticate(email=customer.email, password=customer.password)

            send_registration_code_email.delay(form.cleaned_data['email'], activation_code)

            return HttpResponseRedirect('../confirm-email/')

        context = {'form': form}
        return render(request, 'registration.html', context)


class AccountView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'account.html', context)


class ConfirmEmailView(View):

    def get(self, request, *args, **kwargs):
        form = ConfirmEmailForm(request.POST or None)
        context = {'form': form}
        return render(request, 'confirm_email.html', context)

    def post(self, request, *args, **kwargs):
        form = ConfirmEmailForm(request.POST or None)
        if form.is_valid():
            code = ''
            code += str(form.cleaned_data['d1'])
            code += str(form.cleaned_data['d2'])
            code += str(form.cleaned_data['d3'])
            code += str(form.cleaned_data['d4'])
            code += str(form.cleaned_data['d5'])
            code = int(code)
            customer = Customer.objects.get(activation_code=code)
            if customer:
                customer.is_active = True
                customer.save()
                login(request, customer)
                return HttpResponseRedirect('../account/')
        context = {'form': form}
        return render(request, 'confirm_email.html', context)
