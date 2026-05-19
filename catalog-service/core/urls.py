from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('shop/', views.shop, name='shop'),
    path('shop/<slug:category_slug>/', views.shop, name='shop_by_category'),
    path('filter-products/', views.filter_products, name='filter_products'),
]