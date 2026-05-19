from django.contrib import admin
from .models import Category, Sneaker, Cart, CartItem, UserProfile, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Sneaker)
class SneakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'in_stock', 'category')
    list_filter = ('brand', 'category', 'in_stock')
    search_fields = ('name', 'brand')


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
    list_display = ('cart', 'sneaker', 'quantity', 'get_total_price')

    def get_total_price(self, obj):
        return f'{obj.get_total_price()} ₽'

    get_total_price.short_description = 'Сумма'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')