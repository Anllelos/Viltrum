from .forms import *
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now  # Correct import for 'now'
from users.models import PlayerStats
# Create your views here.

#------------------------------------------------------------------------ Crear torneo ------------------------------------------------------------------------#
@login_required
def create_tournament(request):
    active_user = request.user
    if active_user.groups.filter(name='Gamer').exists():
        if request.method == "POST":
            form = TournamentForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                today = timezone.now() - timedelta(hours=23)
                if start_date < today:
                    form.add_error('start_date', "La fecha de inicio no puede ser anterior al día de hoy")
                elif end_date < start_date:
                    form.add_error('end_date', "La fecha de fin no puede ser anterior a la de inicio")
                else:
                    tournament = form.save(commit=False)
                    tournament.owner = active_user
                    tournament.registration_deadline = timezone.now() + timedelta(hours=72)  # Set deadline
                    tournament.save()
                    return redirect('tournaments')
        else:
            form = TournamentForm()
        data_context = {'form':form}
        return render(request, 'create_tournament.html', data_context)
    return redirect("tournaments")


#------------------------------------------------------------------------ Mostrar torneos ------------------------------------------------------------------------#
def list_tournaments(request):
    tournaments = Tournament.objects.all()
    
    tournaments_list = []

    for tournament in tournaments:
        remaining_time = tournament.registration_deadline - timezone.now()
        
        if remaining_time > timedelta(0):
            days = remaining_time.days
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            inscription_time = f"Días: {days}, Horas: {hours}, Minutos: {minutes}"
            if not tournament.status:
                tournament.status = True
                tournament.save()
        else:
            inscription_time = "Registro cerrado"
            tournament.status = False
            tournament.save()
        
        tournaments_list.append({
            'tournament': tournament,
            'inscription_time': inscription_time,
        })

    return render(request, 'tournaments.html', {'tournaments_list': tournaments_list})

#------------------------------------------------------------------------ Ver detalles de torneo ------------------------------------------------------------------------#

def view_tournament(request, tournament_id):
    active_user = request.user.is_authenticated
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    tournament_inscriptions = TournamentInscription.objects.filter(tournament=tournament, status="P")
    tournament_members = TournamentInscription.objects.filter(tournament=tournament, status="A")
    user_inscription = TournamentInscription.objects.filter(tournament=tournament, user=active_user).first()
    
    n_members = tournament_members.count()
    is_full = tournament.max_members == n_members
    is_not_registered = user_inscription is None or user_inscription.status == "R"

    member_info = [
    {
        'member': member,
        'member_stats': PlayerStats.objects.filter(user=member.user, game=tournament.game, is_active=True).first() or False
    }
        for member in tournament_members
    ]

    data_context = {
        'tournament': tournament,
        'tournament_inscriptions': tournament_inscriptions,
        'member_info': member_info,
        'n_members':n_members,
        'is_not_registered':is_not_registered,
        'is_full':is_full
    }

    return render(request, 'tournament.html', data_context)

#------------------------------------------------------------------------ Manejo de inscripciones de torneo ------------------------------------------------------------------------#

@login_required
def tournament_inscription(request, tournament_id):
    active_user = request.user
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    
    existing_inscription = TournamentInscription.objects.filter(user=active_user, tournament=tournament).first()
    
    if existing_inscription:
        if existing_inscription.status == "R":
            existing_inscription.status = "P"  
            existing_inscription.save()
            return redirect('view_tournament', tournament_id=tournament_id)
        else:
            return redirect('tournaments') 

    if tournament.owner == active_user:
        return redirect('tournaments')

    if not tournament.status:
        return redirect('tournaments')

    inscription = TournamentInscription(user=active_user, tournament=tournament)
    inscription.save()
    

    return redirect('view_tournament', tournament_id=tournament_id)

@login_required
def accept_inscription(request, inscription_id, tournament_id, value):
    active_user = request.user
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    inscription = get_object_or_404(TournamentInscription, pk=inscription_id)
    
    if tournament.owner == active_user:
        if value == 1:
            inscription.status = "A"
            inscription.save()
        else:
            inscription.status = "R"
            inscription.save()
    
        return redirect('view_tournament', tournament_id=tournament_id)

def remove_member(request, inscription_id, tournament_id):
    active_user = request.user
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    inscription = get_object_or_404(TournamentInscription, pk=inscription_id)

    if tournament.owner == active_user:
        inscription.status = "R"
        inscription.save()

        return redirect('view_tournament', tournament_id=tournament_id)


#------------------------------------------------------------------------ Editar torneo ------------------------------------------------------------------------#
@login_required
def edit_tournament(request, tournament_id):
    active_user = request.user
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    members = TournamentInscription.objects.filter(tournament=tournament, status="A")

    # Inicializar el formulario con la instancia del torneo
    if request.method == "POST":
        form = TournamentEditForm(request.POST, instance=tournament)
    else:
        form = TournamentEditForm(instance=tournament)
        
    data_context = {'form': form}

    if tournament.owner == active_user:
        if request.method == "POST":
            if form.is_valid():
                max_members = form.cleaned_data.get('max_members')
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                active_members = members.count()
                today = timezone.now() - timedelta(hours=24)
                print(today)

                if max_members < active_members:
                    form.add_error('max_members', f"No puedes colocar un número menor de miembros a los que tienes actualmente activos: {active_members}")
                elif start_date < today:
                    form.add_error('start_date', "La fecha de inicio no puede ser anterior al día de hoy")
                elif end_date < start_date:
                    form.add_error('end_date', "La fecha de fin no puede ser anterior a la de inicio")
                else:
                    tournament_form = form.save(commit=False)
                    tournament_form.registration_deadline = timezone.now() + timedelta(hours=72)  # Set deadline
                    tournament_form.save()
                    return redirect('view_tournament', tournament_id=tournament_id)
            data_context = {'form': form, 'tournament':tournament}
    
        return render(request, 'tournament_edit.html', data_context)
    return redirect('tournaments')

def set_winner(request, inscription_id, tournament_id):
    active_user = request.user
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    inscription = get_object_or_404(TournamentInscription, pk=inscription_id)
    winner = inscription.user.username

    if tournament.owner == active_user:
        tournament.winner = winner
        tournament.save()

        return redirect('view_tournament', tournament_id=tournament_id)
    return (request) 
