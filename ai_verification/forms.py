from django import forms

class ImageUploadForm(forms.Form):
    user_image = forms.ImageField(label='Sube tu foto')
    document_image = forms.ImageField(label='Sube tu foto del documento')
