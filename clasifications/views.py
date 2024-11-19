from django.shortcuts import render
from django.contrib.auth.models import Group
from users.models import PlayerStats  # Asegúrate de importar correctamente
from django.db.models import Q

def clasifications(request):
    group = Group.objects.get(name='Gamer')
    users = group.user_set.all()
    game_stats = {}

    # Obtener los valores de los filtros desde el request GET
    selected_games = request.GET.getlist('game')
    wins_filter = request.GET.get('wins_filter')
    losses_filter = request.GET.get('losses_filter')
    hours_filter = request.GET.get('hours_filter')

    # Obtener todos los juegos disponibles
    all_games = PlayerStats.objects.values_list('game', flat=True).distinct()

    # Construir la consulta base
    filters = Q()
    if selected_games:
        filters &= Q(game__in=selected_games)
    if wins_filter:
        try:
            filters &= Q(wins__gte=int(wins_filter))
        except ValueError:
            pass  # Manejar entrada no válida
    if losses_filter:
        try:
            filters &= Q(losses__lte=int(losses_filter))
        except ValueError:
            pass  # Manejar entrada no válida
    if hours_filter:
        try:
            filters &= Q(total_played__gte=int(hours_filter))  # Aquí agregamos el filtro de horas jugadas
        except ValueError:
            pass  # Manejar entrada no válida

    # Obtener los perfiles que coinciden con los filtros
    profiles = PlayerStats.objects.filter(filters)

    # Organizar los perfiles por juego
    for profile in profiles:
        game_name = profile.game
        if game_name not in game_stats:
            game_stats[game_name] = []
        game_stats[game_name].append({
            'user': profile.user,
            'profile': profile,
        })

    data_context = {
        'game_stats': game_stats,
        'selected_games': selected_games,
        'wins_filter': wins_filter,
        'losses_filter': losses_filter,
        'hours_filter': hours_filter,
        'all_games': all_games,
    }

    return render(request, 'clasifications/clasifications.html', data_context)
