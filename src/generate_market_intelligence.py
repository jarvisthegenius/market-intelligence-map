#!/usr/bin/env python3
"""
Generate Market Intelligence data for Dubai real estate areas.
Fetches data from Property Finder API and outputs market_intelligence.json
"""

import json
import time
from datetime import datetime
from propertyfinder_client import PropertyFinderClient
from market_intelligence import process_area

# 30 Priority Areas for Proprly Market Intelligence Map
AREAS = [
    "Dubai Marina",
    "Downtown Dubai", 
    "Business Bay",
    "JVC",  # Jumeirah Village Circle
    "JVT",  # Jumeirah Village Triangle
    "Dubai Hills Estate",
    "Palm Jumeirah",
    "DIFC",
    "Dubai Creek Harbour",
    "City Walk",
    "Jumeirah Beach Residence",  # JBR
    "EMAAR Beachfront",
    "MBR City",
    "Sobha Hartland",
    "Arjan",
    "Dubai South",
    "Motor City",
    "Dubai Sports City",
    "Damac Hills",
    "Damac Lagoons",
    "Arabian Ranches",
    "Arabian Ranches 2",
    "The Valley",
    "Tilal Al Ghaf",
    "Dubai Silicon Oasis",
    "Al Furjan",
    "Discovery Gardens",
    "Mirdif",
    "Jumeirah",
    "Bluewaters Island"
]

# Map of alternative names that might work better with API
LOCATION_ALIASES = {
    "JVC": "Jumeirah Village Circle",
    "JVT": "Jumeirah Village Triangle",
    "Jumeirah Beach Residence": "JBR"
}

def main():
    client = PropertyFinderClient()
    results = []
    
    print(f"Starting Market Intelligence Generation at {datetime.utcnow().isoformat()}Z")
    print(f"Processing {len(AREAS)} areas...\n")
    
    for area in AREAS:
        # Try primary name, then alias if needed
        location_names = [area]
        if area in LOCATION_ALIASES:
            location_names.append(LOCATION_ALIASES[area])
        
        buy_listings = []
        rent_listings = []
        buy_total = 0
        rent_total = 0
        
        for location_name in location_names:
            if buy_listings and rent_listings:
                break  # Already got data
                
            print(f"Processing {area} (trying: {location_name})...")
            
            # Fetch Buy listings
            if not buy_listings:
                buy_listings, buy_total = client.fetch_all_listings("Buy", location_name, max_results=50)
            
            # Fetch Rent listings  
            if not rent_listings:
                rent_listings, rent_total = client.fetch_all_listings("Rent", location_name, max_results=50)
            
            if buy_listings or rent_listings:
                break  # Got data, no need to try aliases
        
        # Skip areas with insufficient data
        if len(buy_listings) < 5 and len(rent_listings) < 5:
            print(f"  ⚠️  Skipping {area}: insufficient data ({len(buy_listings)} buy, {len(rent_listings)} rent)")
            continue
        
        # Process area data
        area_data = process_area(buy_listings, rent_listings, buy_total, rent_total)
        area_data["name"] = area
        area_data["query_name"] = location_names[0]  # Store which name worked
        
        results.append(area_data)
        print(f"  ✓ Done: {len(buy_listings)} buy, {len(rent_listings)} rent")
        print(f"    Sales: {list(area_data['sales'].keys())}")
        print(f"    Rent: {list(area_data['rent'].keys())}")
        
        # Rate limiting - be nice to the API
        time.sleep(0.5)
    
    # Build output
    output = {
        "schema_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "PropertyFinder API",
        "refresh_frequency": "weekly",
        "rent_discount_applied": 0.075,
        "areas": results
    }
    
    # Write to file
    output_file = "market_intelligence.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Done! Processed {len(results)} areas successfully.")
    print(f"Output: {output_file}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()