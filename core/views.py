from django.shortcuts import render

# Create your views here.
def home(request):
    active_user = request.user

    return render(request, 'home.html')