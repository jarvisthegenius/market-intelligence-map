import os
import requests
from dotenv import load_dotenv

load_dotenv()

class PropertyFinderClient:
    def __init__(self):
        self.api_key = os.getenv("PROPERTY_FINDER_API_KEY")
        self.base_url = "https://property-finder-uae.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "property-finder-uae.p.rapidapi.com"
        }

    def get_properties(self, category, location, type="for-sale"):
        """
        Fetch properties based on category and location.
        """
        url = f"{self.base_url}/properties/list"
        querystring = {"category": category, "location": location, "type": type}
        
        # Note: Implementation details to be refined by Isla
        response = requests.get(url, headers=self.headers, params=querystring)
        if response.status_code == 200:
            return response.json()
        return None
