from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NotificationSystem(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_receiver")
    message = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
