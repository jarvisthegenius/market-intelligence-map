import statistics

def calculate_sales_psf(properties):
    """
    Calculate average Price Per Square Foot (PSF) for sales properties.
    """
    psf_list = []
    for prop in properties:
        price = prop.get('price')
        size = prop.get('size')
        if price and size and size > 0:
            psf_list.append(price / size)
    
    if not psf_list:
        return 0
    return statistics.mean(psf_list)

def calculate_median_rent(properties):
    """
    Calculate median rent from a list of rental properties.
    """
    rents = [prop.get('price') for prop in properties if prop.get('price')]
    if not rents:
        return 0
    return statistics.median(rents)
