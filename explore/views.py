from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Game
from .forms import GameForm

def explore(request):
    query = request.GET.get('q', '')
    games = Game.objects.filter(
        Q(name__icontains=query) | Q(tags__name__icontains=query)
    ).distinct() if query else Game.objects.all()
    return render(request, 'explore/explore.html', {'games': games, 'query': query})

def upload_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('explore')
    else:
        form = GameForm()
    return render(request, 'explore/upload_game.html', {'form': form})

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'explore/game_detail.html', {'game': game})
