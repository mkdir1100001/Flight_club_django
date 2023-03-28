from django.urls import path

from countries.views import (CountryCreateView, CountryDeleteView,
                             CountryDetailView, CountryListView,
                             CountryUpdateView, fill_country_list)

urlpatterns = [
    path('', CountryListView.as_view(), name='home'),
    path('detail/<int:pk>/', CountryDetailView.as_view(), name='detail'),
    path('create/', CountryCreateView.as_view(), name='create'),
    path('update/<int:pk>/', CountryUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CountryDeleteView.as_view(), name='delete'),
    path('fill_country_list/', fill_country_list, name='fill_country_list'),
]
