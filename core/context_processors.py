from django.contrib.auth.models import Group

def user_role(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Sponsor').exists():
            return {'role': 'sponsor'}
        elif request.user.groups.filter(name='Gamer').exists():
            return {'role': 'gamer'}
        else:
            return {'role': 'other'}
    return {'role': 'guest'}