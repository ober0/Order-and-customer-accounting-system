"""
URL configuration for OrderAndCustomerAccountingSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('clients/add/', views.add_client),
    path('clients/get/<int:id>/', views.get_client),
    path('clients/get/', views.get_all_clients),
    path('clients/edit/<int:id>/', views.edit_client),
    path('clients/delete/<int:id>/', views.delete_client),
    path('orders/add/', views.add_order),
    path('orders/get/<int:id>/', views.get_order),
    path('orders/get/', views.get_all_orders),
    path('orders/edit/<int:id>/', views.add_orders),
    path('orders/delete/<int:id>/', views.delete_orders),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
