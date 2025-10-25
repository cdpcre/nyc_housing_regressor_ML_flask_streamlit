# ☁️ Cloud Deployment Guide

Complete instructions for deploying the NYC Housing Price Predictor to various cloud platforms.

---

## 🚀 Deployment Options

### Option 1: Render.com (Recommended - Free Tier Available)

**Step 1: Prepare Your Repository**

1. Ensure your code is pushed to GitHub
2. Make sure `requirements.txt` is in the root directory
3. Ensure `Dockerfile` exists (already provided)

**Step 2: Deploy to Render**

```bash
# 1. Go to https://render.com and sign up/login
# 2. Click "New +" → "Web Service"
# 3. Connect your GitHub repository
# 4. Configure the service:

Name: nyc-housing-predictor
Environment: Docker
Branch: main (or ml-zoomcamp-midterm)
Instance Type: Free

# 5. Click "Create Web Service"
```

**Step 3: Configure Environment (if needed)**

```bash
# In Render dashboard, go to "Environment" tab
# Add any required environment variables:
PORT=9696
FLASK_ENV=production
```

**Step 4: Access Your Deployed App**

```
Your app will be available at:
https://nyc-housing-predictor.onrender.com

API Endpoint:
https://nyc-housing-predictor.onrender.com/predict
```

**Testing the Deployment:**

```bash
curl -X POST https://nyc-housing-predictor.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "brokertitle": "Brokered by COMPASS",
    "type": "Condo for sale",
    "beds": 2,
    "bath": 1.0,
    "propertysqft": 800.0,
    "sublocality": "Manhattan"
  }'
```

---

### Option 2: Railway.app

**Step 1: Install Railway CLI**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login
```

**Step 2: Initialize and Deploy**

```bash
# From project root directory
railway init

# Deploy the application
railway up

# Get deployment URL
railway domain
```

**Step 3: Configure Service**

```bash
# Railway will automatically detect:
# - Dockerfile (will use Docker deployment)
# - requirements.txt (if no Dockerfile, will use Python)

# Set environment variables
railway variables set PORT=9696
railway variables set FLASK_ENV=production
```

**Configuration File (already provided):**

See `deployment/cloud/railway.toml` for pre-configured settings.

---

### Option 3: Streamlit Cloud (For Streamlit App Only)

**Step 1: Prepare Repository**

1. Ensure `streamlit_app/streamlit_app.py` exists
2. Ensure `streamlit_app/requirements.txt` has all dependencies

**Step 2: Deploy**

```bash
# 1. Go to https://share.streamlit.io/
# 2. Click "New app"
# 3. Connect GitHub repository
# 4. Configure:

Repository: your-username/nyc_housing_regressor_ML_flask_streamlit
Branch: main
Main file path: streamlit_app/streamlit_app.py

# 5. Click "Deploy"
```

**Your app will be live at:**
```
https://your-username-nyc-housing-predictor.streamlit.app
```

---

### Option 4: Google Cloud Run

**Step 1: Install gcloud CLI**

```bash
# Install Google Cloud SDK
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

**Step 2: Build and Deploy**

```bash
# Build container image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/nyc-housing-predictor

# Deploy to Cloud Run
gcloud run deploy nyc-housing-predictor \
  --image gcr.io/YOUR_PROJECT_ID/nyc-housing-predictor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 9696
```

**Step 3: Get Service URL**

```bash
# Get deployment URL
gcloud run services describe nyc-housing-predictor \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

---

### Option 5: Heroku

**Step 1: Install Heroku CLI**

```bash
# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
```

**Step 2: Create and Deploy**

```bash
# Create Heroku app
heroku create nyc-housing-predictor

# Deploy using Docker
heroku container:push web -a nyc-housing-predictor
heroku container:release web -a nyc-housing-predictor

# Or deploy using Git
git push heroku main
```

**Step 3: Configure**

```bash
# Set config vars
heroku config:set FLASK_ENV=production -a nyc-housing-predictor

# Open app
heroku open -a nyc-housing-predictor
```

---

## 🧪 Testing Your Deployment

### Health Check

```bash
# Replace with your deployment URL
curl https://your-app-url.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-01-15T10:30:00"
}
```

### Single Prediction Test

```bash
curl -X POST https://your-app-url.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "brokertitle": "Brokered by COMPASS",
    "type": "Condo for sale",
    "beds": 2,
    "bath": 1.0,
    "propertysqft": 800.0,
    "sublocality": "Manhattan"
  }'
```

Expected response:
```json
{
  "price": 1323814.25,
  "price_formatted": "$1,323,814",
  "confidence": "medium",
  "model_version": "20250110"
}
```

### Load Testing (Optional)

```bash
# Using Apache Bench
ab -n 100 -c 10 -T 'application/json' \
  -p test_payload.json \
  https://your-app-url.com/predict
```

---

## 📊 Monitoring & Maintenance

### Render.com Monitoring

- View logs in Render dashboard
- Monitor service health and metrics
- Set up alerts for downtime

### Railway.app Monitoring

```bash
# View deployment logs
railway logs

# Check service status
railway status
```

### Streamlit Cloud Monitoring

- Check app metrics in Streamlit dashboard
- View usage statistics
- Monitor resource consumption

---

## 🔐 Security Best Practices

1. **Environment Variables**: Store sensitive data in environment variables, not in code
2. **HTTPS**: All platforms provide HTTPS by default
3. **Rate Limiting**: Consider adding rate limiting for production
4. **API Keys**: Implement API key authentication if making publicly available
5. **CORS**: Configure CORS headers appropriately for your use case

---

## 💰 Cost Considerations

| Platform | Free Tier | Limitations | Best For |
|----------|-----------|-------------|----------|
| **Render** | ✅ Yes | 750 hrs/month, sleeps after inactivity | Production demos |
| **Railway** | ✅ Yes | $5 free credit/month | Quick deployments |
| **Streamlit Cloud** | ✅ Yes | Public repos only | Data science apps |
| **Google Cloud Run** | ✅ Limited | 2M requests/month free | Scalable production |
| **Heroku** | ⚠️ Limited | No free tier (as of 2022) | Enterprise apps |

---

## 🐛 Troubleshooting

### Common Issues

**Issue: App crashes on startup**
```bash
# Check logs for error messages
# Ensure all dependencies in requirements.txt
# Verify model files are included in deployment
```

**Issue: "Module not found" errors**
```bash
# Solution: Add missing package to requirements.txt
# Rebuild and redeploy
```

**Issue: App sleeps/cold starts**
```bash
# Free tiers often sleep after inactivity
# Solution: Use a scheduled ping service to keep alive
# Or upgrade to paid tier
```

**Issue: Model file too large**
```bash
# Solution: Use git-lfs for large files
git lfs track "models/*.joblib"
git add .gitattributes
git add models/
git commit -m "Add large model files with git-lfs"
```

---

## 📞 Support

For deployment issues:
- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app
- **Streamlit**: https://docs.streamlit.io/streamlit-cloud
- **GCP**: https://cloud.google.com/run/docs
- **Heroku**: https://devcenter.heroku.com

---

## ✅ Deployment Checklist

Before deploying, ensure:

- [ ] All code committed to GitHub
- [ ] `requirements.txt` is complete and up-to-date
- [ ] `Dockerfile` builds successfully locally
- [ ] Model files are accessible (in repo or remote storage)
- [ ] Environment variables documented
- [ ] README has deployment instructions
- [ ] Health check endpoint works
- [ ] Prediction endpoint tested locally
- [ ] CORS configured if needed
- [ ] Error handling implemented

---

## 🎉 Success!

Once deployed, your ML model is live and accessible to users worldwide!

Share your deployment URL for peer review and showcase your work.
