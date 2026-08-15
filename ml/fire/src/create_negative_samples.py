import pandas as pd
import numpy as np
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

FIRE_FILE = Path(
    "ml/fire/data/raw/firms_fire_data.csv"
)

OUTPUT_FILE = Path(
    "ml/fire/data/processed/negative_samples.csv"
)

NUM_SAMPLES = 100

LAT_MIN = 29
LAT_MAX = 33

LON_MIN = 73
LON_MAX = 77


# --------------------------------------------------
# Load fire data
# --------------------------------------------------

fires = pd.read_csv(FIRE_FILE)

fires["acq_date"] = pd.to_datetime(
    fires["acq_date"]
)


# --------------------------------------------------
# Random generator
# --------------------------------------------------

rng = np.random.default_rng(42)


negative_samples = []


# --------------------------------------------------
# Generate samples
# --------------------------------------------------

for _ in range(NUM_SAMPLES):

    latitude = rng.uniform(
        LAT_MIN,
        LAT_MAX
    )

    longitude = rng.uniform(
        LON_MIN,
        LON_MAX
    )

    date = rng.choice(
        fires["acq_date"].dt.date
    )

    negative_samples.append({
        "latitude": latitude,
        "longitude": longitude,
        "date": date,
        "fire_occurred": 0
    })


negative_df = pd.DataFrame(
    negative_samples
)


# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

negative_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print(
    f"Created {len(negative_df)} negative samples"
)

print(
    negative_df.head()
)