from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import LoginView, RegistrationView, AccountView, ConfirmEmailView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('account/', AccountView.as_view(), name='account'),
]
