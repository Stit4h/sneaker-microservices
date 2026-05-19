from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_items', 'get_total_price', 'created_at')

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Кол-во товаров'

    def get_total_price(self, obj):
        return f'{obj.get_total_price()} ₽'
    get_total_price.short_description = 'Итого'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'sneaker_name', 'quantity', 'get_total_price')

    def get_total_price(self, obj):
        return f'{obj.get_total_price()} ₽'
    get_total_price.short_description = 'Сумма'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'sneaker_name', 'quantity', 'price')