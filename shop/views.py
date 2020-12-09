from django.shortcuts import render
from django.views.generic import View, DetailView

from .models import Category, Product


class CatalogView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        context = {
            'categories': categories,
            'products': products,
        }
        return render(request, 'catalog.html', context)


class CategoryView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_products'] = self.get_object().product_set.all()
        return context


class ProductView(DetailView):

    model = Product
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'product.html'
    slug_url_kwarg = 'slug'

    # def dispatch(self, request, *args, **kwargs):
    #     self.queryset = Product.objects.all()
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
