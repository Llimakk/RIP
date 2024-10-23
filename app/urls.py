from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('bills/', index, name='bills'),  # Добавлено имя
    path('bills/<int:bill_id>/', bill, name='bill'),  # Добавлено имя
    path('operat/<int:operat_id>/', operat, name='operat'),  # Добавлено имя
    path('add_to_cart/<int:bill_id>/', add_to_cart, name='add_to_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
