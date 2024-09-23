from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone
from datetime import timedelta

# Modelo para información extra de usuarios (Jugadores Y Patrocinadores)
class ExtendedData(models.Model):
    profile_img = models.ImageField(null=True, blank=True, upload_to="images/profileimg")  # Imagen de perfil
    profile_banner = models.ImageField(null=True, blank=True, upload_to="images/profilebanner")  # Banner de perfil
    user_description = models.TextField(null=True, blank=True)  # Descripción del usuario
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)  # Relación uno a uno con el usuario
    
    # Campos obligatorios en la creación
    country = CountryField(blank_label='Selecciona tu país', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

# Modelo para agregar estadísticas de jugadores
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


class Tournament(models.Model):
    GAME_CHOICES = [
        ('game1', 'Game 1'),
        ('game2', 'Game 2'),
        ('game3', 'Game 3'),
    ]
    name = models.CharField(max_length=255)
    game = models.CharField(max_length=255, choices=GAME_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    registration_deadline = models.DateTimeField(default=timezone.now() + timedelta(hours=72))  # Default to 72 hours after creation
    start_date = models.DateField(null=True, blank=True)  # Start date of the tournament
    end_date = models.DateField(null=True, blank=True)  # End date of the tournament
    status = models.CharField(max_length=20, default="open")  # Default status is "open"
    max_members = models.IntegerField(default=20)  # Define max members
    banner = models.ImageField(upload_to='tournament_banners/', null=True, blank=True)  # Optional tournament banner
    members = models.ManyToManyField(User, related_name='tournaments', blank=True)

    def is_full(self):
        """Check if the tournament has reached the maximum number of members."""
        return self.members.count() >= self.max_members

    def has_registration_time_passed(self):
        """Check if the registration period (72 hours) has passed."""
        return timezone.now() > self.registration_deadline

    def is_older_than_a_month(self):
        """Check if the tournament is older than one month."""
        return timezone.now() > self.created_at + timedelta(days=30)

    def update_status(self):
        """Update the status of the tournament based on conditions."""
        if self.is_full() or self.has_registration_time_passed() or self.is_older_than_a_month():
            self.status = 'closed'
        else:
            self.status = 'open'
        self.save()

    def time_left_to_register(self):
        """Get the time left to register."""
        remaining_time = self.registration_deadline - timezone.now()
        if remaining_time.total_seconds() > 0:
            return remaining_time
        return timedelta(0)  # No time left

    def __str__(self):
        return self.name


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

# Modelo de notificaciones
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_notifications")
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.sender} to {self.recipient}"

