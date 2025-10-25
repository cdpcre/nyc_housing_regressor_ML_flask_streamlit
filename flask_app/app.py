"""
Enhanced Flask web application for NYC Housing Price Predictor
Combines REST API with HTML frontend using Bootstrap templates
"""
import os
import sys
import logging
import pandas as pd
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, send_file
from werkzeug.exceptions import BadRequest
import tempfile
import io

# Add script module to path (modules moved from shared to script)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
script_dir = os.path.join(parent_dir, 'script')
sys.path.insert(0, script_dir)

try:
    # Import FrequencyEncoder first and add to global namespace (needed for model loading)
    from utils import FrequencyEncoder
    globals()['FrequencyEncoder'] = FrequencyEncoder

    from predict import load_model_and_metadata, predict_price, batch_predict, get_model_info, get_price_category
    from config import (
        API_HOST, API_PORT, DEBUG_MODE, EXPECTED_FEATURES,
        PROPERTY_TYPES, SUBLOCALITIES, BROKER_OPTIONS, PRICE_RANGES
    )
    print(f"✅ Successfully imported script modules from: {script_dir}")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Script directory: {script_dir}")
    print(f"Script directory exists: {os.path.exists(script_dir)}")
    raise

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Load model at startup with error handling
try:
    model, metadata = load_model_and_metadata()
    model_info = get_model_info()
    logger.info(f"✅ Model loaded: {model_info['model_name']}")
    logger.info(f"✅ Performance: R² = {model_info['performance']['validation_r2']:.4f}")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    model, metadata, model_info = None, None, None

@app.context_processor
def inject_model_info():
    """Inject model info into all templates"""
    return {
        'model_info': model_info,
        'property_types': PROPERTY_TYPES,
        'sublocalities': SUBLOCALITIES,
        'brokers': BROKER_OPTIONS
    }

# HTML Routes
@app.route('/')
def index():
    """Main prediction page with HTML form"""
    return render_template('index.html')

@app.route('/batch')
def batch():
    """Batch prediction page with file upload"""
    return render_template('batch.html')

@app.route('/api-docs')
def api_docs():
    """API documentation page"""
    return render_template('api_docs.html')

@app.route('/download-sample')
def download_sample():
    """Download sample CSV file for batch predictions"""
    sample_data = {
        'brokertitle': ['Brokered by COMPASS', 'Brokered by Douglas Elliman - 575 Madison Ave'],
        'type': ['Condo for sale', 'House for sale'],
        'beds': [2, 3],
        'bath': [1.0, 2.0],
        'propertysqft': [800.0, 1200.0],
        'sublocality': ['Manhattan', 'Brooklyn']
    }
    
    df = pd.DataFrame(sample_data)
    
    # Create temporary file
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    # Create BytesIO for Flask send_file
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        as_attachment=True,
        download_name='sample_properties.csv',
        mimetype='text/csv'
    )

# API Routes (Keep existing functionality)
@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict NYC housing price for input property data.
    
    Expected JSON payload:
    {
        "brokertitle": "Brokered by COMPASS",
        "type": "Condo for sale", 
        "beds": 2,
        "bath": 1.0,
        "propertysqft": 800.0,
        "sublocality": "Manhattan"
    }
    """
    if not model or not metadata:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Get input data
        if request.is_json:
            input_data = request.get_json()
        else:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        if not input_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate required features
        missing_features = [f for f in EXPECTED_FEATURES if f not in input_data]
        if missing_features:
            return jsonify({'error': f'Missing required features: {missing_features}'}), 400
        
        # Make prediction
        predicted_price = predict_price(input_data)
        
        # Format response
        response = {
            'predicted_price': round(float(predicted_price), 2),
            'price_formatted': f"${predicted_price:,.0f}",
            'price_category': get_price_category(predicted_price),
            'model_info': metadata['model_info']['name'],
            'features_used': metadata['data_info']['selected_features'],
            'model_performance': {
                'validation_r2': round(metadata['performance']['validation_r2'], 4),
                'validation_rmse': round(metadata['performance']['validation_rmse'], 0)
            }
        }
        
        return jsonify(response)
        
    except ValueError as e:
        logger.error(f"Input validation error: {e}")
        return jsonify({'error': f'Input validation error: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if not model or not metadata:
        return jsonify({
            'status': 'unhealthy',
            'error': 'Model not loaded'
        }), 500
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'model_type': metadata['model_info']['name'],
        'features_required': metadata['data_info']['selected_features'],
        'api_version': '2.0',
        'endpoints': {
            'predict': '/predict',
            'health': '/health',
            'model_info': '/model_metadata_info',
            'web_app': '/',
            'batch_upload': '/batch',
            'api_docs': '/api-docs'
        }
    })

@app.route('/model_metadata_info', methods=['GET'])
def model_metadata_info():
    """Get detailed model metadata information"""
    if not metadata:
        return jsonify({'error': 'Model metadata not loaded'}), 500
    
    return jsonify(metadata)

@app.route('/model_info', methods=['GET'])
def model_info_text():
    """Get model string representation (legacy endpoint)"""
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return str(model)

# Favicon route to prevent 404 errors
@app.route('/favicon.ico')
def favicon():
    """Serve a simple favicon to prevent 404 errors"""
    return '', 204  # No content response

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with HTML or JSON based on request"""
    if request.is_json or request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with HTML or JSON based on request"""
    if request.is_json or request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    
    return render_template('error.html',
                         error_code=500, 
                         error_message="Internal server error"), 500

@app.errorhandler(BadRequest)
def bad_request(error):
    """Handle 400 errors"""
    if request.is_json or request.path.startswith('/api/'):
        return jsonify({'error': 'Bad request'}), 400
    
    flash('Invalid request data', 'error')
    return redirect(url_for('index'))

# Development routes (only in debug mode)
if DEBUG_MODE:
    @app.route('/debug/test-prediction')
    def debug_test_prediction():
        """Debug endpoint to test prediction with sample data"""
        sample_data = {
            'brokertitle': 'Brokered by COMPASS',
            'type': 'Condo for sale',
            'beds': 2,
            'bath': 1.0,
            'propertysqft': 800.0,
            'sublocality': 'Manhattan'
        }
        
        try:
            predicted_price = predict_price(sample_data)
            return jsonify({
                'status': 'success',
                'sample_data': sample_data,
                'predicted_price': predicted_price,
                'price_formatted': f"${predicted_price:,.0f}"
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e)
            }), 500

if __name__ == '__main__':
    print("🚀 Starting NYC Housing Price Predictor Web App...")
    if model_info:
        print(f"📊 Model: {model_info['model_name']}")
        print(f"🎯 Performance: R² = {model_info['performance']['validation_r2']:.4f}")
    print("🌐 Available interfaces:")
    print(f"   🏠 Web App: http://{API_HOST}:{API_PORT}/")
    print(f"   📁 Batch Upload: http://{API_HOST}:{API_PORT}/batch")
    print(f"   📚 API Docs: http://{API_HOST}:{API_PORT}/api-docs")
    print("🔧 API endpoints:")
    print(f"   POST /predict - Make price predictions")
    print(f"   GET /health - Health check")
    print(f"   GET /model_metadata_info - Model metadata")
    print()
    
    app.run(
        debug=DEBUG_MODE, 
        host=API_HOST, 
        port=API_PORT,
        threaded=True  # Enable threading for better concurrent performance
    )