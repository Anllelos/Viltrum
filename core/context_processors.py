from django.contrib.auth.models import Group
from notifications.models import NotificationSystem

def user_role(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Sponsor').exists():
            return {'role': 'sponsor'}
        elif request.user.groups.filter(name='Gamer').exists():
            return {'role': 'gamer'}
        else:
            return {'role': 'other'}
    return {'role': 'guest'}

def notifications(request):
    if request.user.is_authenticated:
        notifications = NotificationSystem.objects.filter(receiver=request.user).order_by('-created_at')
        return {'notifications': notifications}
    return {'notifications': []}