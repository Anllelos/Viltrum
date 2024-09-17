from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import models
from django.utils.translation import gettext_lazy as _

#Form to create an User
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'last_name', 'password1', 'password2']

#Form to authenticate User
class AuthenticationFormUser(AuthenticationForm):
    def get_invalid_login_error(self):
        return self.error_class([_("XXXXXXXX")])

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("XXXXXXX"),
                code='inactive',
            )

#Form to update the profile pic
class ProfilePicForm(forms.ModelForm): 
    class Meta:
        model = models.ExtendedData
        fields = ['profile_img']
    def __init__(self, *args, **kwargs):
        super(ProfilePicForm, self).__init__(*args, **kwargs)
        self.fields['profile_img'].label = 'Imagen de Perfil'

#Form to create stream
class StreamForm(forms.ModelForm):
    class Meta:
        model = models.Stream
        fields = ['titulo', 'descripcion', 'enlace', 'imagen']

#Form to create tournament
class TorneoForm(forms.ModelForm):
    class Meta:
        model = models.Torneo
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'imagen']

#Form to create Clasification
class ClasificacionForm(forms.ModelForm):
    class Meta:
        model = models.Clasificacion
        fields = ['nombre', 'descripcion', 'imagen']

#Form to create Games
class JuegoForm(forms.ModelForm):
    class Meta:
        model = models.Videojuego
        fields = ['nombre', 'portada']

#Form to add game profile
class PlayerStatsForm(forms.ModelForm):
    class Meta:
        model = models.PlayerStats
        fields = ['user_game', 'game', 'rank', 'wins', 'losses', 'total_played'] 

#Edit User Info Form
class EditUserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = []

class EditExtendedDataForm(forms.ModelForm):
    class Meta:
        model = models.ExtendedData
        fields = []