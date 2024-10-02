from django.shortcuts import render
from django.contrib.auth.models import Group
from django.db.models import Prefetch
from users.models import *

# Create your views here.

#Lista de jugadores por juego
def clasifications(request):
    group = Group.objects.get(name='Gamer')
    users = group.user_set.all().select_related('extendeddata')
    game_stats = {}

    for user in users:
        profiles = PlayerStats.objects.filter(user=user, is_active=True) 
        extended_data = user.extendeddata
        viltrum_rank = extended_data.get_viltrum_rank_display() if extended_data else None
        
        # Iterar sobre los perfiles para agrupar por juego
        for profile in profiles:
            game_name = profile.game  # Obtener el nombre del juego
            if game_name not in game_stats:
                game_stats[game_name] = []  # Crear una lista si no existe
            game_stats[game_name].append({
                'user': user,
                'profile': profile,
                'viltrum_rank': viltrum_rank
            })
    
    data_context = {'game_stats': game_stats}
    return render(request, 'clasifications.html', data_context)