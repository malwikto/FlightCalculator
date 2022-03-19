from django.urls import path

from viewer.views import FlightCalculatorView, AirportsView, WaypointsView, airport_search, waypoint_search, \
    AirportCreateView, AirportDeleteView, WaypointCreateView, WaypointDeleteView, FlightPlansView, FlightPlanCreateView

app_name = 'viewer'
urlpatterns = [
    path('airports', AirportsView.as_view(), name="airports"),
    path('waypoints', WaypointsView.as_view(), name="waypoints"),
    path('flightplans/', FlightPlansView.as_view(), name="flight_plans"),
    path('airport/search', airport_search, name="airport_search"),
    path('airport/<int:pk>/delete/', AirportDeleteView.as_view(), name="delete_airport"),
    path('airport/add', AirportCreateView.as_view(), name="airport_add"),
    path('flightplan/add', FlightPlanCreateView.as_view(), name="flight_plan_add"),
    path('waypoint/search', waypoint_search, name="waypoint_search"),
    path('waypoint/add', WaypointCreateView.as_view(), name="waypoint_add"),
    path('waypoint/<int:pk>/delete/', WaypointDeleteView.as_view(), name="delete_waypoint"),
]