from logging import getLogger

import folium
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from viewer.models import FlightPlan, Airport, Waypoint, Aircraft
from viewer.forms import AirportForm, WaypointForm, FlightPlanForm, AircraftForm

from .functions import distances_list_creator, total_distance_creator, ete_calculator, total_time_calculator, \
    hdg_calculator, range_calculaor, hms2float, is_fp_to_be_achived, add_fp_markers, center_coordinates, point_map_view

# add_apt_markers

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


class StaffRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class FlightCalculatorView(ListView):
    template_name = "base.html"
    model = FlightPlan
    paginate_by = 6


class FlightPlansView(LoginRequiredMixin, ListView):
    template_name = "flight_plans.html"
    model = FlightPlan

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FlightPlansView, self).get_context_data(**kwargs)
        flight_plans = context.get('object_list')
        # for fp in flight_plans:
        #     fp.distance = calculate_distance_apt_apt(fp.departure_apt_id, fp.arrival_apt_id)
        return context


class FlightPlanWaypointsView(DetailView):
    template_name = "waypoints_fp.html"
    model = FlightPlan

    def get_context_data(self, **kwargs):
        context = super(FlightPlanWaypointsView, self).get_context_data(**kwargs)

        context.update({
            'waypoints_list': context.get('object').waypoints.all(),
        })

        distances_list_creator(context)
        total_distance_creator(context)
        ete_calculator(context)
        total_time_calculator(context)
        hdg_calculator(context)
        range_calculaor(context)
        hms2float(context.get('object').fob_range)
        is_fp_to_be_achived(context)
        center_coordinates(context)

        context.update({
            'map': add_fp_markers(context)
        })

        return context


class AirportsView(ListView):
    template_name = "airports.html"
    model = Airport
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(AirportsView, self).get_context_data(**kwargs)

        context.update({
            'airports': context.get('airport_list'),
        })
        return context

class AirportDetailView(DetailView):
    template_name = "point_map.html"
    model = Airport

    def get_context_data(self, **kwargs):
        context = super(AirportDetailView, self).get_context_data(**kwargs)
        context.update({
            'map': point_map_view(context)
        })
        return context

class WaypointDetailView(DetailView):
    template_name = "point_map.html"
    model = Waypoint

    def get_context_data(self, **kwargs):
        context = super(WaypointDetailView, self).get_context_data(**kwargs)
        context.update({
            'map': point_map_view(context)
        })
        return context

class AircraftsView(ListView):
    template_name = "aircrafts.html"
    model = Aircraft
    paginate_by = 50


class WaypointsView(ListView):
    template_name = "waypoints.html"
    model = Waypoint
    paginate_by = 50


class AirportCreateView(StaffRequiredMixin, CreateView):
    template_name = 'forms/form.html'
    form_class = AirportForm
    success_url = reverse_lazy('viewer:airports')

    # permission_required = "viewer.add_movie"

    def form_invalid(self, form):
        LOG.warning("User provided invalid data.")
        return super().form_invalid(form)


class WaypointCreateView(StaffRequiredMixin, CreateView):
    template_name = 'forms/form.html'
    form_class = WaypointForm
    success_url = reverse_lazy('viewer:waypoints')

    # permission_required = "viewer.add_movie"

    def form_invalid(self, form):
        LOG.warning("User provided invalid data.")
        return super().form_invalid(form)


class AircraftCreateView(StaffRequiredMixin, CreateView):
    template_name = 'forms/form.html'
    form_class = AircraftForm
    success_url = reverse_lazy('viewer:aircrafts')

    # permission_required = "viewer.add_movie"

    def form_invalid(self, form):
        LOG.warning("User provided invalid data.")
        return super().form_invalid(form)


class FlightPlanCreateView(CreateView):
    template_name = 'forms/form.html'
    form_class = FlightPlanForm
    success_url = reverse_lazy('viewer:flight_plans')

    # permission_required = "viewer.add_movie"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_id = self.request.user
        obj.save()
        return super(FlightPlanCreateView, self).form_valid(form)

    def form_invalid(self, form):
        LOG.warning("User provided invalid data.")
        return super().form_invalid(form)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'data':{'user_id': [self.request.user]}})
    #
    #     print(kwargs)
    #     return kwargs


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


class AircraftDeleteView(DeleteView):
    template_name = "forms/aircraft_delete_form.html"
    model = Aircraft
    success_url = reverse_lazy('viewer:aircrafts')


class FlightPlanDeleteView(DeleteView):
    template_name = "forms/flight_plan_delete_form.html"
    model = FlightPlan
    success_url = reverse_lazy('viewer:flight_plans')
