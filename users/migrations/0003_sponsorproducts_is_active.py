# Generated by Django 5.1 on 2024-10-02 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_playerstats_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorproducts',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]