from django.urls import path
from .views import JourneyView, SearchView

app_name = "route_search_engine"

urlpatterns = [
    path('trip/', JourneyView.as_view(), name='journey'),
    path('search/', SearchView.as_view(), name='search')
]