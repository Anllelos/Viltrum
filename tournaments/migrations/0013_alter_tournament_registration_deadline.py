# Generated by Django 5.0.8 on 2024-11-06 21:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0012_alter_tournament_registration_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='registration_deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 9, 21, 38, 52, 346081, tzinfo=datetime.timezone.utc)),
        ),
    ]