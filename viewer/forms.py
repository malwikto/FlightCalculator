from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, DecimalField, IntegerField, MultipleChoiceField, CheckboxSelectMultiple, \
    HiddenInput

from viewer.models import Airport, Waypoint, FlightPlan, Aircraft


class FlightPlanForm(ModelForm):
    # waypoints = Waypoint.objects.all()
    # CHOICES = [(obj.name, obj.name) for obj in waypoints]
    CHOICES = []

    class Meta:
        model = FlightPlan
        fields = ['departure_apt_id', 'arrival_apt_id', 'aircraft_id', 'waypoints', 'fob']
        # fields = "__all__"
        labels = {
            # 'user_id': 'User',
            'departure_apt_id': 'Departure airport ICAO',
            'arrival_apt_id': 'Arrival airport ICAO',
            'aircraft_id': 'Aircraft ICAO type',
            'waypoints': 'Waypoints',
            'fob': 'FOB',
        }
        # widgets = {
        #     'user_id': HiddenInput()
        # }

    def clean(self):
        result = super().clean()
        if result['fob'] > result['aircraft_id'].fuel_capacity:
            self.add_error("fob", f"FOB can't be lower than fuel capacity. {result['aircraft_id'].type} fuel capacity is {result['aircraft_id'].fuel_capacity}kg")
            raise ValidationError("Please correct the data.")
        return result

    # user_id = IntegerField()
    # departure_apt_id = IntegerField(label="Deparute airport ICAO")
    # arrival_apt_id = IntegerField()
    # aircraft_id = IntegerField()
    # waypoints = CharField(max_length=300)

class AircraftForm(ModelForm):
    class Meta:
        model = Aircraft
        fields = '__all__'


class AirportForm(ModelForm):
    class Meta:
        model = Airport
        fields = '__all__'

    # ICAO = CharField(max_length=4, min_length=4)
    # name = CharField(max_length=40)
    # lat = DecimalField(max_digits=8, decimal_places=6)
    # lon = DecimalField(max_digits=9, decimal_places=6)

class WaypointForm(ModelForm):

    class Meta:
        model = Waypoint
        fields = '__all__'

    name = CharField(max_length=40)
    lat = DecimalField(max_digits=8, decimal_places=6)
    lon = DecimalField(max_digits=9, decimal_places=6)

    # def clean(self):
    #     result = super().clean()
    #     if result['genre'].name == 'Comedy' and result['rating'] > 6:
    #         self.add_error("genre", f"Can't be Comedy if {result['rating']}.")
    #         self.add_error("rating", f"Cant't be {result['rating']} if genre is Comedy.")
    #         # self.add_error("rating", f"Cant't be {result['rating']} if genre is {result['genre'].name}.") !!!Czemu nie dziala??????
    #         raise ValidationError("Comedies are not so good to be rated above 6.")
    #     return result