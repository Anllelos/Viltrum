"""
URL configuration for first_parcial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # Ruta para la vista home
    path('register/', views.create_user, name='register'),  # Ruta para la página de registro
    path('profile/', views.profile, name='profile'),  # Ruta para la página de perfil
    path('subir_stream/', views.subir_stream, name='subir_stream'),  # Ruta para subir stream
    path('subir_torneo/', views.subir_torneo, name='subir_torneo'),  # Ruta para subir torneo
    path('subir_clasificacion/', views.subir_clasificacion, name='subir_clasificacion'),  # Ruta para subir clasificación
    path('subir_juego/', views.subir_juego, name='subir_juego'),  # Ruta para subir juego
    path('user_logout/', views.user_logout, name='user_logout'),  # Ruta para cerrar sesión
]
