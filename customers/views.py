from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login

from .forms import LoginForm


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


class AccountView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'account.html', context)
