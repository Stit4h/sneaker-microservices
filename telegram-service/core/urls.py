from django.urls import path
from . import views

app_name = 'telegram'

urlpatterns = [
    path('send-message/', views.send_telegram_message, name='send_telegram'),
    path('send-notification/', views.send_notification, name='send_notification'),
]