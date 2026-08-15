import os
import time
from pathlib import Path
from io import StringIO

import pandas as pd
import requests
from dotenv import load_dotenv


# ============================================================
# Configuration
# ============================================================

load_dotenv()

MAP_KEY = os.getenv("FIRMS_MAP_KEY")

if not MAP_KEY:
    raise ValueError("FIRMS_MAP_KEY not found in .env")


SOURCE = "VIIRS_SNPP_SP"

# west, south, east, north
AREA = "73,29,77,33"

START_DATE = "2025-02-01"
END_DATE = "2025-12-31"

DAY_RANGE = 5

OUTPUT_DIR = Path(
    "ml/fire/data/raw/historical"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# HTTP session
# ============================================================

session = requests.Session()


# ============================================================
# Download one 5-day block
# ============================================================

def download_period(start_date):

    date_string = start_date.strftime("%Y-%m-%d")

    url = (
        "https://firms.modaps.eosdis.nasa.gov/"
        f"api/area/csv/"
        f"{MAP_KEY}/"
        f"{SOURCE}/"
        f"{AREA}/"
        f"{DAY_RANGE}/"
        f"{date_string}"
    )

    filename = (
        f"fires_{date_string}_"
        f"{DAY_RANGE}days.csv"
    )

    output_file = OUTPUT_DIR / filename

    # Resume support
    if output_file.exists():

        print(
            f"[SKIP] {filename}"
        )

        return 0


    print()
    print("=" * 60)
    print(f"Downloading {date_string}")
    print("=" * 60)


    # Retry up to 3 times
    for attempt in range(1, 4):

        try:

            response = session.get(
                url,
                timeout=(20, 180)
            )

            response.raise_for_status()

            df = pd.read_csv(
                StringIO(response.text)
            )

            df.to_csv(
                output_file,
                index=False
            )

            print(
                f"[OK] {len(df)} records"
            )

            print(
                f"Saved: {output_file}"
            )

            return len(df)

        except Exception as error:

            print(
                f"[Attempt {attempt}/3] "
                f"Failed: {error}"
            )

            if attempt < 3:

                print(
                    "Waiting 10 seconds before retry..."
                )

                time.sleep(10)

            else:

                print(
                    f"[FAILED] {date_string}"
                )

                return None


# ============================================================
# Main loop
# ============================================================

current_date = pd.Timestamp(
    START_DATE
)

final_date = pd.Timestamp(
    END_DATE
)

total_records = 0
successful = 0
skipped = 0
failed = []


while current_date <= final_date:

    output_file = (
        OUTPUT_DIR /
        f"fires_"
        f"{current_date.strftime('%Y-%m-%d')}_"
        f"{DAY_RANGE}days.csv"
    )


    if output_file.exists():

        skipped += 1

    else:

        records = download_period(
            current_date
        )

        if records is None:

            failed.append(
                current_date.strftime(
                    "%Y-%m-%d"
                )
            )

        else:

            successful += 1
            total_records += records


        # Small delay between requests
        time.sleep(2)


    current_date += pd.Timedelta(
        days=DAY_RANGE
    )


# ============================================================
# Final summary
# ============================================================

print()
print("=" * 60)
print("HISTORICAL DOWNLOAD SUMMARY")
print("=" * 60)

print(
    f"Successful: {successful}"
)

print(
    f"Skipped:    {skipped}"
)

print(
    f"Records:    {total_records}"
)

print(
    f"Failed:     {len(failed)}"
)


if failed:

    print()
    print("Failed dates:")

    for date in failed:

        print(
            f"  {date}"
        )