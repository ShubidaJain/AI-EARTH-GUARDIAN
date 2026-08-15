import requests
import pandas as pd
from pathlib import Path


INPUT_FILE = Path("ml/fire/data/raw/firms_fire_data.csv")
OUTPUT_FILE = Path("ml/fire/data/raw/fire_weather_data.csv")


# Load FIRMS data
df = pd.read_csv(INPUT_FILE)

# Remove duplicate location/date combinations
locations = df[
    ["latitude", "longitude", "acq_date"]
].drop_duplicates()


weather_records = []


for _, row in locations.iterrows():

    latitude = row["latitude"]
    longitude = row["longitude"]
    date = pd.to_datetime(row["acq_date"]).strftime("%Y%m%d")

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "parameters": "T2M,RH2M,WS2M,PRECTOTCORR",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": date,
        "end": date,
        "format": "JSON"
    }

    print(
        f"Requesting weather for "
        f"{latitude}, {longitude} on {date}"
    )

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    properties = data["properties"]
    parameter_data = properties["parameter"]

    weather_records.append({
        "latitude": latitude,
        "longitude": longitude,
        "date": row["acq_date"],
        "temperature": parameter_data["T2M"][date],
        "humidity": parameter_data["RH2M"][date],
        "wind_speed": parameter_data["WS2M"][date],
        "rainfall": parameter_data["PRECTOTCORR"][date]
    })


weather_df = pd.DataFrame(weather_records)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

weather_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("Weather data downloaded successfully!")
print(weather_df)