# Generated by Django 5.1.3 on 2024-11-17 20:12

import storages.backends.azure_storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0003_game_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(storage=storages.backends.azure_storage.AzureStorage(), upload_to='games/'),
        ),
    ]