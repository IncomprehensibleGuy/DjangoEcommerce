'''
Issues:
* admin and user login conflict (csrf)
* incorrect work with passwords
'''

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login

from .forms import LoginForm, RegistrationForm
from .models import Customer


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
            customer = form.save(commit=False)
            customer.email = form.cleaned_data['email']
            customer.set_password(form.cleaned_data['password1'])
            customer.save()
            print(Customer.objects.all())
            customer = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            if customer:
                login(request, customer)
                return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'registration.html', context)


class AccountView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'account.html', context)
