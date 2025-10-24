# Quick Start Guide

Get CollegeScrap running in 5 minutes!

## Prerequisites
- Python 3.8+
- Node.js 14+
- npm

## Backend (Terminal 1)

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env

# 5. Initialize database with sample data
python -c "from app.models.database import init_db; init_db()"
python -m app.scrapers.catalog_scraper

# 6. Run backend
python run.py
```

Backend running at: http://localhost:5000

## Frontend (Terminal 2)

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start React app
npm start
```

Frontend running at: http://localhost:3000

## Test the App

1. Open http://localhost:3000
2. Select "Computer Science" as major
3. Choose "B.S." degree type
4. Select "Freshman" classification
5. Click "Analyze My Degree"

## Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check Python version: `python --version` (should be 3.8+)
- Verify all dependencies installed: `pip list`

### Frontend won't start
- Check Node version: `node --version` (should be 14+)
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear npm cache: `npm cache clean --force`

### Database errors
- Delete the database and reinitialize:
  ```bash
  rm collegescrap.db
  python -c "from app.models.database import init_db; init_db()"
  python -m app.scrapers.catalog_scraper
  ```

### CORS errors
- Make sure backend is running on port 5000
- Check `frontend/package.json` has `"proxy": "http://localhost:5000"`
- Restart both servers

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API at http://localhost:5000/api/health
- Customize the database with your own courses in `backend/app/scrapers/catalog_scraper.py`
