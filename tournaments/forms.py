from django import forms
from . import models
from django.utils.translation import gettext_lazy as _
from django import forms
from . models import *

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'start_date', 'end_date', 'max_members'] 

class TournamentInscriptionForm(forms.ModelForm):
    class Meta:
        model = TournamentInscription
        fields = ['user', 'tournament']

class TournamentEditForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'start_date', 'end_date', 'max_members'] 