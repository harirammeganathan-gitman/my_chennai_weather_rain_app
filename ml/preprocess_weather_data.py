import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_CSV = BASE_DIR / "data" / "raw" / "chennai_city_rain_predictor_dataset.csv"
OUTPUT_CSV = BASE_DIR / "data" / "processed" / "chennai_city_rain_model_ready.csv"

REQUIRED_COLUMNS = {"District", "Station", "Rainfall", "Date"}


def build_dataset(raw_csv=RAW_CSV, output_csv=OUTPUT_CSV):
    raw_csv = Path(raw_csv)
    output_csv = Path(output_csv)

    if not raw_csv.exists():
        raise FileNotFoundError(f"Raw dataset not found: {raw_csv}")

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(raw_csv)
    raw.columns = [c.strip() for c in raw.columns]

    missing_cols = REQUIRED_COLUMNS - set(raw.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    for col in ["District", "Station", "Date"]:
        raw[col] = raw[col].astype(str).str.strip()

    raw["Rainfall"] = pd.to_numeric(raw["Rainfall"], errors="coerce")
    raw["Date"] = pd.to_datetime(raw["Date"], format="%d-%m-%Y", errors="coerce")

    raw = raw.dropna(subset=["Date", "Rainfall"])
    raw = raw.drop_duplicates(subset=["District", "Station", "Rainfall", "Date"])

    city = raw.groupby("Date", as_index=False).agg(
        RainfallCity_mm=("Rainfall", "mean"),
        StationCount=("Station", "nunique"),
        RecordCount=("Rainfall", "size")
    ).sort_values("Date")

    full_dates = pd.DataFrame({
        "Date": pd.date_range(city["Date"].min(), city["Date"].max(), freq="D")
    })
    city = full_dates.merge(city, on="Date", how="left")

    city["StationCount"] = city["StationCount"].fillna(0).astype(int)
    city["RecordCount"] = city["RecordCount"].fillna(0).astype(int)
    city["RainfallCity_mm"] = city["RainfallCity_mm"].fillna(0.0)

    city["RainToday"] = (city["RainfallCity_mm"] > 0).astype(int)

    for lag in [1, 2, 3, 7]:
        city[f"RainfallLag{lag}_mm"] = city["RainfallCity_mm"].shift(lag)

    for window in [3, 7]:
        city[f"RainfallRolling{window}_mm"] = (
            city["RainfallCity_mm"].shift(1).rolling(window, min_periods=1).mean()
        )

    city["Month"] = city["Date"].dt.month
    city["DayOfYear"] = city["Date"].dt.dayofyear
    city["Year"] = city["Date"].dt.year
    city["IsNE_Monsoon"] = city["Month"].isin([10, 11, 12]).astype(int)

    city["RainTomorrow"] = (city["RainfallCity_mm"].shift(-1).fillna(0) > 0).astype(int)

    city["MonthSin"] = np.sin(2 * np.pi * city["Month"] / 12)
    city["MonthCos"] = np.cos(2 * np.pi * city["Month"] / 12)
    city["DaySin"] = np.sin(2 * np.pi * city["DayOfYear"] / 365.25)
    city["DayCos"] = np.cos(2 * np.pi * city["DayOfYear"] / 365.25)

    columns = [
        "Date", "Year", "Month", "DayOfYear", "MonthSin", "MonthCos", "DaySin", "DayCos",
        "RainfallCity_mm", "RainToday", "RainfallLag1_mm", "RainfallLag2_mm",
        "RainfallLag3_mm", "RainfallLag7_mm", "RainfallRolling3_mm",
        "RainfallRolling7_mm", "StationCount", "RecordCount",
        "IsNE_Monsoon", "RainTomorrow"
    ]

    city = city[columns]
    city.to_csv(output_csv, index=False)

    print(f"Saved processed dataset to: {output_csv}")
    print(f"Shape: {city.shape}")
    print(city.head())


if __name__ == "__main__":
    build_dataset()