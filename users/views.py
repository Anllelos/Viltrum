from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def profile(request):
    user_to_validate = get_object_or_404(User, id=request.user.id)
    profile_to_validate = get_object_or_404(ExtendedData, user=user_to_validate)
    data_context = {'profile':profile_to_validate}
    return render(request, 'profile.html', data_context)

@login_required
def edit_profile(request):
    data_context = {}
    user_to_validate = get_object_or_404(User, id=request.user.id)
    profile_to_validate = get_object_or_404(ExtendedData, user=user_to_validate)
    upp_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_to_validate)

    if request.method == 'POST':
        if upp_form.is_valid():
            upp_form.save()
            data_context['message'] = 'Imagen Actualizada'
        else:
            data_context['message'] = 'Error al actualizar la imagen'

    data_context['upp_form'] = upp_form
    data_context['profile'] = profile_to_validate

    return render(request, 'edit_profile.html', data_context)

def create_user(request):
    user_form = CreateUserForm()
    user_extended_form = ProfilePicForm()
    data_context = {'user_form':user_form, 'user_extended_form':user_extended_form}
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user_to_validate = User.objects.get(username=request.POST.get('username'))
            user_extended_data = ExtendedData.objects.create(user=user_to_validate)
            user_extended_data.save()
            return redirect('login')
    return render(request, 'register.html', data_context)

#Función para visualizar la pantalla principal con todos los datos
def home(request):
    videojuegos = Videojuego.objects.all()  # Obtén todos los juegos de la base de datos
    return render(request, 'home.html', {'videojuegos': videojuegos})

@login_required
#Función para subir los streams
def subir_stream(request):
    if request.method == 'POST':
        form = StreamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StreamForm()
    return render(request, 'subir_stream.html', {'form': form})

@login_required
#Función para subir los torneos
def subir_torneo(request):
    if request.method == 'POST':
        form = TorneoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TorneoForm()
    return render(request, 'subir_torneo.html', {'form': form})

@login_required
#Función para subir un las clasificaciones
def subir_clasificacion(request):
    if request.method == 'POST':
        form = ClasificacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClasificacionForm()
    return render(request, 'subir_clasificacion.html', {'form': form})

#Función para subir un juego
@login_required
def subir_juego(request):
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = JuegoForm()
    return render(request, 'subir_juego.html', {'form': form})

#Función para cerrar sesión
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')