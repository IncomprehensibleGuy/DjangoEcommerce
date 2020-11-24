from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from PIL import Image

from .models import *


class NotebookAdminForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image1'].help_text = 'Минимальное разрешение: {}Х{}'.format(*Product.MIN_RESOLUTION)
    #
    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #
    #     if img.width < Product.MIN_RESOLUTION[0] or img.height < Product.MIN_RESOLUTION[1]:
    #         raise ValueError('Разрешение изображения меньше минимального')
    #     if img.width > Product.MAX_RESOLUTION[0] or img.height > Product.MAX_RESOLUTION[1]:
    #         raise ValueError('Разрешение изображения больше максимального')
    #
    #     return image


class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="notebooks"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="smartphones"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(ReceiveMethod)
