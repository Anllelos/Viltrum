from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

# Create your models here.
class Tournament(models.Model):
    GAME_CHOICES = [
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    name = models.CharField(max_length=255)
    game = models.CharField(max_length=255, choices=GAME_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    registration_deadline = models.DateTimeField(default=timezone.now() + timedelta(hours=72))  # Default to 72 hours after creation
    start_date = models.DateTimeField(null=True, blank=True)  # Start date of the tournament
    end_date = models.DateTimeField(null=True, blank=True)  # End date of the tournament
    status = models.BooleanField(max_length=20, default=True)  # Default status is "True"
    max_members = models.IntegerField(default=10)  # Define max members
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

#Modelo de inscripción a torneo

class TournamentInscription(models.Model):
    TYPE_CHOICES = [
        ("A", "Approved"),
        ("P", "Pending"),
        ("R", "Rejected")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    inscription_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=TYPE_CHOICES, db_index=True, default="P")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'tournament'], name='unique_user_tournament')
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.tournament.name} ({self.get_status_display()})"

    
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
    


