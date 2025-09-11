import joblib
import pandas as pd
import numpy as np
import sys
import os

# Add shared directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
shared_dir = os.path.join(project_root, 'shared')
models_dir = os.path.join(project_root, 'models')

sys.path.insert(0, shared_dir)
sys.path.insert(0, project_root)

# Change to project root directory for proper file access
os.chdir(project_root)

if __name__ == '__main__':
    # Test model loading
    from utils import FrequencyEncoder
    
    # Add FrequencyEncoder to global namespace (needed for model loading)
    globals()['FrequencyEncoder'] = FrequencyEncoder

    try:
        # Look for the most recent model files in the models directory
        model_files = [f for f in os.listdir('models') if f.startswith('best_model_') and f.endswith('.joblib')]
        metadata_files = [f for f in os.listdir('models') if f.startswith('model_metadata_') and f.endswith('.joblib')]
        
        if not model_files or not metadata_files:
            print("❌ No model files found in models/ directory")
            print("Available files in models/:")
            for f in os.listdir('models'):
                print(f"  - {f}")
            exit(1)
        
        # Use the first available model (or most recent)
        model_file = sorted(model_files)[-1]  # Get the latest
        metadata_file = sorted(metadata_files)[-1]  # Get the latest
        
        print(f"Loading model: {model_file}")
        print(f"Loading metadata: {metadata_file}")
        
        model = joblib.load(os.path.join('models', model_file))
        metadata = joblib.load(os.path.join('models', metadata_file))
        print('✅ Models loaded successfully')
        
        # Test prediction
        test_data = {
            'brokertitle': 'Brokered by COMPASS',
            'type': 'Condo for sale', 
            'beds': 2,
            'bath': 1.0,
            'propertysqft': 800.0,
            'sublocality': 'Manhattan'
        }
        
        expected_features = metadata['data_info']['selected_features']
        print(f'Expected features: {expected_features}')
        
        df = pd.DataFrame([test_data])
        df = df[expected_features]
        print(f'DataFrame shape: {df.shape}')
        print(f'DataFrame columns: {list(df.columns)}')
        
        log_prediction = model.predict(df)
        predicted_price = np.expm1(log_prediction[0])
        
        print(f'✅ Test prediction successful')
        print(f'Predicted price: ${predicted_price:.0f}')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()