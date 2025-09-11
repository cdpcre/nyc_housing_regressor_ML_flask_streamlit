import sys
import os

# Add shared module to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
shared_dir = os.path.join(parent_dir, 'shared')
sys.path.insert(0, shared_dir)

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import FrequencyEncoder first and add to global namespace (needed for model loading)
from utils import FrequencyEncoder
globals()['FrequencyEncoder'] = FrequencyEncoder

from models import predict_price, get_model_info, batch_predict
from config import PROPERTY_TYPES, SUBLOCALITIES, BROKER_OPTIONS, PRICE_RANGES

# Page configuration
st.set_page_config(
    page_title="NYC Housing Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model info with caching
@st.cache_data
def get_cached_model_info():
    """Get model info with caching for performance"""
    try:
        return get_model_info()
    except Exception as e:
        st.error(f"Error loading model info: {e}")
        st.info("Please ensure the model files are in the models directory.")
        st.stop()

def prepare_features(input_data, expected_features):
    """Prepare input data for prediction"""
    # Create DataFrame with correct feature order
    df = pd.DataFrame([input_data])
    df = df[expected_features]  # Ensure correct order
    return df

def predict_price_cached(input_data, use_log_target=True):
    """Make price prediction with caching"""
    try:
        predicted_price = predict_price(input_data, use_log_target)
        return float(predicted_price)
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return None

def create_price_visualization(predicted_price, comparable_ranges):
    """Create a visualization showing the predicted price in context"""
    fig = go.Figure()
    
    # Add price ranges as horizontal bars
    categories = ['Budget Range', 'Mid-Range', 'Luxury Range', 'Your Prediction']
    values = [comparable_ranges['budget'], comparable_ranges['mid'], 
              comparable_ranges['luxury'], predicted_price]
    colors = ['lightblue', 'blue', 'darkblue', 'red']
    
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker_color=colors,
        text=[f'${v:,.0f}' for v in values],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Price Comparison",
        xaxis_title="Price ($)",
        height=300,
        showlegend=False
    )
    
    return fig

# Load model info
model_info = get_cached_model_info()

# Main app
def main():
    # Header
    st.title("🏠 NYC Housing Price Predictor")
    st.markdown("### Predict New York City housing prices using machine learning")
    
    # Display model info
    with st.expander("📊 Model Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model Type", model_info['model_name'])
        with col2:
            st.metric("R² Score", f"{model_info['performance']['validation_r2']:.4f}")
        with col3:
            st.metric("RMSE", f"${model_info['performance']['validation_rmse']:,.0f}")
    
    # Create two tabs for different input methods
    tab1, tab2 = st.tabs(["🏠 Single Property Prediction", "📁 Batch Prediction"])
    
    with tab1:
        single_property_interface()
    
    with tab2:
        batch_prediction_interface()

def single_property_interface():
    """Interface for single property prediction"""
    st.markdown("## Enter Property Details")
    
    # Get expected features from model info
    expected_features = model_info['features']
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏠 Property Characteristics")
        
        # Beds
        beds = st.selectbox(
            "Number of Bedrooms",
            options=[0, 1, 2, 3, 4, 5, 6, 7, 8],
            index=2,  # Default to 2
            help="Select the number of bedrooms"
        )
        
        # Bath
        bath = st.selectbox(
            "Number of Bathrooms",
            options=[0, 1, 2, 3, 4, 5, 6],
            index=1,  # Default to 1
            help="Select the number of bathrooms"
        )
        
        # Property square feet
        propertysqft = st.slider(
            "Property Size (sq ft)",
            min_value=200,
            max_value=5000,
            value=800,
            step=50,
            help="Drag to select property size in square feet"
        )
        
    with col2:
        st.markdown("### 📍 Location & Broker")
        
        # Property type
        property_type = st.selectbox(
            "Property Type",
            options=PROPERTY_TYPES,
            index=0,
            help="Select the type of property"
        )
        
        # Sublocality
        sublocality = st.selectbox(
            "Area/Borough",
            options=SUBLOCALITIES,
            index=0,
            help="Select the NYC area or borough"
        )
        
        # Broker title
        brokertitle = st.selectbox(
            "Broker/Agency",
            options=BROKER_OPTIONS,
            index=0,
            help="Select the real estate broker or agency"
        )
    
    # Prediction button and results
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔮 Predict Price", type="primary", use_container_width=True):
            # Prepare input data
            input_data = {
                'brokertitle': brokertitle,
                'type': property_type,
                'beds': beds,
                'bath': bath,
                'propertysqft': propertysqft,
                'sublocality': sublocality
            }
            
            # Make prediction
            with st.spinner("Analyzing property and predicting price..."):
                try:
                    predicted_price = predict_price_cached(input_data)
                    
                    if predicted_price:
                        # Display results
                        st.success("Prediction Complete!")
                        
                        # Large price display
                        st.markdown(f"### 💰 Predicted Price: ${predicted_price:,.0f}")
                        
                        # Price context
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Price per sq ft", f"${predicted_price/propertysqft:.0f}")
                        with col2:
                            confidence = model_info['performance']['validation_r2']
                            st.metric("Model Confidence", f"{confidence:.1%}")
                        with col3:
                            if predicted_price < 500000:
                                category = "Budget-Friendly"
                            elif predicted_price < 1500000:
                                category = "Mid-Range"
                            else:
                                category = "Luxury"
                            st.metric("Price Category", category)
                        
                        # Price visualization
                        st.markdown("### 📊 Price Comparison")
                        fig = create_price_visualization(predicted_price, PRICE_RANGES)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Property summary
                        with st.expander("📋 Property Summary"):
                            st.write(f"**Property Details:**")
                            st.write(f"- Location: {sublocality}")
                            st.write(f"- Type: {property_type}")
                            st.write(f"- Size: {beds} bed, {bath} bath, {propertysqft:,} sq ft")
                            st.write(f"- Broker: {brokertitle}")
                            st.write(f"- Predicted Price: ${predicted_price:,.0f}")
                            st.write(f"- Price per sq ft: ${predicted_price/propertysqft:.0f}")
                        
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")

def batch_prediction_interface():
    """Interface for batch predictions via file upload"""
    st.markdown("## Batch Property Predictions")
    st.markdown("Upload a CSV file with multiple properties for batch predictions")
    
    # Show expected format
    with st.expander("📋 Expected CSV Format"):
        expected_features = model_info['features']
        sample_data = {
            'brokertitle': ['Brokered by COMPASS', 'Brokered by Douglas Elliman - 575 Madison Ave'],
            'type': ['Condo for sale', 'House for sale'],
            'beds': [2, 3],
            'bath': [1.0, 2.0],
            'propertysqft': [800.0, 1200.0],
            'sublocality': ['Manhattan', 'Brooklyn']
        }
        sample_df = pd.DataFrame(sample_data)
        st.markdown("**Required columns:**")
        st.write(expected_features)
        st.markdown("**Sample format:**")
        st.dataframe(sample_df)
        
        # Download sample CSV
        csv_sample = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample CSV",
            data=csv_sample,
            file_name="sample_properties.csv",
            mime="text/csv"
        )
    
    # File upload
    uploaded_file = st.file_uploader(
        "🎯 Drop your CSV file here or click to browse",
        type=['csv'],
        help="Upload a CSV file with property data for batch predictions"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ File uploaded successfully! Found {len(df)} properties.")
            
            # Show data preview
            st.markdown("### 📊 Data Preview")
            st.dataframe(df.head())
            
            # Validate columns
            expected_features = model_info['features']
            missing_columns = [col for col in expected_features if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ Missing required columns: {missing_columns}")
                return
            
            # Prediction button
            if st.button("🚀 Run Batch Predictions", type="primary"):
                with st.spinner(f"Processing {len(df)} properties..."):
                    try:
                        # Prepare data for batch prediction
                        input_df = df[expected_features].copy()
                        
                        # Make batch predictions
                        predictions = batch_predict(input_df)
                        
                        # Add predictions to dataframe
                        df['predicted_price'] = predictions
                        df['price_formatted'] = df['predicted_price'].apply(lambda x: f"${x:,.0f}")
                        
                        st.success("✅ Batch predictions completed!")
                        
                        # Display results
                        st.markdown("### 📊 Prediction Results")
                        
                        # Summary stats
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Properties", len(df))
                        with col2:
                            st.metric("Avg Price", f"${df['predicted_price'].mean():,.0f}")
                        with col3:
                            st.metric("Min Price", f"${df['predicted_price'].min():,.0f}")
                        with col4:
                            st.metric("Max Price", f"${df['predicted_price'].max():,.0f}")
                        
                        # Results table
                        display_df = df[expected_features + ['predicted_price', 'price_formatted']].copy()
                        st.dataframe(display_df, use_container_width=True)
                        
                        # Price distribution chart
                        st.markdown("### 📈 Price Distribution")
                        fig = px.histogram(
                            df, 
                            x='predicted_price',
                            nbins=20,
                            title="Distribution of Predicted Prices"
                        )
                        fig.update_xaxis(title="Predicted Price ($)")
                        fig.update_yaxis(title="Number of Properties")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Download results
                        csv_results = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results CSV",
                            data=csv_results,
                            file_name="property_predictions.csv",
                            mime="text/csv"
                        )
                        
                    except Exception as e:
                        st.error(f"Prediction error: {str(e)}")
                        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.info("Please make sure your file is a valid CSV with the correct format.")

# Sidebar with additional info
def sidebar_info():
    """Display additional information in sidebar"""
    st.sidebar.markdown("## 📊 Model Info")
    st.sidebar.info(f"**Model:** {model_info['model_name']}")
    st.sidebar.info(f"**R² Score:** {model_info['performance']['validation_r2']:.4f}")
    st.sidebar.info(f"**Training Date:** {model_info['created']}")
    
    st.sidebar.markdown("## 💡 Tips")
    st.sidebar.markdown("""
    - **Higher sq ft** generally means higher prices
    - **Manhattan** properties tend to be more expensive
    - **Luxury brokers** may handle higher-priced properties
    - **Co-ops** are often less expensive than condos
    """)
    
    st.sidebar.markdown("## 🚀 About")
    st.sidebar.markdown(f"""
    This app uses an **XGBoost model** trained on NYC housing data 
    to predict property prices based on key characteristics.
    
    **Model Performance:**
    - R² = {model_info['performance']['validation_r2']:.4f} (explains ~{model_info['performance']['validation_r2']*100:.1f}% of price variance)
    - RMSE = ${model_info['performance']['validation_rmse']:,.0f} (average prediction error)
    """)

if __name__ == "__main__":
    sidebar_info()
    main()