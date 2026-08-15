import requests
from pathlib import Path

import pandas as pd


# ============================================================
# Configuration
# ============================================================

START_DATE = "2023-01-01"
END_DATE = "2023-01-31"

LAT_MIN = 29
LAT_MAX = 33

LON_MIN = 73
LON_MAX = 77

OUTPUT_DIR = Path(
    "ml/fire/data/raw/weather"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Parameters
# ============================================================

PARAMETERS = [
    "T2M",
    "RH2M",
    "WS2M",
    "PRECTOTCORR"
]


# ============================================================
# NASA POWER endpoint
# ============================================================

BASE_URL = (
    "https://power.larc.nasa.gov/"
    "api/temporal/daily/regional"
)


# ============================================================
# Download
# ============================================================

for parameter in PARAMETERS:

    print()
    print("=" * 60)
    print(f"Downloading: {parameter}")
    print("=" * 60)

    output_file = (
        OUTPUT_DIR /
        f"{parameter}_{START_DATE}_{END_DATE}.csv"
    )

    if output_file.exists():

        print(
            f"Already exists: {output_file}"
        )

        continue


    params = {

        "latitude-min":
            LAT_MIN,

        "latitude-max":
            LAT_MAX,

        "longitude-min":
            LON_MIN,

        "longitude-max":
            LON_MAX,

        "parameters":
            parameter,

        "community":
            "AG",

        "start":
            START_DATE.replace("-", ""),

        "end":
            END_DATE.replace("-", ""),

        "format":
            "CSV"
    }


    response = requests.get(
        BASE_URL,
        params=params,
        timeout=(30, 300)
    )


    response.raise_for_status()


    with open(
        output_file,
        "wb"
    ) as file:

        file.write(
            response.content
        )


    print(
        f"Saved: {output_file}"
    )

    print(
        f"Size: "
        f"{len(response.content) / 1024:.1f} KB"
    )


print()
print("Weather download complete.")