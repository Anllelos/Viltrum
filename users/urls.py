from django.urls import path
from . import views

urlpatterns = [
    #Registro
    path('register/', views.create_user, name='register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    #Perfil Jugador - Patrocinador
    path('profile/', views.profile_redirect, name='redirect_profile'),
    path('profile/edit', views.profile_redirect_edit, name='redirect_profile_edit'),
    #Jugador
    path('profile/user/<str:username>/edit', views.edit_profile_user, name='edit_profile_user'),  
    path('profile/user/<str:username>', views.profile_user, name='profile'),
    #Patrocinador  
    path('profile/sponsor/<str:username>', views.profile_sponsor, name='profile_sponsor'),
    path('profile/sponsor/<str:username>/edit', views.edit_profile_sponsor, name='edit_profile_sponsor'),
    #Estadísticas
    path('profile/games_stats/', views.games_stats, name='games_stats'),
    path('profile/add_games_stats/', views.add_games_stats, name='add_games_stats'),
    path('profile/games_stats/edit/<int:game_id>', views.update_game_stats, name='edit_game_stat'),
    path('profile/game_stats/delete/<int:game_id>', views.delete_game_stats, name='delete_game_stats'),
    #Productos  
    path('profile/products/', views.sponsor_products, name='sponsor_products'),  
    path('profile/product/edit/<int:product_id>', views.update_product, name='edit_product'),
    path('profile/product/delete/<int:product_id>', views.delete_product, name='delete_product'),
    #Verificación
    path('verification/<str:username>', views.verification, name='verification'),
    #Aceptar patrocinadores
    path('my-sponsors/', views.sponsorship, name='my-sponsors'),
    path('my-sponsors/accept/<str:sponsorship>/<int:value>', views.accept_sponsorship, name='accept_sponsoship'),
]
