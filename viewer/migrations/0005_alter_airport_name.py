# Generated by Django 4.0.3 on 2022-03-20 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0004_alter_airport_name_alter_flightplan_waypoints'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='name',
            field=models.CharField(max_length=80),
        ),
    ]