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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la vista home
    path('register/', views.create_user, name='register'),  # Ruta para la página de registro
    path('profile/', views.profile_redirect, name='redirect_profile'),                                           #|  Verificación del tipo de usuario    v------------------
    path('profile/user/<str:username>', views.profile_user, name='profile'),                                     #|  Perfil para usuarios jugadores      v------------------
    path('profile/sponsor/<str:username>', views.profile_sponsor, name='profile_sponsor'),                       #|  Perfil para patrocinadores          v------------------
    path('profile/user/<str:username>/edit', views.edit_profile_user, name='edit_profile_user'),                 #|  Editar perfil usuario               v------------------
    path('profile/sponsor/<str:username>/edit', views.edit_profile_sponsor, name='edit_profile_sponsor'),        #|  Editar perfil sponsor               v------------------
    path('subir_stream/', views.subir_stream, name='subir_stream'),  # Ruta para subir stream
    path('subir_torneo/', views.subir_torneo, name='subir_torneo'),  # Ruta para subir torneo
    path('subir_clasificacion/', views.subir_clasificacion, name='subir_clasificacion'),  # Ruta para subir clasificación
    path('subir_juego/', views.subir_juego, name='subir_juego'),  # Ruta para subir juego
    path('user_logout/', views.user_logout, name='user_logout'),  # Ruta para cerrar sesión
    path('profile/games_stats/', views.games_stats, name='games_stats'),                                         #| Guardar estadisticas de juegos   ]
    path('profile/products/', views.sponsor_products, name='sponsor_products'),                                  #| Guardar productos                ]

    
    path('tournaments/', views.list_tournaments, name='tournaments'),  
    path('tournaments/create/', views.create_tournament, name='create_tournament'),  
    path('tournaments/join/<int:tournament_id>/', views.join_tournament, name='join_tournament'), 
    path('notifications/', views.manage_notifications, name='notifications'),  
    path('notifications/handle/<int:notification_id>/<str:action>/', views.handle_notification, name='handle_notification'),  
]
