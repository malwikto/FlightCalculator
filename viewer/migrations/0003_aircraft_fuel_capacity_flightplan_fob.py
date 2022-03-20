# Generated by Django 4.0.3 on 2022-03-20 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0002_remove_flightplan_waypoints_flightplan_waypoints'),
    ]

    operations = [
        migrations.AddField(
            model_name='aircraft',
            name='fuel_capacity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flightplan',
            name='fob',
            field=models.IntegerField(default=20000),
            preserve_default=False,
        ),
    ]
