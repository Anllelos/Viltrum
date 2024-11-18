from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.contrib.auth.models import Group
from django import forms
from .models import Message
from .models import UserGalleryImage


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
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya hay un usuario registrado con ese nombre")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya hay un usuario registrado con ese correo")
        return email
    
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
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya hay un patrocinador registrado con ese nombre")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya hay un patrocinador registrado con ese correo")
        return email

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

# Form to create stream
class StreamForm(forms.ModelForm):
    class Meta:
        model = models.Stream
        fields = ['titulo', 'descripcion', 'enlace', 'imagen']

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
        fields = ['product_name', 'product_description', 'product_image', 'price']

        
# Formulario para editar información del usuario
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
class EditSponsorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

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

class EditGameStat(forms.ModelForm):
    class Meta:
        model = models.PlayerStats
        fields = ['user_game', 'rank', 'wins', 'losses', 'total_played'] 

class EditProduct(forms.ModelForm):
    class Meta:
        model = models.SponsorProducts
        fields = ['product_name', 'product_description', 'product_image', 'price'] 



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write your message here...'}),
        }

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserGalleryImage
        fields = ['image']

class VerificationForm(forms.ModelForm):
    class Meta:
        model = models.ExtendedData
        fields = ['user_identification', 'user_photo']