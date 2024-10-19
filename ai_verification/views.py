from django.shortcuts import render
from .forms import ImageUploadForm
from .services import process_images  # Aquí iría la lógica de recortar y comparar las imágenes

def upload_images(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.cleaned_data['user_image']
            document_image = form.cleaned_data['document_image']

            # Procesar y comparar las imágenes
            result = process_images(user_image, document_image)

            return render(request, 'ai_verification/result.html', {'result': result})
    else:
        form = ImageUploadForm()
    return render(request, 'ai_verification/upload.html', {'form': form})
