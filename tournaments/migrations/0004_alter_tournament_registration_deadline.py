# Generated by Django 5.1.1 on 2024-10-08 03:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_alter_tournament_registration_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='registration_deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 11, 3, 3, 18, 130756, tzinfo=datetime.timezone.utc)),
        ),
    ]