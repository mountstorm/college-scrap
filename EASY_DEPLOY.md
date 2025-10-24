# 🚀 Easy Deployment Guide - Get Your App Live in 5 Minutes!

## ✅ GitHub Actions is Set Up! (Automated Deployment)

I've created a GitHub Actions workflow that **automatically deploys** your frontend to GitHub Pages whenever you push to the main branch!

---

## Step 1: Push to Main Branch (1 minute)

```bash
# If you haven't already, merge your feature branch to main:
git checkout main
git merge claude/init-college-scrap-webapp-011CUSoP5KE9J16SzauLgsc6
git push origin main
```

That's it! GitHub Actions will automatically:
- ✅ Build your React app
- ✅ Deploy to GitHub Pages
- ✅ Make it live at: **https://mountstorm.github.io/college-scrap**

---

## Step 2: Enable GitHub Pages (1 minute)

1. Go to: **https://github.com/mountstorm/college-scrap/settings/pages**
2. Under **"Source"**, select: **`gh-pages`** branch
3. Click **Save**
4. Wait 2-3 minutes

Your frontend will be live at: **https://mountstorm.github.io/college-scrap** 🎉

---

## Step 3: Check Deployment Status

Visit: **https://github.com/mountstorm/college-scrap/actions**

You'll see a workflow called "Deploy to GitHub Pages" running. When it shows a green checkmark ✅, your site is live!

---

## Step 4: Deploy Backend to Render (FREE - 3 minutes)

Your frontend needs a backend API. Let's deploy it for free!

### Quick Deploy to Render:

1. **Sign up**: Go to https://render.com (no credit card needed!)

2. **New Web Service**: Click "New +" → "Web Service"

3. **Connect GitHub**:
   - Connect your GitHub account
   - Select repository: `college-scrap`

4. **Configure Service**:
   ```
   Name: college-scrap-api
   Region: Oregon (US West)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt && python -c "from app.models.database import init_db; init_db()" && python -m app.scrapers.catalog_scraper
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT run:app
   ```

5. **Add Environment Variables**:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-change-this-123456
   DATABASE_URL=sqlite:///collegescrap.db
   ```

6. **Click "Create Web Service"** (Free plan)

7. **Wait 2-3 minutes** for deployment

8. **Copy your backend URL**: something like `https://college-scrap-api.onrender.com`

---

## Step 5: Connect Frontend to Backend (2 minutes)

Now let's connect your live frontend to your live backend:

1. **Edit** `frontend/.env.production`:
   ```bash
   REACT_APP_API_URL=https://college-scrap-api.onrender.com/api
   ```
   *(Replace with your actual Render URL)*

2. **Commit and push**:
   ```bash
   git add frontend/.env.production
   git commit -m "Connect frontend to Render backend"
   git push origin main
   ```

3. **GitHub Actions will automatically redeploy** your frontend! ✨

4. **Wait 2-3 minutes**, then visit: **https://mountstorm.github.io/college-scrap**

---

## 🎉 YOU'RE LIVE!

Your app is now fully deployed and accessible to anyone!

- **Frontend**: https://mountstorm.github.io/college-scrap
- **Backend**: https://your-app.onrender.com
- **Auto-Deploy**: Every push to main automatically updates the site!

---

## 🧪 Test Your Live App

1. Visit: **https://mountstorm.github.io/college-scrap**
2. Select **"Computer Science"** major
3. Choose **"B.S."** degree type
4. Select **"Freshman"** classification
5. Click **"Analyze My Degree"** 🎓

You should see:
- 120 credit breakdown
- 11 courses with prerequisites
- GenEd requirements
- Schedule builder

---

## 🔍 Troubleshooting

### Frontend shows blank page
**Check**: https://github.com/mountstorm/college-scrap/actions

If deployment failed, click on the failed workflow to see errors.

### "Failed to load majors" error
**Problem**: Backend isn't responding

**Solution**:
1. Check your Render dashboard: https://dashboard.render.com
2. Make sure your service is running (should show green "Live")
3. Test backend directly: `curl https://your-app.onrender.com/api/health`

### Backend takes forever to load (first request)
**This is normal!** Render's free tier "sleeps" after 15 minutes of inactivity. First request wakes it up (takes ~30 seconds).

**Solution**: Just wait 30 seconds and refresh. Subsequent requests will be fast!

### CORS errors
**Problem**: Backend isn't allowing frontend domain

**Solution**: Your backend already has CORS enabled. If still seeing errors:
1. Check Render logs: Go to your service → Logs tab
2. Verify FLASK_CORS is installed: Check build logs

---

## 📊 What You Get (FREE Tier)

### GitHub Pages (Frontend)
- ✅ Unlimited bandwidth
- ✅ Free SSL certificate
- ✅ Fast CDN
- ✅ 1GB storage
- ✅ Auto-deploy on push

### Render (Backend)
- ✅ 750 hours/month (enough for 24/7)
- ✅ Free SSL certificate
- ✅ Auto-deploy on push
- ✅ 512MB RAM
- ⚠️ Sleeps after 15min inactivity (wakes in ~30s)

---

## 🎓 Share Your Project!

Your app is now live! Share the link:
**https://mountstorm.github.io/college-scrap**

Perfect for:
- Resume / portfolio
- Showing friends
- Advisor meetings
- Job applications

---

## 🔧 Future Updates

Whenever you want to update your app:

```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push origin main
```

GitHub Actions automatically redeploys! Check status at:
https://github.com/mountstorm/college-scrap/actions

---

## 📈 Next Steps

1. ✅ Deploy frontend (GitHub Pages)
2. ✅ Deploy backend (Render)
3. ✅ Connect them together
4. 🎨 Customize the UI colors/styling
5. 📚 Add more courses and majors
6. 🔍 Implement real Ole Miss catalog scraping
7. 📱 Test on mobile devices
8. 🌟 Add to your resume!

---

## Alternative: Test Locally First

If you want to test locally before deploying:

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -c "from app.models.database import init_db; init_db()"
python -m app.scrapers.catalog_scraper
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

Visit: **http://localhost:3000**

---

## 💡 Pro Tip: Custom Domain

Want a custom domain like `collegescrap.com`?

1. Buy domain from Namecheap/Google Domains (~$12/year)
2. Add CNAME file to frontend: `echo "collegescrap.com" > frontend/public/CNAME`
3. Configure DNS: Point to `mountstorm.github.io`
4. Commit and push!

---

## Need Help?

1. Check Actions logs: https://github.com/mountstorm/college-scrap/actions
2. Check Render logs: https://dashboard.render.com
3. Test API directly: `curl https://your-backend.onrender.com/api/health`
4. Check browser console (F12) for frontend errors

**You got this! 🚀**
