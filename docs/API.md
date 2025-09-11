# NYC Housing Price Predictor API

## Overview

The NYC Housing Price Predictor provides both a REST API and web interfaces for predicting real estate prices in New York City using machine learning.

## Base URL

```
http://localhost:9696
```

## Authentication

No authentication required for public endpoints.

## Endpoints

### POST /predict

Predict housing price for a single property.

**Request Body:**
```json
{
  "brokertitle": "string",     // Real estate broker/agency
  "type": "string",            // Property type
  "beds": integer,             // Number of bedrooms
  "bath": float,               // Number of bathrooms  
  "propertysqft": float,       // Property size in square feet
  "sublocality": "string"      // NYC area/borough
}
```

**Example Request:**
```json
{
  "brokertitle": "Brokered by COMPASS",
  "type": "Condo for sale",
  "beds": 2,
  "bath": 1.0,
  "propertysqft": 800.0,
  "sublocality": "Manhattan"
}
```

**Response:**
```json
{
  "predicted_price": 1323814.25,
  "price_formatted": "$1,323,814",
  "price_category": "Mid-Range",
  "model_info": "XGBoost (Freq)",
  "features_used": [
    "brokertitle", "type", "beds", "bath", "propertysqft", "sublocality"
  ],
  "model_performance": {
    "validation_r2": 0.7183,
    "validation_rmse": 1215863
  }
}
```

**Status Codes:**
- `200` - Successful prediction
- `400` - Invalid input data
- `500` - Internal server error

### GET /health

Health check endpoint to verify API status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "XGBoost (Freq)",
  "features_required": [
    "brokertitle", "type", "beds", "bath", "propertysqft", "sublocality"
  ],
  "api_version": "2.0",
  "endpoints": {
    "predict": "/predict",
    "health": "/health", 
    "model_info": "/model_metadata_info",
    "web_app": "/",
    "batch_upload": "/batch",
    "api_docs": "/api-docs"
  }
}
```

### GET /model_metadata_info

Get detailed model information and metadata.

**Response:**
```json
{
  "model_info": {
    "name": "XGBoost (Freq)",
    "created_timestamp": "2025-09-09T..."
  },
  "performance": {
    "validation_r2": 0.7183,
    "validation_rmse": 1215863
  },
  "data_info": {
    "selected_features": [...]
  }
}
```

## Input Validation

### Required Fields

All fields in the prediction request are required:

- `brokertitle`: Must be a valid broker name
- `type`: Must be a valid property type
- `beds`: Integer between 0-8
- `bath`: Float between 0-6  
- `propertysqft`: Float between 200-5000
- `sublocality`: Must be a valid NYC area/borough

### Valid Values

**Property Types:**
- "Condo for sale"
- "House for sale" 
- "Co-op for sale"
- "Multi-family home for sale"
- "Townhouse for sale"
- "Pending"
- "Contingent"
- "Land for sale"
- "For sale"
- "Foreclosure"

**NYC Areas/Boroughs:**
- "Manhattan"
- "Brooklyn"
- "Queens" 
- "Bronx County"
- "Staten Island"
- "New York"
- "Kings County"
- "Queens County"
- "Richmond County"
- "New York County"
- "The Bronx"

**Top Brokers:**
- "Brokered by COMPASS"
- "Brokered by Douglas Elliman - 575 Madison Ave"
- "Brokered by Brown Harris Stevens"
- "Brokered by Corcoran East Side"
- And many more...

## Error Handling

### Error Response Format

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Errors

**400 Bad Request:**
```json
{
  "error": "Missing required features: ['beds', 'bath']"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Prediction error: Model prediction failed"
}
```

## Rate Limiting

No rate limiting currently implemented. For production use, consider implementing rate limiting based on your requirements.

## Code Examples

### Python with requests

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

if response.status_code == 200:
    result = response.json()
    print(f"Predicted price: {result['price_formatted']}")
else:
    print(f"Error: {response.json()['error']}")

# Health check
health = requests.get('http://localhost:9696/health')
print(f"API Status: {health.json()['status']}")
```

### JavaScript/Node.js

```javascript
// Single prediction
const response = await fetch('http://localhost:9696/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    brokertitle: "Brokered by COMPASS",
    type: "Condo for sale", 
    beds: 2,
    bath: 1.0,
    propertysqft: 800.0,
    sublocality: "Manhattan"
  })
});

const data = await response.json();
console.log('Predicted price:', data.price_formatted);
```

### cURL

```bash
# Single prediction
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "brokertitle": "Brokered by COMPASS",
    "type": "Condo for sale",
    "beds": 2,
    "bath": 1.0,
    "propertysqft": 800.0,
    "sublocality": "Manhattan"
  }'

# Health check
curl http://localhost:9696/health
```

## Web Interface

In addition to the REST API, the application provides web interfaces:

- **Main Web App**: `http://localhost:9696/` - Interactive form-based predictions
- **Batch Upload**: `http://localhost:9696/batch` - CSV file upload for bulk predictions  
- **API Documentation**: `http://localhost:9696/api-docs` - Interactive API explorer
- **Streamlit App**: `http://localhost:8501/` - Alternative Streamlit interface

## Model Information

**Model Type:** XGBoost Regressor with Frequency Encoding

**Performance Metrics:**
- R² Score: 0.7183 (explains ~72% of price variance)
- RMSE: $1,215,863 (average prediction error)

**Features Used:**
- Property characteristics (beds, bath, square footage)
- Location (NYC borough/area)
- Property type (condo, house, co-op, etc.)
- Real estate broker/agency

**Training Data:** 
- Source: NYC housing listings dataset
- Size: 4,000+ properties after cleaning
- Geographic coverage: All NYC boroughs
- Price range: $69K - $55M (after outlier removal)