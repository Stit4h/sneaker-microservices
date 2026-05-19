from django.db import models


class Category(models.Model):
    """Категория кроссовок (Nike, Adidas, Puma)"""
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='URL-метка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Sneaker(models.Model):
    """Модель кроссовок (товар)"""
    name = models.CharField(max_length=200, verbose_name='Название')
    brand = models.CharField(max_length=50, verbose_name='Бренд')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='sneakers/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sneakers', verbose_name='Категория')
    description = models.TextField(blank=True, verbose_name='Описание')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'{self.brand} - {self.name}'

    class Meta:
        verbose_name = 'Кроссовок'
        verbose_name_plural = 'Кроссовки'