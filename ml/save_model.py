import json
from pathlib import Path

import pandas as pd
import joblib
import sklearn

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "data" / "processed" / "chennai_city_rain_model_ready.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "weather_random_forest_model.joblib"
META_PATH = MODEL_DIR / "weather_random_forest_metadata.json"

FEATURE_COLS = [
    "RainfallCity_mm",
    "RainToday",
    "RainfallLag1_mm",
    "RainfallLag2_mm",
    "RainfallLag3_mm",
    "RainfallLag7_mm",
    "RainfallRolling3_mm",
    "RainfallRolling7_mm",
    "Month",
    "DayOfYear",
    "MonthSin",
    "MonthCos",
    "DaySin",
    "DayCos",
    "StationCount",
    "RecordCount",
    "IsNE_Monsoon",
]


def train_and_save_model(csv_path=CSV_PATH, model_path=MODEL_PATH, meta_path=META_PATH):
    csv_path = Path(csv_path)
    model_path = Path(model_path)
    meta_path = Path(meta_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Processed dataset not found: {csv_path}")

    model_dir = model_path.parent
    model_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path, parse_dates=["Date"]).sort_values("Date")

    X = df[FEATURE_COLS]
    y = df["RainTomorrow"].astype(int)

    preprocess = ColumnTransformer([
        (
            "num",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
            ]),
            FEATURE_COLS,
        )
    ])

    model = Pipeline([
        ("prep", preprocess),
        ("model", RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_leaf=5,
            random_state=42,
            class_weight="balanced_subsample",
            n_jobs=-1
        )),
    ])

    model.fit(X, y)

    bundle = {
        "model": model,
        "features": FEATURE_COLS,
        "sklearn_version": sklearn.__version__,
    }

    joblib.dump(bundle, model_path)

    meta = {
        "model_name": "RandomForestClassifier",
        "sklearn_version": sklearn.__version__,
        "feature_count": len(FEATURE_COLS),
        "features": FEATURE_COLS,
        "source_csv": str(csv_path),
    }

    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Saved model to: {model_path}")
    print(f"Saved metadata to: {meta_path}")


if __name__ == "__main__":
    train_and_save_model()