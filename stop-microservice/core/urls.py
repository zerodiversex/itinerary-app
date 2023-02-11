from django.urls import path
from .views import StopView

app_name = "stops_microservice"

urlpatterns = [
    path('stops/', StopView.as_view(), name='stops'),
]