from pathlib import Path

import pandas as pd


INPUT_DIR = Path(
    "ml/fire/data/raw/weather"
)

OUTPUT_DIR = Path(
    "ml/fire/data/processed/weather"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


PARAMETERS = {
    "T2M": "temperature",
    "RH2M": "humidity",
    "WS2M": "wind_speed",
    "PRECTOTCORR": "rainfall"
}


def find_header(file_path):
    """
    Find the actual CSV header in a NASA POWER
    regional CSV file.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(file):

            if line.startswith("LAT"):

                return line_number

    raise ValueError(
        f"Could not find CSV header in {file_path}"
    )


def parse_file(
    parameter,
    column_name
):

    file_path = next(
        INPUT_DIR.glob(
            f"{parameter}_*.csv"
        ),
        None
    )

    if file_path is None:
        raise FileNotFoundError(
            f"No file found for {parameter}"
        )

    header_row = find_header(file_path)

    print(
        f"Reading {file_path.name}"
    )

    print(
        f"Header row: {header_row}"
    )

    df = pd.read_csv(
        file_path,
        skiprows=header_row
    )

    # Remove completely empty columns
    df = df.dropna(
        axis=1,
        how="all"
    )

    print(
        "Columns found:",
        df.columns.tolist()
    )

    # --------------------------------------------------------
    # NASA POWER regional format:
    #
    # LAT | LON | YEAR | DOY | PARAMETER
    #
    # Example:
    # 29.0 | 73.0 | 2023 | 1 | 18.4
    # --------------------------------------------------------

    required_columns = [
        "LAT",
        "LON",
        "YEAR",
        "DOY",
        parameter
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns in {file_path}: {missing}"
        )

    # --------------------------------------------------------
    # Create actual date from YEAR + DOY
    # --------------------------------------------------------

    df["date"] = pd.to_datetime(
        df["YEAR"].astype(str),
        format="%Y"
    ) + pd.to_timedelta(
        df["DOY"] - 1,
        unit="D"
    )

    # --------------------------------------------------------
    # Rename columns
    # --------------------------------------------------------

    df = df.rename(
        columns={
            "LAT": "grid_lat",
            "LON": "grid_lon",
            parameter: column_name
        }
    )

    # --------------------------------------------------------
    # Keep only what we need
    # --------------------------------------------------------

    df = df[
        [
            "grid_lat",
            "grid_lon",
            "date",
            column_name
        ]
    ]

    return df
# ------------------------------------------------------------
# Parse all four variables
# ------------------------------------------------------------

weather = None


for parameter, column_name in PARAMETERS.items():

    current = parse_file(
        parameter,
        column_name
    )


    if weather is None:

        weather = current

    else:

        weather = weather.merge(
            current,
            on=[
                "grid_lat",
                "grid_lon",
                "date"
            ],
            how="outer"
        )


# ------------------------------------------------------------
# Sort
# ------------------------------------------------------------

weather = weather.sort_values(
    [
        "date",
        "grid_lat",
        "grid_lon"
    ]
)


# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

output_file = (
    OUTPUT_DIR /
    "weather_2023-01-01_2023-01-31.csv"
)

weather.to_csv(
    output_file,
    index=False
)


print()
print("=" * 60)
print("WEATHER PARSING COMPLETE")
print("=" * 60)

print(
    f"Rows: {len(weather)}"
)

print(
    f"Columns: {weather.columns.tolist()}"
)

print(
    f"Date range: "
    f"{weather['date'].min().date()} "
    f"→ "
    f"{weather['date'].max().date()}"
)

print()
print(
    weather.head(10)
)

print()
print(
    f"Saved: {output_file}"
)