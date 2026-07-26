# Chennai Rain Prediction

This project predicts **next-day rain/no-rain for Chennai** using historical station rainfall data, daily aggregation, time-series feature engineering, and classification models. The current pipeline prepares a city-level dataset from raw station observations and compares Logistic Regression, Decision Tree, and Random Forest models. The present baseline metrics show Random Forest leading on F1 score at about 0.751, with accuracy about 0.794 and ROC-AUC about 0.888.[1]

## Project Structure

```text
.
├── chennai_city_rain_predictor_dataset.csv
├── chennai_city_rain_model_ready.csv
├── preprocess_weather_data.py
├── train_weather_models.py
├── predict_weather.py
├── weather_model_metrics.csv
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── python-ci.yml
```

## Files

- `chennai_city_rain_predictor_dataset.csv`: Raw station-level rainfall dataset for Chennai with columns such as `District`, `Station`, `Rainfall`, and `Date`.[2]
- `chennai_city_rain_model_ready.csv`: Processed city-level daily dataset with engineered lag, rolling, seasonal, and target columns such as `RainfallCity_mm`, `RainToday`, `RainfallLag1_mm`, `RainfallRolling7_mm`, `IsNE_Monsoon`, and `RainTomorrow`.[3]
- `preprocess_weather_data.py`: Builds the model-ready dataset from the raw CSV.[4]
- `train_weather_models.py`: Trains baseline classifiers and prints evaluation reports.[5]
- `predict_weather.py`: Trains and saves a Random Forest pipeline and supports batch prediction from prepared feature rows.[6]
- `weather_model_metrics.csv`: Stores the current model comparison metrics.[1]

## Current Model Verdict

The project is a **strong baseline prototype**, not yet a production-ready public web application. The data engineering direction is sound because it removes exact duplicates, aggregates station data by date using daily mean rainfall, fills the calendar, and creates lag and rolling features for prediction.[4][3]

However, the attached Python scripts still need cleanup before cloud deployment. The current codebase has overlapping training responsibilities, and some attached scripts show formatting or indentation issues in their uploaded content, which should be corrected before pushing to GitHub.[6][5][4][7]

## Local Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the ML Pipeline

### Step 1: Build the processed dataset

```bash
python preprocess_weather_data.py
```

This script reads the raw station-level rainfall CSV, removes exact duplicates, aggregates rainfall by date using the **daily mean across stations**, fills missing dates, and creates model features plus the `RainTomorrow` target.[4]

### Step 2: Train and evaluate models

```bash
python train_weather_models.py
```

This script trains Logistic Regression, Decision Tree, and Random Forest using a time-ordered train/test split and prints classification reports.[5]

### Step 3: Train and save the serving model

```bash
python predict_weather.py
```

This script currently trains a Random Forest model on the processed dataset and saves a serialized model artifact using `joblib`.[6]

## Expected Features for Prediction

The current serving logic expects already prepared feature columns rather than raw rainfall input. Those columns include:

- `RainfallCity_mm`
- `RainToday`
- `RainfallLag1_mm`
- `RainfallLag2_mm`
- `RainfallLag3_mm`
- `RainfallLag7_mm`
- `RainfallRolling3_mm`
- `RainfallRolling7_mm`
- `Month`
- `DayOfYear`
- `MonthSin`
- `MonthCos`
- `DaySin`
- `DayCos`
- `StationCount`
- `RecordCount`
- `IsNE_Monsoon`[6][3]

## Recommended Deployment Architecture

A practical public deployment path is:

1. Keep the ML training and preprocessing code in the repository.
2. Add a **FastAPI** backend that loads a saved `.joblib` model and exposes prediction endpoints.[8]
3. Add a **Streamlit** frontend for a simple browser UI where users can enter values and see predictions.[9][10]
4. Host the API on Render and connect the UI to it over HTTP.[8]
5. Optionally host the Streamlit UI on Streamlit Community Cloud directly from the same GitHub repository.[11][10]

## Suggested Next Repository Layout

```text
weather-rain-api/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── model_loader.py
│   └── predict.py
├── ui/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   └── weather_random_forest_model.joblib
├── tests/
├── preprocess_weather_data.py
├── train_weather_models.py
├── predict_weather.py
├── requirements.txt
├── README.md
└── .github/workflows/python-ci.yml
```

## Cloud Hosting Plan

### Backend API

Render provides a documented path to deploy FastAPI applications, including Git-based deployment and HTTPS-enabled hosted services.[8]

Typical start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend UI

Streamlit Community Cloud supports deployment directly from a GitHub repository by selecting the repo, branch, and app entry file.[10][11]

## CI/CD

The included GitHub Actions workflow installs dependencies and runs a basic Python validation pipeline on pushes and pull requests. GitHub maintains starter workflow patterns for Python CI that can be adapted for linting and tests.[12]

## Recommended Next Improvements

Before exposing the model publicly, the following updates are recommended:

- Fix and format the Python source files consistently.[6][4][7]
- Save the trained model in a dedicated `models/` folder instead of retraining during inference.[6]
- Add a FastAPI app with request validation and a `/predict` endpoint.[8]
- Add a Streamlit or HTML UI for public usage.[9][10]
- Add tests for preprocessing, model loading, and API input validation.[12]
- Expand features with humidity, pressure, wind, and temperature for better predictive power, since the current baseline relies mainly on rainfall-history and calendar-derived features.[3][1]

## License and Usage

Choose a repository license before publishing, such as MIT for broad reuse or Apache-2.0 if explicit patent language is preferred. If the dataset source has restrictions, verify redistribution permissions before making the raw data public.