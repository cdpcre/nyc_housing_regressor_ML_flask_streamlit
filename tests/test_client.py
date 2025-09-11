import requests
import json

# API endpoint
url = 'http://localhost:9696/predict'

# Example property data for prediction
sample_properties = [
    {
        "name": "Manhattan Condo",
        "data": {
            "brokertitle": "Brokered by COMPASS",
            "type": "Condo for sale",
            "beds": 2,
            "bath": 1.0,
            "propertysqft": 800.0,
            "sublocality": "Manhattan"
        }
    },
    {
        "name": "Brooklyn House",
        "data": {
            "brokertitle": "Brokered by Douglas Elliman - 575 Madison Ave",
            "type": "House for sale",
            "beds": 3,
            "bath": 2.0,
            "propertysqft": 1200.0,
            "sublocality": "Brooklyn"
        }
    },
    {
        "name": "Queens Co-op",
        "data": {
            "brokertitle": "Brokered by Brown Harris Stevens",
            "type": "Co-op for sale",
            "beds": 1,
            "bath": 1.0,
            "propertysqft": 600.0,
            "sublocality": "Queens"
        }
    }
]

def test_prediction(property_data, property_name):
    """Test a single prediction"""
    try:
        response = requests.post(url, json=property_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"🏠 {property_name}")
            print(f"   Predicted Price: {result['price_formatted']}")
            print(f"   Model R²: {result['model_performance']['validation_r2']}")
            print(f"   RMSE: ${result['model_performance']['validation_rmse']:,.0f}")
            print(f"   Model Used: {result['model_info']}")
            print()
            return True
        else:
            print(f"❌ Error for {property_name}: {response.status_code}")
            print(f"   {response.json()}")
            print()
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask app is running on localhost:9696")
        return False
    except Exception as e:
        print(f"❌ Error for {property_name}: {e}")
        return False

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get('http://localhost:9696/health')
        if response.status_code == 200:
            health_info = response.json()
            print("✅ Health Check Passed")
            print(f"   Status: {health_info['status']}")
            print(f"   Model: {health_info['model_type']}")
            print()
            return True
    except:
        print("❌ Health check failed")
        return False

if __name__ == '__main__':
    print("🧪 Testing NYC Housing Price Prediction API")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("⚠️  API not available. Start the Flask app with: python app.py")
        exit(1)

    # Get model info
    print("📋 Fetching Model Info:")
    print("-" * 30)
    try:
        response = requests.get('http://localhost:9696/model_info')
        if response.status_code == 200:
            model_info = response.text
            print(model_info)
        else:
            print("❌ Failed to fetch model info")
    except Exception as e:
        print(f"❌ Error fetching model info: {e}")
    print()

    # Test predictions
    print("📊 Testing Predictions:")
    print("-" * 30)
    
    for property_info in sample_properties:
        test_prediction(property_info["data"], property_info["name"])
    
    print("✅ All tests completed!")
    print("\n💡 Usage Instructions:")
    print("   1. Start the API: python app.py")
    print("   2. Send POST requests to http://localhost:9696/predict")
    print("   3. Include JSON data with required features:")
    print("      ['brokertitle', 'type', 'beds', 'bath', 'propertysqft', 'sublocality']")