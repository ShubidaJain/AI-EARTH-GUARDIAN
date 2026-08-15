import requests
from pathlib import Path
from datetime import datetime

import pandas as pd


# ============================================================
# Configuration
# ============================================================

START_DATE = "2023-01-01"
END_DATE = "2025-12-31"

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


PARAMETERS = [
    "T2M",
    "RH2M",
    "WS2M",
    "PRECTOTCORR"
]


BASE_URL = (
    "https://power.larc.nasa.gov/"
    "api/temporal/daily/regional"
)


# ============================================================
# Download one month
# ============================================================

def download_month(
    parameter,
    start_date,
    end_date
):

    start_string = start_date.strftime(
        "%Y-%m-%d"
    )

    end_string = end_date.strftime(
        "%Y-%m-%d"
    )

    filename = (
        f"{parameter}_"
        f"{start_string}_"
        f"{end_string}.csv"
    )

    output_file = (
        OUTPUT_DIR / filename
    )


    if output_file.exists():

        print(
            f"[SKIP] {filename}"
        )

        return


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
            start_date.strftime("%Y%m%d"),

        "end":
            end_date.strftime("%Y%m%d"),

        "format":
            "CSV"
    }


    print()
    print("=" * 60)

    print(
        f"{parameter}: "
        f"{start_string} → {end_string}"
    )

    print("=" * 60)


    response = requests.get(
        BASE_URL,
        params=params,
        timeout=(30, 300)
    )


    if response.status_code != 200:

        print(
            "NASA POWER response:"
        )

        print(
            response.text[:1000]
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
        f"[OK] Saved: {output_file}"
    )

    print(
        f"Size: "
        f"{len(response.content) / 1024:.1f} KB"
    )


# ============================================================
# Generate monthly periods
# ============================================================

start = pd.Timestamp(
    START_DATE
)

end = pd.Timestamp(
    END_DATE
)


months = pd.date_range(
    start=start,
    end=end,
    freq="MS"
)


# ============================================================
# Download
# ============================================================

for month_start in months:

    month_end = (
        month_start
        + pd.offsets.MonthEnd(1)
    )

    # Don't go beyond requested end date
    if month_end > end:

        month_end = end


    for parameter in PARAMETERS:

        download_month(
            parameter,
            month_start,
            month_end
        )


print()
print("=" * 60)
print("ALL WEATHER DOWNLOADS COMPLETE")
print("=" * 60)