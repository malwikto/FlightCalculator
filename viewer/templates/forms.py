from django.forms import ModelForm, CharField, DecimalField

from viewer.models import Airport, Waypoint


class AirportForm(ModelForm):
    class Meta:
        model = Airport
        fields = '__all__'

    ICAO = CharField(max_length=4, min_length=4)
    name = CharField(max_length=40)
    lat = DecimalField(max_digits=8, decimal_places=6)
    lon = DecimalField(max_digits=9, decimal_places=6)

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