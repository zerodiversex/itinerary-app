from django.urls import path
from .views import DummyView

app_name = "database_microservice"

urlpatterns = [
    path('/', DummyView.as_view(), name='test'),
]