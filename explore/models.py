from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)  # Ensure to store categories like Action, Shooter, etc.
    popularity = models.IntegerField()  # For sorting by popularity
    release_date = models.DateField()  # For sorting by release date
    cover_image = models.ImageField(upload_to='game_covers/')  # For displaying game covers
