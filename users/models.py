from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Modelo para información extra de usuarios (Jugadores Y Patrocinadores)
class ExtendedData(models.Model):
    TYPE_CHOICES = [
        ("E", "Elite"),
        ("S", "Sakura"),
        ("S+", "Sakura +"),
        ("V", "Viltrum"),
        ("V+", "Viltrum +")
    ]
    profile_img = models.ImageField(null=True, blank=True, upload_to="images/profileimg")  # Imagen de perfil
    profile_banner = models.ImageField(null=True, blank=True, upload_to="images/profilebanner")  # Banner de perfil
    user_description = models.TextField(null=True, blank=True)  # Descripción del usuario}
    viltrum_rank = models.CharField(max_length=3, choices=TYPE_CHOICES, default="E")
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
    is_active = models.BooleanField(default=True)  #Bandera en caso de ser eliminado

    class Meta:
        unique_together = ('user', 'game')  # Asegura que el usuario no pueda repetir el juego con el mismo tipo

# Modelo para agregar productos de patrocinador
class SponsorProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=254, null=True)
    product_description = models.CharField(max_length=512, null=True)
    product_image = models.ImageField(null=True, blank=True, upload_to="images/sponsorProducts")
    is_active = models.BooleanField(default=True)

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



class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"

class UserGalleryImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s image"
