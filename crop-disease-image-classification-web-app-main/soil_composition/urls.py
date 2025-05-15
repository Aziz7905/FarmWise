from django.urls import path
from .views import choropleth_map

urlpatterns = [
    path("map/", choropleth_map, name="soil-map"),
]
