from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('register/', views.create_user, name='register'),  
    path('profile/', views.profile_redirect, name='redirect_profile'),  
    path('profile/user/<str:username>', views.profile_user, name='profile'),  
    path('profile/sponsor/<str:username>', views.profile_sponsor, name='profile_sponsor'),  
    path('profile/user/<str:username>/edit', views.edit_profile_user, name='edit_profile_user'),  
    path('profile/sponsor/<str:username>/edit', views.edit_profile_sponsor, name='edit_profile_sponsor'),  
    path('subir_stream/', views.subir_stream, name='subir_stream'),  
    path('subir_torneo/', views.subir_torneo, name='subir_torneo'),  
    path('subir_clasificacion/', views.subir_clasificacion, name='subir_clasificacion'),  
    path('subir_juego/', views.subir_juego, name='subir_juego'),  
    path('user_logout/', views.user_logout, name='user_logout'),  
    path('profile/games_stats/', views.games_stats, name='games_stats'),  
    path('profile/products/', views.sponsor_products, name='sponsor_products'),  
    path('tournaments/', views.list_tournaments, name='tournaments'),
    path('tournaments/create/', views.create_tournament, name='crear_torneo'),  
    path('tournaments/join/<int:tournament_id>/', views.join_tournament, name='join_tournament'),  
    path('notifications/', views.manage_notifications, name='notifications'),  
    path('notifications/handle/<int:notification_id>/<str:action>/', views.handle_notification, name='handle_notification'),  
]
