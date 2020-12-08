from django.contrib import admin

from .models import Category, Product, ProductPhoto


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'quantity', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'quantity', 'available']
    prepopulated_fields = {'slug': ('title',)}


class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'title']
    list_filter = ['product', 'title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPhoto, ProductPhotoAdmin)