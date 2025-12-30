from src.services.maps_api import MapsService
from src.services.serp_api import SerpApiService
import time

class OsintInvestigatorAgent:
    def __init__(self, maps_key, serp_key):
        self.maps_service = MapsService(maps_key)
        self.serp_service = SerpApiService(serp_key)
        self.logs = []

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] [INVESTIGATOR] {message}")

    def investigate(self, place_query):
        self.logs = [] # Reset logs
        self.log(f"Starting investigation for query: {place_query}")
        
        # Step 1: Get Ground Truth
        self.log("Step 1: Fetching official Maps data...")
        place_data = self.maps_service.get_place_details(place_query)
        
        if not place_data:
            self.log("ERROR: Business not found on Maps.")
            return None, None
            
        self.log(f"Target Acquired: {place_data.get('name')} ({place_data.get('address')})")
        
        # Step 2: Digital Footprint
        self.log("Step 2: Searching Digital Footprint (SerpApi)...")
        osint_results = self.serp_service.search_business_footprint(
            place_data.get('name'), 
            place_data.get('phone'),
            place_data.get('address')
        )
        
        self.log(f"Found {len(osint_results)} external signals.")
        
        return place_data, osint_results
