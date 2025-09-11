# 🏠 NYC Housing Price Predictor

A complete machine learning web application for predicting New York City housing prices.
Features both a professional Flask web interface and Streamlit app, with comprehensive API access and beautiful visualizations.

## 🎯 Project Overview

This project demonstrates a complete ML pipeline from data preprocessing to production deployment:

- **🧠 Machine Learning**: XGBoost model with R² = 0.7183 performance
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
├── 🔧 shared/
│   ├── models.py             # Model utilities with caching
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

### Flask Web App Features

| Feature | Description |
|---------|-------------|
| 🏠 **Single Prediction** | Interactive form with dropdowns and sliders |
| 📁 **Batch Upload** | CSV file processing with progress tracking |
| 📊 **Price Visualization** | Charts comparing predicted vs market ranges |
| 📚 **API Documentation** | Interactive testing interface |
| 💾 **Data Export** | Download predictions as CSV |
| 📱 **Mobile Responsive** | Works perfectly on all devices |

### Streamlit App Features

| Feature | Description |
|---------|-------------|
| 🎯 **Model Metrics** | Real-time performance display |
| 📈 **Interactive Charts** | Plotly visualizations |
| 🔄 **Batch Processing** | Upload and process multiple properties |
| 💡 **Usage Tips** | Sidebar with prediction guidance |
| 📋 **Property Summary** | Detailed prediction breakdown |

## ⚡ REST API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict` | Single property prediction |
| `GET` | `/health` | API health check |
| `GET` | `/model_metadata_info` | Model details |
| `GET` | `/download-sample` | Sample CSV download |

### Example API Usage

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

### Quick Docker Start

```bash
# Build and run Flask app
docker build -f deployment/docker/Dockerfile.flask -t nyc-housing-flask .
docker run -p 9696:9696 nyc-housing-flask

# Build and run Streamlit app
docker build -f deployment/docker/Dockerfile.streamlit -t nyc-housing-streamlit .
docker run -p 8501:8501 nyc-housing-streamlit
```

### Docker Compose (Both Apps)

```bash
cd deployment/docker
docker-compose up -d
```

This starts:
- **Flask app**: http://localhost:9696
- **Streamlit app**: http://localhost:8501
- **Nginx proxy**: http://localhost:80

## ☁️ Cloud Deployment

### Railway.app

# Push to GitHub then connect to Railway
# Uses deployment/cloud/railway.toml configuration

### Render.com

# Push to GitHub then connect to Render
# Uses deployment/cloud/render.yaml configuration

## 📊 Model Performance

| Metric | Value | Description |
|--------|-------|-------------|
| **R² Score** | 0.7183 | Explains 72% of price variance |
| **RMSE** | $1,215,863 | Average prediction error |
| **Features** | 6 | Property characteristics + location |
| **Training Data** | 2,948 | Properties after cleaning |
| **Response Time** | <100ms | API response time |

## 🎨 Visualization Examples

### Altair Charts in Notebooks

- **Price Distribution**: Interactive histogram with log scale
- **Geographic Clusters**: Scatter plot with color-coded regions  
- **Correlation Matrix**: Heatmap with hover tooltips
- **Property Types**: Horizontal bar chart with counts
- **Price vs Distance**: Scatter plot from Manhattan center

### Web Interface Charts

- **Price Comparison**: Horizontal bar chart showing budget/mid/luxury ranges
- **Batch Results**: Distribution histogram for uploaded datasets
- **Real-time Updates**: Charts update automatically with predictions

## 🛠️ Development

### Running Tests

```bash
# Test Flask API
cd flask_app
python -m pytest tests/

# Test model functionality  
python tests/test_model.py

# Test API endpoints
python tests/test_api.py
```

### File Organization

```bash
# Shared utilities
shared/
├── config.py       # Configuration constants
├── models.py       # Model loading with caching
└── utils.py        # FrequencyEncoder class

# Flask application
flask_app/
├── app.py          # Main Flask application
├── templates/      # Jinja2 HTML templates  
└── static/         # CSS, JavaScript, images

# Streamlit application
streamlit_app/
└── streamlit_app.py # Streamlit interface

# Data and models
data/
├── raw/            # Original datasets
└── processed/      # Cleaned data splits

models/             # Trained model files
```

## 🔧 Configuration

### Key Configuration Files

- **`shared/config.py`**: Centralized settings
- **`flask_app/requirements.txt`**: Flask dependencies
- **`streamlit_app/requirements.txt`**: Streamlit dependencies
- **`deployment/docker/`**: Docker configurations
- **`deployment/cloud/`**: Cloud deployment settings

### Environment Variables

```bash
# Flask app
FLASK_ENV=production
PORT=9696

# Streamlit app
STREAMLIT_SERVER_PORT=8501
```

## 📈 Advanced Features

### Caching & Performance

- **Model Caching**: Models loaded once and cached
- **Prediction Caching**: Identical requests cached with LRU
- **Static Assets**: CSS/JS cached by browser
- **Database Ready**: Architecture supports future DB integration

### Security Features

- **Input Validation**: Comprehensive request validation
- **Error Handling**: Secure error messages
- **CORS Headers**: Configurable cross-origin requests
- **Rate Limiting Ready**: Architecture supports rate limiting

### Monitoring & Analytics

- **Health Checks**: Built-in endpoints for monitoring
- **Request Logging**: Comprehensive logging system
- **Performance Metrics**: Response time tracking
- **Error Tracking**: Detailed error reporting

## 🎯 Use Cases

### For Data Scientists
- **Research**: Interactive Jupyter notebooks with Altair
- **Experimentation**: Streamlit interface for model testing
- **Visualization**: Beautiful charts and graphs

### For Developers  
- **API Integration**: RESTful endpoints for applications
- **Web Interface**: Professional Flask web app
- **Docker Deployment**: Easy containerization

### For Business Users
- **Single Predictions**: Easy-to-use web forms
- **Batch Processing**: Upload CSV files for bulk predictions
- **Data Export**: Download results and visualizations

## 🤝 Contributing

This project demonstrates best practices for:
- ✅ **Clean Architecture**: Separation of concerns
- ✅ **Multiple Interfaces**: Web, API, and notebook access
- ✅ **Production Ready**: Docker, cloud deployment, monitoring
- ✅ **User Experience**: Professional design and interactions
- ✅ **Data Visualization**: Interactive charts and graphs
- ✅ **Documentation**: Comprehensive guides and examples

---

## 📞 Support

For questions about this project:
- 📚 **API Docs**: Visit http://localhost:9696/api-docs
- 🔍 **Health Check**: Visit http://localhost:9696/health  
- 📊 **Model Info**: Visit http://localhost:9696/model_metadata_info
