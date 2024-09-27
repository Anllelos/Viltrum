import os
import glob
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.files.base import ContentFile
import base64
from django.http import Http404
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now  # Correct import for 'now'
# Create your views here.
# Corrected create_tournament function
@login_required
def create_tournament(request):
    active_user = request.user
    data_context = {'gamer':False}
    if active_user.groups.filter(name='Gamer').exists():
        data_context = {'gamer':True}
    if request.method == "POST":
        form = TournamentForm(request.POST, request.FILES)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.registration_deadline = timezone.now() + timedelta(hours=72)  # Set deadline
            tournament.save()
            return redirect('tournaments')
        else:
            print(form.errors)
    else:
        form = TournamentForm()

    return render(request, 'create_tournament.html', {'form': form})


# Corrected list_tournaments function
def list_tournaments(request):
    tournaments = Tournament.objects.all()

    # Update the status of all tournaments before rendering the page
    for tournament in tournaments:
        if tournament.registration_deadline:
            remaining_time = tournament.registration_deadline - now()
            if remaining_time > timedelta(0):
                days = remaining_time.days
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                tournament.time_left_to_register = f"{days} días, {hours} horas, {minutes} minutos"
            else:
                tournament.time_left_to_register = "Registro cerrado"
        else:
            tournament.time_left_to_register = "No hay fecha límite"

    return render(request, 'tournaments.html', {'tournaments': tournaments})

@login_required
def join_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    notification = Notification.objects.create(
        sender=request.user,
        recipient=tournament.created_by,
        tournament=tournament,
        message=f"{request.user.username} wants to join the tournament {tournament.name}",
    )
    return redirect('tournaments')

@login_required
def manage_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def handle_notification(request, notification_id, action):
    notification = get_object_or_404(Notification, id=notification_id)
    if action == 'accept':
        notification.tournament.participants.add(notification.sender)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

@login_required
def subir_clasificacion(request):
    if request.method == 'POST':
        form = ClasificacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClasificacionForm()
    return render(request, 'subir_clasificacion.html', {'form': form})