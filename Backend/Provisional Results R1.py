import pandas as pd
import matplotlib.pyplot as plt

# --------------------------
# Load your file
# --------------------------
file_path = r"C:/Users/khush/Downloads/indianapolis/indianapolis/03_Provisional Results_Race 1.csv"

df = pd.read_csv(file_path, sep=';', nrows=30)

# --------------------------
# Convert FL_KPH to numeric
# --------------------------
df['FL_KPH'] = pd.to_numeric(df['FL_KPH'], errors='coerce')

# Drop rows with missing speed
df = df.dropna(subset=['FL_KPH']).reset_index(drop=True)

# --------------------------
# Create synthetic telemetry
# (because dataset has no real time data)
# --------------------------
df['Speed'] = df['FL_KPH']
df['Acceleration'] = df['Speed'].diff().fillna(0)
df['Braking'] = (-df['Acceleration']).clip(lower=0)    # only negative accel
df['Smoothness'] = df['Acceleration'].rolling(3).std().fillna(0)

# --------------------------
# Plot SPEED
# --------------------------
plt.figure(figsize=(10,5))
plt.plot(df['Speed'])
plt.title("Speed (FL_KPH)")
plt.xlabel("Driver Index")
plt.ylabel("Speed (KPH)")
plt.grid(True)
plt.show()

# --------------------------
# Plot ACCELERATION
# --------------------------
plt.figure(figsize=(10,5))
plt.plot(df['Acceleration'])
plt.title("Acceleration (from FL_KPH)")
plt.xlabel("Driver Index")
plt.ylabel("ΔSpeed")
plt.grid(True)
plt.show()

# --------------------------
# Plot BRAKING
# --------------------------
plt.figure(figsize=(10,5))
plt.plot(df['Braking'])
plt.title("Braking (Negative Acceleration)")
ದೆzer.xlabel("Driver Index")
plt.ylabel("Brake Strength")
plt.grid(True)
plt.show()

# --------------------------
# Plot SMOOTHNESS
# --------------------------
plt.figure(figsize=(10,5))
plt.plot(df['Smoothness'])
plt.title("Smoothness (Acceleration Variability)")
plt.xlabel("Driver Index")
plt.ylabel("Std Dev of Acceleration")
plt.grid(True)
plt.show()
