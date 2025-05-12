from django.urls import path
from . import views

urlpatterns = [
    path('soil-lookup/', views.soil_lookup, name='soil_lookup'),
    path('api/get-location/', views.get_location, name='get_location'),
    path('api/search-by-city/', views.search_by_city, name='search_by_city'),
    path('api/get-soil-data/', views.get_soil_data_ajax, name='get_soil_data_ajax'),
]