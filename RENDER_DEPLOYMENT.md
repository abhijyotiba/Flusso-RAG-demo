# Render Deployment Guide for Flusso RAG Demo

## 🚀 Quick Deployment to Render

Follow these steps to deploy your RAG demo to Render's free tier.

---

## Prerequisites

1. ✅ A GitHub account
2. ✅ A Render account (sign up at https://render.com - free)
3. ✅ Your Gemini API key: `AIzaSyAvSB3HkGc7gN0nT4EbJU6NZzvL7FMxg_I`
4. ✅ Your Store ID: `fileSearchStores/flusso-complete-knowledge-b-n8g5l5u765nh`

---

## Step 1: Push to GitHub

### Option A: Create New Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `flusso-rag-demo`)
3. Make it **Private** (recommended) or Public
4. Don't initialize with README

### Option B: Use Git Commands

Open PowerShell in the `rag_demo` folder and run:

```powershell
cd "c:\Users\abhishek jyotiba\Downloads\Flusso-Product-Labs-Share-20251114T133529Z-1-001\Flusso-Product-Labs-Share\rag_demo"

git init
git add .
git commit -m "Initial commit - Flusso RAG Demo"

# Replace with your GitHub username and repo name
git remote add origin https://github.com/YOUR_USERNAME/flusso-rag-demo.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Render

### 2.1 Create Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account (if not already connected)
4. Select your repository: `flusso-rag-demo`
5. Click **"Connect"**

### 2.2 Configure Service

Fill in the following details:

| Field | Value |
|-------|-------|
| **Name** | `flusso-rag-demo` (or your choice) |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT` |
| **Instance Type** | `Free` |

### 2.3 Add Environment Variables

Scroll down to **"Environment Variables"** section and add:

| Key | Value |
|-----|-------|
| `GEMINI_API_KEY` | `AIzaSyAvSB3HkGc7gN0nT4EbJU6NZzvL7FMxg_I` |
| `STORE_ID` | `fileSearchStores/flusso-complete-knowledge-b-n8g5l5u765nh` |
| `PYTHON_VERSION` | `3.11.0` |
| `RENDER` | `true` |

Click **"Add"** for each variable.

### 2.4 Deploy

1. Click **"Create Web Service"** at the bottom
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your application
3. Wait 3-5 minutes for first deployment

---

## Step 3: Access Your Live Demo

Once deployment completes:

1. You'll see a green **"Live"** status
2. Your URL will be: `https://flusso-rag-demo.onrender.com` (or similar)
3. Click the URL to open your live demo!

---

## 🎯 Important Notes

### Free Tier Limitations

- ⚠️ **Spins down after 15 minutes of inactivity**
- ⏱️ **First request after spin-down takes 30-60 seconds**
- ✅ **750 hours/month free** (plenty for demos)
- ✅ **Auto-deploy on Git push**

### Custom Domain (Optional)

1. Go to **Settings** → **Custom Domain**
2. Add your domain (e.g., `demo.yourcompany.com`)
3. Update DNS records as instructed

### Auto-Deploy

Every time you push to GitHub:
```powershell
git add .
git commit -m "Update demo"
git push
```
Render automatically redeploys (takes 2-3 minutes)

---

## 🐛 Troubleshooting

### Deployment Failed

1. Check **Logs** tab in Render dashboard
2. Verify environment variables are set correctly
3. Ensure `requirements.txt` has all dependencies

### App Shows Error

1. Check **Logs** for error messages
2. Verify API key is correct
3. Test Store ID is accessible

### Slow First Load

This is normal for free tier - app spins down after inactivity. Consider:
- Upgrade to paid tier ($7/month) for always-on
- Use a ping service to keep it warm

---

## 📊 Monitoring

### View Logs

1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. See real-time application logs

### Metrics

1. Click **"Metrics"** tab
2. View:
   - Request count
   - Response time
   - Memory usage
   - CPU usage

---

## 🔒 Security Best Practices

### Protect API Keys

✅ Environment variables (already done)
✅ Private GitHub repo (recommended)
❌ Never commit `.env` file
❌ Never hardcode API keys

### Rate Limiting (Optional)

For production, consider adding rate limiting:
```python
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["100 per hour"])
```

---

## 📱 Share With Client

Once deployed, share:

1. **Live URL**: `https://your-app.onrender.com`
2. **Example Queries**: Already built into the UI
3. **Note**: First load might be slow (free tier)

---

## 🚀 Next Steps After Demo

### Upgrade Options

1. **Render Paid ($7/month)**
   - No spin-down
   - Faster response
   - More resources

2. **Google Cloud Run**
   - Pay per use
   - Better Gemini integration
   - Auto-scaling

3. **Custom Infrastructure**
   - Full control
   - Company servers
   - Enterprise features

---

## 📞 Support

If you encounter issues:

1. Check Render documentation: https://render.com/docs
2. Review deployment logs
3. Test locally first: `python backend/app.py`

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] Environment variables added
- [ ] Build command set
- [ ] Start command set
- [ ] Deployment successful
- [ ] Live URL accessible
- [ ] Test queries working
- [ ] Share URL with client

---

**Your demo is now live! 🎉**

Access it at: `https://your-app-name.onrender.com`
