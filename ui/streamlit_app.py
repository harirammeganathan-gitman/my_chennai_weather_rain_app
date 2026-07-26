# import math
# import requests
# import streamlit as st
# from datetime import date
#
# API_URL = "https://my-chennai-weather-rain-app.onrender.com/predict"
#
# st.set_page_config(
#     page_title="Chennai Rain Predictor",
#     page_icon="🌧️",
#     layout="wide"
# )
#
# st.markdown(
#     """
#     <style>
#     .app-header {
#         padding: 18px 24px;
#         border-radius: 14px;
#         background: linear-gradient(135deg, #0f4c75, #3282b8);
#         color: white;
#         margin-bottom: 20px;
#     }
#     .app-header h1 {
#         margin: 0;
#         font-size: 28px;
#     }
#     .app-header p {
#         margin: 4px 0 0 0;
#         opacity: 0.9;
#         font-size: 14px;
#     }
#     .forecast-card {
#         border-radius: 14px;
#         padding: 20px;
#         text-align: center;
#         color: white;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.15);
#     }
#     .card-rain {
#         background: linear-gradient(135deg, #2b5876, #4e4376);
#     }
#     .card-dry {
#         background: linear-gradient(135deg, #56ab2f, #a8e063);
#     }
#     .card-title {
#         font-size: 16px;
#         opacity: 0.85;
#         margin-bottom: 6px;
#     }
#     .card-value {
#         font-size: 32px;
#         font-weight: 700;
#     }
#     .card-sub {
#         font-size: 13px;
#         opacity: 0.85;
#         margin-top: 6px;
#     }
#     .disclaimer-box {
#         background-color: #fff3cd;
#         border: 1px solid #ffe69c;
#         border-radius: 10px;
#         padding: 12px 16px;
#         color: #664d03;
#         font-size: 13px;
#         margin-top: 16px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#
# st.markdown(
#     """
#     <div class="app-header">
#         <h1>🌧️ Chennai Rain Prediction Dashboard</h1>
#         <p>Historical ML-based rain prediction using a trained Random Forest classifier</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
#
#
# def apply_preset(preset_name):
#     presets = {
#         "Dry Day": {
#             "rainfall_city": 0.0, "rain_today": 0,
#             "rain_1": 0.0, "rain_2": 0.0, "rain_3": 0.0,
#             "rain_4": 0.0, "rain_5": 0.0, "rain_6": 0.0, "rain_7": 0.0,
#             "station_count": 8, "record_count": 8,
#         },
#         "Moderate Rain": {
#             "rainfall_city": 6.0, "rain_today": 1,
#             "rain_1": 5.0, "rain_2": 7.0, "rain_3": 4.0,
#             "rain_4": 3.0, "rain_5": 2.0, "rain_6": 5.0, "rain_7": 6.0,
#             "station_count": 8, "record_count": 8,
#         },
#         "Monsoon Day": {
#             "rainfall_city": 18.0, "rain_today": 1,
#             "rain_1": 20.0, "rain_2": 15.0, "rain_3": 12.0,
#             "rain_4": 10.0, "rain_5": 8.0, "rain_6": 14.0, "rain_7": 16.0,
#             "station_count": 8, "record_count": 8,
#         }
#     }
#     preset = presets[preset_name]
#     for key, value in preset.items():
#         st.session_state[key] = value
#
#
# def get_confidence_label(probability):
#     if probability < 0.50:
#         return "Low rain likelihood"
#     elif probability < 0.60:
#         return "Weak rain signal"
#     elif probability < 0.75:
#         return "Moderate rain signal"
#     else:
#         return "Strong rain signal"
#
#
# def build_payload(target_date, rainfall_city, rain_today, rain_1, rain_2, rain_3,
#                    rain_4, rain_5, rain_6, rain_7, station_count, record_count):
#     month = target_date.month
#     day_of_year = target_date.timetuple().tm_yday
#
#     month_sin = math.sin(2 * math.pi * month / 12)
#     month_cos = math.cos(2 * math.pi * month / 12)
#     day_sin = math.sin(2 * math.pi * day_of_year / 366)
#     day_cos = math.cos(2 * math.pi * day_of_year / 366)
#
#     rolling3 = (rain_1 + rain_2 + rain_3) / 3
#     rolling7 = (rain_1 + rain_2 + rain_3 + rain_4 + rain_5 + rain_6 + rain_7) / 7
#     is_ne_monsoon = 1 if month in [10, 11, 12] else 0
#
#     return {
#         "RainfallCity_mm": float(rainfall_city),
#         "RainToday": int(rain_today),
#         "RainfallLag1_mm": float(rain_1),
#         "RainfallLag2_mm": float(rain_2),
#         "RainfallLag3_mm": float(rain_3),
#         "RainfallLag7_mm": float(rain_7),
#         "RainfallRolling3_mm": float(rolling3),
#         "RainfallRolling7_mm": float(rolling7),
#         "Month": int(month),
#         "DayOfYear": int(day_of_year),
#         "MonthSin": float(month_sin),
#         "MonthCos": float(month_cos),
#         "DaySin": float(day_sin),
#         "DayCos": float(day_cos),
#         "StationCount": int(station_count),
#         "RecordCount": int(record_count),
#         "IsNE_Monsoon": int(is_ne_monsoon),
#     }
#
#
# left_col, right_col = st.columns([1, 1.3])
#
# with left_col:
#     st.subheader("Quick presets")
#     p1, p2, p3 = st.columns(3)
#     with p1:
#         if st.button("☀️ Dry Day"):
#             apply_preset("Dry Day")
#     with p2:
#         if st.button("🌦️ Moderate"):
#             apply_preset("Moderate Rain")
#     with p3:
#         if st.button("🌧️ Monsoon"):
#             apply_preset("Monsoon Day")
#
#     with st.form("rain_prediction_form"):
#         target_date = st.date_input("Target Date", value=date.today())
#
#         rainfall_city = st.number_input("Today's City Rainfall (mm)", min_value=0.0,
#                                          value=st.session_state.get("rainfall_city", 0.0), step=0.1, key="rainfall_city")
#         rain_today = st.selectbox("Did it rain today?", options=[0, 1],
#                                    format_func=lambda x: "Yes" if x == 1 else "No",
#                                    index=st.session_state.get("rain_today", 0), key="rain_today")
#
#         station_count = st.number_input("Station Count", min_value=0,
#                                          value=st.session_state.get("station_count", 8), step=1, key="station_count")
#         record_count = st.number_input("Record Count", min_value=0,
#                                         value=st.session_state.get("record_count", 8), step=1, key="record_count")
#
#         st.markdown("**Recent rainfall history (last 7 days)**")
#         rc = st.columns(4)
#         with rc[0]:
#             rain_1 = st.number_input("1 day ago", min_value=0.0, value=st.session_state.get("rain_1", 0.0), step=0.1, key="rain_1")
#             rain_5 = st.number_input("5 days ago", min_value=0.0, value=st.session_state.get("rain_5", 0.0), step=0.1, key="rain_5")
#         with rc[1]:
#             rain_2 = st.number_input("2 days ago", min_value=0.0, value=st.session_state.get("rain_2", 0.0), step=0.1, key="rain_2")
#             rain_6 = st.number_input("6 days ago", min_value=0.0, value=st.session_state.get("rain_6", 0.0), step=0.1, key="rain_6")
#         with rc[2]:
#             rain_3 = st.number_input("3 days ago", min_value=0.0, value=st.session_state.get("rain_3", 0.0), step=0.1, key="rain_3")
#             rain_7 = st.number_input("7 days ago", min_value=0.0, value=st.session_state.get("rain_7", 0.0), step=0.1, key="rain_7")
#         with rc[3]:
#             rain_4 = st.number_input("4 days ago", min_value=0.0, value=st.session_state.get("rain_4", 0.0), step=0.1, key="rain_4")
#
#         submitted = st.form_submit_button("Predict")
#
# with right_col:
#     st.subheader("Forecast result")
#
#     if submitted:
#         payload = build_payload(target_date, rainfall_city, rain_today, rain_1, rain_2,
#                                   rain_3, rain_4, rain_5, rain_6, rain_7, station_count, record_count)
#
#         try:
#             response = requests.post(API_URL, json=payload, timeout=10)
#             response.raise_for_status()
#             result = response.json()
#
#             probability = result["predicted_probability"]
#             rain_flag = result["predicted_rain_tomorrow"]
#             model_name = result["model_name"]
#             confidence_label = get_confidence_label(probability)
#
#             card_class = "card-rain" if rain_flag == 1 else "card-dry"
#             icon = "🌧️" if rain_flag == 1 else "☀️"
#             label = "Rain predicted tomorrow" if rain_flag == 1 else "No rain predicted tomorrow"
#
#             st.markdown(
#                 f"""
#                 <div class="forecast-card {card_class}">
#                     <div class="card-title">{icon} {label}</div>
#                     <div class="card-value">{probability:.1%}</div>
#                     <div class="card-sub">Rain probability · {confidence_label} · Model: {model_name}</div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#
#             m1, m2, m3 = st.columns(3)
#             with m1:
#                 st.metric("Rolling 3-day avg", f"{payload['RainfallRolling3_mm']:.2f} mm")
#             with m2:
#                 st.metric("Rolling 7-day avg", f"{payload['RainfallRolling7_mm']:.2f} mm")
#             with m3:
#                 st.metric("NE Monsoon", "Yes" if payload["IsNE_Monsoon"] == 1 else "No")
#
#             with st.expander("View derived payload sent to API"):
#                 st.json(payload)
#
#             with st.expander("View raw API response"):
#                 st.json(result)
#
#             st.markdown(
#                 """
#                 <div class="disclaimer-box">
#                 ⚠️ This is a historical machine-learning prediction based on engineered rainfall features.
#                 It is not a substitute for operational forecasts from services such as BBC or IMD.
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#
#         except requests.exceptions.RequestException as e:
#             st.error(f"API request failed: {e}")
#     else:
#         st.info("Fill in the form on the left and click **Predict** to see the forecast card here.")

import math
import requests
import streamlit as st
from datetime import date

API_URL = "https://my-chennai-weather-rain-app.onrender.com/predict"

st.set_page_config(
    page_title="Chennai Rain Predictor",
    page_icon="🌧️",
    layout="wide"
)

st.markdown(
    """
    <style>
    .app-header {
        padding: 18px 24px;
        border-radius: 14px;
        background: linear-gradient(135deg, #0f4c75, #3282b8);
        color: white;
        margin-bottom: 20px;
    }
    .app-header h1 {
        margin: 0;
        font-size: 28px;
    }
    .app-header p {
        margin: 4px 0 0 0;
        opacity: 0.9;
        font-size: 14px;
    }
    .forecast-card {
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .card-rain {
        background: linear-gradient(135deg, #2b5876, #4e4376);
    }
    .card-dry {
        background: linear-gradient(135deg, #56ab2f, #a8e063);
    }
    .card-title {
        font-size: 16px;
        opacity: 0.85;
        margin-bottom: 6px;
    }
    .card-value {
        font-size: 32px;
        font-weight: 700;
    }
    .card-sub {
        font-size: 13px;
        opacity: 0.85;
        margin-top: 6px;
    }
    .disclaimer-box {
        background-color: #fff3cd;
        border: 1px solid #ffe69c;
        border-radius: 10px;
        padding: 12px 16px;
        color: #664d03;
        font-size: 13px;
        margin-top: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="app-header">
        <h1>🌧️ Chennai Rain Prediction Dashboard</h1>
        <p>Historical ML-based rain prediction using a trained Random Forest classifier</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# Feature name contract — MUST match the FastAPI backend's Pydantic schema
# and the exact column names/order used when the model was trained.
# Change this dict in ONE place if the backend contract changes.
# ---------------------------------------------------------------------------
FEATURE_KEYS = {
    "rainfall_city": "RainfallCity_mm",
    "rain_today": "RainToday",
    "lag1": "RainfallLag1_mm",
    "lag2": "RainfallLag2_mm",
    "lag3": "RainfallLag3_mm",
    "lag7": "RainfallLag7_mm",
    "rolling3": "RainfallRolling3_mm",
    "rolling7": "RainfallRolling7_mm",
    "month": "Month",
    "day_of_year": "DayOfYear",
    "month_sin": "MonthSin",
    "month_cos": "MonthCos",
    "day_sin": "DaySin",
    "day_cos": "DayCos",
    "station_count": "StationCount",
    "record_count": "RecordCount",
    "is_ne_monsoon": "IsNE_Monsoon",
}


def apply_preset(preset_name):
    presets = {
        "Dry Day": {
            "rainfall_city": 0.0, "rain_today": 0,
            "rain_1": 0.0, "rain_2": 0.0, "rain_3": 0.0,
            "rain_4": 0.0, "rain_5": 0.0, "rain_6": 0.0, "rain_7": 0.0,
            "station_count": 8, "record_count": 8,
        },
        "Moderate Rain": {
            "rainfall_city": 6.0, "rain_today": 1,
            "rain_1": 5.0, "rain_2": 7.0, "rain_3": 4.0,
            "rain_4": 3.0, "rain_5": 2.0, "rain_6": 5.0, "rain_7": 6.0,
            "station_count": 8, "record_count": 8,
        },
        "Monsoon Day": {
            "rainfall_city": 18.0, "rain_today": 1,
            "rain_1": 20.0, "rain_2": 15.0, "rain_3": 12.0,
            "rain_4": 10.0, "rain_5": 8.0, "rain_6": 14.0, "rain_7": 16.0,
            "station_count": 8, "record_count": 8,
        }
    }
    preset = presets[preset_name]
    for key, value in preset.items():
        st.session_state[key] = value


def get_confidence_label(probability):
    if probability < 0.50:
        return "Low rain likelihood"
    elif probability < 0.60:
        return "Weak rain signal"
    elif probability < 0.75:
        return "Moderate rain signal"
    else:
        return "Strong rain signal"


def build_payload(target_date, rainfall_city, rain_today, rain_1, rain_2, rain_3,
                   rain_4, rain_5, rain_6, rain_7, station_count, record_count):
    month = target_date.month
    day_of_year = target_date.timetuple().tm_yday

    month_sin = math.sin(2 * math.pi * month / 12)
    month_cos = math.cos(2 * math.pi * month / 12)
    day_sin = math.sin(2 * math.pi * day_of_year / 365.25)
    day_cos = math.cos(2 * math.pi * day_of_year / 365.25)

    rolling3 = (rain_1 + rain_2 + rain_3) / 3
    rolling7 = (rain_1 + rain_2 + rain_3 + rain_4 + rain_5 + rain_6 + rain_7) / 7
    is_ne_monsoon = 1 if month in (10, 11, 12) else 0

    values = {
        "rainfall_city": float(rainfall_city),
        "rain_today": int(rain_today),
        "lag1": float(rain_1),
        "lag2": float(rain_2),
        "lag3": float(rain_3),
        "lag7": float(rain_7),
        "rolling3": float(rolling3),
        "rolling7": float(rolling7),
        "month": int(month),
        "day_of_year": int(day_of_year),
        "month_sin": float(month_sin),
        "month_cos": float(month_cos),
        "day_sin": float(day_sin),
        "day_cos": float(day_cos),
        "station_count": int(station_count),
        "record_count": int(record_count),
        "is_ne_monsoon": int(is_ne_monsoon),
    }

    # Map internal keys -> exact backend/model field names in one place.
    return {FEATURE_KEYS[k]: v for k, v in values.items()}


left_col, right_col = st.columns([1, 1.3])

with left_col:
    st.subheader("Quick presets")
    p1, p2, p3 = st.columns(3)
    with p1:
        if st.button("☀️ Dry Day"):
            apply_preset("Dry Day")
    with p2:
        if st.button("🌦️ Moderate"):
            apply_preset("Moderate Rain")
    with p3:
        if st.button("🌧️ Monsoon"):
            apply_preset("Monsoon Day")

    with st.form("rain_prediction_form"):
        target_date = st.date_input("Target Date", value=date.today())

        rainfall_city = st.number_input(
            "Today's City Rainfall (mm)", min_value=0.0,
            value=st.session_state.get("rainfall_city", 0.0), step=0.1, key="rainfall_city"
        )
        rain_today = st.selectbox(
            "Did it rain today?", options=[0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No",
            index=st.session_state.get("rain_today", 0), key="rain_today"
        )

        # Advanced/technical inputs collapsed by default so laypeople only
        # see date + rain-today + presets on first glance.
        with st.expander("Advanced: station coverage & 7-day rainfall history", expanded=False):
            station_count = st.number_input(
                "Station Count", min_value=0,
                value=st.session_state.get("station_count", 8), step=1, key="station_count"
            )
            record_count = st.number_input(
                "Record Count", min_value=0,
                value=st.session_state.get("record_count", 8), step=1, key="record_count"
            )

            st.markdown("**Recent rainfall history (last 7 days, mm)**")
            rc = st.columns(4)
            with rc[0]:
                rain_1 = st.number_input("1 day ago", min_value=0.0, value=st.session_state.get("rain_1", 0.0), step=0.1, key="rain_1")
                rain_5 = st.number_input("5 days ago", min_value=0.0, value=st.session_state.get("rain_5", 0.0), step=0.1, key="rain_5")
            with rc[1]:
                rain_2 = st.number_input("2 days ago", min_value=0.0, value=st.session_state.get("rain_2", 0.0), step=0.1, key="rain_2")
                rain_6 = st.number_input("6 days ago", min_value=0.0, value=st.session_state.get("rain_6", 0.0), step=0.1, key="rain_6")
            with rc[2]:
                rain_3 = st.number_input("3 days ago", min_value=0.0, value=st.session_state.get("rain_3", 0.0), step=0.1, key="rain_3")
                rain_7 = st.number_input("7 days ago", min_value=0.0, value=st.session_state.get("rain_7", 0.0), step=0.1, key="rain_7")
            with rc[3]:
                rain_4 = st.number_input("4 days ago", min_value=0.0, value=st.session_state.get("rain_4", 0.0), step=0.1, key="rain_4")

        submitted = st.form_submit_button("Predict", use_container_width=True)

with right_col:
    st.subheader("Forecast result")

    if submitted:
        payload = build_payload(
            target_date, rainfall_city, rain_today,
            rain_1, rain_2, rain_3, rain_4, rain_5, rain_6, rain_7,
            station_count, record_count
        )

        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            probability = result["predicted_probability"]
            rain_flag = result["predicted_rain_tomorrow"]
            model_name = result["model_name"]
            confidence_label = get_confidence_label(probability)

            card_class = "card-rain" if rain_flag == 1 else "card-dry"
            icon = "🌧️" if rain_flag == 1 else "☀️"
            label = "Rain predicted tomorrow" if rain_flag == 1 else "No rain predicted tomorrow"

            st.markdown(
                f"""
                <div class="forecast-card {card_class}">
                    <div class="card-title">{icon} {label}</div>
                    <div class="card-value">{probability:.1%}</div>
                    <div class="card-sub">Rain probability &middot; {confidence_label} &middot; Model: {model_name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Rolling 3-day avg", f"{payload[FEATURE_KEYS['rolling3']]:.2f} mm")
            with m2:
                st.metric("Rolling 7-day avg", f"{payload[FEATURE_KEYS['rolling7']]:.2f} mm")
            with m3:
                st.metric("NE Monsoon", "Yes" if payload[FEATURE_KEYS["is_ne_monsoon"]] == 1 else "No")

            with st.expander("View derived payload sent to API"):
                st.json(payload)

            with st.expander("View raw API response"):
                st.json(result)

            st.markdown(
                """
                <div class="disclaimer-box">
                ⚠️ This is a historical machine-learning prediction based on engineered rainfall features.
                It is not a substitute for operational forecasts from services such as BBC or IMD.
                </div>
                """,
                unsafe_allow_html=True
            )

        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
    else:
        st.info("Fill in the form on the left and click **Predict** to see the forecast card here.")