import statistics
from typing import List, Dict, Optional
from collections import defaultdict

RENT_DISCOUNT = 0.925  # 7.5% discount from asking to estimated actual
MIN_SAMPLE_SIZE = 5

def calculate_sales_psf(listings: List[Dict]) -> Dict[str, Dict]:
    """
    Calculate median PSF from Buy listings, grouped by bedroom type.
    
    Returns:
        Dict with bedroom type as key, containing median_psf, median_price, median_size
    """
    by_bedroom = defaultdict(list)
    
    for listing in listings:
        try:
            price = float(listing.get('price', 0))
            size = float(listing.get('size', 0))
            beds = listing.get('bedrooms', '0')
            
            # Validation filters
            if price < 100000:  # Filter errors (< AED 100K)
                continue
            if size < 200:  # Filter tiny units (< 200 sqft)
                continue
            if size > 20000:  # Filter errors (> 20,000 sqft)
                continue
                
            psf = price / size
            beds_label = 'Studio' if beds == '0' else f'{beds}BR'
            
            by_bedroom[beds_label].append({
                'psf': psf,
                'price': price,
                'size': size
            })
        except (ValueError, TypeError):
            continue
    
    # Calculate medians (need minimum 5 samples)
    result = {}
    for bedroom, data in by_bedroom.items():
        if len(data) >= MIN_SAMPLE_SIZE:
            psfs = [d['psf'] for d in data]
            prices = [d['price'] for d in data]
            sizes = [d['size'] for d in data]
            
            result[bedroom] = {
                'median_psf': round(statistics.median(psfs)),
                'median_price': round(statistics.median(prices)),
                'median_size': round(statistics.median(sizes)),
                'sample_count': len(data)
            }
    
    return result


def calculate_median_rent(listings: List[Dict]) -> Dict[str, Dict]:
    """
    Calculate median rent from Rent listings, grouped by bedroom type.
    Applies 7.5% discount to convert asking → estimated actual.
    
    Returns:
        Dict with bedroom type as key, containing median_rent and sample_count
    """
    by_bedroom = defaultdict(list)
    
    for listing in listings:
        try:
            price = float(listing.get('price', 0))
            beds = listing.get('bedrooms', '0')
            
            # Validation filters
            if price < 15000:  # Filter errors (< AED 15K/year)
                continue
            if price > 2000000:  # Filter errors (> AED 2M/year)
                continue
            
            # Apply discount
            estimated_rent = price * RENT_DISCOUNT
            beds_label = 'Studio' if beds == '0' else f'{beds}BR'
            
            by_bedroom[beds_label].append(estimated_rent)
        except (ValueError, TypeError):
            continue
    
    # Calculate medians (need minimum 5 samples)
    result = {}
    for bedroom, rents in by_bedroom.items():
        if len(rents) >= MIN_SAMPLE_SIZE:
            result[bedroom] = {
                'median_rent': round(statistics.median(rents)),
                'sample_count': len(rents)
            }
    
    return result


def calculate_centroid(listings: List[Dict]) -> Optional[Dict[str, float]]:
    """
    Calculate geographic center of area from listing coordinates.
    
    Returns:
        Dict with lat/lon or None if no coordinates
    """
    coords = []
    
    for listing in listings:
        location = listing.get('location', {})
        coord = location.get('coordinates', {})
        lat = coord.get('lat')
        lon = coord.get('lon')
        
        if lat and lon:
            try:
                coords.append((float(lat), float(lon)))
            except (ValueError, TypeError):
                continue
    
    if len(coords) >= 3:
        avg_lat = sum(c[0] for c in coords) / len(coords)
        avg_lon = sum(c[1] for c in coords) / len(coords)
        return {
            'lat': round(avg_lat, 6),
            'lon': round(avg_lon, 6)
        }
    
    return None


def process_area(buy_listings: List[Dict], rent_listings: List[Dict], 
                 buy_total: int, rent_total: int) -> Dict:
    """
    Process all listings for an area and return computed metrics.
    """
    centroid = calculate_centroid(buy_listings + rent_listings)
    sales = calculate_sales_psf(buy_listings)
    rent = calculate_median_rent(rent_listings)
    
    return {
        "centroid": centroid,
        "listing_counts": {
            "buy": buy_total,
            "rent": rent_total
        },
        "sales": sales,
        "rent": rent
    }