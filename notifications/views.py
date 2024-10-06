from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *

# Create your views here.
def notifications(request):
    
    notifications = NotificationSystem.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'notificationsystem.html', {'notifications': notifications})
