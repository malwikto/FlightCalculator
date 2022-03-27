from django.urls import path

from viewer.views import FlightCalculatorView, AirportsView, WaypointsView, airport_search, waypoint_search, \
    AirportCreateView, AirportDeleteView, WaypointCreateView, WaypointDeleteView, FlightPlansView, FlightPlanCreateView, \
    FlightPlanWaypointsView, FlightPlanDeleteView, AircraftsView, AircraftDeleteView, AircraftCreateView, \
    AirportDetailView, WaypointDetailView, AirportsMapView

app_name = 'viewer'
urlpatterns = [
    path('airports', AirportsView.as_view(), name="airports"),
    path('airports/map', AirportsMapView.as_view(), name="airports_map"),
    path('airports/<int:pk>/map', AirportDetailView.as_view(), name="airport_map"),
    path('waypoints', WaypointsView.as_view(), name="waypoints"),
    path('waypoints/<int:pk>/map', WaypointDetailView.as_view(), name="waypoint_map"),
    path('aircrafts', AircraftsView.as_view(), name="aircrafts"),
    path('flightplans/', FlightPlansView.as_view(), name="flight_plans"),
    path('airport/search', airport_search, name="airport_search"),
    path('airport/<int:pk>/delete/', AirportDeleteView.as_view(), name="delete_airport"),
    path('airport/add', AirportCreateView.as_view(), name="airport_add"),
    path('flightplan/add', FlightPlanCreateView.as_view(), name="flight_plan_add"),
    path('flightplan/<int:pk>/waypoints', FlightPlanWaypointsView.as_view(), name="flight_plan_waypoint_view"),
    path('waypoint/search', waypoint_search, name="waypoint_search"),
    path('waypoint/add', WaypointCreateView.as_view(), name="waypoint_add"),
    path('aircraft/add', AircraftCreateView.as_view(), name="aircraft_add"),
    path('waypoint/<int:pk>/delete/', WaypointDeleteView.as_view(), name="delete_waypoint"),
    path('aircraft/<int:pk>/delete/', AircraftDeleteView.as_view(), name="delete_aircraft"),
    path('flightplan/<int:pk>/delete/', FlightPlanDeleteView.as_view(), name="delete_flight_plan"),
]