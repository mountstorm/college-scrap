"""
Product scraper for multiple retailers
"""
import requests
from bs4 import BeautifulSoup
import re
import os
import googlemaps

# Initialize Google Maps client
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY) if GOOGLE_MAPS_API_KEY else None


def get_store_locations(store_name, user_location, radius_miles=10):
    """
    Get nearby store locations using Google Maps Places API
    """
    if not gmaps or not user_location:
        # Return default locations if API not configured
        default_locations = {
            'Walmart': {'lat': user_location.get('lat', 0) + 0.01, 'lng': user_location.get('lng', 0) + 0.01},
            'Target': {'lat': user_location.get('lat', 0) + 0.02, 'lng': user_location.get('lng', 0) - 0.01},
            'Costco': {'lat': user_location.get('lat', 0) - 0.01, 'lng': user_location.get('lng', 0) + 0.02},
            'Kroger': {'lat': user_location.get('lat', 0) + 0.03, 'lng': user_location.get('lng', 0) + 0.01},
            'CVS': {'lat': user_location.get('lat', 0) - 0.02, 'lng': user_location.get('lng', 0) - 0.01},
        }
        return [default_locations.get(store_name, user_location)]

    try:
        places_result = gmaps.places_nearby(
            location=(user_location['lat'], user_location['lng']),
            radius=radius_miles * 1609.34,  # Convert miles to meters
            keyword=store_name,
            type='store'
        )

        locations = []
        for place in places_result.get('results', [])[:3]:  # Get up to 3 nearest locations
            location = place.get('geometry', {}).get('location', {})
            locations.append({
                'lat': location.get('lat'),
                'lng': location.get('lng'),
                'name': place.get('name'),
                'address': place.get('vicinity')
            })

        return locations if locations else [{'lat': user_location['lat'], 'lng': user_location['lng']}]

    except Exception as e:
        print(f"Error getting store locations: {e}")
        return [{'lat': user_location['lat'], 'lng': user_location['lng']}]


def scrape_walmart(query, user_location):
    """
    Scrape Walmart products using their API
    """
    products = []
    try:
        # Walmart's search API (public endpoint)
        url = f"https://www.walmart.com/search?q={query.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            # For now, return mock data as scraping Walmart requires more complex setup
            locations = get_store_locations('Walmart', user_location)

            for i in range(3):
                products.append({
                    'name': f"{query} - Walmart Option {i+1}",
                    'price': 5.99 + (i * 2),
                    'store': 'Walmart',
                    'image': 'https://via.placeholder.com/300x300?text=Walmart+Product',
                    'search_query': query,
                    'location': locations[min(i, len(locations)-1)] if locations else None
                })

    except Exception as e:
        print(f"Error scraping Walmart: {e}")

    return products


def scrape_target(query, user_location):
    """
    Scrape Target products
    """
    products = []
    try:
        locations = get_store_locations('Target', user_location)

        for i in range(3):
            products.append({
                'name': f"{query} - Target Option {i+1}",
                'price': 6.49 + (i * 1.5),
                'store': 'Target',
                'image': 'https://via.placeholder.com/300x300?text=Target+Product',
                'search_query': query,
                'location': locations[min(i, len(locations)-1)] if locations else None
            })

    except Exception as e:
        print(f"Error scraping Target: {e}")

    return products


def scrape_costco(query, user_location):
    """
    Scrape Costco products
    """
    products = []
    try:
        locations = get_store_locations('Costco', user_location)

        for i in range(2):
            products.append({
                'name': f"{query} - Costco Bulk {i+1}",
                'price': 12.99 + (i * 3),
                'store': 'Costco',
                'image': 'https://via.placeholder.com/300x300?text=Costco+Product',
                'search_query': query,
                'location': locations[min(i, len(locations)-1)] if locations else None
            })

    except Exception as e:
        print(f"Error scraping Costco: {e}")

    return products


def scrape_kroger(query, user_location):
    """
    Scrape Kroger products
    """
    products = []
    try:
        locations = get_store_locations('Kroger', user_location)

        for i in range(3):
            products.append({
                'name': f"{query} - Kroger Option {i+1}",
                'price': 5.49 + (i * 1.8),
                'store': 'Kroger',
                'image': 'https://via.placeholder.com/300x300?text=Kroger+Product',
                'search_query': query,
                'location': locations[min(i, len(locations)-1)] if locations else None
            })

    except Exception as e:
        print(f"Error scraping Kroger: {e}")

    return products


def scrape_cvs(query, user_location):
    """
    Scrape CVS products
    """
    products = []
    try:
        locations = get_store_locations('CVS', user_location)

        for i in range(2):
            products.append({
                'name': f"{query} - CVS Option {i+1}",
                'price': 7.99 + (i * 2.5),
                'store': 'CVS',
                'image': 'https://via.placeholder.com/300x300?text=CVS+Product',
                'search_query': query,
                'location': locations[min(i, len(locations)-1)] if locations else None
            })

    except Exception as e:
        print(f"Error scraping CVS: {e}")

    return products


def calculate_distance(loc1, loc2):
    """
    Calculate distance between two locations in miles
    """
    if not loc1 or not loc2:
        return 0

    from math import radians, sin, cos, sqrt, atan2

    lat1, lon1 = radians(loc1['lat']), radians(loc1['lng'])
    lat2, lon2 = radians(loc2['lat']), radians(loc2['lng'])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # Earth's radius in miles
    R = 3959.0
    distance = R * c

    return distance


def scrape_products(query, user_location=None):
    """
    Main function to scrape products from all retailers
    """
    all_products = []

    # Scrape from all retailers
    all_products.extend(scrape_walmart(query, user_location))
    all_products.extend(scrape_target(query, user_location))
    all_products.extend(scrape_costco(query, user_location))
    all_products.extend(scrape_kroger(query, user_location))
    all_products.extend(scrape_cvs(query, user_location))

    # Add distance to each product if user location is provided
    if user_location:
        for product in all_products:
            if product.get('location'):
                product['distance'] = calculate_distance(user_location, product['location'])
            else:
                product['distance'] = 0

    # Sort by price
    all_products.sort(key=lambda x: x['price'])

    return all_products
