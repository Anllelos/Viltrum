from django.urls import path
from . import views

app_name = 'shop'  # Agrega esto para el namespace

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]

