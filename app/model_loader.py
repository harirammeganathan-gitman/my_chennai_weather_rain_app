from functools import lru_cache
from pathlib import Path

import joblib

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "weather_random_forest_model.joblib"


@lru_cache(maxsize=1)
def load_model_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

    bundle = joblib.load(MODEL_PATH)

    if "model" not in bundle or "features" not in bundle:
        raise ValueError("Invalid model bundle format. Expected keys: 'model' and 'features'.")

    return bundle


def get_model():
    return load_model_bundle()["model"]


def get_feature_names():
    return load_model_bundle()["features"]