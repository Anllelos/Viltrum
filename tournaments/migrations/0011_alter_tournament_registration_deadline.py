# Generated by Django 5.0.8 on 2024-10-21 22:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0010_alter_tournament_registration_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='registration_deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 24, 22, 49, 0, 845657, tzinfo=datetime.timezone.utc)),
        ),
    ]
