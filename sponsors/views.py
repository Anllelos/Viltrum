from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group
from users.models import *

# Create your views here.
def sponsors(request):
    group = Group.objects.get(name='Sponsor')
    sponsors = group.user_set.all()
    sponsor_data = []

    for sponsor in sponsors:
        # Obtener el perfil asociado (suponiendo que hay una relación uno a uno)
        profile = ExtendedData.objects.filter(user=sponsor).first()  # Esto devuelve el primer perfil o None
        sponsor_data.append({'sponsor': sponsor, 'profile': profile})  # Cambiar profiles a profile para relación 1 a 1
    
    data_context = {'sponsor_data': sponsor_data}
    return render(request, 'sponsors.html', data_context)