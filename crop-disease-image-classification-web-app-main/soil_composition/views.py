from django.shortcuts import render
from django.http import JsonResponse
from .models.location import LocationLookup, get_coords_from_city
import logging
import json
import pandas as pd
import os
from django.conf import settings
from shapely.geometry import Point, Polygon
import numpy as np

logger = logging.getLogger(__name__)

def soil_lookup(request):
    """Render the initial soil lookup page"""
    context = {
        'title': 'Soil Composition Lookup'
    }
    return render(request, 'soil_composition/soil_lookup.html', context)

def get_location(request):
    """Get user location from IP address"""
    try:
        location_lookup = LocationLookup()
        location = location_lookup.get_user_location()
        
        # Log the response for debugging
        logger.info(f"Location API response: {location}")
        
        # Add a default response if location is empty
        if not location or not isinstance(location, dict):
            return JsonResponse({
                'error': 'Unable to detect location',
                'latitude': 36.8065,  # Default to Tunis coordinates
                'longitude': 10.1815,
                'region': 'Tunis (Default)',
                'city': 'Tunis'
            })
            
        return JsonResponse(location)
    except Exception as e:
        logger.error(f"Error in get_location view: {str(e)}")
        return JsonResponse({
            'error': f'Location detection failed: {str(e)}',
            'latitude': 36.8065,  # Default to Tunis coordinates
            'longitude': 10.1815,
            'region': 'Tunis (Default)',
            'city': 'Tunis'
        })

def search_by_city(request):
    """Search coordinates by city name"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city_name = data.get('city', '')
            
            if not city_name:
                return JsonResponse({'error': 'City name is required'}, status=400)
                
            location = get_coords_from_city(city_name)
            
            if 'error' in location:
                return JsonResponse(location, status=404)
                
            # If city is found, get soil data for these coordinates
            soil_data = get_soil_data(location['latitude'], location['longitude'])
            location.update(soil_data)
                
            return JsonResponse(location)
            
        except Exception as e:
            logger.error(f"Error in city search: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST request required'}, status=400)

def get_soil_data(lat, lon):
    """Get soil data from CSV files based on coordinates"""
    try:
        # Log the request
        logger.info(f"Getting soil data for coordinates: {lat}, {lon}")
        
        # Create point from coordinates
        point = Point(lon, lat)
        
        # Load CSV files
        base_dir = os.path.join(settings.BASE_DIR, 'soil_composition', 'soil data')
        
        # Initialize result
        result = {
            'params': None,
            'soter': None,
            'units': None
        }
        
        # Try to load and process each CSV file separately to handle potential file errors
        try:
            params_file = os.path.join(base_dir, 'cleaned_params_data.csv')
            if os.path.exists(params_file):
                params_df = pd.read_csv(params_file)
                logger.info(f"Loaded params data with {len(params_df)} rows")
                
                # Search in params data
                for idx, row in params_df.iterrows():
                    try:
                        if 'polygon' in row and row['polygon']:
                            # If polygon data exists, check if point inside polygon
                            try:
                                coords = json.loads(row['polygon']) if isinstance(row['polygon'], str) else row['polygon']
                                polygon = Polygon(coords)
                                if polygon.contains(point):
                                    result['params'] = row.to_dict()
                                    break
                            except Exception as polygon_error:
                                logger.warning(f"Error processing polygon in params data: {str(polygon_error)}")
                                continue
                                
                        elif 'latitude' in row and 'longitude' in row:
                            # If just coordinates, check proximity (within ~1km)
                            try:
                                lat_val = float(row['latitude'])
                                lon_val = float(row['longitude'])
                                distance = np.sqrt((lat_val - lat)**2 + (lon_val - lon)**2)
                                if distance < 0.01:  # ~1km at equator
                                    result['params'] = row.to_dict()
                                    break
                            except Exception as coord_error:
                                logger.warning(f"Error processing coordinates in params data: {str(coord_error)}")
                                continue
                    except Exception as row_error:
                        logger.warning(f"Error processing row in params data: {str(row_error)}")
                        continue
            else:
                logger.warning(f"Params file not found: {params_file}")
        except Exception as params_error:
            logger.error(f"Error processing params data: {str(params_error)}")
        
        # Search in soter data with similar logic
        try:
            soter_file = os.path.join(base_dir, 'cleaned_soter_data.csv')
            if os.path.exists(soter_file):
                soter_df = pd.read_csv(soter_file)
                logger.info(f"Loaded soter data with {len(soter_df)} rows")
                
                for idx, row in soter_df.iterrows():
                    try:
                        if 'polygon' in row and row['polygon']:
                            try:
                                coords = json.loads(row['polygon']) if isinstance(row['polygon'], str) else row['polygon']
                                polygon = Polygon(coords)
                                if polygon.contains(point):
                                    result['soter'] = row.to_dict()
                                    break
                            except Exception as polygon_error:
                                continue
                                
                        elif 'latitude' in row and 'longitude' in row:
                            try:
                                lat_val = float(row['latitude'])
                                lon_val = float(row['longitude'])
                                distance = np.sqrt((lat_val - lat)**2 + (lon_val - lon)**2)
                                if distance < 0.01:
                                    result['soter'] = row.to_dict()
                                    break
                            except Exception as coord_error:
                                continue
                    except Exception as row_error:
                        continue
            else:
                logger.warning(f"Soter file not found: {soter_file}")
        except Exception as soter_error:
            logger.error(f"Error processing soter data: {str(soter_error)}")
        
        # Search in units data with similar logic
        try:
            units_file = os.path.join(base_dir, 'cleaned_units_data.csv')
            if os.path.exists(units_file):
                units_df = pd.read_csv(units_file)
                logger.info(f"Loaded units data with {len(units_df)} rows")
                
                for idx, row in units_df.iterrows():
                    try:
                        if 'polygon' in row and row['polygon']:
                            try:
                                coords = json.loads(row['polygon']) if isinstance(row['polygon'], str) else row['polygon']
                                polygon = Polygon(coords)
                                if polygon.contains(point):
                                    result['units'] = row.to_dict()
                                    break
                            except Exception as polygon_error:
                                continue
                                
                        elif 'latitude' in row and 'longitude' in row:
                            try:
                                lat_val = float(row['latitude'])
                                lon_val = float(row['longitude'])
                                distance = np.sqrt((lat_val - lat)**2 + (lon_val - lon)**2)
                                if distance < 0.01:
                                    result['units'] = row.to_dict()
                                    break
                            except Exception as coord_error:
                                continue
                    except Exception as row_error:
                        continue
            else:
                logger.warning(f"Units file not found: {units_file}")
        except Exception as units_error:
            logger.error(f"Error processing units data: {str(units_error)}")
        
        # Check if any data was found
        if not any(result.values()):
            logger.warning(f"No soil data found for coordinates: {lat}, {lon}")
            return {
                'error': 'No soil data found for these coordinates',
                'coordinates': {
                    'latitude': lat,
                    'longitude': lon
                }
            }
        
        logger.info(f"Successfully found soil data for coordinates: {lat}, {lon}")
        return {'soil_data': result}
        
    except Exception as e:
        logger.error(f"Error getting soil data: {str(e)}")
        return {
            'error': f'Error retrieving soil data: {str(e)}',
            'coordinates': {
                'latitude': lat,
                'longitude': lon
            }
        }

def get_soil_data_ajax(request):
    """AJAX endpoint to get soil data for coordinates"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = float(data.get('latitude'))
            lon = float(data.get('longitude'))
            
            soil_data = get_soil_data(lat, lon)
            return JsonResponse(soil_data)
            
        except Exception as e:
            logger.error(f"Error in AJAX soil data lookup: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST request required'}, status=400)