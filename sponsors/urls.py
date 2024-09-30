"""
URL configuration for Viltrum project.

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

#test
from django.contrib import admin
from django.urls import path, re_path, include
#Static Files config
from django.conf import settings
from django.conf.urls.static import static
#Reset password config
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('sponsors/', views.sponsors, name='sponsors')
    #path('clasifications/', views.clasifications, name='clasifications')
    #path('tournaments/', views.list_tournaments, name='tournaments'),
    #path('tournaments/create/', views.create_tournament, name='crear_torneo'),  
    #path('tournaments/join/<int:tournament_id>/', views.join_tournament, name='join_tournament'),  
]