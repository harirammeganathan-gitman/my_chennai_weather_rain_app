import pandas as pd

from app.model_loader import get_model, get_feature_names
from app.schemas import WeatherPredictionRequest, WeatherPredictionResponse


def predict_weather(payload: WeatherPredictionRequest) -> WeatherPredictionResponse:
    model = get_model()
    feature_names = get_feature_names()

    input_data = payload.model_dump()
    df = pd.DataFrame([input_data])

    df = df[feature_names]

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return WeatherPredictionResponse(
        predicted_rain_tomorrow=int(prediction),
        predicted_probability=float(probability),
        model_name="RandomForest",
    )