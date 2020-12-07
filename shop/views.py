from django.shortcuts import render
from django.views.generic import View, DetailView

from .models import Category, Product
from cart.mixins import CartMixin



class CatalogView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart,
        }
        return render(request, 'catalog.html', context)


class CategoryView(CartMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class ProductView(CartMixin, DetailView):

    context_object_name = 'product'
    template_name = 'product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context
