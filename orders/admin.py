from django.contrib import admin

from .models import ReceiveMethod, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'city', 'receive_method', 'address', 'apartment_number', 'porch_number', 'floor_number',
                    'intercom', 'full_passport_name', 'phone', 'email', 'delivery_date', 'delivery_time',
                    'payment_method', 'comment', 'status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(ReceiveMethod)
