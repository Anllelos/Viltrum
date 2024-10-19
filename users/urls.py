from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_user, name='register'),  
    path('profile/', views.profile_redirect, name='redirect_profile'),  
    path('profile/user/<str:username>', views.profile_user, name='profile'),  
    path('profile/sponsor/<str:username>', views.profile_sponsor, name='profile_sponsor'),
    path('profile/edit', views.profile_redirect_edit, name='redirect_profile_edit'),  
    path('profile/user/<str:username>/edit', views.edit_profile_user, name='edit_profile_user'),  
    path('profile/sponsor/<str:username>/edit', views.edit_profile_sponsor, name='edit_profile_sponsor'),
    path('subir_stream/', views.subir_stream, name='subir_stream'),  
    path('subir_juego/', views.subir_juego, name='subir_juego'),  
    path('user_logout/', views.user_logout, name='user_logout'),
    path('profile/games_stats/', views.games_stats, name='games_stats'),  
    path('profile/products/', views.sponsor_products, name='sponsor_products'),  
    path('profile/games_stats/edit/<int:game_id>', views.update_game_stats, name='edit_game_stat'),
    path('profile/game_stats/delete/<int:game_id>', views.delete_game_stats, name='delete_game_stats'),
    path('profile/product/edit/<int:product_id>', views.update_product, name='edit_product'),
    path('profile/product/delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('verification/<str:username>', views.verification, name='verification'),
    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('upload-image/', views.upload_image, name='upload_image'),
]
