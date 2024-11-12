# shop/models.py
from django.db import models
from django.contrib.auth.models import User  # Usamos el modelo de usuario para los patrocinadores
from storages.backends.azure_storage import AzureStorage

class Product(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/images/', storage=AzureStorage())
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
