"""search_flights URL Configuration"""

from django.urls import path

from app.views import SearchFlights

urlpatterns = [
    path(r'flights/search', SearchFlights.as_view(), name='SearchFlights')
]
