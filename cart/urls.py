from django.urls import path

from .views import (
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQuantityView,
)


urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-quantity/<str:slug>/', ChangeQuantityView.as_view(), name='change_quantity'),
]
