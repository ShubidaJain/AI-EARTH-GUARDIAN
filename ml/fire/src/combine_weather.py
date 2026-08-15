from pathlib import Path

import pandas as pd


INPUT_DIR = Path(
    "ml/fire/data/raw/weather"
)

OUTPUT_FILE = Path(
    "ml/fire/data/processed/"
    "weather_2023-01-01_2025-12-31.csv"
)


PARAMETERS = {
    "T2M": "temperature",
    "RH2M": "humidity",
    "WS2M": "wind_speed",
    "PRECTOTCORR": "rainfall"
}


# ============================================================
# Find and parse one POWER file
# ============================================================

def find_header(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(file):

            if line.startswith("LAT"):

                return line_number

    raise ValueError(
        f"Could not find header in {file_path}"
    )


def parse_file(
    file_path,
    parameter,
    output_name
):

    header = find_header(
        file_path
    )

    df = pd.read_csv(
        file_path,
        skiprows=header
    )

    df = df.dropna(
        axis=1,
        how="all"
    )

    required = [
        "LAT",
        "LON",
        "YEAR",
        "DOY",
        parameter
    ]

    missing = [
        col
        for col in required
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"{file_path.name} missing "
            f"columns: {missing}"
        )

    # Create date from YEAR + DOY
    df["date"] = (
        pd.to_datetime(
            df["YEAR"].astype(str),
            format="%Y"
        )
        +
        pd.to_timedelta(
            df["DOY"] - 1,
            unit="D"
        )
    )

    df = df.rename(
        columns={
            "LAT": "grid_lat",
            "LON": "grid_lon",
            parameter: output_name
        }
    )

    return df[
        [
            "grid_lat",
            "grid_lon",
            "date",
            output_name
        ]
    ]


# ============================================================
# Process all parameters
# ============================================================

weather_tables = []


for parameter, output_name in PARAMETERS.items():

    print()
    print("=" * 60)
    print(f"Processing {parameter}")
    print("=" * 60)

    files = sorted(
        INPUT_DIR.glob(
            f"{parameter}_*.csv"
        )
    )

    print(
        f"Files found: {len(files)}"
    )

    if not files:

        raise FileNotFoundError(
            f"No files found for {parameter}"
        )

    parameter_tables = []

    for file in files:

        print(
            f"  {file.name}"
        )

        current = parse_file(
            file,
            parameter,
            output_name
        )

        parameter_tables.append(
            current
        )

    parameter_df = pd.concat(
        parameter_tables,
        ignore_index=True
    )

    # Remove duplicate grid/date records
    parameter_df = (
        parameter_df
        .drop_duplicates(
            subset=[
                "grid_lat",
                "grid_lon",
                "date"
            ]
        )
    )

    weather_tables.append(
        parameter_df
    )


# ============================================================
# Merge all weather parameters
# ============================================================

weather = weather_tables[0]


for current in weather_tables[1:]:

    weather = weather.merge(
        current,
        on=[
            "grid_lat",
            "grid_lon",
            "date"
        ],
        how="outer"
    )


# ============================================================
# Filter exact training period
# ============================================================

weather = weather[
    (weather["date"] >= "2023-01-01") &
    (weather["date"] <= "2025-12-31")
]


# ============================================================
# Sort
# ============================================================

weather = weather.sort_values(
    [
        "date",
        "grid_lat",
        "grid_lon"
    ]
)


# ============================================================
# Save
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

weather.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# Summary
# ============================================================

print()
print("=" * 60)
print("WEATHER DATASET COMPLETE")
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
    "Missing values:"
)

print(
    weather.isnull().sum()
)

print()

print(
    f"Saved: {OUTPUT_FILE}"
)