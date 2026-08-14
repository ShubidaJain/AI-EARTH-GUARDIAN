import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

MAP_KEY = os.getenv("FIRMS_MAP_KEY")

if not MAP_KEY:
    raise ValueError("FIRMS_MAP_KEY not found in .env")


# --------------------------------------------------
# Configuration
# --------------------------------------------------

SOURCE = "VIIRS_SNPP_NRT"

# Punjab / Northern India region
# west, south, east, north
AREA = "73,29,77,33"

DAY_RANGE = 3


# --------------------------------------------------
# Create API URL
# --------------------------------------------------

url = (
    f"https://firms.modaps.eosdis.nasa.gov/"
    f"api/area/csv/"
    f"{MAP_KEY}/"
    f"{SOURCE}/"
    f"{AREA}/"
    f"{DAY_RANGE}"
)


print("Requesting NASA FIRMS data...")
print(f"Source: {SOURCE}")
print(f"Area: {AREA}")
print(f"Days: {DAY_RANGE}")


# --------------------------------------------------
# Request data
# --------------------------------------------------

response = requests.get(url, timeout=60)

if response.status_code != 200:
    raise RuntimeError(
        f"FIRMS API request failed: "
        f"{response.status_code}\n"
        f"{response.text}"
    )


# --------------------------------------------------
# Convert CSV response to DataFrame
# --------------------------------------------------

from io import StringIO

df = pd.read_csv(StringIO(response.text))


# --------------------------------------------------
# Save raw data
# --------------------------------------------------

output_dir = Path("ml/fire/data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "firms_fire_data.csv"

df.to_csv(output_file, index=False)


print()
print("Data downloaded successfully!")
print(f"Records: {len(df)}")
print(f"Saved to: {output_file}")

print()
print("Columns:")
print(df.columns.tolist())