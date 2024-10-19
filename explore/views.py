from django.shortcuts import render, redirect
from .models import Game
from .forms import GameForm

def explore(request):
    games = Game.objects.all()  # Asegúrate de que esto esté trayendo los juegos
    return render(request, 'explore/explore.html', {'games': games})

def upload_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('explore')  # Redirige a la página de explorar después de guardar
    else:
        form = GameForm()
    
    return render(request, 'explore/upload_game.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Game

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'explore/game_detail.html', {'game': game})
