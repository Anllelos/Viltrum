from django.contrib.auth.models import Group
from notifications.models import NotificationSystem
from chat.models import ChatGroup
from users.models import ExtendedData
from django.core.exceptions import ObjectDoesNotExist

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
        notifications = NotificationSystem.objects.filter(receiver=request.user).order_by('-created_at')[:8]
        return {'notifications': notifications}
    return {'notifications': []}

def chats(request):
    if request.user.is_authenticated:
        notifications = ChatGroup.objects.filter(member=request.user).order_by('-created_at')
        return {'chats': chats}
    return {'chats': []}

def verification(request):
    if request.user.is_authenticated:
        verificate = ExtendedData.objects.filter(user=request.user, user_verification=True)
        if verificate.exists():
            return {'verified':True}
        else:
            return {'verified':False}
    return {'verified':False}

def profile_img(request):
    if request.user.is_authenticated:
        try:
            extended_data = ExtendedData.objects.get(user=request.user)
            return {'prof_img': extended_data.profile_img.url if extended_data.profile_img else None}
        except ObjectDoesNotExist:
            return {'prof_img': None}
    return {'prof_img': None}