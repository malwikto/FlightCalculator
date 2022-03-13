from django.urls import path

from viewer.views import FlightCalculatorView, AirportsView, search

app_name = 'viewer'
urlpatterns = [
    path('airports', AirportsView.as_view(), name="airports"),
    path('search/', search, name="search"),
]