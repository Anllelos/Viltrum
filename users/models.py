from django.db import models
from django.contrib.auth.models import User

# Model for extra information for the user
class ExtendedData(models.Model):
    profile_img = models.ImageField(null=True, blank=True, upload_to="images/")
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
