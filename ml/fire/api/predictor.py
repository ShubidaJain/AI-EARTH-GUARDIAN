from pathlib import Path
import json

import pandas as pd
from xgboost import XGBClassifier

from .weather_service import (
    get_current_weather,
    extract_weather_features
)

# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_FILE = (
    BASE_DIR
    / "ml"
    / "fire"
    / "models"
    / "fire_risk_model.json"
)

FEATURE_FILE = (
    BASE_DIR
    / "ml"
    / "fire"
    / "models"
    / "model_features.json"
)

DATA_FILE = (
    BASE_DIR
    / "ml"
    / "fire"
    / "data"
    / "processed"
    / "earth_guardian_features.csv"
)


# ============================================================
# Load model configuration
# ============================================================

with open(
    FEATURE_FILE,
    "r",
    encoding="utf-8"
) as file:

    config = json.load(file)


FEATURES = config["features"]
THRESHOLD = config["threshold"]


# ============================================================
# Load model
# ============================================================

model = XGBClassifier()

model.load_model(
    MODEL_FILE
)


# ============================================================
# Load historical dataset
# ============================================================

print("Loading Earth Guardian dataset...")

dataset = pd.read_csv(
    DATA_FILE
)

dataset["date"] = pd.to_datetime(
    dataset["date"]
)


# ============================================================
# Find nearest grid cell
# ============================================================

def find_nearest_grid(
    latitude: float,
    longitude: float
):

    grids = dataset[
        [
            "grid_lat",
            "grid_lon"
        ]
    ].drop_duplicates()


    grids = grids.copy()


    grids["distance"] = (
        (grids["grid_lat"] - latitude) ** 2
        +
        (grids["grid_lon"] - longitude) ** 2
    )


    nearest = grids.loc[
        grids["distance"].idxmin()
    ]


    return (
        float(nearest["grid_lat"]),
        float(nearest["grid_lon"])
    )


# ============================================================
# Get latest available features
# ============================================================

def get_latest_features(
    latitude: float,
    longitude: float
):

    grid_lat, grid_lon = find_nearest_grid(
        latitude,
        longitude
    )


    grid_data = dataset[
        (dataset["grid_lat"] == grid_lat)
        &
        (dataset["grid_lon"] == grid_lon)
    ].copy()


    if grid_data.empty:

        raise ValueError(
            "No historical data available "
            "for this location."
        )


    # Latest row with complete historical features
    grid_data = grid_data.dropna(
        subset=[
            "temperature_7d_mean",
            "humidity_7d_mean",
            "wind_7d_mean",
            "rainfall_7d_sum"
        ]
    )


    if grid_data.empty:

        raise ValueError(
            "Insufficient historical "
            "weather data for this location."
        )


    latest = grid_data.sort_values(
        "date"
    ).iloc[-1]


    return latest, grid_lat, grid_lon


# ============================================================
# Prediction
# ============================================================

def predict_fire_risk(
    latitude: float,
    longitude: float
):

    row, grid_lat, grid_lon = (
        get_latest_features(
            latitude,
            longitude
        )
    )


    X = pd.DataFrame(
        [[
            row[feature]
            for feature in FEATURES
        ]],
        columns=FEATURES
    )


    probability = float(
        model.predict_proba(X)[0][1]
    )


    prediction = int(
        probability >= THRESHOLD
    )


    # --------------------------------------------------------
    # Risk level
    # --------------------------------------------------------

    if probability < 0.30:

        risk_level = "LOW"

    elif probability < 0.60:

        risk_level = "MODERATE"

    elif probability < 0.80:

        risk_level = "HIGH"

    else:

        risk_level = "EXTREME"


    return {

        "latitude": latitude,

        "longitude": longitude,

        "grid_lat": grid_lat,

        "grid_lon": grid_lon,

        "date": row["date"].strftime(
            "%Y-%m-%d"
        ),

        "fire_probability": round(
            probability,
            4
        ),

        "fire_prediction": prediction,

        "risk_level": risk_level,

        "threshold": THRESHOLD
    }
def predict_live_fire_risk(
    latitude: float,
    longitude: float
):

    # --------------------------------------------------------
    # Find nearest model grid
    # --------------------------------------------------------

    grid_lat, grid_lon = find_nearest_grid(
        latitude,
        longitude
    )


    # --------------------------------------------------------
    # Get live weather
    # --------------------------------------------------------

    weather_data = get_current_weather(
        latitude,
        longitude
    )


    features = extract_weather_features(
        weather_data
    )


    # --------------------------------------------------------
    # Add grid coordinates
    # --------------------------------------------------------

    features["grid_lat"] = grid_lat

    features["grid_lon"] = grid_lon


    # --------------------------------------------------------
    # Create model input
    # --------------------------------------------------------

    X = pd.DataFrame(
        [[
            features[feature]
            for feature in FEATURES
        ]],
        columns=FEATURES
    )


    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    probability = float(
        model.predict_proba(X)[0][1]
    )


    prediction = int(
        probability >= THRESHOLD
    )


    # --------------------------------------------------------
    # Risk level
    # --------------------------------------------------------

    if probability < 0.30:

        risk_level = "LOW"

    elif probability < 0.60:

        risk_level = "MODERATE"

    elif probability < 0.80:

        risk_level = "HIGH"

    else:

        risk_level = "EXTREME"


    return {

        "location": {

            "latitude":
                latitude,

            "longitude":
                longitude,

            "grid_lat":
                grid_lat,

            "grid_lon":
                grid_lon
        },

        "weather": {

            "temperature":
                round(
                    features["temperature"],
                    2
                ),

            "humidity":
                round(
                    features["humidity"],
                    2
                ),

            "wind_speed":
                round(
                    features["wind_speed"],
                    2
                ),

            "rainfall":
                round(
                    features["rainfall"],
                    2
                )
        },

        "historical_weather": {

            "temperature_3d_mean":
                round(
                    features[
                        "temperature_3d_mean"
                    ],
                    2
                ),

            "temperature_7d_mean":
                round(
                    features[
                        "temperature_7d_mean"
                    ],
                    2
                ),

            "humidity_3d_mean":
                round(
                    features[
                        "humidity_3d_mean"
                    ],
                    2
                ),

            "humidity_7d_mean":
                round(
                    features[
                        "humidity_7d_mean"
                    ],
                    2
                ),

            "wind_3d_mean":
                round(
                    features[
                        "wind_3d_mean"
                    ],
                    2
                ),

            "wind_7d_mean":
                round(
                    features[
                        "wind_7d_mean"
                    ],
                    2
                ),

            "rainfall_3d_sum":
                round(
                    features[
                        "rainfall_3d_sum"
                    ],
                    2
                ),

            "rainfall_7d_sum":
                round(
                    features[
                        "rainfall_7d_sum"
                    ],
                    2
                )
        },

        "prediction": {

            "fire_probability":
                round(
                    probability,
                    4
                ),

            "fire_prediction":
                prediction,

            "risk_level":
                risk_level,

            "threshold":
                THRESHOLD
        }
    }