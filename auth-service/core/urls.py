from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
]