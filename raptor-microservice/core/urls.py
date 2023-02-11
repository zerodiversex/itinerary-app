from django.urls import path
from .views import JourneyView

app_name = "raptor_microservice"

urlpatterns = [
    path('trip/', JourneyView.as_view(), name='journey'),
]