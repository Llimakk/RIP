"""
URL configuration for lab1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from migrations import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.GetBills),
#     path('bills/', views.GetBills),
#     path('bill/<int:id>/', views.GetBill, name='bill_url'),
#     path('operat/', views.GetOperat, name= 'operat'),
# ]

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.Index),
    path('bills/', views.Index),
    # path('bills/', views.GetBills),
    path('bills/<int:bill_id>/', views.bill),
    path('operat/<int:operat_id>/', views.operat),
]
