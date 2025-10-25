#!/usr/bin/env python3
"""
NYC Housing Price Prediction - Training Script
===============================================

This script trains the XGBoost regression model for NYC housing price prediction.
Extracted from the feature_engineering.ipynb notebook for ML Zoomcamp midterm project.

Usage:
    cd script
    python train.py

    Or from project root:
    python script/train.py

Output:
    - Trained model saved to models/best_model_xgboost_freq_{date}.joblib
    - Model metadata saved to models/model_metadata_xgboost_freq_{date}.joblib
"""

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Get project root directory (parent of script folder)
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / 'shared'))

# Scikit-learn imports
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Model imports
from xgboost import XGBRegressor
import joblib

# Import custom FrequencyEncoder
try:
    from utils import FrequencyEncoder
    print("✅ FrequencyEncoder imported successfully")
except ImportError:
    print("❌ Error: Could not import FrequencyEncoder from shared/utils.py")
    print("Make sure you're running this script from the script/ directory")
    sys.exit(1)


def load_and_preprocess_data(data_path=None):
    """Load and preprocess the NYC housing dataset."""
    if data_path is None:
        data_path = project_root / 'data' / 'raw' / 'NY-House-Dataset.csv'
    else:
        data_path = Path(data_path)

    print("\n" + "="*60)
    print("STEP 1: DATA LOADING AND PREPROCESSING")
    print("="*60)

    # Define selected features
    model_features = ['BROKERTITLE', 'TYPE', 'BEDS', 'BATH', 'PROPERTYSQFT', 'SUBLOCALITY', 'PRICE']

    # Load dataset
    print(f"Loading data from: {data_path}")
    df_full = pd.read_csv(data_path, usecols=model_features)

    # Standardize column names
    df_full.columns = [col.lower() for col in df_full.columns]

    print(f"Initial dataset shape: {df_full.shape}")

    # Data cleaning
    print("\nCleaning data...")
    df_clean = df_full.dropna()
    print(f"After removing NaN: {len(df_clean)} rows")

    # Remove price outliers (1st to 99th percentile)
    price_q01 = df_clean['price'].quantile(0.01)
    price_q99 = df_clean['price'].quantile(0.99)
    df_clean = df_clean[(df_clean['price'] >= price_q01) & (df_clean['price'] <= price_q99)]
    print(f"After price filtering: {len(df_clean)} rows")

    # Remove property size outliers
    sqft_q01 = df_clean['propertysqft'].quantile(0.01)
    sqft_q99 = df_clean['propertysqft'].quantile(0.99)
    df_clean = df_clean[(df_clean['propertysqft'] >= sqft_q01) & (df_clean['propertysqft'] <= sqft_q99)]
    print(f"After property size filtering: {len(df_clean)} rows")

    print(f"✅ Final cleaned dataset: {df_clean.shape}")

    return df_clean


def split_data(df_clean, random_state=42):
    """Split data into train, validation, and test sets."""
    print("\n" + "="*60)
    print("STEP 2: DATA SPLITTING")
    print("="*60)

    target_col = 'price'
    feature_cols = [col for col in df_clean.columns if col != target_col]

    # Stratified split by price quantiles
    stratify_series = None
    try:
        price_bins = pd.qcut(df_clean["price"], q=10, duplicates="drop")
        if price_bins.nunique() > 1:
            stratify_series = price_bins
    except Exception:
        stratify_series = None

    if stratify_series is None and "type" in df_clean.columns:
        stratify_series = df_clean["type"]

    # First split: 80% train, 20% temp
    try:
        train_df, temp_df = train_test_split(
            df_clean, test_size=0.2, random_state=random_state, stratify=stratify_series
        )
    except ValueError:
        train_df, temp_df = train_test_split(
            df_clean, test_size=0.2, random_state=random_state, stratify=None
        )

    # Second split: 10% val, 10% test
    stratify_temp = None
    if stratify_series is not None:
        stratify_temp = stratify_series.loc[temp_df.index]

    try:
        val_df, test_df = train_test_split(
            temp_df, test_size=0.5, random_state=random_state, stratify=stratify_temp
        )
    except ValueError:
        val_df, test_df = train_test_split(
            temp_df, test_size=0.5, random_state=random_state, stratify=None
        )

    # Extract features and target
    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    X_val = val_df[feature_cols]
    y_val = val_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]

    print(f"Train set: {X_train.shape[0]} samples ({len(X_train)/len(df_clean)*100:.1f}%)")
    print(f"Validation set: {X_val.shape[0]} samples ({len(X_val)/len(df_clean)*100:.1f}%)")
    print(f"Test set: {X_test.shape[0]} samples ({len(X_test)/len(df_clean)*100:.1f}%)")
    print(f"Features: {feature_cols}")

    return X_train, X_val, X_test, y_train, y_val, y_test, feature_cols


def create_preprocessor(X_train):
    """Create preprocessing pipeline with frequency encoding for high cardinality features."""
    print("\n" + "="*60)
    print("STEP 3: PREPROCESSING PIPELINE CREATION")
    print("="*60)

    # Define feature types
    categorical_features = ['brokertitle', 'type', 'sublocality']
    numerical_features = ['beds', 'bath', 'propertysqft']

    # Separate high and low cardinality
    high_cardinality_threshold = 50
    high_cardinality_features = []
    low_cardinality_features = []

    for col in categorical_features:
        unique_count = X_train[col].nunique()
        if unique_count > high_cardinality_threshold:
            high_cardinality_features.append(col)
        else:
            low_cardinality_features.append(col)

    print(f"Low cardinality features: {low_cardinality_features}")
    print(f"High cardinality features: {high_cardinality_features}")

    # Create transformers
    transformers = []

    # Frequency encoding for high cardinality
    if high_cardinality_features:
        freq_encoder = FrequencyEncoder(handle_unknown='zero')
        transformers.append(('categorical_high', freq_encoder, high_cardinality_features))

    # OneHot encoding for low cardinality
    if low_cardinality_features:
        onehot_encoder = OneHotEncoder(drop='first', handle_unknown='ignore')
        transformers.append(('categorical_low', onehot_encoder, low_cardinality_features))

    # Standard scaling for numerical features
    transformers.append(('numerical', StandardScaler(), numerical_features))

    # Create column transformer
    preprocessor = ColumnTransformer(transformers=transformers, remainder='drop')

    print("✅ Preprocessor created successfully")

    return preprocessor


def train_model(X_train, y_train, X_val, y_val, n_estimators=50):
    """Train XGBoost model with frequency encoding."""
    print("\n" + "="*60)
    print("STEP 4: MODEL TRAINING")
    print("="*60)

    # Log-transform target
    use_log_target = True
    y_train_transformed = np.log1p(y_train)
    y_val_transformed = np.log1p(y_val)

    print(f"Using log-transformed target for training")
    print(f"Training XGBoost with n_estimators={n_estimators}")

    # Create preprocessor
    preprocessor = create_preprocessor(X_train)

    # Create pipeline
    model_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', XGBRegressor(
            n_estimators=n_estimators,
            random_state=42,
            n_jobs=-1
        ))
    ])

    # Cross-validation
    print("\nPerforming 5-fold cross-validation...")
    cv_scores = cross_val_score(
        model_pipeline, X_train, y_train_transformed,
        cv=5, scoring='r2', n_jobs=-1
    )

    print(f"CV R² scores: {cv_scores}")
    print(f"CV R² mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    # Train on full training set
    print("\nTraining on full training set...")
    model_pipeline.fit(X_train, y_train_transformed)

    # Validation predictions
    y_val_pred = model_pipeline.predict(X_val)
    y_val_pred_original = np.expm1(y_val_pred)

    # Calculate metrics
    val_r2 = r2_score(y_val, y_val_pred_original)
    val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred_original))
    val_mae = mean_absolute_error(y_val, y_val_pred_original)

    print(f"\n📊 Validation Performance:")
    print(f"   R²: {val_r2:.4f}")
    print(f"   RMSE: ${val_rmse:,.0f}")
    print(f"   MAE: ${val_mae:,.0f}")

    return model_pipeline, {
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'val_r2': val_r2,
        'val_rmse': val_rmse,
        'val_mae': val_mae,
        'use_log_target': use_log_target
    }


def evaluate_on_test(model, X_test, y_test, use_log_target=True):
    """Evaluate model on test set."""
    print("\n" + "="*60)
    print("STEP 5: TEST SET EVALUATION")
    print("="*60)

    # Predictions
    if use_log_target:
        y_test_pred = model.predict(X_test)
        y_test_pred_original = np.expm1(y_test_pred)
    else:
        y_test_pred_original = model.predict(X_test)

    # Metrics
    test_r2 = r2_score(y_test, y_test_pred_original)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred_original))
    test_mae = mean_absolute_error(y_test, y_test_pred_original)

    print(f"🎯 Test Set Performance:")
    print(f"   R²: {test_r2:.4f}")
    print(f"   RMSE: ${test_rmse:,.0f}")
    print(f"   MAE: ${test_mae:,.0f}")

    return {
        'test_r2': test_r2,
        'test_rmse': test_rmse,
        'test_mae': test_mae
    }


def save_model(model, feature_cols, metrics, test_metrics):
    """Save trained model and metadata."""
    print("\n" + "="*60)
    print("STEP 6: MODEL EXPORT")
    print("="*60)

    # Create models directory
    models_dir = project_root / 'models'
    models_dir.mkdir(exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d")
    model_filename = f'best_model_xgboost_freq_{timestamp}.joblib'
    metadata_filename = f'model_metadata_xgboost_freq_{timestamp}.joblib'

    model_path = models_dir / model_filename
    metadata_path = models_dir / metadata_filename

    # Save model
    joblib.dump(model, model_path)
    print(f"✅ Model saved: {model_path}")

    # Create metadata
    model_metadata = {
        'model_info': {
            'name': 'XGBoost with Frequency Encoding',
            'type': 'regression',
            'target': 'housing_price',
            'created_timestamp': timestamp,
            'framework': 'scikit-learn + xgboost'
        },
        'features': {
            'feature_list': feature_cols,
            'categorical': ['brokertitle', 'type', 'sublocality'],
            'numerical': ['beds', 'bath', 'propertysqft']
        },
        'preprocessing': {
            'use_log_target': metrics['use_log_target'],
            'categorical_encoding': 'frequency (high cardinality) + onehot (low cardinality)',
            'numerical_scaling': 'StandardScaler'
        },
        'performance': {
            'cv_r2_mean': metrics['cv_mean'],
            'cv_r2_std': metrics['cv_std'],
            'val_r2': metrics['val_r2'],
            'val_rmse': metrics['val_rmse'],
            'val_mae': metrics['val_mae'],
            'test_r2': test_metrics['test_r2'],
            'test_rmse': test_metrics['test_rmse'],
            'test_mae': test_metrics['test_mae']
        }
    }

    # Save metadata
    joblib.dump(model_metadata, metadata_path)
    print(f"✅ Metadata saved: {metadata_path}")

    print(f"\n💾 Files created:")
    print(f"   • {model_path} ({model_path.stat().st_size/1024/1024:.2f} MB)")
    print(f"   • {metadata_path} ({metadata_path.stat().st_size/1024:.2f} KB)")

    return model_path, metadata_path


def main():
    """Main training pipeline."""
    print("\n" + "="*60)
    print("NYC HOUSING PRICE PREDICTION - MODEL TRAINING")
    print("ML Zoomcamp Midterm Project")
    print("="*60)

    # Check if data file exists
    data_path = project_root / 'data' / 'raw' / 'NY-House-Dataset.csv'
    if not data_path.exists():
        print(f"❌ Error: Data file not found at {data_path}")
        print("Please ensure the dataset is in the correct location.")
        sys.exit(1)

    # Step 1: Load and preprocess data
    df_clean = load_and_preprocess_data(data_path)

    # Step 2: Split data
    X_train, X_val, X_test, y_train, y_val, y_test, feature_cols = split_data(df_clean)

    # Step 3 & 4: Train model
    model, metrics = train_model(X_train, y_train, X_val, y_val, n_estimators=50)

    # Step 5: Evaluate on test set
    test_metrics = evaluate_on_test(model, X_test, y_test, metrics['use_log_target'])

    # Step 6: Save model
    model_path, metadata_path = save_model(model, feature_cols, metrics, test_metrics)

    print("\n" + "="*60)
    print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📋 Quick Summary:")
    print(f"   • Model: XGBoost with Frequency Encoding")
    print(f"   • Validation R²: {metrics['val_r2']:.4f}")
    print(f"   • Test R²: {test_metrics['test_r2']:.4f}")
    print(f"   • Model file: {model_path}")
    print(f"\n🚀 Ready for deployment!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
