from django.contrib import admin
from django.urls import path, include
from django.conf import settings          # ← ДОБАВИТЬ ЭТУ СТРОКУ
from django.conf.urls.static import static  # ← ДОБАВИТЬ ЭТУ СТРОКУ

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

# ← ДОБАВИТЬ ЭТОТ БЛОК (В САМОМ КОНЦЕ ФАЙЛА)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)