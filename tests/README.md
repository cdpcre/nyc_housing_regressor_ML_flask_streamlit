# 🧪 Test Suite - NYC Housing Price Predictor

Comprehensive testing suite for the NYC Housing Price Predictor application.

## 📁 Test Files

### `test_model.py`
**Basic Model Test** - Tests core model functionality

**What it tests:**
- ✅ Model and metadata loading from `models/` directory
- ✅ FrequencyEncoder import and configuration
- ✅ Single prediction functionality
- ✅ Data preprocessing pipeline

**Usage:**
```bash
cd nyc_housing_regressor_ML_flask_streamlit
python tests/test_model.py
```

**Expected Output:**
```
Loading model: best_model_xgboost_freq_20250910.joblib
Loading metadata: model_metadata_xgboost_freq_20250910.joblib
✅ Models loaded successfully
Expected features: ['brokertitle', 'type', 'beds', 'bath', 'propertysqft', 'sublocality']
DataFrame shape: (1, 6)
DataFrame columns: ['brokertitle', 'type', 'beds', 'bath', 'propertysqft', 'sublocality']
✅ Test prediction successful
Predicted price: $1323814
```

### `test_system.py`
**Comprehensive System Test** - Full end-to-end testing

**What it tests:**
- 🏗️ **Project Structure**: All required directories and files
- 🔧 **Shared Modules**: Import and functionality of shared utilities
- 🤖 **Model Loading**: Model and metadata validation
- 🔮 **Model Prediction**: End-to-end prediction testing with multiple test cases
- 🌐 **Flask App**: Web application health and API endpoints (if running)
- 📊 **Streamlit App**: Data science interface health check (if running)

**Usage:**
```bash
cd nyc_housing_regressor_ML_flask_streamlit
python tests/test_system.py
```

## 🚀 Running Tests

### Prerequisites
1. **Environment Setup:**
   ```bash
   conda activate env_mlzoomcamp
   cd nyc_housing_regressor_ML_flask_streamlit
   ```

2. **Required Components:**
   - Trained model files in `models/` directory
   - Raw data file: `data/raw/NY-House-Dataset.csv`
   - All shared modules properly installed

### Test Scenarios

#### 1. **Basic Testing** (Model Only)
```bash
# Test just the model functionality
python tests/test_model.py
```

#### 2. **Full System Testing** (Recommended)
```bash
# Test everything including live apps
python tests/test_system.py
```

#### 3. **Testing with Live Applications**
For complete testing, start both applications first:

**Terminal 1:**
```bash
cd flask_app
python app.py
```

**Terminal 2:**
```bash
cd streamlit_app
streamlit run streamlit_app.py
```

**Terminal 3:**
```bash
# Run tests
python tests/test_system.py
```

## 📊 Test Results Interpretation

### ✅ Success Indicators
- **All tests pass**: System is fully functional
- **Flask/Streamlit warnings**: Apps not running (acceptable for basic testing)

### ❌ Failure Indicators
- **Import errors**: Check Python path and shared modules
- **Model loading errors**: Verify model files in `models/` directory
- **Prediction errors**: Check data format and model compatibility
- **App health failures**: Verify apps are running and accessible

## 🔧 Troubleshooting

### Common Issues

#### 1. **Import Errors**
```
ModuleNotFoundError: No module named 'shared'
```
**Solution:** Tests automatically configure Python path. Run from project root.

#### 2. **Model Files Not Found**
```
❌ No model files found in models/ directory
```
**Solution:** Train a model using the notebooks to generate model files.

#### 3. **App Connection Errors**
```
⚠️ Flask app not running
```
**Solution:** This is OK for basic testing. Start apps for full testing.

#### 4. **Data File Missing**
```
❌ data/raw/NY-House-Dataset.csv - MISSING
```
**Solution:** Ensure the dataset is in the correct location.

### Manual Verification

If tests fail, you can manually verify components:

```bash
# Check model files
ls -la models/

# Check data files  
ls -la data/raw/

# Check shared modules
python -c "import sys; sys.path.append('shared'); from utils import FrequencyEncoder; print('✅ Import OK')"

# Test Flask app manually
curl http://localhost:9696/health

# Test prediction manually
curl -X POST http://localhost:9696/predict -H "Content-Type: application/json" -d '{
  "brokertitle": "Brokered by COMPASS",
  "type": "Condo for sale", 
  "beds": 2,
  "bath": 1.0,
  "propertysqft": 800.0,
  "sublocality": "Manhattan"
}'
```

## 🎯 Test Coverage

### Components Tested
- ✅ **Data Pipeline**: Loading, preprocessing, feature engineering
- ✅ **Model System**: Loading, metadata, predictions
- ✅ **Shared Utilities**: FrequencyEncoder, configuration, model utilities
- ✅ **Web Applications**: Flask API, Streamlit interface
- ✅ **File Structure**: All required directories and files
- ✅ **Integration**: End-to-end prediction workflow

### Performance Benchmarks
- **Model Loading**: Should complete in < 2 seconds
- **Single Prediction**: Should complete in < 100ms
- **API Response**: Should return valid JSON with predicted price
- **Health Checks**: Should return 200 status codes

## 🚀 Continuous Integration

For automated testing in CI/CD pipelines:

```bash
#!/bin/bash
# CI test script
set -e

echo "🧪 Running NYC Housing Price Predictor Tests..."

# Run basic model test
python tests/test_model.py

# Run system test (without requiring live apps)
python tests/test_system.py

echo "✅ All tests passed!"
```

---

**💡 Tip:** Run tests after any significant changes to verify system integrity!