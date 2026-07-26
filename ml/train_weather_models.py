import pandas as pd
from pathlib import Path

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "data" / "processed" / "chennai_city_rain_model_ready.csv"
METRICS_PATH = BASE_DIR / "weather_model_metrics.csv"

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


def train_models(csv_path=CSV_PATH, metrics_path=METRICS_PATH):
    csv_path = Path(csv_path)
    metrics_path = Path(metrics_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Processed dataset not found: {csv_path}")

    df = pd.read_csv(csv_path, parse_dates=["Date"]).sort_values("Date")

    X = df[FEATURE_COLS]
    y = df["RainTomorrow"].astype(int)

    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    preprocess_scaled = ColumnTransformer([
        (
            "num",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]),
            FEATURE_COLS,
        )
    ])

    preprocess_tree = ColumnTransformer([
        (
            "num",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
            ]),
            FEATURE_COLS,
        )
    ])

    models = {
        "LogisticRegression": Pipeline([
            ("prep", preprocess_scaled),
            ("model", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ]),
        "DecisionTree": Pipeline([
            ("prep", preprocess_tree),
            ("model", DecisionTreeClassifier(
                max_depth=6,
                min_samples_leaf=10,
                random_state=42,
                class_weight="balanced"
            )),
        ]),
        "RandomForest": Pipeline([
            ("prep", preprocess_tree),
            ("model", RandomForestClassifier(
                n_estimators=300,
                max_depth=10,
                min_samples_leaf=5,
                random_state=42,
                class_weight="balanced_subsample",
                n_jobs=-1
            )),
        ]),
    }

    metrics_rows = []
    best_model = None
    best_model_name = None
    best_f1 = -1

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        auc = roc_auc_score(y_test, probs)

        metrics_rows.append({
            "model": name,
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "roc_auc": auc,
        })

        print(f"\n{name}")
        print(classification_report(y_test, preds, zero_division=0))

        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_model_name = name

    metrics_df = pd.DataFrame(metrics_rows).sort_values("f1", ascending=False)
    metrics_df.to_csv(metrics_path, index=False)

    print("\nBest model:", best_model_name)
    print("\nSaved metrics to:", metrics_path)
    print(metrics_df)

    return best_model, best_model_name, metrics_df


if __name__ == "__main__":
    train_models()