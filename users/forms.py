from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import models
from django.utils.translation import gettext_lazy as _
from .models import GameImage
from django_countries.fields import CountryField
from django.contrib.auth.models import Group
from django import forms
from .models import Tournament

# Formulario para crear usuario jugador "Gamer"
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'last_name', 'password1', 'password2']
    #Deifinir rol de usuario
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            player_group, created = Group.objects.get_or_create(name='Gamer')
            user.groups.add(player_group)
        
        return user
    
# Formulario para crear usuario sponsor "sponsor"
class CreateSponsorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    #Definir rol de sponsor
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            sponsor_group, created = Group.objects.get_or_create(name='Sponsor')
            user.groups.add(sponsor_group)
        
        return user

#ExtendedData User
class UserExtendedDataForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = models.ExtendedData
        fields = ['country', 'birthdate']

#ExtendedData Sponsor
class SponsorExtendedDataForm(forms.ModelForm):
    class Meta:
        model = models.ExtendedData
        fields = ['country']

# Formulario para crear usuario
class AuthenticationFormUser(AuthenticationForm):
    def get_invalid_login_error(self):
        return self.error_class([_("Invalid login")])

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code='inactive',
            )

# Form to create stream
class StreamForm(forms.ModelForm):
    class Meta:
        model = models.Stream
        fields = ['titulo', 'descripcion', 'enlace', 'imagen']


# Form to create Clasification
class ClasificacionForm(forms.ModelForm):
    class Meta:
        model = models.Clasificacion
        fields = ['nombre', 'descripcion', 'imagen']

# Form to create Games
class JuegoForm(forms.ModelForm):
    class Meta:
        model = models.Videojuego
        fields = ['nombre', 'portada']

# Form to add game profile
class PlayerStatsForm(forms.ModelForm):
    class Meta:
        model = models.PlayerStats
        fields = ['user_game', 'game', 'rank', 'wins', 'losses', 'total_played'] 

#Formulario para agregar productos del patrocinador
class SponsorProductsForm(forms.ModelForm):
    class Meta:
        model = models.SponsorProducts
        fields = ['product_name', 'product_description', 'product_image']

# Form to upload images for a game
class GameImageForm(forms.ModelForm):
    class Meta:
        model = GameImage
        fields = ['image']
        
# Formulario para editar información del usuario
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

#Formulario para editar información adicional del usuario
class EditExtendedDataUserForm(forms.ModelForm):
    class Meta:
        model = models.ExtendedData
        fields = ['user_description', 'country', 'birthdate']

#Formulario para subir la imagen de perfil
class ProfilePicForm(forms.ModelForm): 
    class Meta:
        model = models.ExtendedData
        fields = ['profile_img']

#Formulario para subir el banner de perfil
class BannerPicForm(forms.ModelForm):
    class Meta:
        model = models.ExtendedData
        fields = ['profile_banner']


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'game', 'start_date', 'end_date', 'max_members', 'banner']  # Include relevant fields only
        widgets = {
            'game': forms.Select(choices=Tournament.GAME_CHOICES)  # Dropdown for games
        }
