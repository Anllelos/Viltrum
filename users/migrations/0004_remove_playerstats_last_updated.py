# Generated by Django 5.1 on 2024-09-14 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_playerstats_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerstats',
            name='last_updated',
        ),
    ]