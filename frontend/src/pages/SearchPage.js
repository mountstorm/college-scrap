import React, { useState, useEffect, useCallback } from 'react';
import { GoogleMap, DirectionsRenderer, useJsApiLoader, Marker } from '@react-google-maps/api';
import axios from 'axios';
import '../styles/SearchPage.css';

const GOOGLE_MAPS_API_KEY = process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '';

const libraries = ['places', 'directions'];

const mapContainerStyle = {
  width: '100%',
  height: '500px',
  borderRadius: '12px',
  marginTop: '20px'
};

const defaultCenter = {
  lat: 37.7749,
  lng: -122.4194
};

function SearchPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [budget, setBudget] = useState('');
  const [products, setProducts] = useState([]);
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userLocation, setUserLocation] = useState(null);
  const [directions, setDirections] = useState(null);
  const [searchHistory, setSearchHistory] = useState([]);
  const [routeHistory, setRouteHistory] = useState([]);
  const [mapCenter, setMapCenter] = useState(defaultCenter);

  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: GOOGLE_MAPS_API_KEY,
    libraries
  });

  // Get user's current location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setUserLocation(location);
          setMapCenter(location);
        },
        (error) => {
          console.error('Error getting location:', error);
          alert('Please enable location services to use route planning features.');
        }
      );
    }
  }, []);

  // Load history from localStorage
  useEffect(() => {
    const savedSearchHistory = localStorage.getItem('searchHistory');
    const savedRouteHistory = localStorage.getItem('routeHistory');
    if (savedSearchHistory) {
      setSearchHistory(JSON.parse(savedSearchHistory));
    }
    if (savedRouteHistory) {
      setRouteHistory(JSON.parse(savedRouteHistory));
    }
  }, []);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      alert('Please enter a product to search');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('/api/search-products', {
        query: searchQuery,
        budget: parseFloat(budget) || null,
        location: userLocation
      });

      setProducts(response.data.products || []);

      // Add to search history
      const newHistory = [
        { query: searchQuery, budget, timestamp: new Date().toISOString() },
        ...searchHistory.filter(h => h.query !== searchQuery).slice(0, 9)
      ];
      setSearchHistory(newHistory);
      localStorage.setItem('searchHistory', JSON.stringify(newHistory));
    } catch (error) {
      console.error('Search error:', error);
      alert('Error searching for products. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const toggleProductSelection = (product) => {
    const isSelected = selectedProducts.some(p =>
      p.name === product.name && p.store === product.store
    );

    if (isSelected) {
      setSelectedProducts(selectedProducts.filter(p =>
        !(p.name === product.name && p.store === product.store)
      ));
    } else {
      setSelectedProducts([...selectedProducts, product]);
    }
  };

  const calculateRoute = useCallback(async () => {
    if (!userLocation) {
      alert('Please allow location access to calculate routes');
      return;
    }

    if (selectedProducts.length === 0) {
      alert('Please select at least one product to create a route');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('/api/calculate-route', {
        products: selectedProducts,
        userLocation
      });

      const { optimizedRoute } = response.data;

      // Create waypoints for Google Maps
      if (window.google && optimizedRoute && optimizedRoute.length > 0) {
        const directionsService = new window.google.maps.DirectionsService();

        const waypoints = optimizedRoute.slice(1, -1).map(store => ({
          location: new window.google.maps.LatLng(store.lat, store.lng),
          stopover: true
        }));

        const origin = new window.google.maps.LatLng(userLocation.lat, userLocation.lng);
        const destination = optimizedRoute.length > 1
          ? new window.google.maps.LatLng(
              optimizedRoute[optimizedRoute.length - 1].lat,
              optimizedRoute[optimizedRoute.length - 1].lng
            )
          : new window.google.maps.LatLng(optimizedRoute[0].lat, optimizedRoute[0].lng);

        directionsService.route(
          {
            origin,
            destination,
            waypoints,
            optimizeWaypoints: false, // We already optimized with A*
            travelMode: window.google.maps.TravelMode.DRIVING
          },
          (result, status) => {
            if (status === window.google.maps.DirectionsStatus.OK) {
              setDirections(result);

              // Save to route history
              const newRoute = {
                products: selectedProducts,
                route: optimizedRoute,
                timestamp: new Date().toISOString(),
                totalDistance: result.routes[0].legs.reduce((sum, leg) => sum + leg.distance.value, 0),
                totalDuration: result.routes[0].legs.reduce((sum, leg) => sum + leg.duration.value, 0)
              };
              const newRouteHistory = [newRoute, ...routeHistory.slice(0, 9)];
              setRouteHistory(newRouteHistory);
              localStorage.setItem('routeHistory', JSON.stringify(newRouteHistory));
            } else {
              console.error('Directions request failed:', status);
              alert('Could not calculate route. Please try again.');
            }
          }
        );
      }
    } catch (error) {
      console.error('Route calculation error:', error);
      alert('Error calculating route. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [userLocation, selectedProducts, routeHistory]);

  const getTotalCost = () => {
    return selectedProducts.reduce((sum, p) => sum + p.price, 0).toFixed(2);
  };

  const clearSearchHistory = () => {
    setSearchHistory([]);
    localStorage.removeItem('searchHistory');
  };

  const clearRouteHistory = () => {
    setRouteHistory([]);
    localStorage.removeItem('routeHistory');
  };

  return (
    <div className="search-page">
      <header className="header">
        <h1 className="logo">Cheap Stop</h1>
        <p className="tagline">Find the cheapest route to your shopping needs</p>
      </header>

      <div className="search-container">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search for products (e.g., 'diapers, soda')"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="search-input"
          />
          <input
            type="number"
            placeholder="Budget ($)"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            className="budget-input"
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="search-button"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        {searchHistory.length > 0 && (
          <div className="history-section">
            <div className="history-header">
              <h3>Recent Searches</h3>
              <button onClick={clearSearchHistory} className="clear-button">Clear</button>
            </div>
            <div className="history-items">
              {searchHistory.slice(0, 5).map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setSearchQuery(item.query);
                    setBudget(item.budget);
                  }}
                  className="history-item"
                >
                  {item.query} {item.budget && `($${item.budget})`}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {products.length > 0 && (
        <div className="products-section">
          <div className="products-header">
            <h2>Available Products</h2>
            {selectedProducts.length > 0 && (
              <div className="selection-info">
                <span className="selected-count">{selectedProducts.length} items selected</span>
                <span className="total-cost">Total: ${getTotalCost()}</span>
                <button onClick={calculateRoute} className="route-button" disabled={loading}>
                  {loading ? 'Calculating...' : 'Get Route'}
                </button>
              </div>
            )}
          </div>

          <div className="products-grid">
            {products.map((product, idx) => {
              const isSelected = selectedProducts.some(p =>
                p.name === product.name && p.store === product.store
              );
              return (
                <div
                  key={idx}
                  className={`product-card ${isSelected ? 'selected' : ''}`}
                  onClick={() => toggleProductSelection(product)}
                >
                  {product.image && (
                    <img src={product.image} alt={product.name} className="product-image" />
                  )}
                  <div className="product-info">
                    <h3 className="product-name">{product.name}</h3>
                    <p className="product-store">{product.store}</p>
                    <p className="product-price">${product.price.toFixed(2)}</p>
                    {product.distance && (
                      <p className="product-distance">{product.distance.toFixed(1)} mi away</p>
                    )}
                  </div>
                  {isSelected && <div className="selected-badge">✓</div>}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {isLoaded && (
        <div className="map-section">
          <h2>Route Map</h2>
          <GoogleMap
            mapContainerStyle={mapContainerStyle}
            center={mapCenter}
            zoom={12}
            options={{
              styles: [
                {
                  featureType: 'poi',
                  elementType: 'labels',
                  stylers: [{ visibility: 'off' }]
                }
              ],
              disableDefaultUI: false,
              zoomControl: true,
              mapTypeControl: false,
              streetViewControl: false,
              fullscreenControl: true
            }}
          >
            {userLocation && !directions && (
              <Marker
                position={userLocation}
                icon={{
                  path: window.google.maps.SymbolPath.CIRCLE,
                  scale: 10,
                  fillColor: '#4285F4',
                  fillOpacity: 1,
                  strokeColor: '#ffffff',
                  strokeWeight: 2
                }}
              />
            )}
            {directions && (
              <DirectionsRenderer
                directions={directions}
                options={{
                  polylineOptions: {
                    strokeColor: '#4285F4',
                    strokeWeight: 5,
                    strokeOpacity: 0.8
                  },
                  suppressMarkers: false
                }}
              />
            )}
          </GoogleMap>

          {directions && (
            <div className="directions-panel">
              <h3>Turn-by-Turn Directions</h3>
              {directions.routes[0].legs.map((leg, legIdx) => (
                <div key={legIdx} className="leg-section">
                  <h4>Stop {legIdx + 1}: {leg.end_address}</h4>
                  <p className="leg-info">
                    Distance: {leg.distance.text} • Duration: {leg.duration.text}
                  </p>
                  <ol className="step-list">
                    {leg.steps.map((step, stepIdx) => (
                      <li
                        key={stepIdx}
                        className="step-item"
                        dangerouslySetInnerHTML={{ __html: step.instructions }}
                      />
                    ))}
                  </ol>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {routeHistory.length > 0 && (
        <div className="route-history">
          <div className="history-header">
            <h2>Route History</h2>
            <button onClick={clearRouteHistory} className="clear-button">Clear</button>
          </div>
          {routeHistory.map((route, idx) => (
            <div key={idx} className="route-history-item">
              <p className="route-date">
                {new Date(route.timestamp).toLocaleString()}
              </p>
              <p className="route-products">
                {route.products.map(p => p.name).join(', ')}
              </p>
              <p className="route-stats">
                {(route.totalDistance / 1609.34).toFixed(1)} mi • {Math.round(route.totalDuration / 60)} min
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SearchPage;
