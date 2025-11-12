# Pivot the long telemetry dataset into a usable format
import pandas as pd
import numpy as np

# --- 1) Load dataset ---




file_path = r"/Users/khush/Downloads/barber-motorsports-park/barber/R1_barber_telemetry_data.csv"

df = pd.read_csv(file_path)
print(f"Rows loaded: {len(df):,}")

# 1. Sample based on unique timestamps
unique_times = df['timestamp'].drop_duplicates().sample(n=1000, random_state=42)
df_sample = df[df['timestamp'].isin(unique_times)]
print(f"Rows after timestamp sampling: {len(df_sample):,}")

# 2. Pivot — IMPORTANT: use telemetry_value (not value)
df_wide = df_sample.pivot_table(
    index=["timestamp", "vehicle_id", "lap"],
    columns="telemetry_name",
    values="telemetry_value",
    aggfunc="mean"
).reset_index()

# 3. Rename columns to readable names
rename_map = {
    "accx_can": "accx",
    "accy_can": "accy",
    "pbrake_f": "brake_front",
    "pbrake_r": "brake_rear",
    "Steering_Angle": "steering_angle",
    "nmot": "rpm",
    "Laptrigger_lapdist_dls": "lapdist",
    "aps": "throttle"
}
df_wide = df_wide.rename(columns=rename_map)

print("\nShape after pivot:", df_wide.shape)
print("Columns:", list(df_wide.columns))

# 4. Missing % report
print("\nMissing Value % per column:")
for col, pct in (df_wide.isna().mean() * 100).items():
    print(f"{col}: {pct:.2f}%")

#new code block
#Data Cleaning / Interpolation

# Convert timestamp to datetime for ordering
df_wide['timestamp'] = pd.to_datetime(df_wide['timestamp'])

# Sort by vehicle and timestamp
df_wide = df_wide.sort_values(by=['vehicle_id', 'timestamp'])

# Interpolate missing values inside each vehicle's time series
df_interp = df_wide.groupby('vehicle_id').apply(lambda group: group.interpolate(method='linear')).reset_index(drop=True)

print("\n✅ After interpolation:")
print(df_interp.isna().mean() * 100)

#Creating Driver Performance Metric - Model Refinement

# Ensure numeric columns are numeric
numeric_cols = ['steering_angle', 'throttle', 'brake_front', 'brake_rear', 'accx', 'accy', 'speed']
for col in numeric_cols:
    df_interp[col] = pd.to_numeric(df_interp[col], errors='coerce')

# Fill missing values *properly*
df_interp[numeric_cols] = df_interp[numeric_cols].interpolate(method='linear').ffill().bfill()

# Calculate Driver Metrics
df_interp['steering_smoothness'] = df_interp['steering_angle'].rolling(50).std()
df_interp['throttle_variation'] = df_interp['throttle'].rolling(50).std()
df_interp['braking_aggression'] = df_interp['brake_front'].rolling(50).mean()
df_interp['g_force'] = np.sqrt(df_interp['accx']**2 + df_interp['accy']**2)
df_interp['speed_change'] = df_interp['speed'].diff()

# 🚫 Drop first 50 rows (rolling window warmup)
df_metrics = df_interp.dropna(subset=['steering_smoothness', 'throttle_variation', 'speed_change']).copy()

print("Driver Metrics Added")
print(df_metrics[['steering_smoothness', 'throttle_variation', 'braking_aggression', 'g_force', 'speed_change']].head())

#Comparing Drivers metrics

import pandas as pd
import matplotlib.pyplot as plt

# --- If driver column is named differently, rename here ---
# Example: df.rename(columns={"telemetry_name": "driver"}, inplace=True)

# --- Group and calculate averages per driver ---

# Compare drivers using df_metrics
driver_stats = df_metrics.groupby("vehicle_id").agg({
    "steering_smoothness": "mean",
    "throttle_variation": "mean",
    "braking_aggression": "mean",
    "g_force": "mean",
    "speed_change": "mean"
}).reset_index()

print("\n=== Driver Performance Comparison ===\n")
print(driver_stats)

import matplotlib.pyplot as plt

metrics = ["steering_smoothness", "throttle_variation", "braking_aggression", "g_force", "speed_change"]

for metric in metrics:
    plt.figure()
    plt.bar(driver_stats["vehicle_id"], driver_stats[metric])
    plt.title(f"Driver Comparison: {metric.replace('_', ' ').title()}")
    plt.xlabel("Driver (vehicle_id)")
    plt.ylabel(metric.replace('_', ' ').title())
    plt.xticks(rotation=45)
    plt.show()

