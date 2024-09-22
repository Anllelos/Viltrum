import os
import glob
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.files.base import ContentFile
import base64
from django.http import Http404

#Verificación de roles dentro de la página
def profile_redirect(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login') 

    # Verifica si el usuario es patrocinador "Sponsor"
    if user.groups.filter(name='Sponsor').exists():
        return redirect('profile_sponsor', username=user.username)

    # Verifica si el usuario es jugador "Gamer"
    elif user.groups.filter(name='Gamer').exists():
        return redirect('profile', username=user.username)

    return redirect('home')

def profile_user(request, username):
    # Buscar al usuario por el nombre de usuario en lugar del ID del request
    user_to_validate = get_object_or_404(User, username=username)
    if user_to_validate.groups.filter(name='Gamer').exists():
        extended_data_table = get_object_or_404(ExtendedData, user=user_to_validate)
        game_stats_table = PlayerStats.objects.filter(user=user_to_validate)
    
        data_context = {'profile': extended_data_table, 'profile_user': user_to_validate}

        # Si hay estadísticas de juegos, calcular el winrate
        if game_stats_table.exists():
            for game in game_stats_table:
                total_games = game.wins + game.losses
                game.winrate = (game.wins / total_games) * 100 if total_games > 0 else 0
            data_context['games'] = game_stats_table
        else:
            data_context['game_exist'] = True

        return render(request, 'profile_user.html', data_context)
    else:
        raise Http404("No existe ese usuario")

def profile_sponsor(request, username):
    user_to_validate = get_object_or_404(User, username=username)
    if user_to_validate.groups.filter(name='Sponsor').exists():
        extended_data_table = ExtendedData.objects.filter(user=user_to_validate)
        products_table = SponsorProducts.objects.filter(user=user_to_validate)
        data_context = {'profile_sponsor': user_to_validate, 
                        'extended_data':extended_data_table,
                        'products':products_table}
        return render(request, 'profile_sponsor.html', data_context)
    else:
        raise Http404("No existe ese patrocinador")


@login_required
def edit_profile_user(request, username):
    active_user = request.user
    if active_user.groups.filter(name='Gamer').exists():
        data_context = {}
        user_to_validate = get_object_or_404(User, username=username)
        profile_to_validate = get_object_or_404(ExtendedData, user=user_to_validate)
        upp_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_to_validate)

        if active_user.username == username:
            if request.method == 'POST':
                cropped_image = request.POST.get('cropped_image')
            
                # Procesar la imagen recortada
                if cropped_image:
                    format, imgstr = cropped_image.split(';base64,') 
                    ext = format.split('/')[-1]
                    img_data = ContentFile(base64.b64decode(imgstr), name=f"profile_{request.user.username}.{ext}")
                    profile_to_validate.profile_img = img_data

                if upp_form.is_valid():
                    upp_form.save()
                    data_context['message'] = 'Imagen Actualizada'
                else:
                    data_context['message'] = 'Error al actualizar la imagen'

            data_context['upp_form'] = upp_form
            data_context['profile'] = profile_to_validate
            return render(request, 'edit_profile_user.html', data_context)
        else:
            return redirect('edit_profile_user', username=request.user.username)

@login_required
def edit_profile_sponsor(request, username):
    data_context = {}
    user_to_validate = get_object_or_404(User, username=username)
    profile_to_validate = get_object_or_404(ExtendedData, user=user_to_validate)
    upp_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_to_validate)

    if request.user.username == username:
        if request.method == 'POST':
            cropped_image = request.POST.get('cropped_image')
            
            # Procesar la imagen recortada
            if cropped_image:
                format, imgstr = cropped_image.split(';base64,') 
                ext = format.split('/')[-1]
                img_data = ContentFile(base64.b64decode(imgstr), name=f"profile_{request.user.username}.{ext}")
                profile_to_validate.profile_img = img_data

            if upp_form.is_valid():
                upp_form.save()
                data_context['message'] = 'Imagen Actualizada'
            else:
                data_context['message'] = 'Error al actualizar la imagen'

        data_context['upp_form'] = upp_form
        data_context['profile'] = profile_to_validate
        return render(request, 'edit_profile.html', data_context)
    else:
        return redirect('edit_profile', username=request.user.username)

def create_user(request):
    user_form = CreateUserForm()
    sponsor_form = CreateSponsorForm()
    user_extended_form = UserExtendedDataForm()
    sponsor_extended_form = SponsorExtendedDataForm()
    data_context = {'user_form': user_form, 
                    'sponsor_form': sponsor_form, 
                    'user_extended_form': user_extended_form, 
                    'sponsor_extended_form':sponsor_extended_form
                    }

    if request.method == 'POST':
        form_type = request.POST.get('submit_form')
        if form_type == 'user_form':
            user_form = CreateUserForm(request.POST)
            user_extended_form = UserExtendedDataForm(request.POST)

            if user_form.is_valid() and user_extended_form.is_valid():
                user = user_form.save()
                extended_data = user_extended_form.save(commit=False)
                extended_data.user = user
                extended_data.save()

                return redirect('login')
            else:
                print("Error en los formularios: ", user_form.errors, user_extended_form.errors)

        elif form_type == 'sponsor_form':
            sponsor_form = CreateSponsorForm(request.POST)
            user_extended_form = SponsorExtendedDataForm(request.POST)

            if sponsor_form.is_valid() and user_extended_form.is_valid():
                sponsor = sponsor_form.save()
                extended_data = user_extended_form.save(commit=False)
                extended_data.user = sponsor
                extended_data.save()

                return redirect('login')
            else:
                print("Error en los formularios: ", sponsor_form.errors, user_extended_form.errors)

    return render(request, 'register.html', data_context)

#Función para visualizar la pantalla principal con todos los datos
def home(request):
    videojuegos = Videojuego.objects.all()  # Obtener todos los juegos de la base de datos

    # Directorio de las imágenes del carrusel
    carrusel_dir = os.path.join(settings.BASE_DIR, 'static/images/CarruselHome')

    # Usar glob para encontrar todas las imágenes
    carrusel_images = glob.glob(os.path.join(carrusel_dir, '*'))

    # Normalizar la ruta para asegurarse de que las barras estén correctamente formateadas
    carrusel_images = [os.path.basename(os.path.normpath(image)) for image in carrusel_images if image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    return render(request, 'home.html', {
        'videojuegos': videojuegos,
        'carrusel_images': carrusel_images,  # Pasamos las imágenes del carrusel al template
    })

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
#Función para subir las clasificaciones
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

#Player stats upload
@login_required
def games_stats(request):
    active_user = request.user
    if active_user.groups.filter(name='Gamer').exists():
        player_stats_form = PlayerStatsForm()
        data_context = {'player_stats_form':player_stats_form}
        if request.method == "POST":
            active_user_id = active_user.id
            player_stats_form = PlayerStatsForm(request.POST)
            if player_stats_form.is_valid():
                try:
                    game_validate = PlayerStats.objects.get(user=active_user_id, game=request.POST.get('game'))
                    if game_validate is not None:
                        data_context['game_exist'] = True
                except:
                # Crear una instancia del modelo, pero no guardarla todavía
                    player_stats = player_stats_form.save(commit=False)
                
                # Asignar el usuario activo
                    player_stats.user_id = active_user_id

                # Guardar el objeto en la base de datos
                    player_stats.save()
            else:
                print(player_stats_form.errors)
        return render(request, 'game_stats.html', data_context)
    else:
        return redirect('home')


@login_required
def sponsor_products(request):
    active_user = request.user
    if active_user.groups.filter(name='Sponsor').exists():
        product_form = SponsorProductsForm()
        data_context = {'product_form':product_form}
        if request.method == "POST":
            product_form = SponsorProductsForm(request.POST, request.FILES)
            if product_form.is_valid():
                # Crea el objeto, pero no lo guarda todavía.
                product = product_form.save(commit=False)
                product.user = active_user  # Asigna el usuario.
                product.save()  # Guarda el producto en la base de datos.
                data_context['message'] = "Se ha guardado el producto con éxito"
                return render(request, 'sponsor_products.html', data_context)
        
        return render(request, 'sponsor_products.html', data_context)
    else:
        return redirect('home')
