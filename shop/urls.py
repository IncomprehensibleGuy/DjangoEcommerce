from django.urls import path

from .views import (
    CatalogView,
    ProductView,
    CategoryView,
)


urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),
    path('catalog/<str:slug>/', ProductView.as_view(), name='product'),
]
