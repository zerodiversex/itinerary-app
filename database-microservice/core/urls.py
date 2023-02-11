from django.urls import path
from .views import DummyView

app_name = "route_search_engine"

urlpatterns = [
    path('/', DummyView.as_view(), name='test'),
]