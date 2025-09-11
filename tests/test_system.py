#!/usr/bin/env python3
"""
Comprehensive system test for NYC Housing Price Predictor
Tests all components: model loading, shared modules, predictions, and file structure
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np
import requests
import time

# Add shared directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
shared_dir = os.path.join(project_root, 'shared')
sys.path.insert(0, shared_dir)
sys.path.insert(0, project_root)

# Change to project root for proper file access
os.chdir(project_root)

def test_project_structure():
    """Test that all required directories and files exist"""
    print("🏗️  Testing Project Structure...")
    
    required_dirs = [
        'flask_app',
        'streamlit_app', 
        'shared',
        'models',
        'data/raw',
        'data/processed',
        'notebooks',
        'tests'
    ]
    
    required_files = [
        'flask_app/app.py',
        'streamlit_app/streamlit_app.py',
        'shared/models.py',
        'shared/utils.py',
        'shared/config.py',
        'data/raw/NY-House-Dataset.csv'
    ]
    
    # Test directories
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - MISSING")
            return False
    
    # Test files
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            return False
    
    print("✅ Project structure test passed!")
    return True

def test_shared_modules():
    """Test that shared modules can be imported and work"""
    print("\n🔧 Testing Shared Modules...")
    
    try:
        # Test FrequencyEncoder import
        from utils import FrequencyEncoder
        globals()['FrequencyEncoder'] = FrequencyEncoder
        print("  ✅ FrequencyEncoder imported")
        
        # Test FrequencyEncoder functionality
        sample_data = pd.DataFrame({'category': ['A', 'B', 'A', 'C', 'B', 'A']})
        encoder = FrequencyEncoder()
        encoder.fit(sample_data)
        transformed = encoder.transform(sample_data)
        expected_shape = (6, 1)
        
        if transformed.shape == expected_shape:
            print("  ✅ FrequencyEncoder functionality test passed")
        else:
            print(f"  ❌ FrequencyEncoder shape mismatch: got {transformed.shape}, expected {expected_shape}")
            return False
        
        # Test config import
        from config import PROPERTY_TYPES, SUBLOCALITIES, BROKER_OPTIONS
        print("  ✅ Configuration constants imported")
        
        # Test models module import
        from models import get_model_info
        print("  ✅ Models module imported")
        
        print("✅ Shared modules test passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Shared modules test failed: {e}")
        return False

def test_model_loading():
    """Test model loading and metadata"""
    print("\n🤖 Testing Model Loading...")
    
    try:
        # Find model files
        model_files = [f for f in os.listdir('models') if f.startswith('best_model_') and f.endswith('.joblib')]
        metadata_files = [f for f in os.listdir('models') if f.startswith('model_metadata_') and f.endswith('.joblib')]
        
        if not model_files:
            print("  ❌ No model files found")
            return False
        
        if not metadata_files:
            print("  ❌ No metadata files found")
            return False
        
        # Load latest model and metadata
        model_file = sorted(model_files)[-1]
        metadata_file = sorted(metadata_files)[-1]
        
        print(f"  📂 Loading {model_file}")
        model = joblib.load(os.path.join('models', model_file))
        
        print(f"  📂 Loading {metadata_file}")
        metadata = joblib.load(os.path.join('models', metadata_file))
        
        # Validate metadata structure
        required_metadata_keys = ['model_info', 'data_info', 'performance']
        for key in required_metadata_keys:
            if key not in metadata:
                print(f"  ❌ Missing metadata key: {key}")
                return False
        
        print(f"  ✅ Model type: {metadata['model_info']['name']}")
        print(f"  ✅ Performance R²: {metadata['performance']['validation_r2']:.4f}")
        print(f"  ✅ Features: {len(metadata['data_info']['selected_features'])}")
        
        print("✅ Model loading test passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Model loading test failed: {e}")
        return False

def test_prediction():
    """Test end-to-end prediction"""
    print("\n🔮 Testing Model Prediction...")
    
    try:
        # Load model and metadata
        model_files = [f for f in os.listdir('models') if f.startswith('best_model_') and f.endswith('.joblib')]
        metadata_files = [f for f in os.listdir('models') if f.startswith('model_metadata_') and f.endswith('.joblib')]
        
        model = joblib.load(os.path.join('models', sorted(model_files)[-1]))
        metadata = joblib.load(os.path.join('models', sorted(metadata_files)[-1]))
        
        # Test data
        test_cases = [
            {
                'brokertitle': 'Brokered by COMPASS',
                'type': 'Condo for sale',
                'beds': 2,
                'bath': 1.0,
                'propertysqft': 800.0,
                'sublocality': 'Manhattan'
            },
            {
                'brokertitle': 'Brokered by Douglas Elliman - 575 Madison Ave',
                'type': 'House for sale',
                'beds': 3,
                'bath': 2.0,
                'propertysqft': 1500.0,
                'sublocality': 'Brooklyn'
            }
        ]
        
        expected_features = metadata['data_info']['selected_features']
        
        for i, test_data in enumerate(test_cases):
            print(f"  🏠 Test case {i+1}:")
            
            # Prepare data
            df = pd.DataFrame([test_data])
            df = df[expected_features]
            
            # Make prediction
            log_prediction = model.predict(df)
            predicted_price = np.expm1(log_prediction[0])
            
            # Validate prediction
            if predicted_price > 0 and predicted_price < 1e8:  # Reasonable bounds
                print(f"    ✅ Predicted price: ${predicted_price:,.0f}")
            else:
                print(f"    ❌ Unreasonable price: ${predicted_price:,.0f}")
                return False
        
        print("✅ Prediction test passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Prediction test failed: {e}")
        return False

def test_flask_app():
    """Test Flask app health (if running)"""
    print("\n🌐 Testing Flask App...")
    
    try:
        # Check if Flask app is running
        response = requests.get('http://localhost:9696/health', timeout=5)
        
        if response.status_code == 200:
            print("  ✅ Flask app is running and healthy")
            
            # Test prediction endpoint
            test_data = {
                'brokertitle': 'Brokered by COMPASS',
                'type': 'Condo for sale',
                'beds': 2,
                'bath': 1.0,
                'propertysqft': 800.0,
                'sublocality': 'Manhattan'
            }
            
            pred_response = requests.post('http://localhost:9696/predict', json=test_data, timeout=10)
            
            if pred_response.status_code == 200:
                result = pred_response.json()
                if 'predicted_price' in result:
                    print(f"  ✅ Prediction API working: ${result['predicted_price']:,.0f}")
                    print("✅ Flask app test passed!")
                    return True
                else:
                    print("  ❌ Invalid prediction response format")
                    return False
            else:
                print(f"  ❌ Prediction endpoint error: {pred_response.status_code}")
                return False
        else:
            print(f"  ❌ Flask app health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException:
        print("  ⚠️  Flask app not running (this is OK if you haven't started it)")
        return True  # Don't fail the test if app is not running

def test_streamlit_app():
    """Test Streamlit app health (if running)"""
    print("\n📊 Testing Streamlit App...")
    
    try:
        # Check if Streamlit app is running
        response = requests.get('http://localhost:8501/_stcore/health', timeout=5)
        
        if response.status_code == 200:
            print("  ✅ Streamlit app is running and healthy")
            print("✅ Streamlit app test passed!")
            return True
        else:
            print(f"  ❌ Streamlit app health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException:
        print("  ⚠️  Streamlit app not running (this is OK if you haven't started it)")
        return True  # Don't fail the test if app is not running

def run_all_tests():
    """Run all system tests"""
    print("🧪 NYC HOUSING PRICE PREDICTOR - SYSTEM TESTS")
    print("=" * 60)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Shared Modules", test_shared_modules), 
        ("Model Loading", test_model_loading),
        ("Model Prediction", test_prediction),
        ("Flask App", test_flask_app),
        ("Streamlit App", test_streamlit_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} {test_name}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"🎯 OVERALL: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)