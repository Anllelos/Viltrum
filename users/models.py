from django.db import models
from django.contrib.auth.models import User

# Model for extra information for the user
class ExtendedData(models.Model):
    profile_img = models.ImageField(null=True, blank=True, upload_to="images/profileimg")
    profile_banner = models.ImageField(null=True, blank=True, upload_to="images/profilebanner")
    user_description = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)


# Nuevos modelos
class Videojuego(models.Model):
    nombre = models.CharField(max_length=100)
    portada = models.ImageField(upload_to='portadas/')

    def __str__(self):
        return self.nombre

class Stream(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    enlace = models.URLField()
    fecha = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='streams/')

    def __str__(self):
        return self.titulo

class Torneo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    imagen = models.ImageField(upload_to='torneos/')

    def __str__(self):
        return self.nombre

class Clasificacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='clasificaciones/')

    def __str__(self):
        return self.nombre

#Model to add game stadistics to the user
class PlayerStats(models.Model):
    TYPE_CHOICES = [
    ("LoL", "League of Legends"),
    ("D2", "Dota 2"),
    ("CSGO", "Counter-Strike: Global Offensive"),
    ("VAL", "Valorant"),
    ("OW", "Overwatch"),
    ("PUBG", "PlayerUnknown's Battlegrounds"),
    ("FORT", "Fortnite"),
    ("Apex", "Apex Legends"),
    ("R6", "Rainbow Six Siege"),
    ("RL", "Rocket League")
    ]   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_game = models.CharField(max_length=50)
    game = models.CharField(max_length=5, choices=TYPE_CHOICES)
    rank = models.CharField(max_length=50)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    total_played = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'game')