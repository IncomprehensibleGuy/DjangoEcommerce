from django.urls import path

from .views import (
    BaseView,
    ProductView,
    CategoryView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQuantityView,
    CheckoutView,
    CreateOrderView,
)


urlpatterns = [
    path('', BaseView.as_view(), name='catalog'),
    path('catalog/', BaseView.as_view(), name='catalog'),
    path('catalog/<str:ct_model>/<str:slug>/', ProductView.as_view(), name='product'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-quantity/<str:ct_model>/<str:slug>/', ChangeQuantityView.as_view(), name='change_quantity'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('create-order/', CreateOrderView.as_view(), name='create_order'),
]
