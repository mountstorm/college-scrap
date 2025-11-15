# Cheap Stop 🛒🗺️

**Find the cheapest route to your shopping needs**

Cheap Stop is a smart shopping web app that searches for products across major retailers (Walmart, Target, Costco, Kroger, CVS), finds the best deals within your budget, and calculates the optimal route using A* pathfinding algorithm with Google Maps integration.

## Features

- **Multi-Retailer Search**: Search for products across Walmart, Target, Costco, Kroger, and CVS
- **Budget-Aware**: Filter products based on your budget
- **AI-Powered Search**: Uses Google Gemini AI to enhance search queries and match products
- **A* Route Optimization**: Calculates the shortest route to visit all selected stores
- **Turn-by-Turn Directions**: Google Maps integration with Apple Maps-style UI
- **Product Images**: Shows product photos directly from retailer websites
- **Search History**: Keeps track of your recent searches
- **Route History**: Saves your past shopping routes
- **Clean UI**: Target-inspired design with Apple-style fonts

## Tech Stack

### Frontend
- **React 18** - UI framework
- **React Router** - Client-side routing
- **Google Maps React** - Interactive maps with directions
- **Axios** - HTTP client
- **Apple-style fonts** - Clean, modern typography

### Backend
- **Python 3.8+** - Backend language
- **Flask** - Web framework
- **Google Gemini AI** - Intelligent product search and matching
- **Google Maps API** - Distance calculation and directions
- **BeautifulSoup4** - Web scraping
- **A* Algorithm** - Optimal route calculation

## Prerequisites

Before you begin, you'll need:

1. **Python 3.8 or higher**
2. **Node.js 14 or higher**
3. **Google Maps API Key** - [Get it here](https://developers.google.com/maps/documentation/javascript/get-api-key)
4. **Google Gemini API Key** - [Get it here](https://ai.google.dev/)

### Getting API Keys

#### Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable these APIs:
   - Maps JavaScript API
   - Directions API
   - Distance Matrix API
   - Places API
4. Go to "Credentials" and create an API key
5. Copy the API key

#### Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the API key

## Installation

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add your API keys:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here

   # Google APIs
   GOOGLE_MAPS_API_KEY=your-actual-google-maps-api-key
   GEMINI_API_KEY=your-actual-gemini-api-key
   ```

5. **Run the Flask server**
   ```bash
   python run.py
   ```

   The backend will be running at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add your Google Maps API key:
   ```
   REACT_APP_GOOGLE_MAPS_API_KEY=your-actual-google-maps-api-key
   REACT_APP_API_URL=http://localhost:5000/api
   ```

4. **Start the React development server**
   ```bash
   npm start
   ```

   The frontend will be running at `http://localhost:3000`

## Usage

1. **Allow Location Access**: When you first open the app, allow location access so the app can find nearby stores and calculate routes

2. **Search for Products**:
   - Enter product names in the search box (e.g., "diapers, soda")
   - Optionally enter your budget
   - Click "Search"

3. **Select Products**:
   - Click on product cards to select the ones you want to buy
   - You'll see the total cost update as you select products

4. **Get Your Route**:
   - Click "Get Route" to calculate the optimal path
   - The map will show turn-by-turn directions
   - Follow the directions like you would in Google Maps or Apple Maps

5. **View History**:
   - Check your recent searches to repeat past queries
   - View your route history to see past shopping trips

## How It Works

### Product Search
1. User enters search query (e.g., "diapers")
2. Gemini AI enhances the query with relevant keywords and brand names
3. Backend scrapes product data from all supported retailers
4. Products are filtered by budget if specified
5. Gemini AI ranks and matches products to the search query
6. Results are displayed with images, prices, and store info

### Route Optimization
1. User selects products from different stores
2. Backend groups products by store location
3. A* algorithm calculates the optimal route considering:
   - Current location
   - All selected store locations
   - Actual driving distances (via Google Maps)
   - Minimum total distance
4. Google Maps Directions API provides turn-by-turn navigation
5. Map displays the route with Apple Maps-style design

### A* Algorithm Details
The app uses a proper A* implementation with:
- **G-cost**: Actual distance traveled from start
- **H-cost**: Minimum spanning tree heuristic for remaining stores
- **F-cost**: G + H for path evaluation
- **Google Maps Distance Matrix**: Real driving distances, not just straight-line

## API Endpoints

### `GET /api/health`
Health check endpoint

### `POST /api/search-products`
Search for products across retailers

**Request body:**
```json
{
  "query": "diapers, soda",
  "budget": 10.0,
  "location": {
    "lat": 34.3665,
    "lng": -89.5348
  }
}
```

**Response:**
```json
{
  "products": [
    {
      "name": "Pampers Diapers",
      "price": 24.99,
      "store": "Walmart",
      "image": "https://...",
      "location": { "lat": 34.37, "lng": -89.54 },
      "distance": 2.3
    }
  ]
}
```

### `POST /api/calculate-route`
Calculate optimal route using A*

**Request body:**
```json
{
  "products": [...],
  "userLocation": {
    "lat": 34.3665,
    "lng": -89.5348
  }
}
```

**Response:**
```json
{
  "optimizedRoute": [
    {
      "lat": 34.37,
      "lng": -89.54,
      "name": "Walmart",
      "address": "123 Main St",
      "products": ["Pampers Diapers"]
    }
  ]
}
```

## Supported Retailers

- **Walmart** - General merchandise and groceries
- **Target** - General merchandise and groceries
- **Costco** - Bulk products and groceries
- **Kroger** - Groceries and pharmacy
- **CVS** - Pharmacy and convenience items

## Project Structure

```
cheap-stop/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # API endpoints
│   │   ├── scrapers/
│   │   │   └── product_scraper.py # Retailer scrapers
│   │   ├── utils/
│   │   │   ├── route_optimizer.py # A* algorithm
│   │   │   └── gemini_search.py   # Gemini AI integration
│   │   └── __init__.py            # Flask app factory
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── SearchPage.js      # Main search interface
│   │   ├── styles/
│   │   │   ├── index.css
│   │   │   └── SearchPage.css     # Apple-style design
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env.example
│
└── CHEAP_STOP_README.md
```

## Troubleshooting

### Location not working
- Make sure you've allowed location access in your browser
- Check that you're using HTTPS or localhost (browsers block location on HTTP)

### No products found
- Verify your Gemini API key is correct
- Check that the backend is running
- Look at the backend console for error messages

### Route not displaying
- Verify your Google Maps API key is correct
- Make sure you've enabled all required APIs in Google Cloud Console
- Check browser console for errors

### API Key Errors
- Double-check that your API keys are correctly copied into the `.env` files
- Ensure there are no extra spaces or quotes around the keys
- Verify the APIs are enabled in Google Cloud Console

## Future Enhancements

- [ ] Real-time price scraping from actual retailer websites
- [ ] Product reviews and ratings integration
- [ ] Multiple route options (fastest vs. cheapest)
- [ ] Save favorite shopping lists
- [ ] Share routes with friends
- [ ] Mobile app version
- [ ] Coupons and deals integration
- [ ] Nutrition information for food products
- [ ] Alternative product suggestions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Contact

For questions or support, please open an issue on GitHub.

---

Built with ❤️ to help you shop smarter and save money
