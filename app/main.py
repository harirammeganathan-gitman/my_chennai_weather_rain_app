from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    WeatherPredictionRequest,
    WeatherPredictionResponse,
    HealthResponse,
)
from app.predict import predict_weather
from app.model_loader import load_model_bundle

app = FastAPI(
    title="Chennai Rain Prediction API",
    description="API to predict next-day rain/no-rain for Chennai using a trained Random Forest model.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Chennai Rain Prediction API is running",
        "docs_url": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    try:
        load_model_bundle()
        return HealthResponse(status="ok", model_loaded=True)
    except Exception:
        return HealthResponse(status="error", model_loaded=False)


@app.post("/predict", response_model=WeatherPredictionResponse)
def predict(payload: WeatherPredictionRequest):
    return predict_weather(payload)