"""
A* algorithm for optimal route calculation
"""
import heapq
from math import radians, sin, cos, sqrt, atan2
import os
import googlemaps

# Initialize Google Maps client
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY) if GOOGLE_MAPS_API_KEY else None


def haversine_distance(coord1, coord2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Returns distance in miles
    """
    lat1, lon1 = coord1['lat'], coord1['lng']
    lat2, lon2 = coord2['lat'], coord2['lng']

    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # Radius of earth in miles
    r = 3959
    return r * c


def get_actual_distance(origin, destination):
    """
    Get actual driving distance using Google Maps Distance Matrix API
    """
    if not gmaps:
        # Fall back to haversine distance if API not configured
        return haversine_distance(origin, destination)

    try:
        result = gmaps.distance_matrix(
            origins=[(origin['lat'], origin['lng'])],
            destinations=[(destination['lat'], destination['lng'])],
            mode='driving'
        )

        if result['rows'][0]['elements'][0]['status'] == 'OK':
            # Return distance in miles
            distance_meters = result['rows'][0]['elements'][0]['distance']['value']
            return distance_meters / 1609.34
        else:
            return haversine_distance(origin, destination)

    except Exception as e:
        print(f"Error getting actual distance: {e}")
        return haversine_distance(origin, destination)


class AStarNode:
    """
    Node for A* algorithm
    """
    def __init__(self, location, stores_visited, g_cost, h_cost, parent=None):
        self.location = location
        self.stores_visited = frozenset(stores_visited)
        self.g_cost = g_cost  # Cost from start to current node
        self.h_cost = h_cost  # Heuristic cost to goal
        self.f_cost = g_cost + h_cost  # Total cost
        self.parent = parent

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        return (self.location == other.location and
                self.stores_visited == other.stores_visited)

    def __hash__(self):
        return hash((str(self.location), self.stores_visited))


def calculate_optimal_route(products, user_location):
    """
    Calculate optimal route using A* algorithm

    Args:
        products: List of selected products with store locations
        user_location: User's starting location {lat, lng}

    Returns:
        List of stores in optimal visit order
    """
    # Group products by store location
    stores_dict = {}
    for product in products:
        if product.get('location'):
            location = product['location']
            key = f"{location['lat']},{location['lng']}"

            if key not in stores_dict:
                stores_dict[key] = {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'name': product['store'],
                    'address': location.get('address', product['store']),
                    'products': []
                }

            stores_dict[key]['products'].append(product['name'])

    stores = list(stores_dict.values())

    if not stores:
        return []

    # If only one store, return it directly
    if len(stores) == 1:
        return stores

    # Use A* to find optimal route
    start_node = AStarNode(
        location=user_location,
        stores_visited=set(),
        g_cost=0,
        h_cost=calculate_min_spanning_tree_cost(user_location, stores),
        parent=None
    )

    open_set = []
    heapq.heappush(open_set, start_node)
    closed_set = set()

    best_route = None
    best_cost = float('inf')

    while open_set:
        current = heapq.heappop(open_set)

        # If all stores visited, we found a complete route
        if len(current.stores_visited) == len(stores):
            if current.g_cost < best_cost:
                best_cost = current.g_cost
                best_route = reconstruct_path(current, stores)
            continue

        state = (str(current.location), current.stores_visited)
        if state in closed_set:
            continue
        closed_set.add(state)

        # Try visiting each unvisited store
        for idx, store in enumerate(stores):
            if idx in current.stores_visited:
                continue

            # Calculate cost to this store
            distance = get_actual_distance(current.location, store)
            new_g_cost = current.g_cost + distance

            # Calculate heuristic (remaining minimum cost)
            unvisited = [s for i, s in enumerate(stores) if i not in current.stores_visited and i != idx]
            h_cost = calculate_min_spanning_tree_cost(store, unvisited) if unvisited else 0

            new_stores_visited = set(current.stores_visited)
            new_stores_visited.add(idx)

            neighbor = AStarNode(
                location=store,
                stores_visited=new_stores_visited,
                g_cost=new_g_cost,
                h_cost=h_cost,
                parent=(current, idx)
            )

            heapq.heappush(open_set, neighbor)

    # If no route found, fall back to nearest neighbor
    if not best_route:
        best_route = nearest_neighbor_route(user_location, stores)

    return best_route


def calculate_min_spanning_tree_cost(start, stores):
    """
    Calculate minimum spanning tree cost as heuristic
    This is an admissible heuristic for A*
    """
    if not stores:
        return 0

    # Use Prim's algorithm to calculate MST cost
    visited = set()
    min_cost = 0

    # Start from the nearest store to current location
    current = min(stores, key=lambda s: haversine_distance(start, s))
    visited.add(id(current))

    while len(visited) < len(stores):
        min_edge = float('inf')
        next_store = None

        for v_store in [s for s in stores if id(s) in visited]:
            for u_store in [s for s in stores if id(s) not in visited]:
                edge_cost = haversine_distance(v_store, u_store)
                if edge_cost < min_edge:
                    min_edge = edge_cost
                    next_store = u_store

        if next_store:
            min_cost += min_edge
            visited.add(id(next_store))
        else:
            break

    return min_cost


def reconstruct_path(node, stores):
    """
    Reconstruct the path from A* result
    """
    path = []
    current = node

    while current.parent:
        parent, store_idx = current.parent
        path.append(stores[store_idx])
        current = parent

    return list(reversed(path))


def nearest_neighbor_route(start, stores):
    """
    Fallback: Simple nearest neighbor algorithm
    """
    route = []
    remaining = list(stores)
    current_location = start

    while remaining:
        nearest = min(remaining, key=lambda s: haversine_distance(current_location, s))
        route.append(nearest)
        remaining.remove(nearest)
        current_location = nearest

    return route
