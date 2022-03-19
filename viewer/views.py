from logging import getLogger

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from viewer.models import FlightPlan, Airport, Waypoint
from viewer.forms import AirportForm, WaypointForm, FlightPlanForm

LOG = getLogger()

def airport_search(request):
    airport_icao = request.GET.get("airport_icao")
    if airport_icao:
        data = Airport.objects.filter(ICAO__contains=airport_icao)
        return render(request, "airport_search.html", context={'data': data, 'count': data.count()})
    return render(request, "airport_search.html", context={'data': None, 'count': 0})

def waypoint_search(request):
    waypoint_name = request.GET.get("waypoint_name")
    if waypoint_name:
        data = Waypoint.objects.filter(name__contains=waypoint_name)
        return render(request, "waypoint_search.html", context={'data': data, 'count': data.count()})
    return render(request, "waypoint_search.html", context={'data': None, 'count': 0})

class FlightCalculatorView(ListView):
    template_name = "base.html"
    model = FlightPlan
    paginate_by = 6

class FlightPlansView(ListView):
    template_name = "flight_plans.html"
    model = FlightPlan
    paginate_by = 5

class AirportsView(ListView):
    template_name = "airports.html"
    model = Airport
    paginate_by = 200

class WaypointsView(ListView):
    template_name = "waypoints.html"
    model = Waypoint
    paginate_by = 200


class AirportCreateView(CreateView):
    template_name = 'forms/form.html'
    form_class = AirportForm
    success_url = reverse_lazy('viewer:airports')
    # permission_required = "viewer.add_movie"

    def form_invalid(self, form):
        LOG.warning("User provided invalid data.")
        return super().form_invalid(form)

class WaypointCreateView(CreateView):
    template_name = 'forms/form.html'
    form_class = WaypointForm
    success_url = reverse_lazy('viewer:waypoints')
    # permission_required = "viewer.add_movie"

    def form_invalid(self, form):
        LOG.warning("User provided invalid data.")
        return super().form_invalid(form)

class FlightPlanCreateView(CreateView):
    template_name = 'forms/form.html'
    form_class = FlightPlanForm
    success_url = reverse_lazy('viewer:flight_plans')
    # permission_required = "viewer.add_movie"

    def form_invalid(self, form):
        LOG.warning("User provided invalid data.")
        return super().form_invalid(form)

class AirportDeleteView(DeleteView):
    template_name = "forms/airport_delete_form.html"
    model = Airport
    success_url = reverse_lazy('viewer:airports')
    # permission_required = "viewer.delete_movie"

    # def test_func(self):
    #     return super().test_func() and self.request.user.is_superuser

class WaypointDeleteView(DeleteView):
    template_name = "forms/waypoint_delete_form.html"
    model = Waypoint
    success_url = reverse_lazy('viewer:waypoints')