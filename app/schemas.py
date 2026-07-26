from pydantic import BaseModel, Field, ConfigDict


class WeatherPredictionRequest(BaseModel):
    RainfallCity_mm: float = Field(..., description="Current day's average city rainfall in mm")
    RainToday: int = Field(..., ge=0, le=1, description="1 if it rained today, else 0")
    RainfallLag1_mm: float = Field(..., description="Rainfall 1 day ago in mm")
    RainfallLag2_mm: float = Field(..., description="Rainfall 2 days ago in mm")
    RainfallLag3_mm: float = Field(..., description="Rainfall 3 days ago in mm")
    RainfallLag7_mm: float = Field(..., description="Rainfall 7 days ago in mm")
    RainfallRolling3_mm: float = Field(..., description="3-day rolling average rainfall")
    RainfallRolling7_mm: float = Field(..., description="7-day rolling average rainfall")
    Month: int = Field(..., ge=1, le=12, description="Month number")
    DayOfYear: int = Field(..., ge=1, le=366, description="Day number in year")
    MonthSin: float = Field(..., description="Cyclical month sine encoding")
    MonthCos: float = Field(..., description="Cyclical month cosine encoding")
    DaySin: float = Field(..., description="Cyclical day-of-year sine encoding")
    DayCos: float = Field(..., description="Cyclical day-of-year cosine encoding")
    StationCount: int = Field(..., ge=0, description="Number of stations reporting")
    RecordCount: int = Field(..., ge=0, description="Number of rainfall records for the day")
    IsNE_Monsoon: int = Field(..., ge=0, le=1, description="1 if Northeast monsoon month, else 0")

    model_config = ConfigDict(extra="forbid")


class WeatherPredictionResponse(BaseModel):
    predicted_rain_tomorrow: int = Field(..., description="1 means rain expected tomorrow, 0 means no rain")
    predicted_probability: float = Field(..., ge=0.0, le=1.0, description="Probability of rain tomorrow")
    model_name: str = Field(..., description="Model used for prediction")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool