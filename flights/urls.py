from django.urls import path

from flights.views import *

urlpatterns = [
    path('', flight_list, name='flight_list'),
    path('search_page', search_page, name='search_page'),
    path('search_results', search_flight, name='search_flight'),
    path('detail/<pk>/', FlightDetailView.as_view(), name='detail'),
    path('add_flight/', add_flight, name='add_flight'),
    path('save_flight/', save_flight, name='save_flight'),
    path('delete/<pk>/', FlightDeleteView.as_view(), name='delete'),
]
