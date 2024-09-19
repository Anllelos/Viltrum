from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    groups = ['Gamer', 'Sponsor']
    
    for group in groups:
        Group.objects.get_or_create(name=group)