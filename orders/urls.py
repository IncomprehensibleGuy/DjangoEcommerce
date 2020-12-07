from django.urls import path

from .views import (
    CheckoutView,
    CreateOrderView,
)


urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('create-order/', CreateOrderView.as_view(), name='create_order'),
]
