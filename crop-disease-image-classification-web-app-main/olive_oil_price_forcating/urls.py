from django.urls import path
from .views import forecast_price_view

urlpatterns = [
    path('forecast/', forecast_price_view, name='forecast_price'),
]
