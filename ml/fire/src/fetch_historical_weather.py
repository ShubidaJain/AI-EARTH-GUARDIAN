import pandas as pd
import requests
import time

from pathlib import Path


INPUT_FILE = Path(
    "ml/fire/data/processed/historical_fire_dataset.csv"
)

OUTPUT_FILE = Path(
    "ml/fire/data/raw/historical_weather.csv"
)


# --------------------------------------------------
# Load fire dataset
# --------------------------------------------------

fires = pd.read_csv(INPUT_FILE)

fires["acq_date"] = pd.to_datetime(
    fires["acq_date"]
)


# --------------------------------------------------
# Create unique location/date combinations
# --------------------------------------------------

locations = fires[
    ["latitude", "longitude", "acq_date"]
].drop_duplicates()


print(
    f"Unique weather requests needed: {len(locations)}"
)


weather_records = []


# --------------------------------------------------
# NASA POWER
# --------------------------------------------------

URL = (
    "https://power.larc.nasa.gov/"
    "api/temporal/daily/point"
)


for index, row in locations.iterrows():

    latitude = row["latitude"]
    longitude = row["longitude"]

    date = row["acq_date"]

    date_string = date.strftime(
        "%Y%m%d"
    )

    params = {

        "parameters":
            "T2M,RH2M,WS2M,PRECTOTCORR",

        "community":
            "AG",

        "longitude":
            longitude,

        "latitude":
            latitude,

        "start":
            date_string,

        "end":
            date_string,

        "format":
            "JSON"
    }


    try:

        response = requests.get(
            URL,
            params=params,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        parameters = (
            data["properties"]["parameter"]
        )


        weather_records.append({

            "latitude":
                latitude,

            "longitude":
                longitude,

            "date":
                date.strftime("%Y-%m-%d"),

            "temperature":
                parameters["T2M"][date_string],

            "humidity":
                parameters["RH2M"][date_string],

            "wind_speed":
                parameters["WS2M"][date_string],

            "rainfall":
                parameters["PRECTOTCORR"][date_string]

        })


        print(
            f"[{index + 1}/{len(locations)}] "
            f"{date_string} "
            f"{latitude:.3f}, "
            f"{longitude:.3f}"
        )


    except Exception as error:

        print(
            f"[ERROR] "
            f"{date_string}: {error}"
        )


    time.sleep(0.5)


# --------------------------------------------------
# Save
# --------------------------------------------------

weather_df = pd.DataFrame(
    weather_records
)


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


weather_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("Weather collection complete.")
print(
    f"Records: {len(weather_df)}"
)

print(
    f"Saved: {OUTPUT_FILE}"
)