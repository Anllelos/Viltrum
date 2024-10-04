from django.shortcuts import render
from .models import Game

def explore_home(request):
    games = Game.objects.all()

    # Filtering logic
    category = request.GET.get('category')
    sort_by = request.GET.get('sort_by')

    if category:
        games = games.filter(category=category)

    # Sorting logic (e.g., by popularity or release date)
    if sort_by == 'popularity':
        games = games.order_by('-popularity')
    elif sort_by == 'release_date':
        games = games.order_by('-release_date')

    context = {
        'games': games,
        'selected_category': category,
        'sort_by': sort_by,
    }
    return render(request, 'explore.html', context)
