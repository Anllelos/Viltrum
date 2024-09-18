# Generated by Django 5.1 on 2024-09-14 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_playerstats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerstats',
            name='game',
            field=models.CharField(choices=[('LoL', 'League of Legends'), ('D2', 'Dota 2'), ('CSGO', 'Counter-Strike: Global Offensive'), ('VAL', 'Valorant'), ('OW', 'Overwatch'), ('PUBG', "PlayerUnknown's Battlegrounds"), ('FORT', 'Fortnite'), ('Apex', 'Apex Legends'), ('R6', 'Rainbow Six Siege'), ('FIFA', 'FIFA'), ('RL', 'Rocket League')], max_length=5),
        ),
    ]
