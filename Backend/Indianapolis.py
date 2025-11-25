# ------------------------------------------------------------
# Indianapolis Telemetry Processing + Driver Metrics + Plots
# ------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load your Indianapolis telemetry file
file_path = r"C:/Users/khush/Downloads/indianapolis/indianapolis/R1_indianapolis_motor_speedway_telemetry.csv"
df = pd.read_csv(file_path)

print("Rows loaded:", len(df))
print("Columns:", df.columns.tolist())


# ------------------------------------------------------------
# 2. SAMPLE DATA (because file is huge - 2.7GB)
# ------------------------------------------------------------
unique_times = df['timestamp'].drop_duplicates().sample(n=1500, random_state=42)
df_sample = df[df['timestamp'].isin(unique_times)]
print("After sampling:", len(df_sample))


# ------------------------------------------------------------
# 3. PIVOT: Convert long format → wide format
# ------------------------------------------------------------
df_wide = df_sample.pivot_table(
    index=["timestamp", "vehicle_id", "lap"],
    columns="telemetry_name",
    values="telemetry_value",
    aggfunc="mean"
).reset_index()


# Rename to nice readable names
rename_map = {
    "accx_can": "accx",
    "accy_can": "accy",
    "nmot": "rpm",
    "pbrake_f": "brake_front",
    "pbrake_r": "brake_rear",
    "Steering_Angle": "steering_angle",
    "aps": "throttle",
    "Laptrigger_lapdist_dls": "lapdist"
}
df_wide = df_wide.rename(columns=rename_map)

print("After pivot:", df_wide.shape)


# ------------------------------------------------------------
# 4. CLEANING & INTERPOLATION
# ------------------------------------------------------------
df_wide['timestamp'] = pd.to_datetime(df_wide['timestamp'])
df_wide = df_wide.sort_values(by=['vehicle_id', 'timestamp'])

df_interp = df_wide.groupby("vehicle_id").apply(lambda g: g.interpolate()).reset_index(drop=True)


# ------------------------------------------------------------
# 5. CREATE DRIVER METRICS
# ------------------------------------------------------------
# Convert numeric
numeric_cols = ["steering_angle", "throttle", "brake_front", "brake_rear", "accx", "accy", "speed"]
for col in numeric_cols:
    if col in df_interp.columns:
        df_interp[col] = pd.to_numeric(df_interp[col], errors='coerce')

df_interp[numeric_cols] = df_interp[numeric_cols].interpolate().ffill().bfill()

# Metrics
df_interp["acceleration"] = df_interp["speed"].diff()
df_interp["g_force"] = np.sqrt(df_interp["accx"]**2 + df_interp["accy"]**2)
df_interp["steering_smoothness"] = df_interp["steering_angle"].rolling(40).std()
df_interp["brake_intensity"] = df_interp["brake_front"].rolling(20).mean()

df_metrics = df_interp.dropna(subset=["steering_smoothness"]).copy()


# ------------------------------------------------------------
# 6. PLOT: SPEED over time
# ------------------------------------------------------------
plt.figure(figsize=(10,5))
plt.plot(df_metrics["timestamp"], df_metrics["speed"])
plt.title("Speed Over Time")
plt.xlabel("Time")
plt.ylabel("Speed")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 7. PLOT: ACCELERATION over time
# ------------------------------------------------------------
plt.figure(figsize=(10,5))
plt.plot(df_metrics["timestamp"], df_metrics["acceleration"])
plt.title("Acceleration Over Time")
plt.xlabel("Time")
plt.ylabel("Acceleration")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 8. PLOT: BRAKE intensity
# ------------------------------------------------------------
plt.figure(figsize=(10,5))
plt.plot(df_metrics["timestamp"], df_metrics["brake_intensity"])
plt.title("Brake Intensity Over Time")
plt.xlabel("Time")
plt.ylabel("Brake Intensity")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 9. PLOT: STEERING SMOOTHNESS
# ------------------------------------------------------------
plt.figure(figsize=(10,5))
plt.plot(df_metrics["timestamp"], df_metrics["steering_smoothness"])
plt.title("Steering Smoothness Over Time")
plt.xlabel("Time")
plt.ylabel("Smoothness (Std. Dev.)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n🚗 All metrics and visualizations generated successfully!")


