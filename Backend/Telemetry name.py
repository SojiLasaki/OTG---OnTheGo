import pandas as pd


# Load the dataset (already working for you)
df = pd.read_csv("/Users/khush/Downloads/barber-motorsports-park/barber/R1_barber_telemetry_data.csv")




df_sample = df.sample(n=1000, random_state=42)

print(df_sample['telemetry_name'].value_counts().head(20))

# Pivot the long telemetry dataset into a usable format
df_wide = df_sample.pivot_table(
    index=["timestamp","vehicle_id","lap"], 
    columns="telemetry_name", 
    values="telemetry_value"
).reset_index()

df_wide.head()
