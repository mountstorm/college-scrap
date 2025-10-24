# Deployment Guide for CollegeScrap

## GitHub Pages Deployment (Frontend Only)

The frontend is now configured for GitHub Pages! Here's how to test it:

### Option 1: GitHub Pages + Local Backend (Recommended for Testing)

This is the easiest way to test the app right now.

**Step 1: Deploy Frontend to GitHub Pages**

Already configured! The frontend will be available at:
https://mountstorm.github.io/college-scrap

**Step 2: Run Backend Locally**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -c "from app.models.database import init_db; init_db()"
python -m app.scrapers.catalog_scraper
python run.py
```

Backend runs at: http://localhost:5000

**Step 3: Open the App**

Visit https://mountstorm.github.io/college-scrap and it will connect to your local backend!

### Option 2: Full Cloud Deployment (For Production)

For a fully hosted version that anyone can access:

#### Deploy Backend to Render (Free)

1. **Create account** at https://render.com (no credit card needed)

2. **Create new Web Service**
   - Connect your GitHub repo
   - Select `backend` directory
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT run:app`

3. **Add Environment Variables**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key-here
   DATABASE_URL=sqlite:///collegescrap.db
   ```

4. **Deploy** - Render will give you a URL like:
   `https://college-scrap-backend.onrender.com`

#### Update Frontend for Production Backend

1. **Update** `frontend/.env.production`:
   ```
   REACT_APP_API_URL=https://college-scrap-backend.onrender.com/api
   ```

2. **Commit and push** the change

3. **Redeploy to GitHub Pages**:
   ```bash
   cd frontend
   npm install
   npm run deploy
   ```

Now your app is fully live at:
- Frontend: https://mountstorm.github.io/college-scrap
- Backend: https://college-scrap-backend.onrender.com

### Option 3: Deploy Backend to Railway (Alternative)

Railway is even easier but requires credit card (free $5/month credit):

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy**:
   ```bash
   cd backend
   railway login
   railway init
   railway up
   ```

3. **Get your backend URL** from Railway dashboard

4. **Update frontend .env.production** with your Railway URL

5. **Redeploy frontend**:
   ```bash
   cd frontend
   npm run deploy
   ```

### Option 4: Deploy Backend to PythonAnywhere (Free)

1. **Create account** at https://www.pythonanywhere.com

2. **Upload your code** or clone from GitHub

3. **Set up virtual environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 collegescrap
   pip install -r requirements.txt
   ```

4. **Configure Web App**:
   - Framework: Flask
   - Python version: 3.10
   - Source code: `/home/yourusername/college-scrap/backend`
   - WSGI file: Point to `run.py`

5. **Initialize database** in PythonAnywhere console:
   ```python
   from app.models.database import init_db
   init_db()
   from app.scrapers.catalog_scraper import OleMissCatalogScraper
   scraper = OleMissCatalogScraper()
   scraper.populate_database()
   ```

6. **Your backend URL**: `https://yourusername.pythonanywhere.com`

7. **Update frontend .env.production** with PythonAnywhere URL

8. **Redeploy frontend**

## Testing Locally Before Deployment

Always test locally first:

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm install
npm start
```

Visit: http://localhost:3000

## Current Status

✅ Frontend configured for GitHub Pages
✅ Production build ready
✅ Router configured with basename
✅ API service ready for environment variables

⏳ Backend needs to be deployed to a hosting service
⏳ Production .env needs to be updated with backend URL

## Deploying to GitHub Pages

To deploy the frontend:

```bash
cd frontend
npm install           # Install dependencies including gh-pages
npm run deploy        # Build and deploy to GitHub Pages
```

This will:
1. Build the React app for production
2. Deploy to gh-pages branch
3. Make it available at https://mountstorm.github.io/college-scrap

## Important Notes

1. **CORS**: When deploying backend, make sure CORS allows your GitHub Pages domain
2. **Database**: SQLite works for testing, but use PostgreSQL for production
3. **Environment Variables**: Never commit .env files with secrets
4. **GitHub Pages Limitations**: Only serves static files, no backend
5. **Free Tier Limits**:
   - Render: Free tier sleeps after 15 min of inactivity
   - PythonAnywhere: Limited requests per day
   - Railway: $5/month free credit

## Recommended Architecture

**For Testing/Portfolio**:
- Frontend: GitHub Pages (free, fast)
- Backend: Render free tier or PythonAnywhere

**For Production**:
- Frontend: Vercel or Netlify (free)
- Backend: Render paid tier or AWS EC2
- Database: PostgreSQL on Render or AWS RDS

## Quick Deploy Commands

```bash
# Deploy frontend to GitHub Pages
cd frontend && npm install && npm run deploy

# Deploy backend to Render (via dashboard)
# 1. Go to https://render.com
# 2. Connect GitHub
# 3. Select backend directory
# 4. Deploy

# Check deployment
curl https://mountstorm.github.io/college-scrap
curl https://your-backend.onrender.com/api/health
```

## Troubleshooting

**Frontend shows CORS error**:
- Check backend CORS settings in `backend/app/__init__.py`
- Make sure backend allows GitHub Pages domain

**API calls fail**:
- Check .env.production has correct backend URL
- Verify backend is running and accessible
- Check browser console for exact error

**GitHub Pages shows 404**:
- Check homepage in package.json is correct
- Verify gh-pages branch exists
- Check GitHub repo settings > Pages

**Backend database empty**:
- Run the catalog scraper to populate data:
  ```bash
  python -m app.scrapers.catalog_scraper
  ```

## Need Help?

1. Check logs in your hosting service dashboard
2. Test API endpoints directly with curl or Postman
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly
