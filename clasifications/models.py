from django.db import models
from django.contrib.auth.models import User

class PlayerStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clasifications_playerstats')
    game = models.CharField(max_length=100)
    wins = models.IntegerField()
    losses = models.IntegerField()
    total_played = models.IntegerField()  # Hours played
    user_game = models.CharField(max_length=100)  # Game-specific username

    def __str__(self):
        return f"{self.user.username} - {self.game}"
