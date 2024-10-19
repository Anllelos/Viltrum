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
from tournaments.models import Tournament
from django.http import JsonResponse
from notifications.models import NotificationSystem
import iamodule as imgia
import json

#-------------------------------------------------------------- Ver perfil --------------------------------------------------------------#
# Verificación de roles dentro de la página
@login_required
def profile_redirect(request):
    user = request.user

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
        game_stats_table = PlayerStats.objects.filter(user=user_to_validate, is_active=True)
        tournaments_created = Tournament.objects.filter(owner=user_to_validate)
        notification_sended = NotificationSystem.objects.filter(receiver=user_to_validate, sender=request.user).first()

        # Query gallery images associated with the user
        gallery_images = UserGalleryImage.objects.filter(user=user_to_validate)

        data_context = {
            'profile': extended_data_table,
            'profile_user': user_to_validate,
            'tournaments_created': tournaments_created,
            'gallery_images': gallery_images,  # Pass gallery images to the template
        }

        if notification_sended:
            data_context['notify_sended'] = True

        n_games = 0
        if game_stats_table.exists():
            for game in game_stats_table:
                total_games = game.wins + game.losses
                game.winrate = (game.wins / total_games) * 100 if total_games > 0 else 0
                n_games += 1
            data_context['games'] = game_stats_table
            data_context['n_games'] = n_games
        else:
            data_context['game_exist'] = True

        return render(request, 'profile_user.html', data_context)
    else:
        raise Http404("No existe ese usuario")


def profile_sponsor(request, username):
    user_to_validate = get_object_or_404(User, username=username)
    if user_to_validate.groups.filter(name='Sponsor').exists():
        extended_data_table = get_object_or_404(ExtendedData, user=user_to_validate)
        products_table = SponsorProducts.objects.filter(user=user_to_validate, is_active=True)

        data_context = {
            'profile_sponsor': user_to_validate,
            'extended_data': extended_data_table,   
            'products': products_table
        }
        return render(request, 'profile_sponsor.html', data_context)

    raise Http404("No existe ese patrocinador")


#-------------------------------------------------------------- Editar usuario --------------------------------------------------------------#
@login_required
def profile_redirect_edit(request):
    user = request.user

    # Verifica los roles del usuario y redirige apropiadamente
    if user.groups.filter(name='Sponsor').exists():
        return redirect('edit_profile_sponsor', username=user.username)
    elif user.groups.filter(name='Gamer').exists():
        return redirect('edit_profile_user', username=user.username)

    return redirect('home')



@login_required
def edit_profile_user(request, username):
    active_user = request.user

    if not active_user.groups.filter(name='Gamer').exists():
        return redirect('home')

    if active_user.username != username:
        return redirect('edit_profile_user', username=active_user.username)

    extended_data = get_object_or_404(ExtendedData, user=active_user)

    data_context = {
        'extended_data':extended_data,
        'edit_user': EditUserForm(instance=active_user),
        'edit_extended_data_user': EditExtendedDataUserForm(instance=extended_data),
        'edit_profile_pic': ProfilePicForm(instance=extended_data),
        'edit_profile_banner': BannerPicForm(instance=extended_data)
    }

    if request.method == 'POST':
        form_type = request.POST.get('submit_form')
        print(form_type)

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


#-------------------------------------------------------------- Editar sponsor --------------------------------------------------------------#
@login_required
def edit_profile_sponsor(request, username):
    user_to_validate = get_object_or_404(User, username=username)
    profile_to_validate = get_object_or_404(ExtendedData, user=user_to_validate)
    active_user = request.user

    if not active_user.groups.filter(name='Sponsor').exists():
        return redirect('home')

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
                username = sponsor_form.cleaned_data.get('username')
                if len(username) < 3:
                    sponsor_form.add_error('username', "El usuario debe contener al menos 3 caracteres")
                if not (sponsor_form.errors or sponsor_extended_form.errors):
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

#-------------------------------------------------------------- Cerrar sesión --------------------------------------------------------------#
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')  


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

#-------------------------------------------------------------- Subir información (estadisticas/productos) --------------------------------------------------------------#
#-------------------------------------------------------------- Estadísticas --------------------------------------------------------------#
@login_required
def games_stats(request):
    active_user = request.user

    if active_user.groups.filter(name='Gamer').exists():
        player_stats_form = PlayerStatsForm()
        data_context = {'player_stats_form': player_stats_form}

        if request.method == "POST":
            player_stats_form = PlayerStatsForm(request.POST)
            
            if player_stats_form.is_valid():
                game_value = player_stats_form.cleaned_data.get('game')
                user_game = player_stats_form.cleaned_data.get('user_game')
                rank = player_stats_form.cleaned_data.get('rank')
                wins = player_stats_form.cleaned_data.get('wins')
                losses = player_stats_form.cleaned_data.get('losses')
                total_played = player_stats_form.cleaned_data.get('total_played')

                # Buscar el juego inactivo
                game = PlayerStats.objects.filter(game=game_value, user=active_user, is_active=False).first()

                if game:
                    # Actualizar las estadísticas del juego
                    game.user_game = user_game
                    game.rank = rank
                    game.wins = wins
                    game.losses = losses
                    game.total_played = total_played
                    game.is_active = True
                    game.save()
                    data_context['message'] = "Estadísticas registradas"
                else:
                    # Verificar si ya se registró el juego
                    existing_game = PlayerStats.objects.filter(game=game_value, user=active_user, is_active=True).exists()
                    
                    if existing_game:
                        data_context['message'] = "Ya registraste este juego"
                    else:
                        # Crear nuevo registro
                        player_stats = player_stats_form.save(commit=False)
                        player_stats.user = active_user
                        player_stats.save()
                        data_context['message'] = "Estadísticas registradas"

        return render(request, 'game_stats.html', data_context)

    return redirect('home')

# Editar estadísticas de juego
@login_required
def update_game_stats(request, game_id):
    active_user = request.user
    
    # Obtiene el juego o devuelve un error 404 si no existe
    game = get_object_or_404(PlayerStats, pk=game_id)
    
    # Verifica si el usuario es parte del grupo 'Gamer' y si tiene acceso al juego
    if active_user.groups.filter(name='Gamer').exists() and PlayerStats.objects.filter(user=active_user, pk=game.id).exists():
        if request.method == "POST":
            edit_game_stat = EditGameStat(request.POST, instance=game)
            if edit_game_stat.is_valid():
                edit_game_stat.save()
                return redirect('profile', username=active_user.username)  # Asegúrate de pasar el username

        # Si no es POST, muestra el formulario para editar
        edit_game_stat = EditGameStat(instance=game)  # Crear instancia del formulario para GET
        data_context = {'edit_game_stat': edit_game_stat, 'game': game}
        return render(request, 'edit_game_stat.html', data_context)
    
    # Redirige a 'home' si el usuario no tiene acceso
    return redirect('home')

# Borrar estadísticas de juego
@login_required
def delete_game_stats(request, game_id):
    active_user = request.user

    # Verifica si el usuario es parte del grupo 'Gamer' y si tiene acceso al juego
    game = get_object_or_404(PlayerStats, pk=game_id, user=active_user)
    
    if active_user.groups.filter(name='Gamer').exists():
        game.is_active = False
        game.save()
        return redirect('profile', username=active_user.username)
    
    # Redirige a 'home' si el usuario no tiene acceso
    return redirect('home')


#-------------------------------------------------------------- Productos --------------------------------------------------------------#
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

@login_required
def update_product(request, product_id):
    active_user = request.user
    
    # Obtiene el juego o devuelve un error 404 si no existe
    product = get_object_or_404(SponsorProducts, pk=product_id)
    
    # Verifica si el usuario es parte del grupo 'Gamer' y si tiene acceso al juego
    if active_user.groups.filter(name='Sponsor').exists() and SponsorProducts.objects.filter(user=active_user, pk=product.id).exists():
        if request.method == "POST":
            edit_product = EditProduct(request.POST, request.FILES, instance=product)
            if edit_product.is_valid():
                edit_product.save()
                return redirect('profile_sponsor', username=active_user.username)  # Asegúrate de pasar el username

        # Si no es POST, muestra el formulario para editar
        edit_product = EditProduct(instance=product)  # Crear instancia del formulario para GET
        data_context = {'edit_product': edit_product, 'product': product}
        return render(request, 'edit_product.html', data_context)
    
    # Redirige a 'home' si el usuario no tiene acceso
    return redirect('home')

# Borrar estadísticas de juego
@login_required
def delete_product(request, product_id):
    active_user = request.user

    # Verifica si el usuario es parte del grupo 'Gamer' y si tiene acceso al juego
    product = get_object_or_404(SponsorProducts, pk=product_id, user=active_user)
    
    if active_user.groups.filter(name='Sponsor').exists():
        product.is_active = False
        product.save()
        return redirect('profile_sponsor', username=active_user.username)
    
    # Redirige a 'home' si el usuario no tiene acceso
    return redirect('home')

@login_required
def send_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect('profile', user_id=recipient_id)
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form, 'recipient': recipient})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'inbox.html', {'messages': messages})

@login_required
def profile_view(request):
    profile_user = request.user  # or however you're fetching the profile owner
    images = UserGalleryImage.objects.filter(user=profile_user)
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect('profile')  # Redirect to refresh the page and display new images
    else:
        form = ImageUploadForm()

    return render(request, 'profile_user.html', {
        'profile_user': profile_user,
        'form': form,
        'images': images,
    })

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            user_image.user = request.user
            user_image.save()
            return redirect('profile', username=request.user.username)  # Update this line
    else:
        form = ImageUploadForm()
    return render(request, 'users/upload_image.html', {'form': form})

def verification(request, username):
    active_user = request.user
    verification_profile = get_object_or_404(User, username=username)
    extended_data = get_object_or_404(ExtendedData, user=active_user)
    
    if verification_profile == active_user:
        if extended_data.user_verification == True:
            return redirect('home')
        if request.method == "POST":
            verification_form = VerificationForm(request.POST, request.FILES, instance=extended_data)
            if verification_form.is_valid():
                form = verification_form.save(commit=False)
                form.user = active_user
                form.save()
                identification_photo = extended_data.user_identification.url
                user_photo = extended_data.user_photo.url
                verification = imgia.llm_promt_engineering_image(identification_photo, user_photo)
                print(verification)
                if verification is None:
                    return redirect('home')
                else:
                    verification = json.loads(verification)
                    if verification['is_verified'] == "True":
                        extended_data.user_verification = True
                        extended_data.save()
                    elif verification['is_verified'] == "False":
                        print("No esta verificado")
        else:
            verification_form = VerificationForm()

        data_context = {"verification_form": verification_form}
        return render(request, "verification.html", data_context)
    
    else:
        return render(request, "error.html", {"message": "No estás autorizado para verificar este perfil."})
