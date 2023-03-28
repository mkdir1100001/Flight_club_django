from django.contrib import admin
from django.urls import include, path

from flight_club.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='homepage'),
    path('countries/', include(('countries.urls', 'countries'))),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('flights/', include(('flights.urls', 'flights'))),
]
