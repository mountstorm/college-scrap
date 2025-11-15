# Cheap Stop - Quick Start Guide 🚀

Get your Cheap Stop app running in 5 minutes!

## Step 1: Get Your API Keys (2 minutes)

### Google Maps API Key
1. Visit: https://console.cloud.google.com/
2. Create/select a project
3. Enable: Maps JavaScript API, Directions API, Distance Matrix API, Places API
4. Create credentials → API Key
5. Copy the key

### Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## Step 2: Backend Setup (1 minute)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `backend/.env`:
```
GOOGLE_MAPS_API_KEY=paste-your-key-here
GEMINI_API_KEY=paste-your-key-here
```

Start backend:
```bash
python run.py
```

## Step 3: Frontend Setup (1 minute)

Open new terminal:
```bash
cd frontend
npm install
cp .env.example .env
```

Edit `frontend/.env`:
```
REACT_APP_GOOGLE_MAPS_API_KEY=paste-your-key-here
```

Start frontend:
```bash
npm start
```

## Step 4: Use the App! (1 minute)

1. Open http://localhost:3000
2. Allow location access
3. Search: "diapers, soda"
4. Set budget: 10
5. Click products to select
6. Click "Get Route"
7. See your optimized shopping route!

## Troubleshooting

**Backend won't start?**
- Make sure Python 3.8+ is installed: `python --version`
- Activate virtual environment first

**Frontend won't start?**
- Make sure Node.js is installed: `node --version`
- Try: `npm cache clean --force && npm install`

**No location?**
- Allow location in your browser
- Use Chrome/Firefox (Safari can be finicky)

**No products found?**
- Check your API keys in `.env` files
- Make sure backend is running on port 5000
- Check backend console for errors

**Map not loading?**
- Verify Google Maps API key is correct
- Check that Maps JavaScript API is enabled in Google Cloud Console

## What's Next?

- Read the full documentation: `CHEAP_STOP_README.md`
- Customize the retailers in `backend/app/scrapers/product_scraper.py`
- Adjust the UI colors in `frontend/src/styles/SearchPage.css`

Happy shopping! 🛒
