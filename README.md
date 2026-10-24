# Chennai Rain Prediction

A completed machine learning project that predicts whether it will rain tomorrow in Chennai using historical rainfall patterns, engineered time-based features, and a trained Random Forest classifier.

## Project Overview

This project is designed to solve a practical classification problem: predicting next-day rain/no-rain conditions for Chennai based on daily rainfall history and seasonal patterns. The workflow includes data preprocessing, feature engineering, model training, validation, and a simple API/UI for inference.

### Key results

- Model type: Random Forest Classifier
- Target: Rain tomorrow (Yes/No)
- Best-performing baseline: Random Forest
- Approximate accuracy: 79.4%
- ROC-AUC: 0.888

## Why this project stands out

- Uses real rainfall data with time-series feature engineering
- Includes lag and rolling rainfall features to capture short-term weather patterns
- Adds seasonal cues such as month and monsoon signals
- Provides both backend prediction API and interactive frontend access
- Ready to run locally or extend for deployment

## Tech Stack

- Python
- Pandas and NumPy
- Scikit-learn
- FastAPI
- Streamlit
- Joblib

## Project Structure

```text
Rain_Prediction_app/
├── app/
│   ├── main.py
│   ├── model_loader.py
│   ├── predict.py
│   └── schemas.py
├── ml/
│   ├── preprocess_weather_data.py
│   ├── train_weather_models.py
│   └── save_model.py
├── ui/
│   └── streamlit_app.py
├── data/
│   └── (processed/raw datasets)
├── models/
│   ├── weather_random_forest_model.joblib
│   └── weather_random_forest_metadata.json
├── requirements.txt
├── README.md
└── weather_model_metrics.csv
```

## Features

- Daily Chennai rainfall aggregation
- Duplicate cleanup and missing-date handling
- Lag and rolling rainfall features
- Monsoon and calendar feature encoding
- Model comparison and evaluation
- Prediction API with request validation
- Streamlit dashboard for user-friendly interaction

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Rain_Prediction_app.git
cd Rain_Prediction_app
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

### Start the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open the API docs here:

```text
http://localhost:8000/docs
```

### Start the Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

This launches the interactive Chennai Rain Predictor dashboard.

## API Example

The backend accepts a JSON payload aligned with the trained model features:

```json
{
  "RainfallCity_mm": 4.5,
  "RainToday": 1,
  "RainfallLag1_mm": 6.2,
  "RainfallLag2_mm": 3.9,
  "RainfallLag3_mm": 5.1,
  "RainfallLag7_mm": 7.8,
  "RainfallRolling3_mm": 5.1,
  "RainfallRolling7_mm": 5.5,
  "Month": 11,
  "DayOfYear": 315,
  "MonthSin": 0.866,
  "MonthCos": 0.5,
  "DaySin": 0.12,
  "DayCos": 0.99,
  "StationCount": 8,
  "RecordCount": 8,
  "IsNE_Monsoon": 1
}
```

Example request:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "RainfallCity_mm": 4.5,
    "RainToday": 1,
    "RainfallLag1_mm": 6.2,
    "RainfallLag2_mm": 3.9,
    "RainfallLag3_mm": 5.1,
    "RainfallLag7_mm": 7.8,
    "RainfallRolling3_mm": 5.1,
    "RainfallRolling7_mm": 5.5,
    "Month": 11,
    "DayOfYear": 315,
    "MonthSin": 0.866,
    "MonthCos": 0.5,
    "DaySin": 0.12,
    "DayCos": 0.99,
    "StationCount": 8,
    "RecordCount": 8,
    "IsNE_Monsoon": 1
  }'
```

## Model and Data

The project uses historical Chennai rainfall records and transforms them into a supervised learning dataset with engineered variables such as:

- rainfall lag values
- rolling averages
- monthly seasonality
- day-of-year cycles
- monsoon indicators

This feature design helps the classifier capture both temporal and seasonal rainfall trends.

## Project Status

Completed and ready to use locally for prediction, experimentation, and portfolio demonstration.

## License

This project is currently shared for educational and portfolio purposes. Add a license if you plan to publish or distribute it publicly in a production-ready environment.
