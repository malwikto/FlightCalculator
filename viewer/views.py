from django.shortcuts import render
from django.views.generic import ListView

from viewer.models import FlightPlan, Airport

def search(request):
    airport_icao = request.GET.get("airport_icao")
    if airport_icao:
        data = Airport.objects.filter(ICAO__contains=airport_icao)
        return render(request, "search.html", context={'data': data, 'count': data.count()})
    return render(request, "search.html", context={'data': None, 'count': 0})

class FlightCalculatorView(ListView):
    template_name = "base.html"
    model = FlightPlan
    paginate_by = 6

class AirportsView(ListView):
    template_name = "airports.html"
    model = Airport
    paginate_by = 200