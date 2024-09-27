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
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now  # Correct import for 'now'

# Verificación de roles dentro de la página
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
    user_to_validate = get_object_or_404(User, username=username)
    if user_to_validate.groups.filter(name='Gamer').exists():
        extended_data_table = get_object_or_404(ExtendedData, user=user_to_validate)
        game_stats_table = PlayerStats.objects.filter(user=user_to_validate)
    
        data_context = {'profile': extended_data_table, 'profile_user': user_to_validate}

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
        data_context = {
            'profile_sponsor': user_to_validate,
            'extended_data': extended_data_table,
            'products': products_table
        }
        return render(request, 'profile_sponsor.html', data_context)
    else:
        raise Http404("No existe ese patrocinador")


@login_required
def edit_profile_user(request, username):
    active_user = request.user

    if not active_user.groups.filter(name='Gamer').exists():
        return redirect('home')

    if active_user.username != username:
        return redirect('edit_profile_user', username=active_user.username)

    edit_user = EditUserForm(instance=active_user)
    extended_data = ExtendedData.objects.get(user=active_user)
    edit_extended_data_user = EditExtendedDataUserForm(instance=extended_data)
    edit_profile_pic = ProfilePicForm(instance=extended_data)
    edit_profile_banner = BannerPicForm(instance=extended_data)

    data_context = {
        'edit_user': edit_user,
        'edit_extended_data_user': edit_extended_data_user,
        'edit_profile_pic': edit_profile_pic,
        'edit_profile_banner': edit_profile_banner
    }

    if request.method == 'POST':
        form_type = request.POST.get('submit_form')
        
        if form_type == "personal_data":
            edit_user = EditUserForm(request.POST, instance=active_user)
            if edit_user.is_valid():
                edit_user.save()

        elif form_type == "extra_data":
            edit_extended_data_user = EditExtendedDataUserForm(request.POST, instance=extended_data)
            if edit_extended_data_user.is_valid():
                edit_extended_data_user.save()
            else:
                print(edit_extended_data_user.errors)

        elif form_type == "profile_image":
            edit_profile_pic = ProfilePicForm(request.POST, request.FILES, instance=extended_data)
            if edit_profile_pic.is_valid():
                profile_pic = edit_profile_pic.save(commit=False)
                profile_pic.user = active_user
                profile_pic.save()

        elif form_type == "profile_banner":
            edit_profile_banner = BannerPicForm(request.POST, request.FILES, instance=extended_data)
            if edit_profile_banner.is_valid():
                banner = edit_profile_banner.save(commit=False)
                banner.user = active_user
                banner.save()

    return render(request, 'edit_profile_user.html', data_context)


@login_required
def edit_profile_sponsor(request, username):
    user_to_validate = get_object_or_404(User, username=username)
    profile_to_validate = get_object_or_404(ExtendedData, user=user_to_validate)
    upp_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_to_validate)

    if request.user.username == username:
        if request.method == 'POST':
            cropped_image = request.POST.get('cropped_image')
            
            if cropped_image:
                format, imgstr = cropped_image.split(';base64,') 
                ext = format.split('/')[-1]
                img_data = ContentFile(base64.b64decode(imgstr), name=f"profile_{request.user.username}.{ext}")
                profile_to_validate.profile_img = img_data

            if upp_form.is_valid():
                upp_form.save()
                return redirect('edit_profile', username=username)  # Updated to redirect after success
            else:
                data_context = {'upp_form': upp_form, 'message': 'Error al actualizar la imagen'}

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
    data_context = {
        'user_form': user_form, 
        'sponsor_form': sponsor_form, 
        'user_extended_form': user_extended_form, 
        'sponsor_extended_form': sponsor_extended_form
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
            sponsor_extended_form = SponsorExtendedDataForm(request.POST)

            if sponsor_form.is_valid() and sponsor_extended_form.is_valid():
                sponsor = sponsor_form.save()
                extended_data = sponsor_extended_form.save(commit=False)
                extended_data.user = sponsor
                extended_data.save()

                return redirect('login')
            else:
                print("Error en los formularios: ", sponsor_form.errors, sponsor_extended_form.errors)

    return render(request, 'register.html', data_context)

def home(request):

    active_user = request.user
    data_context = {'gamer':False}
    if active_user.groups.filter(name='Gamer').exists():
        data_context = {'gamer':True}
    videojuegos = Videojuego.objects.all()

    carrusel_dir = os.path.join(settings.BASE_DIR, 'static/images/CarruselHome')
    carrusel_images = glob.glob(os.path.join(carrusel_dir, '*'))
    carrusel_images = [os.path.basename(os.path.normpath(image)) for image in carrusel_images if image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    return render(request, 'home.html', data_context)


@login_required
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
def subir_juego(request):
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = JuegoForm()
    return render(request, 'subir_juego.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the appropriate URL name for your home page

@login_required
def games_stats(request):
    active_user = request.user

    # Only gamers should have access
    if active_user.groups.filter(name='Gamer').exists():
        player_stats_form = PlayerStatsForm()
        data_context = {'player_stats_form': player_stats_form}

        if request.method == "POST":
            player_stats_form = PlayerStatsForm(request.POST)
            if player_stats_form.is_valid():
                # Save or update game statistics
                player_stats = player_stats_form.save(commit=False)
                player_stats.user = active_user
                player_stats.save()
            else:
                print(player_stats_form.errors)

        return render(request, 'game_stats.html', data_context)
    
    # Redirect users who are not in the 'Gamer' group
    return redirect('home')

@login_required
def sponsor_products(request):
    active_user = request.user

    # Only sponsors should have access
    if active_user.groups.filter(name='Sponsor').exists():
        product_form = SponsorProductsForm()
        data_context = {'product_form': product_form}

        if request.method == "POST":
            product_form = SponsorProductsForm(request.POST, request.FILES)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.user = active_user
                product.save()
                data_context['message'] = "Product saved successfully."
                return render(request, 'sponsor_products.html', data_context)
        
        return render(request, 'sponsor_products.html', data_context)
    
    # Redirect users who are not in the 'Sponsor' group
    return redirect('home')
