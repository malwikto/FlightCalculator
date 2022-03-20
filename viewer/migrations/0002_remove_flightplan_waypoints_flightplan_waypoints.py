# Generated by Django 4.0.3 on 2022-03-19 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightplan',
            name='waypoints',
        ),
        migrations.AddField(
            model_name='flightplan',
            name='waypoints',
            field=models.ManyToManyField(to='viewer.waypoint'),
        ),
    ]
