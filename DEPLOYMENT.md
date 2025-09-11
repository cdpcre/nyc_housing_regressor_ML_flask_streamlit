# 🚀 Deployment Guide - NYC Housing Price Predictor

## Streamlit Cloud Deployment (FREE)

### Step 1: Prepare Repository
1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add Streamlit web app for NYC housing predictions"
   git push origin main
   ```

2. **Ensure files are present:**
   - ✅ `streamlit_app.py` - Main Streamlit application
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `utils.py` - FrequencyEncoder class
   - ✅ `best_model_xgboost_freq_20250909.joblib` - Trained model
   - ✅ `model_metadata_xgboost_freq_20250909.joblib` - Model metadata

### Step 2: Deploy on Streamlit Cloud
1. **Go to:** https://share.streamlit.io/
2. **Sign in** with GitHub account
3. **Click "New app"**
4. **Select your repository:** `mlzooomcamp-course`
5. **Set branch:** `main` 
6. **Set main file path:** `midterm_project/streamlit_app.py`
7. **Click "Deploy!"**

### Step 3: Access Your App
- Your app will be available at: `https://your-app-name.streamlit.app`
- Share this URL with anyone - it's publicly accessible!

---

## Alternative Deployment Options

### 1. Heroku (Simple)
```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy to Heroku
heroku create nyc-housing-predictor
git push heroku main
```

### 2. Railway.app (Free Tier)
```bash
# Just connect GitHub repo to Railway
# Railway auto-detects Python and installs requirements
```

### 3. Render.com (Free Tier)
```yaml
# render.yaml
services:
  - type: web
    name: nyc-housing-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run streamlit_app.py --server.port=10000 --server.address=0.0.0.0
```

---

## Local Development

### Run Locally
```bash
# Activate conda environment
conda activate env_mlzoomcamp

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app.py
```

### Access locally at:
- **Local URL:** http://localhost:8501
- **Network URL:** http://192.168.1.8:8501

---

## App Features

### 🏠 Single Property Prediction
- **Interactive sliders** for beds, baths, square footage
- **Dropdown menus** for property type, location, broker
- **Real-time predictions** with price visualization
- **Price per sq ft** calculations
- **Market category** classification (Budget/Mid/Luxury)

### 📁 Batch Predictions
- **Drag & drop CSV upload** for multiple properties
- **Data validation** and preview
- **Batch processing** with progress indicators
- **Results download** in CSV format
- **Price distribution** visualizations

### 📊 Model Information
- **Performance metrics** (R², RMSE)
- **Feature importance** insights
- **Training details** and metadata
- **Usage tips** and recommendations

---

## Troubleshooting

### Common Issues:
1. **Model files not found:** Ensure `.joblib` files are in the same directory
2. **Dependencies missing:** Check `requirements.txt` is complete
3. **Memory issues:** Streamlit Cloud has 1GB RAM limit
4. **Slow loading:** Model caching with `@st.cache_resource` helps

### Support:
- **Streamlit Community:** https://discuss.streamlit.io/
- **Documentation:** https://docs.streamlit.io/