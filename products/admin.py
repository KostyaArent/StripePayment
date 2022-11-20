from django.contrib import admin
from .models import Item, OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['item']


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description']
    list_filter = ['name', 'price']
    list_editable = ['price', 'description']


admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
