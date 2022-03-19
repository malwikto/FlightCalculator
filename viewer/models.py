from django.contrib.auth.models import User
from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, IntegerField, DateField, TextField, \
    DateTimeField, ImageField, DecimalField


class Aircraft(Model):
    type = CharField(max_length=30)
    acft_range = IntegerField()
    fuel_consumption = IntegerField()
    avg_speed = IntegerField()

    def __str__(self):


         return f"{self.type}"


class Airport(Model):
    ICAO = CharField(max_length=4)
    name = CharField(max_length=40)
    lat = DecimalField(max_digits=8, decimal_places=6)
    lon = DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):


         return f"{self.ICAO}"

class Waypoint(Model):
    name = CharField(max_length=5)
    lat = DecimalField(max_digits=8, decimal_places=6)
    lon = DecimalField(max_digits=9, decimal_places=6)


class FlightPlan(Model):
    user_id = ForeignKey(User, on_delete=DO_NOTHING)
    departure_apt_id = ForeignKey(Airport, on_delete=DO_NOTHING, related_name="departure_apt_id")
    arrival_apt_id = ForeignKey(Airport, on_delete=DO_NOTHING, related_name="arrival_apt_id")
    aircraft_id = ForeignKey(Aircraft, on_delete=DO_NOTHING)
    waypoints = CharField(max_length=300)

#     def __str__(self):
#         return f"{self.name}"
#     #
#     # def __hash__(self):
#     #     return hash(str(self))
#

#
#
#     def __str__(self):
#         return f"{self.title}; {self.released.year}"
