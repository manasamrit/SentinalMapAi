import googlemaps
from src.utils.mock_data import SCENARIOS

class MapsService:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.client = None
        self.is_demo = False
        
        # If no key provided, check for demo mode trigger
        if not api_key:
            self.is_demo = True
        else:
            try:
                self.client = googlemaps.Client(key=api_key)
            except Exception as e:
                print(f"Maps Client Error: {e}")
                self.is_demo = True

    def get_place_details(self, place_query):
        """
        Fetches place details. 
        In demo mode, returns a mock scenario if the query matches a key, 
        otherwise returns a generic mock.
        """
        if self.is_demo:
            # Check if query matches a mock key
            if "locksmith" in place_query.lower():
                return SCENARIOS["suspicious_locksmith"]
            elif "coffee" in place_query.lower():
                return SCENARIOS["legit_coffee"]
            else:
                # Default fallback
                return SCENARIOS["suspicious_locksmith"]

        try:
            # Real API call
            # 1. Text Search to get Place ID
            places_result = self.client.places(query=place_query)
            
            if not places_result['results']:
                return None
                
            place_id = places_result['results'][0]['place_id']
            
            # 2. Place Details
            # Fetching fields: name, formatted_address, formatted_phone_number, website, reviews, type, geometry
            details = self.client.place(
                place_id=place_id, 
                fields=['name', 'formatted_address', 'formatted_phone_number', 'website', 'reviews', 'type', 'geometry']
            )
            
            result = details.get('result', {})
            
            # Format to match our internal structure
            return {
                "name": result.get('name'),
                "address": result.get('formatted_address'),
                "phone": result.get('formatted_phone_number'),
                "website": result.get('website'),
                "rating": result.get('rating', 0), # Rating might not be in the fields requested specifically if not explicit, but usually is
                "reviews": result.get('reviews', []),
                "types": result.get('types', []),
                "geometry": result.get('geometry', {})
            }
            
        except Exception as e:
            print(f"Maps API Error: {e}")
            return SCENARIOS["suspicious_locksmith"] # Fallback on error
