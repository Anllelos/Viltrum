from django.urls import path
from . import views

urlpatterns = [
    path('explore/', views.explore, name='explore'),
    path('upload/', views.upload_game, name='upload_game'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),  # Ruta para los detalles del juego
]
