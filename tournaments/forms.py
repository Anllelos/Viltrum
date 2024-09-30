from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import models
from django.utils.translation import gettext_lazy as _
from .models import GameImage
from django_countries.fields import CountryField
from django.contrib.auth.models import Group
from django import forms
from . models import Clasificacion, Tournament
# Form to upload images for a game
class GameImageForm(forms.ModelForm):
    class Meta:
        model = GameImage
        fields = ['image']

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'start_date', 'end_date', 'max_members', 'banner']  # Include relevant fields only
        widgets = {
            'game': forms.Select(choices=Tournament.GAME_CHOICES)  # Dropdown for games
        }