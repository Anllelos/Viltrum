from django.shortcuts import render
from django.contrib.auth.models import Group
from django.db.models import Prefetch
from users.models import PlayerStats

# Lista de jugadores por juego con filtros
def clasifications(request):
    group = Group.objects.get(name='Gamer')
    users = group.user_set.all().select_related('extendeddata')
    
    # Filter parameters from GET request (to be used for filtering logic)
    selected_game = request.GET.getlist('game')
    selected_rank = request.GET.get('viltrum_rank')
    wins_filter = request.GET.get('wins_filter')
    losses_filter = request.GET.get('losses_filter')
    hours_filter = request.GET.get('hours_filter')

    game_stats = {}

    # Iterating over users to gather statistics
    for user in users:
        profiles = PlayerStats.objects.filter(user=user, is_active=True)
        extended_data = user.extendeddata
        viltrum_rank = extended_data.get_viltrum_rank_display() if extended_data else None
        
        # Iterating over profiles to group by game
        for profile in profiles:
            game_name = profile.game
            if game_name not in game_stats:
                game_stats[game_name] = []  # Create a list if it doesn't exist
            game_stats[game_name].append({
                'user': user,
                'profile': profile,
                'viltrum_rank': viltrum_rank
            })
    
    data_context = {
        'game_stats': game_stats,
        'selected_game': selected_game,
        'selected_rank': selected_rank,
        'wins_filter': wins_filter,
        'losses_filter': losses_filter,
        'hours_filter': hours_filter,
    }
    
    return render(request, 'clasifications.html', data_context)

