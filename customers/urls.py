from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import LoginView, AccountView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
]
