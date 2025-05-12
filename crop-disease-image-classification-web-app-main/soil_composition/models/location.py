import requests
import logging
from django.conf import settings
from ipstack import GeoLookup

logger = logging.getLogger(__name__)

# Singleton pattern for location lookup
class LocationLookup:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocationLookup, cls).__new__(cls)
            cls._instance.geo_lookup = GeoLookup("aa3597740168c50609f2767a6430e238")
        return cls._instance
    
    def get_user_location(self, ip_address=None):
        """Get location from IP address or default to client IP"""
        try:
            # Add a timeout to the request
            import time
            start_time = time.time()
            
            if ip_address:
                location = self.geo_lookup.get_location(ip_address)
            else:
                try:
                    location = self.geo_lookup.get_own_location()
                except Exception as ipstack_error:
                    logger.error(f"IPStack error: {str(ipstack_error)}")
                    # Fall back to a default location in Tunisia
                    return {
                        'error': f'Could not detect location: {str(ipstack_error)}',
                        'latitude': 36.8065,  # Tunis coordinates
                        'longitude': 10.1815,
                        'region': 'Tunis (Default)',
                        'city': 'Tunis',
                        'country': 'Tunisia'
                    }
            
            # Log how long the request took
            logger.info(f"IPStack lookup took {time.time() - start_time:.2f} seconds")
            
            # Validate the response
            if not location or not isinstance(location, dict):
                logger.error(f"Invalid location response: {location}")
                return {
                    'error': 'Invalid location data received',
                    'latitude': 36.8065,  # Default to Tunis
                    'longitude': 10.1815,
                    'region': 'Tunis (Default)',
                    'city': 'Tunis',
                    'country': 'Tunisia'
                }
            
            # Log the full location data for debugging
            logger.debug(f"IPStack location data: {location}")
            
            # Check if location is in Tunisia
            if location.get('country_code') != 'TN':
                return {
                    'error': 'Location not in Tunisia',
                    'latitude': location.get('latitude'),
                    'longitude': location.get('longitude'),
                    'region': location.get('region_name'),
                    'city': location.get('city', 'Unknown'),
                    'country': location.get('country_name')
                }
            
            return {
                'latitude': location.get('latitude'),
                'longitude': location.get('longitude'),
                'region': location.get('region_name'),
                'city': location.get('city', 'Unknown'),
                'country': location.get('country_name', 'Tunisia')
            }
        except Exception as e:
            logger.error(f"Error in location lookup: {str(e)}")
            return {
                'error': f'Location detection failed: {str(e)}',
                'latitude': 36.8065,  # Default to Tunis
                'longitude': 10.1815,
                'region': 'Tunis (Default)',
                'city': 'Tunis',
                'country': 'Tunisia'
            }

def get_coords_from_city(city_name):
    """Get coordinates from city name using Nominatim API"""
    try:
        # Using OpenStreetMap's Nominatim service
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{city_name}, Tunisia",
            'format': 'json',
            'limit': 1,
            'countrycodes': 'tn'
        }
        headers = {
            'User-Agent': 'SoilCompositionApp/1.0'
        }
        
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        
        if data and len(data) > 0:
            return {
                'latitude': float(data[0]['lat']),
                'longitude': float(data[0]['lon']),
                'display_name': data[0]['display_name']
            }
        else:
            return {'error': 'City not found in Tunisia'}
    except Exception as e:
        logger.error(f"Error in city lookup: {str(e)}")
        return {'error': str(e)}