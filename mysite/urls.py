"""
URL configuration for mysite project.

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
from django.urls import path,include
from django.contrib import admin
from app.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Набор методов для услуг
    path('api/bills/search/', search_bills),  # GET
    path('api/bills/<int:bill_id>/', get_bill_by_id),  # GET
    # path('api/bills/<int:bill_id>/image/', get_bill_image),  # GET
    path('api/bills/<int:bill_id>/update/', update_bill),  # PUT
    path('api/bills/<int:bill_id>/update_image/', update_bill_image),  # PUT
    path('api/bills/<int:bill_id>/delete/', delete_bill),  # DELETE
    path('api/bills/create/', create_bill),  # POST
    path('api/bills/<int:bill_id>/add_to_operat/', add_bill_to_operat),  # POST

    # Набор методов для заявок
    path('api/operats/search/', search_operats),  # GET
    path('api/operats/<int:operat_id>/', get_operat_by_id),  # GET
    path('api/operats/<int:operat_id>/update/', update_operat),  # PUT
    path('api/operats/<int:operat_id>/update_status_user/', update_status_user),  # PUT
    path('api/operats/<int:operat_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/operats/<int:operat_id>/delete/', delete_operat),  # DELETE

    # Набор методов для м-м
    path('api/operats/<int:operat_id>/update_bill/<int:bill_id>/', update_bill_in_operat),  # PUT
    path('api/operats/<int:operat_id>/delete_bill/<int:bill_id>/', delete_bill_from_operat),  # DELETE

    # Набор методов пользователей
    path('api/users/register/', register), # POST
    path('api/users/<int:user_id>/update/', update_user), # PUT
    path("api/users/logout/", logout),  # POST 
    path("api/users/login/", login),  # POST 

    #Доп
    path('api/bills/<int:bill_id>/restore/', restore_bill), # POST 
]