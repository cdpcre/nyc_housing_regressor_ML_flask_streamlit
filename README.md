# 🏠 NYC Housing Price Predictor

**DataTalks.Club ML Zoomcamp 2025 - Midterm Project**

A complete machine learning solution for predicting New York City housing prices with production-ready deployment. This project demonstrates end-to-end ML engineering from data analysis to cloud deployment.

---

## 📋 Problem Description

### The Challenge

The New York City real estate market is one of the most complex and volatile in the world, with property prices varying dramatically based on location, property characteristics, and market conditions. Buyers, sellers, and real estate agents struggle to accurately estimate fair market values without extensive market research.

### Business Context

- **Target Users**: Real estate agents, property buyers, sellers, and investors
- **Problem**: Lack of accessible, data-driven tools for accurate property valuation
- **Impact**: Poor pricing decisions leading to prolonged listing times or undervalued properties

### The Solution

This project provides an automated housing price prediction system that:

1. **Estimates property values** based on key features (location, size, type, bedrooms, bathrooms)
2. **Provides instant predictions** through multiple interfaces (Web UI, REST API, Streamlit)
3. **Enables data-driven decisions** for buyers and sellers in the NYC market
4. **Scales efficiently** with containerization and cloud deployment

### How It Will Be Used

- **Real Estate Agents**: Quick property valuations during client consultations
- **Home Buyers**: Assess if listing prices are fair before making offers
- **Sellers**: Set competitive asking prices based on property features
- **Investors**: Analyze potential returns on property investments
- **APIs**: Integrate predictions into existing real estate platforms

### Dataset

- **Source**: NYC Housing Market Dataset (2024)
- **Size**: 4,801 properties (4,610 after cleaning)
- **Features**: 6 input features (location, property type, size, beds, baths, broker)
- **Target**: Sale price in USD
- **Geographic Coverage**: All 5 NYC boroughs (Manhattan, Brooklyn, Queens, Bronx, Staten Island)

---

## 🎯 Project Overview

This project demonstrates a complete ML pipeline from data preprocessing to production deployment:

- **🧠 Machine Learning**: XGBoost model with R² = 0.7183 (72% variance explained)
- **🌐 Flask Web App**: Professional HTML interface with Bootstrap styling
- **📊 Streamlit App**: Interactive data science interface
- **⚡ REST API**: Programmatic access for integration
- **📈 Altair Visualizations**: Beautiful, interactive charts in Jupyter notebooks
- **🐳 Docker Ready**: Complete containerization for deployment
- **☁️ Cloud Deploy**: Ready for Railway, Render, Streamlit Cloud

## 📁 New Project Structure

```
nyc_housing_regressor_ML_flask_streamlit/
├── 📱 flask_app/
│   ├── app.py                 # Enhanced Flask web app + API
│   ├── templates/             # Bootstrap HTML templates
│   │   ├── base.html         # Base template with navigation
│   │   ├── index.html        # Main prediction form
│   │   ├── batch.html        # Batch upload interface
│   │   └── api_docs.html     # Interactive API documentation
│   ├── static/
│   │   ├── css/style.css     # Custom styling
│   │   └── js/main.js        # Frontend JavaScript
│   └── requirements.txt      # Flask dependencies
├── 📊 streamlit_app/
│   ├── streamlit_app.py      # Streamlit interface
│   └── requirements.txt      # Streamlit dependencies
├── 📚 notebooks/
│   ├── eda_preprocessing.ipynb    # Updated with Altair plots
│   └── feature_engineering.ipynb # Model training
├── 🔧 script/
│   ├── train.py              # Training script
│   ├── predict.py            # Model loading and prediction utilities
│   ├── utils.py              # FrequencyEncoder and utilities
│   └── config.py             # Shared configuration
├── 📊 models/                # Model files
├── 💾 data/
│   ├── raw/                  # Original data
│   └── processed/            # Cleaned datasets
├── 🐳 deployment/
│   ├── docker/               # Docker configurations
│   └── cloud/                # Cloud deployment configs
├── 🧪 tests/                 # Test files
└── 📝 docs/                  # Documentation
```

## 🔧 Environment Setup & Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/nyc_housing_regressor_ML_flask_streamlit.git
cd nyc_housing_regressor_ML_flask_streamlit
```

### 2. Create Virtual Environment

**Using venv (recommended):**

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

**Using conda:**

```bash
# Create conda environment
conda create -n nyc-housing python=3.9

# Activate environment
conda activate nyc-housing
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Check if packages are installed correctly
python -c "import pandas, numpy, sklearn, xgboost, flask, streamlit; print('All packages installed successfully!')"
```

---

## 🔄 Reproducibility Guide

### Training the Model from Scratch

**Option 1: Using the Training Script (Recommended)**

```bash
# Make sure you're in the project root directory
python script/train.py

# Or navigate to script folder
cd script
python train.py
```

This will:
- Load and preprocess the NYC housing dataset
- Split data into train/validation/test sets (80/10/10)
- Train XGBoost model with frequency encoding
- Perform 5-fold cross-validation
- Evaluate on test set
- Save model to `models/best_model_xgboost_freq_YYYYMMDD.joblib`

**Option 2: Using Jupyter Notebooks**

```bash
# Start Jupyter
jupyter notebook

# Navigate to and run in order:
# 1. notebooks/eda_preprocessing.ipynb  - Exploratory Data Analysis
# 2. notebooks/feature_engineering.ipynb - Model Training & Selection
```

### Expected Training Results

After training, you should see:
- **Validation R²**: ~0.72 (explains 72% of price variance)
- **Test R²**: ~0.71
- **RMSE**: ~$1.2M (reasonable for NYC housing market)
- **Training time**: 2-5 minutes on modern hardware

---

## 🚀 Quick Start Guide

### 🌐 Flask Web Application (NEW!)

**Professional web interface with Bootstrap styling:**

1. **Navigate to Flask app**:
```bash
cd flask_app
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Start the web application**:
```bash
python app.py
```

4. **Open in browser**:
- **Main Web App**: http://localhost:9696/
- **Batch Upload**: http://localhost:9696/batch
- **API Docs**: http://localhost:9696/api-docs
- **Health Check**: http://localhost:9696/health

### 📊 Streamlit Application

- **Streamlit Cloud**: https://nychousingcdpcreapp-regress.streamlit.app

**For data science workflows:**

1. **Navigate to Streamlit app**:
```bash
cd streamlit_app
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Start the app**:
```bash
streamlit run streamlit_app.py
```

4. **Open in browser**: http://localhost:8501

## ✨ New Features

### 🎨 Flask Web Interface

- **Professional Design**: Bootstrap 5 with custom styling
- **Interactive Forms**: Real-time validation and feedback
- **Batch Processing**: Drag-and-drop CSV upload
- **API Explorer**: Built-in documentation with testing
- **Responsive Layout**: Mobile-friendly design
- **Chart Visualizations**: Real-time price comparisons

### 📈 Enhanced Visualizations

**Notebooks now include beautiful Altair charts:**
- Interactive price distributions
- Geographic clustering maps
- Correlation heatmaps with hover details
- Property type frequency charts
- Price vs. distance scatter plots

### 🔧 Improved Architecture

- **Shared Modules**: No code duplication between apps
- **Model Caching**: Faster prediction responses
- **Error Handling**: Comprehensive error management
- **Type Safety**: Better input validation
- **Configuration**: Centralized settings

## 🌐 Web Interfaces

# Flask Web App Features

| Feature | Description |
|---------|-------------|
| 🏠 **Single Prediction** | Interactive form with dropdowns and sliders |
| 📁 **Batch Upload** | CSV file processing with progress tracking |
| 📊 **Price Visualization** | Charts comparing predicted vs market ranges |
| 📚 **API Documentation** | Interactive testing interface |
| 💾 **Data Export** | Download predictions as CSV |
| 📱 **Mobile Responsive** | Works perfectly on all devices |

# Streamlit App Features

| Feature | Description |
|---------|-------------|
| 🎯 **Model Metrics** | Real-time performance display |
| 📈 **Interactive Charts** | Plotly visualizations |
| 🔄 **Batch Processing** | Upload and process multiple properties |
| 💡 **Usage Tips** | Sidebar with prediction guidance |
| 📋 **Property Summary** | Detailed prediction breakdown |

## ⚡ REST API Endpoints

# Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict` | Single property prediction |
| `GET` | `/health` | API health check |
| `GET` | `/model_metadata_info` | Model details |
| `GET` | `/download-sample` | Sample CSV download |

# Example API Usage

```python
import requests

# Single prediction
response = requests.post('http://localhost:9696/predict', json={
    "brokertitle": "Brokered by COMPASS",
    "type": "Condo for sale",
    "beds": 2,
    "bath": 1.0,
    "propertysqft": 800.0,
    "sublocality": "Manhattan"
})

result = response.json()
print(f"Predicted price: {result['price_formatted']}")
# Output: Predicted price: $1,323,814
```

## 🐳 Docker Deployment

# Quick Docker Start

```bash
# Build and run Flask app
docker build -f deployment/docker/Dockerfile.flask -t nyc-housing-flask .
docker run -p 9696:9696 nyc-housing-flask

# Build and run Streamlit app
docker build -f deployment/docker/Dockerfile.streamlit -t nyc-housing-streamlit .
docker run -p 8501:8501 nyc-housing-streamlit
```

# Docker Compose (Both Apps)

```bash
cd deployment/docker
docker-compose up -d
```

This starts:
- **Flask app**: http://localhost:9696
- **Streamlit app**: http://localhost:8501
- **Nginx proxy**: http://localhost:80

## ☁️ Cloud Deployment

- 🔍 **Health Check**: Visit http://localhost:9696/health  
- 📊 **Model Info**: Visit http://localhost:9696/model_metadata_info
