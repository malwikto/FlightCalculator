from django.contrib.auth.models import User
from django.db import models


# from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, IntegerField, DateField, TextField, \
#     DateTimeField, ImageField, DecimalField
from django.db.models import CharField, TextField


class Waypoint(models.Model):
    name = models.CharField(max_length=5)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.name}"


class Aircraft(models.Model):
    type = models.CharField(max_length=30)
    acft_range = models.IntegerField()
    fuel_consumption = models.IntegerField()
    fuel_capacity = models.IntegerField()
    avg_speed = models.IntegerField()

    def __str__(self):
        return f"{self.type}"


class Airport(models.Model):
    ICAO = models.CharField(max_length=4)
    name = models.CharField(max_length=60)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.ICAO}"


class FlightPlan(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    departure_apt_id = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name="departure_apt_id")
    arrival_apt_id = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name="arrival_apt_id")
    aircraft_id = models.ForeignKey(Aircraft, on_delete=models.DO_NOTHING)
    # waypoints = TextField()
    waypoints = models.ManyToManyField(Waypoint, null=True)
    fob = models.IntegerField()
    # waypoint = models.ForeignKey(Waypoint, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.departure_apt_id} - {self.arrival_apt_id}"
#     #
#     # def __hash__(self):
#     #     return hash(str(self))
#

#
#
#     def __str__(self):
#         return f"{self.title}; {self.released.year}"
