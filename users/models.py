from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Modelo para información extra de usuarios (Jugadores Y Patrocinadores)
class ExtendedData(models.Model):
    profile_img = models.ImageField(null=True, blank=True, upload_to="images/profileimg")  # Imagen de perfil
    profile_banner = models.ImageField(null=True, blank=True, upload_to="images/profilebanner")  # Banner de perfil
    user_description = models.TextField(null=True, blank=True)  # Descripción del usuario
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)  # Relación uno a uno con el usuario
    
    # Campos obligatorios en la creación
    country = CountryField(blank_label='Selecciona tu país', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)

# Modelo para agregar estadísticas de juego
# Modelo para estadísticas de jugadores
class PlayerStats(models.Model):
    # Definición de las opciones de juegos disponibles
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    user_game = models.CharField(max_length=50)  # Nombre del juego jugado por el usuario
    game = models.CharField(max_length=5, choices=TYPE_CHOICES)  # Juego, limitado a las opciones disponibles
    rank = models.CharField(max_length=50)  # Rango del jugador
    wins = models.IntegerField(default=0)  # Número de victorias
    losses = models.IntegerField(default=0)  # Número de derrotas
    total_played = models.IntegerField(default=0)  # Total de juegos jugados

    class Meta:
        unique_together = ('user', 'game')  # Asegura que el usuario no pueda repetir el juego con el mismo tipo

# Modelo para agregar productos de patrocinador
class SponsorProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=254, null=True)
    product_description = models.CharField(max_length=512, null=True)
    product_image = models.ImageField(null=True, blank=True, upload_to="images/sponsorProducts")


# Modelo para videojuegos
class Videojuego(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del videojuego
    portada = models.ImageField(upload_to='portadas/')  # Portada del videojuego

    def __str__(self):
        return self.nombre  # Método para devolver el nombre del juego como string

# Modelo para streams
class Stream(models.Model):
    titulo = models.CharField(max_length=100)  # Título del stream
    descripcion = models.TextField()  # Descripción del stream
    enlace = models.URLField()  # Enlace al stream
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    imagen = models.ImageField(upload_to='streams/')  # Imagen asociada al stream

    def __str__(self):
        return self.titulo  # Devuelve el título del stream

# Modelo para torneos
class Torneo(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del torneo
    descripcion = models.TextField()  # Descripción del torneo
    fecha_inicio = models.DateField()  # Fecha de inicio del torneo
    fecha_fin = models.DateField()  # Fecha de finalización del torneo
    imagen = models.ImageField(upload_to='torneos/')  # Imagen asociada al torneo

    def __str__(self):
        return self.nombre  # Devuelve el nombre del torneo

# Modelo para clasificaciones
class Clasificacion(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre de la clasificación
    descripcion = models.TextField()  # Descripción de la clasificación
    imagen = models.ImageField(upload_to='clasificaciones/')  # Imagen de la clasificación

    def __str__(self):
        return self.nombre  # Devuelve el nombre de la clasificación

# Definimos el modelo para cada juego
class Game(models.Model):
    name = models.CharField(max_length=100)  # Nombre del juego
    description = models.TextField()  # Descripción del juego
    cover_image = models.ImageField(upload_to='games/covers/', null=True, blank=True)  # Imagen de portada

    def __str__(self):
        return self.name  # Devuelve el nombre del juego

# Modelo para almacenar imágenes subidas por los usuarios asociadas a un juego
class GameImage(models.Model):
    game = models.ForeignKey(Game, related_name='images', on_delete=models.CASCADE)  # Relación con el juego
    image = models.ImageField(upload_to='games/images/')  # Imagen subida por el usuario
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que sube la imagen
    upload_date = models.DateTimeField(auto_now_add=True)  # Fecha de subida automática

    def __str__(self):
        return f"Image of {self.game.name} by {self.uploaded_by.username}"  # Muestra el juego y quién subió la imagen

# Modelo para crear torneos asociados a un juego
class Tournament(models.Model):
    game = models.ForeignKey(Game, related_name='tournaments', on_delete=models.CASCADE)  # Relación con el juego
    name = models.CharField(max_length=100)  # Nombre del torneo
    description = models.TextField()  # Descripción del torneo
    start_date = models.DateTimeField()  # Fecha de inicio del torneo
    end_date = models.DateTimeField()  # Fecha de fin del torneo

    def __str__(self):
        return f"Tournament {self.name} for {self.game.name}"  # Devuelve el nombre del torneo y el juego asociado
