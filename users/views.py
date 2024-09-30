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
from datetime import date

# Verificación de roles dentro de la página
def profile_redirect(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    # Verifica los roles del usuario y redirige apropiadamente
    if user.groups.filter(name='Sponsor').exists():
        return redirect('profile_sponsor', username=user.username)
    elif user.groups.filter(name='Gamer').exists():
        return redirect('profile', username=user.username)

    return redirect('home')

def profile_user(request, username):
    user_to_validate = get_object_or_404(User, username=username)
    if user_to_validate.groups.filter(name='Gamer').exists():
        extended_data_table = get_object_or_404(ExtendedData, user=user_to_validate)
        game_stats_table = PlayerStats.objects.filter(user=user_to_validate)

        # Calcular winrate solo si existen estadísticas de juego
        for game in game_stats_table:
            total_games = game.wins + game.losses
            game.winrate = (game.wins / total_games) * 100 if total_games > 0 else 0

        data_context = {
            'profile': extended_data_table,
            'profile_user': user_to_validate,
            'games': game_stats_table,
            'game_exist': game_stats_table.exists()
        }
        return render(request, 'profile_user.html', data_context)

    raise Http404("No existe ese usuario")

def profile_sponsor(request, username):
    user_to_validate = get_object_or_404(User, username=username)
    if user_to_validate.groups.filter(name='Sponsor').exists():
        extended_data_table = get_object_or_404(ExtendedData, user=user_to_validate)
        products_table = SponsorProducts.objects.filter(user=user_to_validate)

        data_context = {
            'profile_sponsor': user_to_validate,
            'extended_data': extended_data_table,
            'products': products_table
        }
        return render(request, 'profile_sponsor.html', data_context)

    raise Http404("No existe ese patrocinador")

@login_required
def edit_profile_user(request, username):
    active_user = request.user

    if not active_user.groups.filter(name='Gamer').exists():
        return redirect('home')

    if active_user.username != username:
        return redirect('edit_profile_user', username=active_user.username)

    extended_data = get_object_or_404(ExtendedData, user=active_user)

    data_context = {
        'edit_user': EditUserForm(instance=active_user),
        'edit_extended_data_user': EditExtendedDataUserForm(instance=extended_data),
        'edit_profile_pic': ProfilePicForm(instance=extended_data),
        'edit_profile_banner': BannerPicForm(instance=extended_data)
    }

    if request.method == 'POST':
        form_type = request.POST.get('submit_form')

        if form_type == "personal_data":
            form = EditUserForm(request.POST, instance=active_user)
            if form.is_valid():
                form.save()

        elif form_type == "extra_data":
            form = EditExtendedDataUserForm(request.POST, instance=extended_data)
            if form.is_valid():
                form.save()

        elif form_type == "profile_image":
            form = ProfilePicForm(request.POST, request.FILES, instance=extended_data)
            if form.is_valid():
                profile_pic = form.save(commit=False)
                profile_pic.user = active_user
                profile_pic.save()

        elif form_type == "profile_banner":
            form = BannerPicForm(request.POST, request.FILES, instance=extended_data)
            if form.is_valid():
                banner = form.save(commit=False)
                banner.user = active_user
                banner.save()

    return render(request, 'edit_profile_user.html', data_context)

@login_required
def edit_profile_sponsor(request, username):
    user_to_validate = get_object_or_404(User, username=username)
    profile_to_validate = get_object_or_404(ExtendedData, user=user_to_validate)

    if request.user.username != username:
        return redirect('edit_profile', username=request.user.username)

    upp_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_to_validate)

    if request.method == 'POST':
        cropped_image = request.POST.get('cropped_image')
        if cropped_image:
            format, imgstr = cropped_image.split(';base64,') 
            ext = format.split('/')[-1]
            img_data = ContentFile(base64.b64decode(imgstr), name=f"profile_{request.user.username}.{ext}")
            profile_to_validate.profile_img = img_data

        if upp_form.is_valid():
            upp_form.save()
            return redirect('edit_profile', username=username)  # Redirigir después de éxito

    data_context = {'upp_form': upp_form, 'profile': profile_to_validate}
    return render(request, 'edit_profile.html', data_context)


#-------------------------------------------------------------- Crear usuario --------------------------------------------------------------#
def create_user(request):
    if request.method == 'POST':
        form_type = request.POST.get('submit_form')
        if form_type == 'user_form':
            user_form = CreateUserForm(request.POST)
            user_extended_form = UserExtendedDataForm(request.POST)

            if user_form.is_valid() and user_extended_form.is_valid():
                username = user_form.cleaned_data.get('username')
                birthdate = user_extended_form.cleaned_data.get('birthdate')
                today = date.today()
                age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

                if len(username) < 3:
                    user_form.add_error('username', "El usuario debe contener al menos 3 caracteres")
                if age < 18:
                    user_extended_form.add_error('birthdate', "Debes tener por lo menos 18 años para registrarte")

                if not (user_form.errors or user_extended_form.errors):
                    user = user_form.save()
                    extended_data = user_extended_form.save(commit=False)
                    extended_data.user = user
                    extended_data.save()
                    return redirect('login')

            data_context = {
                'user_form': user_form,
                'user_extended_form': user_extended_form,
                'sponsor_form': CreateSponsorForm(),
                'sponsor_extended_form': SponsorExtendedDataForm()
            }

        elif form_type == 'sponsor_form':
            sponsor_form = CreateSponsorForm(request.POST)
            sponsor_extended_form = SponsorExtendedDataForm(request.POST)

            if sponsor_form.is_valid() and sponsor_extended_form.is_valid():
                username = user_form.cleaned_data.get('username')
                if len(username) < 3:
                    sponsor_form.add_error('username', "El usuario debe contener al menos 3 caracteres")
                if not (user_form.errors or user_extended_form.errors):
                    sponsor = sponsor_form.save()
                    extended_data = sponsor_extended_form.save(commit=False)
                    extended_data.user = sponsor
                    extended_data.save()
                    return redirect('login')

            data_context = {
                'user_form': CreateUserForm(),
                'user_extended_form': UserExtendedDataForm(),
                'sponsor_form': sponsor_form,
                'sponsor_extended_form': sponsor_extended_form
            }

    else:
        data_context = {
            'user_form': CreateUserForm(),
            'user_extended_form': UserExtendedDataForm(),
            'sponsor_form': CreateSponsorForm(),
            'sponsor_extended_form': SponsorExtendedDataForm()
        }

    return render(request, 'register.html', data_context)


def home(request):
    active_user = request.user
    data_context = {'gamer': active_user.groups.filter(name='Gamer').exists()}
    videojuegos = Videojuego.objects.all()

    # Optimización para cargar imágenes de carrusel
    carrusel_dir = os.path.join(settings.BASE_DIR, 'static/images/CarruselHome')
    carrusel_images = [
        os.path.basename(image)
        for image in glob.glob(os.path.join(carrusel_dir, '*'))
        if image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    ]

    return render(request, 'home.html', data_context)

@login_required
def subir_stream(request):
    return handle_upload(request, StreamForm, 'subir_stream.html')

@login_required
def subir_juego(request):
    return handle_upload(request, JuegoForm, 'subir_juego.html')

def handle_upload(request, form_class, template_name):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = form_class()
    return render(request, template_name, {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')  # Reemplaza 'home' con el nombre de URL apropiado

@login_required
def games_stats(request):
    active_user = request.user

    if active_user.groups.filter(name='Gamer').exists():
        player_stats_form = PlayerStatsForm()
        if request.method == "POST":
            player_stats_form = PlayerStatsForm(request.POST)
            if player_stats_form.is_valid():
                player_stats = player_stats_form.save(commit=False)
                player_stats.user = active_user
                player_stats.save()

        return render(request, 'game_stats.html', {'player_stats_form': player_stats_form})

    return redirect('home')

@login_required
def sponsor_products(request):
    active_user = request.user

    if active_user.groups.filter(name='Sponsor').exists():
        product_form = SponsorProductsForm()
        if request.method == "POST":
            product_form = SponsorProductsForm(request.POST, request.FILES)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.user = active_user
                product.save()
                return render(request, 'sponsor_products.html', {'product_form': product_form, 'message': "Product saved successfully."})

        return render(request, 'sponsor_products.html', {'product_form': product_form})

    return redirect('home')
