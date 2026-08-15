import requests
import pandas as pd


BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(
    latitude: float,
    longitude: float
):
    """
    Get current weather plus the previous 7 days
    of hourly weather data.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "precipitation"
        ),

        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "precipitation"
        ),

        "past_days": 7,

        "forecast_days": 1,

        "timezone": "auto",

        "temperature_unit": "celsius",

        "wind_speed_unit": "ms",

        "precipitation_unit": "mm"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def extract_weather_features(
    weather_data
):
    """
    Convert live weather data into the same
    feature structure used by the ML model.
    """

    current = weather_data["current"]

    # --------------------------------------------------------
    # Current weather
    # --------------------------------------------------------

    temperature = float(
        current["temperature_2m"]
    )

    humidity = float(
        current["relative_humidity_2m"]
    )

    wind_speed = float(
        current["wind_speed_10m"]
    )

    rainfall = float(
        current["precipitation"]
    )


    # --------------------------------------------------------
    # Hourly historical data
    # --------------------------------------------------------

    hourly = weather_data["hourly"]

    history = pd.DataFrame({

        "time": pd.to_datetime(
            hourly["time"]
        ),

        "temperature":
            hourly["temperature_2m"],

        "humidity":
            hourly["relative_humidity_2m"],

        "wind_speed":
            hourly["wind_speed_10m"],

        "rainfall":
            hourly["precipitation"]
    })


    # --------------------------------------------------------
    # Convert hourly data into daily values
    # --------------------------------------------------------

    history["date"] = (
        history["time"]
        .dt.date
    )


    daily = (
        history
        .groupby("date")
        .agg(
            temperature=(
                "temperature",
                "mean"
            ),

            humidity=(
                "humidity",
                "mean"
            ),

            wind_speed=(
                "wind_speed",
                "mean"
            ),

            rainfall=(
                "rainfall",
                "sum"
            )
        )
        .reset_index()
    )


    # --------------------------------------------------------
    # Remove today's incomplete day
    # --------------------------------------------------------

    today = (
        pd.Timestamp
        .now(
            tz=weather_data["timezone"]
        )
        .date()
    )

    daily = daily[
        daily["date"] < today
    ]


    daily = (
        daily
        .sort_values("date")
        .tail(7)
    )


    if len(daily) < 7:

        raise ValueError(
            "Not enough historical weather "
            "data to calculate 7-day features."
        )


    # --------------------------------------------------------
    # Historical features
    # --------------------------------------------------------

    temperature_3d_mean = (
        daily["temperature"]
        .tail(3)
        .mean()
    )

    temperature_7d_mean = (
        daily["temperature"]
        .mean()
    )


    humidity_3d_mean = (
        daily["humidity"]
        .tail(3)
        .mean()
    )

    humidity_7d_mean = (
        daily["humidity"]
        .mean()
    )


    wind_3d_mean = (
        daily["wind_speed"]
        .tail(3)
        .mean()
    )

    wind_7d_mean = (
        daily["wind_speed"]
        .mean()
    )


    rainfall_3d_sum = (
        daily["rainfall"]
        .tail(3)
        .sum()
    )

    rainfall_7d_sum = (
        daily["rainfall"]
        .sum()
    )


    # --------------------------------------------------------
    # Calendar
    # --------------------------------------------------------

    now = pd.Timestamp.now(
        tz=weather_data["timezone"]
    )

    month = now.month

    day_of_year = now.dayofyear


    return {

        "temperature":
            temperature,

        "humidity":
            humidity,

        "wind_speed":
            wind_speed,

        "rainfall":
            rainfall,

        "temperature_3d_mean":
            float(
                temperature_3d_mean
            ),

        "temperature_7d_mean":
            float(
                temperature_7d_mean
            ),

        "humidity_3d_mean":
            float(
                humidity_3d_mean
            ),

        "humidity_7d_mean":
            float(
                humidity_7d_mean
            ),

        "wind_3d_mean":
            float(
                wind_3d_mean
            ),

        "wind_7d_mean":
            float(
                wind_7d_mean
            ),

        "rainfall_3d_sum":
            float(
                rainfall_3d_sum
            ),

        "rainfall_7d_sum":
            float(
                rainfall_7d_sum
            ),

        "month":
            month,

        "day_of_year":
            day_of_year
    }