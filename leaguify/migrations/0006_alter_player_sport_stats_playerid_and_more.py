# Generated by Django 5.2 on 2025-05-11 19:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leaguify", "0005_tracks"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player_sport_stats",
            name="playerID",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="leaguify.player",
            ),
        ),
        migrations.AlterField(
            model_name="team_sport_stats",
            name="teamID",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="leaguify.team",
            ),
        ),
    ]
