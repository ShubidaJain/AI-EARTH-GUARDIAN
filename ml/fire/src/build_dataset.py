import pandas as pd


fire_file = "ml/fire/data/raw/firms_fire_data.csv"
weather_file = "ml/fire/data/raw/fire_weather_data.csv"

fires = pd.read_csv(fire_file)
weather = pd.read_csv(weather_file)


# Create matching date column
fires["date"] = pd.to_datetime(
    fires["acq_date"]
).dt.strftime("%Y-%m-%d")


weather["date"] = pd.to_datetime(
    weather["date"]
).dt.strftime("%Y-%m-%d")


# Merge using location + date
dataset = fires.merge(
    weather,
    on=["latitude", "longitude", "date"],
    how="left"
)


# Save
output_file = "ml/fire/data/processed/fire_environment_dataset.csv"

dataset.to_csv(
    output_file,
    index=False
)


print("Dataset created!")
print()
print(dataset.head())
print()
print(dataset.shape)