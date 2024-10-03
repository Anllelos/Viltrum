# Generated by Django 5.1 on 2024-10-02 19:14

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0006_alter_tournament_registration_deadline_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='max_members',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='registration_deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 5, 19, 14, 59, 636190, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
