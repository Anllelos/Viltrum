"""
URL configuration for Viltrum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#test
from django.contrib import admin
from django.urls import path, re_path, include
#Static Files config
from django.conf import settings
from django.conf.urls.static import static
#Reset password config
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('', include('django.contrib.auth.urls')),  # Rutas para autenticación
    path('', include('core.urls')),  # Incluye todas las rutas de `core.urls` sin prefijo adicional
    path('', include('users.urls')),  # Incluye todas las rutas de `users.urls` sin prefijo adicional
    path('', include('tournaments.urls')), # Incluye todas las rutas de `tournaments.urls` sin prefijo adicional
    path('', include('clasifications.urls')), # Incluye todas las rutas de `clasifications.urls` sin prefijo adicional
    path('', include('sponsors.urls')), # Incluye todas las rutas de `sponsors.urls` sin prefijo adicional
    path('', include('explore.urls')), # Incluye todas las rutas de `explore.urls` sin prefijo adicional
    # Rutas para el restablecimiento de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    #Manejo de subida de archivos
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)