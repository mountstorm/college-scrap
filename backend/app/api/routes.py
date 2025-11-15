"""
API Routes for Cheap Stop
"""
from flask import Blueprint, jsonify, request
import os
from app.scrapers.product_scraper import scrape_products
from app.utils.route_optimizer import calculate_optimal_route
from app.utils.gemini_search import enhance_search_query, match_products
import google.generativeai as genai

api = Blueprint('api', __name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


@api.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@api.route('/search-products', methods=['POST'])
def search_products():
    """
    Search for products across multiple retailers
    """
    try:
        data = request.json
        query = data.get('query', '')
        budget = data.get('budget')
        user_location = data.get('location')

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Split query into individual items
        items = [item.strip() for item in query.split(',')]

        # Use Gemini to enhance search queries
        enhanced_queries = []
        for item in items:
            try:
                enhanced = enhance_search_query(item)
                enhanced_queries.append(enhanced)
            except Exception as e:
                print(f"Error enhancing query with Gemini: {e}")
                enhanced_queries.append(item)

        # Scrape products from retailers
        all_products = []
        for idx, item in enumerate(items):
            query_to_use = enhanced_queries[idx] if idx < len(enhanced_queries) else item
            products = scrape_products(query_to_use, user_location)
            all_products.extend(products)

        # Filter by budget if provided
        if budget:
            # Group products by item
            items_dict = {}
            for product in all_products:
                item_key = product.get('search_query', 'unknown')
                if item_key not in items_dict:
                    items_dict[item_key] = []
                items_dict[item_key].append(product)

            # For each item, only include products that fit within budget
            filtered_products = []
            for item_key, products in items_dict.items():
                affordable = [p for p in products if p['price'] <= budget]
                if affordable:
                    # Sort by price and take cheapest options
                    affordable.sort(key=lambda x: x['price'])
                    filtered_products.extend(affordable[:5])  # Top 5 cheapest per item
                else:
                    # If nothing is affordable, include cheapest option anyway
                    products.sort(key=lambda x: x['price'])
                    if products:
                        filtered_products.append(products[0])

            all_products = filtered_products

        # Use Gemini to match and rank products
        try:
            matched_products = match_products(items, all_products)
            return jsonify({'products': matched_products}), 200
        except Exception as e:
            print(f"Error matching products with Gemini: {e}")
            # Fall back to returning all products
            return jsonify({'products': all_products}), 200

    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'error': str(e)}), 500


@api.route('/calculate-route', methods=['POST'])
def calculate_route():
    """
    Calculate optimal route using A* algorithm
    """
    try:
        data = request.json
        products = data.get('products', [])
        user_location = data.get('userLocation')

        if not products:
            return jsonify({'error': 'Products are required'}), 400

        if not user_location:
            return jsonify({'error': 'User location is required'}), 400

        # Calculate optimal route
        optimized_route = calculate_optimal_route(products, user_location)

        return jsonify({'optimizedRoute': optimized_route}), 200

    except Exception as e:
        print(f"Route calculation error: {e}")
        return jsonify({'error': str(e)}), 500
