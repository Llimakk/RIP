# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('', Index, name='index'),
#     path('bills/', Index),
#     path('bills/<int:bill_id>/', bill),
#     path('operat/<int:operat_id>/', operat),
#     path('add_to_cart/<int:bill_id>/', add_to_cart, name='add_to_cart'),
#     path('clear_cart/', clear_cart, name='clear_cart'),
# ]

from django.urls import path
from .views import *

urlpatterns = [
    path('', Index, name='index'),
    path('bills/', Index, name='bills'),  # Добавлено имя
    path('bills/<int:bill_id>/', bill, name='bill'),  # Добавлено имя
    path('operat/<int:operat_id>/', operat, name='operat'),  # Добавлено имя
    path('add_to_cart/<int:bill_id>/', add_to_cart, name='add_to_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
]

