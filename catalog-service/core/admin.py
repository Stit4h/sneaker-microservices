from django.contrib import admin
from .models import Category, Sneaker

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Sneaker)
class SneakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'in_stock', 'category')
    list_filter = ('brand', 'category', 'in_stock')
    search_fields = ('name', 'brand')