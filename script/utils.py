from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

class FrequencyEncoder(BaseEstimator, TransformerMixin):
    """
    Custom frequency encoder for categorical features using scikit-learn interface.
    Replaces categorical values with their frequency of occurrence in the training data.
    """
    
    def __init__(self, handle_unknown='zero'):
        """
        Parameters:
        - handle_unknown: how to handle unknown categories during transform
          'zero': assign frequency 0
          'rare': assign frequency 1
        """
        self.handle_unknown = handle_unknown
        self.frequency_maps_ = {}
        self.feature_names_in_ = None
        
    def fit(self, X, y=None):
        """Fit the frequency encoder by computing frequencies for each column."""
        
        # Convert to DataFrame if numpy array
        if hasattr(X, 'columns'):
            df = X
            self.feature_names_in_ = list(X.columns)
        else:
            df = pd.DataFrame(X)
            self.feature_names_in_ = [f'feature_{i}' for i in range(X.shape[1])]
        
        # Compute frequency maps for each column
        for col in df.columns:
            value_counts = df[col].value_counts()
            self.frequency_maps_[col] = value_counts.to_dict()
            
        return self
    
    def transform(self, X):
        """Transform categorical values to their frequencies."""
        
        
        # Convert to DataFrame if numpy array
        if hasattr(X, 'columns'):
            df = X.copy()
        else:
            df = pd.DataFrame(X, columns=self.feature_names_in_)
        
        # Transform each column
        for col in df.columns:
            if col in self.frequency_maps_:
                # Map values to frequencies
                frequency_map = self.frequency_maps_[col]
                
                if self.handle_unknown == 'zero':
                    # Unknown categories get frequency 0
                    df[col] = df[col].map(frequency_map).fillna(0)
                else:  # handle_unknown == 'rare'
                    # Unknown categories get frequency 1 (treated as rare)
                    df[col] = df[col].map(frequency_map).fillna(1)
        
        return df.values
    
    def get_feature_names_out(self, input_features=None):
        """Get output feature names."""
        if input_features is None:
            return np.array(self.feature_names_in_)
        return np.array(input_features)

