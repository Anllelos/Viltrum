from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='games/')
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.name
