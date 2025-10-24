# How to Test CollegeScrap Right Now! 🚀

Great news! The frontend is built and ready to deploy. Here's the FASTEST way to test it:

## Option 1: Test Locally (2 Minutes) ⚡

This is the quickest way to see the app working right now!

### Terminal 1 - Start Backend
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

Backend will run at: http://localhost:5000

### Terminal 2 - Start Frontend
```bash
cd frontend
npm install  # Only needed first time
npm start
```

Frontend will run at: http://localhost:3000

**That's it!** Open http://localhost:3000 in your browser and test the app!

---

## Option 2: Deploy to GitHub Pages (5 Minutes) 🌐

To get a live URL anyone can visit:

### Step 1: Merge to Main Branch

First, you need to merge your feature branch to main:

```bash
# Option A: Via GitHub (Recommended)
# 1. Go to: https://github.com/mountstorm/college-scrap
# 2. Click "Pull Requests" > "New Pull Request"
# 3. Select your branch: claude/init-college-scrap-webapp-011CUSoP5KE9J16SzauLgsc6
# 4. Create and merge the PR

# Option B: Via Command Line
git checkout main
git merge claude/init-college-scrap-webapp-011CUSoP5KE9J16SzauLgsc6
git push origin main
```

### Step 2: Deploy to GitHub Pages

```bash
cd frontend
npm install
npm run deploy
```

This will deploy your app to: **https://mountstorm.github.io/college-scrap**

### Step 3: Enable GitHub Pages in Settings

1. Go to your repo: https://github.com/mountstorm/college-scrap/settings/pages
2. Under "Source", select: **gh-pages** branch
3. Click Save

Wait 1-2 minutes, then visit: https://mountstorm.github.io/college-scrap

### Step 4: Test with Local Backend

The deployed frontend will try to connect to http://localhost:5000, so:

1. **Run the backend locally** (see Terminal 1 commands above)
2. **Visit the GitHub Pages URL** in your browser
3. **The app will connect to your local backend!**

---

## Option 3: Full Cloud Deployment (10 Minutes) ☁️

Want a fully hosted app with no local backend needed? Deploy the backend too!

### Deploy Backend to Render (FREE)

1. **Sign up** at https://render.com (no credit card needed!)

2. **Create New Web Service**:
   - Connect your GitHub repo
   - Name: `college-scrap-backend`
   - Region: Oregon (US West)
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT run:app`

3. **Add Environment Variables**:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key-123456
   DATABASE_URL=sqlite:///collegescrap.db
   ```

4. **Click "Create Web Service"**

5. **Wait for deployment** (2-3 minutes)

6. **Copy your backend URL**: https://college-scrap-backend.onrender.com

### Update Frontend to Use Cloud Backend

1. **Edit** `frontend/.env.production`:
   ```
   REACT_APP_API_URL=https://college-scrap-backend.onrender.com/api
   ```

2. **Commit and push**:
   ```bash
   git add frontend/.env.production
   git commit -m "Update production API URL"
   git push origin main
   ```

3. **Redeploy frontend**:
   ```bash
   cd frontend
   npm run deploy
   ```

4. **Wait 1-2 minutes**, then visit: https://mountstorm.github.io/college-scrap

**Now it's fully live!** Anyone can use it without running anything locally!

---

## What You'll See

### Step 1: Degree Selection
- Select "Computer Science" major
- Choose "B.S." degree type
- Optionally add "Accounting" minor
- Select "Freshman" classification

### Step 2: Requirements Results
- Total: 120 credits breakdown
- 11 Computer Science courses listed
- Math requirements (Calculus I & II)
- GenEd requirements
- Prerequisite chains (AI requires 4 courses!)

### Step 3: Schedule Builder
- Choose semester (Fall 2025, etc.)
- Select credit load (Light/Standard/Heavy)
- Check off completed courses

### Step 4: Generated Schedule
- Balanced course schedule
- Workload warnings (e.g., "2 heavy courses")
- Download option for advisor meeting

---

## Troubleshooting

### "Failed to load majors" error
**Problem**: Frontend can't reach backend

**Solution**: Make sure backend is running at http://localhost:5000

Test with: `curl http://localhost:5000/api/health`

### GitHub Pages shows blank page
**Problem**: Build didn't deploy properly

**Solution**:
```bash
cd frontend
rm -rf build node_modules
npm install
npm run build
npm run deploy
```

### Backend database is empty
**Problem**: Sample data not loaded

**Solution**:
```bash
cd backend
source venv/bin/activate
python -m app.scrapers.catalog_scraper
```

### CORS errors in browser console
**Problem**: Backend not allowing frontend domain

**Solution**: Backend CORS is already configured for localhost and GitHub Pages. If still seeing errors, check that backend is running.

---

## Quick Commands Reference

```bash
# Start backend
cd backend && source venv/bin/activate && python run.py

# Start frontend locally
cd frontend && npm start

# Build frontend
cd frontend && npm run build

# Deploy to GitHub Pages
cd frontend && npm run deploy

# Check backend is running
curl http://localhost:5000/api/health

# Check frontend build
cd frontend && ls -la build/

# Reinitialize database
cd backend && python -m app.scrapers.catalog_scraper
```

---

## What's Working Right Now ✅

- ✅ Complete React frontend (4 pages)
- ✅ Flask REST API (6 endpoints)
- ✅ SQLite database with sample data
- ✅ 11 courses with prerequisites
- ✅ Computer Science B.S. major
- ✅ Degree analyzer algorithm
- ✅ Schedule generator with workload balancing
- ✅ Production build ready
- ✅ GitHub Pages configured

## What You Need to Do 📝

1. **Test locally** (Option 1) - Fastest way to see it working
2. **Deploy to GitHub Pages** (Option 2) - Get a live URL
3. **Deploy backend** (Option 3) - Make it fully cloud-hosted

---

## Screenshots & Demo

Once deployed, your app will look like this:

**Homepage**: Purple gradient background with clean white card
**Step 1**: Dropdown selectors for major/minor/classification
**Step 2**: Stats cards showing credit breakdown, course lists with badges
**Step 3**: Checkboxes for completed courses
**Step 4**: Final schedule with warnings and download button

The UI is fully responsive and looks great on mobile!

---

## Next Steps After Testing

1. ⭐ **Add more courses** in `backend/app/scrapers/catalog_scraper.py`
2. 🔍 **Implement real web scraping** from Ole Miss catalog
3. 📱 **Test on mobile devices**
4. 🎨 **Customize colors/styling** in `frontend/src/styles/index.css`
5. 📊 **Add more majors** (Engineering, Business, etc.)
6. 🚀 **Deploy to production** with PostgreSQL database

---

## Need Help?

1. Check the `DEPLOYMENT_GUIDE.md` for detailed instructions
2. Check the `README.md` for full documentation
3. Check browser console for errors (F12)
4. Check backend logs in terminal

**Enjoy testing your new degree planning app!** 🎓
