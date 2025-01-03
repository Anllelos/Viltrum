# Generated by Django 5.1.3 on 2024-11-17 20:12

import storages.backends.azure_storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(storage=storages.backends.azure_storage.AzureStorage(), upload_to='products/images/'),
        ),
    ]
