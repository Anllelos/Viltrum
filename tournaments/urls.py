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
    path('tournaments/', views.list_tournaments, name='tournaments'),
    path('tournaments/create/', views.create_tournament, name='crear_torneo'),
    path('tournament/view/<int:tournament_id>', views.view_tournament, name='view_tournament'),
    path('tournament/inscription/<int:tournament_id>', views.tournament_inscription, name='tournament_inscription'),
    path('tournament/inscription/status/<int:inscription_id>/<int:tournament_id>/<int:value>/', views.accept_inscription, name='accept_inscription'),
    path('tournament/inscription/remove/<int:inscription_id>/<int:tournament_id>/',  views.remove_member, name='remove_member'),
    path('tournament/edit/<int:tournament_id>', views.edit_tournament, name='edit_tournament')
]