FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model files
COPY app.py .
COPY utils.py .
COPY best_model_xgboost_freq_20250909.joblib .
COPY model_metadata_xgboost_freq_20250909.joblib .

EXPOSE 9696

CMD ["python", "app.py"]