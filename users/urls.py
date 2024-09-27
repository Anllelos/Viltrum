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
    path('subir_juego/', views.subir_juego, name='subir_juego'),  
    path('user_logout/', views.user_logout, name='user_logout'),  
    path('profile/games_stats/', views.games_stats, name='games_stats'),  
    path('profile/products/', views.sponsor_products, name='sponsor_products'),  
]
