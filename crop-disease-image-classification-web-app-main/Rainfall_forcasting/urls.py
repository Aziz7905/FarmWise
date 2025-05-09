from django.urls import path
from .views import rainfall_forecast_view

urlpatterns = [
    path('Rforecast/', rainfall_forecast_view, name='rainfall_forecast'),
]
