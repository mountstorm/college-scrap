"""
Gemini AI integration for intelligent product search and matching
"""
import os
import google.generativeai as genai

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def enhance_search_query(query):
    """
    Use Gemini to enhance and expand search query

    Args:
        query: User's search query (e.g., "diapers")

    Returns:
        Enhanced search query with relevant keywords
    """
    if not GEMINI_API_KEY:
        return query

    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""You are a shopping assistant. Enhance this product search query to include relevant variations and brand names.

User query: "{query}"

Provide a single enhanced search query (max 10 words) that includes:
- Common brand names
- Product variations
- Key specifications

Output only the enhanced query, nothing else."""

        response = model.generate_content(prompt)
        enhanced = response.text.strip()

        # If response is too long or doesn't make sense, return original
        if len(enhanced.split()) > 15 or not enhanced:
            return query

        return enhanced

    except Exception as e:
        print(f"Error enhancing query with Gemini: {e}")
        return query


def match_products(search_queries, products):
    """
    Use Gemini to intelligently match and rank products based on search queries

    Args:
        search_queries: List of user's search queries
        products: List of scraped products

    Returns:
        Filtered and ranked list of products
    """
    if not GEMINI_API_KEY or not products:
        return products

    try:
        model = genai.GenerativeModel('gemini-pro')

        # Create a concise product summary for Gemini
        product_summary = []
        for idx, product in enumerate(products[:50]):  # Limit to first 50 to avoid token limits
            product_summary.append(f"{idx}. {product['name']} - ${product['price']} at {product['store']}")

        prompt = f"""You are a shopping assistant. Match these products to the user's search.

User is searching for: {', '.join(search_queries)}

Available products:
{chr(10).join(product_summary)}

Task: Return a comma-separated list of product indices (0-{len(product_summary)-1}) that best match the user's search, ordered by relevance. Include only products that are actually relevant to what the user is looking for.

Output format: Just the numbers separated by commas (e.g., "5,12,3,18")
"""

        response = model.generate_content(prompt)
        result = response.text.strip()

        # Parse the result
        try:
            indices = [int(x.strip()) for x in result.split(',') if x.strip().isdigit()]

            # Reorder products based on Gemini's ranking
            matched_products = []
            for idx in indices:
                if 0 <= idx < len(products):
                    matched_products.append(products[idx])

            # Add any unmatched products at the end
            for idx, product in enumerate(products):
                if idx not in indices:
                    matched_products.append(product)

            return matched_products if matched_products else products

        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return products

    except Exception as e:
        print(f"Error matching products with Gemini: {e}")
        return products


def is_product_match(product_name, query):
    """
    Use Gemini to determine if a product matches the search query

    Args:
        product_name: Name of the product
        query: User's search query

    Returns:
        Boolean indicating if it's a match
    """
    if not GEMINI_API_KEY:
        # Fallback to simple string matching
        return query.lower() in product_name.lower()

    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""Does this product match what the user is searching for?

User search: "{query}"
Product name: "{product_name}"

Answer only "YES" or "NO"."""

        response = model.generate_content(prompt)
        result = response.text.strip().upper()

        return 'YES' in result

    except Exception as e:
        print(f"Error checking product match: {e}")
        return query.lower() in product_name.lower()
