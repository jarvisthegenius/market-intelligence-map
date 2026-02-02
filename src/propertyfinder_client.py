import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Tuple

load_dotenv()

class PropertyFinderClient:
    """Client for UAE Real Estate API - PropertyFinder.ae Data"""
    
    def __init__(self):
        self.api_key = os.getenv("PROPERTY_FINDER_API_KEY", "5cd51e7bb4msh5c08b657b2e1006p1a49dbjsn5fd0a0608e8c")
        self.base_url = "https://uae-real-estate-api-propertyfinder-ae-data.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "uae-real-estate-api-propertyfinder-ae-data.p.rapidapi.com"
        }

    def get_properties(self, listing_category: str, location_name: str, offset: int = 0) -> Tuple[List[Dict], int]:
        """
        Fetch properties from Property Finder API.
        
        Args:
            listing_category: "Buy" or "Rent"
            location_name: Area name (e.g., "Dubai Marina")
            offset: Pagination offset
            
        Returns:
            Tuple of (listings, total_count)
        """
        url = f"{self.base_url}/properties"
        params = {
            "listing_category": listing_category,
            "location_name": location_name,
            "offset": offset
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            listings = data.get('data', [])
            total = data.get('pagination', {}).get('total', 0)
            
            return listings, total
        except Exception as e:
            print(f"Error fetching {location_name}: {e}")
            return [], 0

    def fetch_all_listings(self, listing_category: str, location_name: str, max_results: int = 50) -> List[Dict]:
        """
        Fetch up to max_results listings for a location.
        """
        listings, total = self.get_properties(listing_category, location_name, offset=0)
        return listings[:max_results]