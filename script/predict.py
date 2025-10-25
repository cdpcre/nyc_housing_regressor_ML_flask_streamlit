"""
Model loading and prediction utilities with caching
"""
import joblib
import numpy as np
import pandas as pd
from functools import lru_cache
from typing import Dict, Any, Optional
import logging

from config import MODEL_PATH, METADATA_PATH, EXPECTED_FEATURES, ENABLE_CACHING
from utils import FrequencyEncoder

logger = logging.getLogger(__name__)

class ModelCache:
    """Thread-safe model cache with lazy loading"""
    _instance = None
    _model = None
    _metadata = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelCache, cls).__new__(cls)
        return cls._instance
    
    def get_model_and_metadata(self):
        """Get cached model and metadata, load if not cached"""
        if self._model is None or self._metadata is None:
            self._load_model()
        return self._model, self._metadata
    
    def _load_model(self):
        """Load model and metadata from disk"""
        try:
            logger.info(f"Loading model from {MODEL_PATH}")
            self._model = joblib.load(MODEL_PATH)
            self._metadata = joblib.load(METADATA_PATH)
            logger.info(f"✅ Model loaded: {self._metadata['model_info']['name']}")
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            raise

# Global cache instance
_model_cache = ModelCache() if ENABLE_CACHING else None

def load_model_and_metadata():
    """Load model and metadata with optional caching"""
    if ENABLE_CACHING and _model_cache:
        return _model_cache.get_model_and_metadata()
    else:
        # Direct loading without caching
        model = joblib.load(MODEL_PATH)
        metadata = joblib.load(METADATA_PATH)
        return model, metadata

def prepare_features(input_data: Dict[str, Any], expected_features: Optional[list] = None) -> pd.DataFrame:
    """
    Prepare input data for prediction by ensuring correct format and feature order.
    
    Args:
        input_data: Dictionary with feature values
        expected_features: List of expected features (uses config default if None)
    
    Returns:
        DataFrame with correctly ordered features
    
    Raises:
        ValueError: If required features are missing
    """
    if expected_features is None:
        expected_features = EXPECTED_FEATURES
    
    # Validate required features
    missing_features = [f for f in expected_features if f not in input_data]
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    
    # Create DataFrame with correct feature order
    df = pd.DataFrame([input_data])
    df = df[expected_features]  # Ensure correct order
    
    return df

def predict_price(input_data: Dict[str, Any], use_log_target: bool = True) -> float:
    """
    Make price prediction using cached model
    
    Args:
        input_data: Dictionary with feature values
        use_log_target: Whether model outputs log-transformed values
    
    Returns:
        Predicted price as float
    """
    model, metadata = load_model_and_metadata()
    
    # Prepare features
    input_df = prepare_features(input_data)
    
    # Make prediction
    log_prediction = model.predict(input_df)
    
    # Transform back to original scale if needed
    if use_log_target:
        predicted_price = np.expm1(log_prediction[0])
    else:
        predicted_price = log_prediction[0]
    
    return float(predicted_price)

def get_model_info() -> Dict[str, Any]:
    """Get model information and metadata"""
    _, metadata = load_model_and_metadata()

    # Handle both old and new metadata structures
    features = metadata.get('data_info', {}).get('selected_features', EXPECTED_FEATURES)

    return {
        'model_name': metadata['model_info']['name'],
        'performance': metadata['performance'],
        'features': features,
        'created': metadata['model_info']['created_timestamp']
    }

@lru_cache(maxsize=1000)
def cached_predict(input_tuple: tuple) -> float:
    """
    Cached prediction for identical inputs (converts tuple back to dict)
    Useful for repeated predictions with same parameters
    """
    # Convert tuple back to dict (for hashability in cache)
    keys = ['brokertitle', 'type', 'beds', 'bath', 'propertysqft', 'sublocality']
    input_data = dict(zip(keys, input_tuple))
    return predict_price(input_data)

def batch_predict(data: pd.DataFrame) -> np.ndarray:
    """
    Efficient batch prediction for multiple properties

    Args:
        data: DataFrame with property features

    Returns:
        Array of predicted prices
    """
    model, metadata = load_model_and_metadata()

    # Handle both old and new metadata structures
    expected_features = metadata.get('data_info', {}).get('selected_features', EXPECTED_FEATURES)

    # Ensure correct feature order
    input_df = data[expected_features].copy()

    # Make batch predictions
    log_predictions = model.predict(input_df)

    # Transform back to original scale
    predictions = np.expm1(log_predictions)

    return predictions

def get_price_category(price: float) -> str:
    """Categorize price into budget/mid-range/luxury"""
    from config import PRICE_RANGES
    
    if price < PRICE_RANGES['budget']:
        return "Budget-Friendly"
    elif price < PRICE_RANGES['luxury']:
        return "Mid-Range"
    else:
        return "Luxury"