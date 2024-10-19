from django.db import models


class ImageVerification(models.Model):
    user_image = models.ImageField(upload_to='user_images/')
    document_image = models.ImageField(upload_to='document_images/')
    result = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
