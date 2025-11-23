import os
import pandas as pd

# ==========================================
# CONFIG
# ==========================================
INPUT_CSV = "telemetry.csv"         # path to the big flattened file
OUTPUT_ROOT = "telemetry_split"     # root folder to store drivers

# ==========================================
# LOAD CSV
# ==========================================
df = pd.read_csv(INPUT_CSV)

# Normalize column names
df.columns = [c.lower().strip() for c in df.columns]

required_cols = [
    "vehicle_number",
    "lap",
    "telemetry_name",
    "telemetry_value",
    "timestamp"
]

for col in required_cols:
    if col not in df.columns:
        raise KeyError(f"Required column missing: {col}")

# Convert timestamp safely
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Ensure numeric
df["telemetry_value"] = pd.to_numeric(df["telemetry_value"], errors="coerce")

# ==========================================
# GROUP BY DRIVER
# ==========================================
drivers = df["vehicle_number"].unique()

print(f"Found {len(drivers)} drivers.")

for driver in drivers:
    df_driver = df[df["vehicle_number"] == driver].copy()

    driver_folder = os.path.join(OUTPUT_ROOT, f"driver_{driver}")
    os.makedirs(driver_folder, exist_ok=True)

    print(f"Processing Driver {driver} → {driver_folder}")

    # --------------------------------------
    # GROUP BY LAP
    # --------------------------------------
    laps = sorted(df_driver["lap"].dropna().unique())

    for lap in laps:
        df_lap = df_driver[df_driver["lap"] == lap].copy()

        output_csv = os.path.join(driver_folder, f"lap_{int(lap)}.csv")
        df_lap.to_csv(output_csv, index=False)

        print(f"  Saved lap {lap} → {output_csv}")

print("\nDONE!")
