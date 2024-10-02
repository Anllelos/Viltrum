from django.shortcuts import render
from django.contrib.auth.models import Group
from users.models import PlayerStats

# List of players by game with filtering options
def clasifications(request):
    group = Group.objects.get(name='Gamer')
    users = group.user_set.all().select_related('extendeddata')
    game_stats = {}
    
    # Get the filter values from the request (GET)
    selected_game = request.GET.getlist('game')
    selected_rank = request.GET.get('viltrum_rank')
    wins_filter = request.GET.get('wins_filter')
    losses_filter = request.GET.get('losses_filter')
    hours_filter = request.GET.get('hours_filter')

    # Iterate over each user and their game profiles
    for user in users:
        profiles = PlayerStats.objects.filter(user=user, is_active=True)
        extended_data = user.extendeddata
        viltrum_rank = extended_data.get_viltrum_rank_display() if extended_data else None
        
        # Apply filtering logic based on the selected filters
        for profile in profiles:
            game_name = profile.game  # Name of the game

            # Filter by selected game
            if selected_game and game_name not in selected_game:
                continue

            # Filter by Viltrum rank
            if selected_rank and selected_rank != viltrum_rank:
                continue

            # Filter by number of wins and losses
            if wins_filter and int(profile.wins) < int(wins_filter):
                continue
            if losses_filter and int(profile.losses) > int(losses_filter):
                continue

            # Filter by hours played
            if hours_filter and int(profile.total_played) < int(hours_filter):
                continue

            # Add to game stats if it passes the filters
            if game_name not in game_stats:
                game_stats[game_name] = []
            game_stats[game_name].append({
                'user': user,
                'profile': profile,
                'viltrum_rank': viltrum_rank
            })

    # Pass the filter values back to the template for display
    data_context = {
        'game_stats': game_stats,
        'selected_game': selected_game,
        'selected_rank': selected_rank,
        'wins_filter': wins_filter,
        'losses_filter': losses_filter,
        'hours_filter': hours_filter
    }
    
    return render(request, 'clasifications.html', data_context)
