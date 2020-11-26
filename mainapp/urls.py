from django.urls import path

from .views import (
    CatalogView,
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
    path('', CatalogView.as_view(), name='catalog'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('catalog/<str:slug>/', ProductView.as_view(), name='product'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-quantity/<str:slug>/', ChangeQuantityView.as_view(), name='change_quantity'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('create-order/', CreateOrderView.as_view(), name='create_order'),
]
