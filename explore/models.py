from django.db import models
from taggit.managers import TaggableManager  # Importamos el administrador de tags

class Game(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='games/')
    description = models.TextField()
    is_live = models.BooleanField(default=False)
    tags = TaggableManager()  # Añadimos los tags

    def __str__(self):
        return self.name
