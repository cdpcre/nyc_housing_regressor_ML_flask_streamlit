"""
Configuration settings for the NYC Housing Price Predictor
"""
import os

# Model paths (relative to project root)
def get_project_root():
    """Get the project root directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # shared/
    return os.path.dirname(current_dir)  # project root/

PROJECT_ROOT = get_project_root()
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'best_model_xgboost_freq_20251025.joblib')
METADATA_PATH = os.path.join(PROJECT_ROOT, 'models', 'model_metadata_xgboost_freq_20251025.joblib')

# API settings
API_HOST = '0.0.0.0'
API_PORT = 9696
DEBUG_MODE = True

# Streamlit settings
STREAMLIT_PORT = 8501

# Cache settings
ENABLE_CACHING = True
CACHE_TTL = 3600  # 1 hour in seconds

# Expected features (in correct order)
EXPECTED_FEATURES = [
    'brokertitle', 'type', 'beds', 'bath', 'propertysqft', 'sublocality'
]

# Feature options for frontend
PROPERTY_TYPES = [
    "Condo for sale", "House for sale", "Co-op for sale", 
    "Multi-family home for sale", "Townhouse for sale",
    "Pending", "Contingent", "Land for sale", "For sale", "Foreclosure"
]

SUBLOCALITIES = [
    "Manhattan", "Brooklyn", "Queens", "Bronx County", "Staten Island",
    "New York", "Kings County", "Queens County", "Richmond County",
    "New York County", "The Bronx"
]

BROKER_OPTIONS = [
    "Brokered by COMPASS",
    "Brokered by Douglas Elliman - 575 Madison Ave",
    "Brokered by Brown Harris Stevens",
    "Brokered by Corcoran East Side",
    "Brokered by RE MAX Edge",
    "Brokered by Winzone Realty Inc",
    "Brokered by E Realty International Corp",
    "Brokered by Sotheby's International Realty - East Side Manhattan Brokerage",
    "Brokered by RE MAX Real Estate Professionals",
    "Brokered by Serhant"
]

# Price categories
PRICE_RANGES = {
    'budget': 400000,
    'mid': 1000000,
    'luxury': 2000000
}