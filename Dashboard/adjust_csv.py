import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import defaultdict
import numpy as np

filepath = (
    f"../../Datasets/indianapolis/{data['race']}/"
    f"{race_abriv}_indianapolis_motor_speedway_telemetry.CSV"
)
def load_and_process_telemetry(filepath, chunk_size=50000):
    """
    Load large CSV file in chunks and process telemetry data.
    
    Expected CSV columns: vehicle_id, timestamp, telemetry_name, telemetry_value
    Adjust column names in the function if your CSV has different names.
    """
    
    # Dictionary structure: {vehicle_id: {telemetry_name: {timestamp: value}}}
    vehicle_data = defaultdict(lambda: defaultdict(dict))
    
    print(f"Loading CSV file in chunks of {chunk_size} rows...")
    
    # Process CSV in chunks to handle large files
    for i, chunk in enumerate(pd.read_csv(filepath, chunksize=chunk_size)):
        print(f"Processing chunk {i+1}...")
        
        # Adjust these column names to match your CSV
        for _, row in chunk.iterrows():
            vehicle_id = row['vehicle_id']
            timestamp = pd.to_datetime(row['timestamp'])
            telemetry_name = row['telemetry_name']
            telemetry_value = float(row['telemetry_value'])
            
            vehicle_data[vehicle_id][telemetry_name][timestamp] = telemetry_value
    
    print(f"Loaded data for {len(vehicle_data)} vehicles")
    return dict(vehicle_data)

def aggregate_telemetry(vehicle_data, resample_freq='1min'):
    """
    Aggregate telemetry data by averaging over time intervals.
    
    Args:
        vehicle_data: Dictionary from load_and_process_telemetry
        resample_freq: Pandas frequency string ('1min', '5min', '1H', etc.)
    
    Returns:
        Dictionary with aggregated data
    """
    aggregated_data = {}
    
    for vehicle_id, telemetry_dict in vehicle_data.items():
        aggregated_data[vehicle_id] = {}
        
        for telemetry_name, time_values in telemetry_dict.items():
            # Convert to DataFrame for easy resampling
            df = pd.DataFrame(list(time_values.items()), 
                            columns=['timestamp', 'value'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.set_index('timestamp').sort_index()
            
            # Resample and average
            resampled = df.resample(resample_freq).mean()
            
            aggregated_data[vehicle_id][telemetry_name] = resampled
    
    return aggregated_data

def plot_telemetry(aggregated_data, vehicle_ids=None, telemetry_names=None):
    """
    Plot telemetry data using Plotly.
    
    Args:
        aggregated_data: Output from aggregate_telemetry
        vehicle_ids: List of vehicle IDs to plot (None = all)
        telemetry_names: List of telemetry names to plot (None = all)
    """
    
    if vehicle_ids is None:
        vehicle_ids = list(aggregated_data.keys())[:5]  # Limit to 5 vehicles by default
    
    if telemetry_names is None:
        # Get all unique telemetry names
        telemetry_names = set()
        for vid in vehicle_ids:
            if vid in aggregated_data:
                telemetry_names.update(aggregated_data[vid].keys())
        telemetry_names = list(telemetry_names)
    
    # Create subplots - one per telemetry type
    num_plots = len(telemetry_names)
    fig = make_subplots(
        rows=num_plots, 
        cols=1,
        subplot_titles=telemetry_names,
        vertical_spacing=0.05
    )
    
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    
    for i, telemetry_name in enumerate(telemetry_names, 1):
        for j, vehicle_id in enumerate(vehicle_ids):
            if vehicle_id in aggregated_data and telemetry_name in aggregated_data[vehicle_id]:
                df = aggregated_data[vehicle_id][telemetry_name]
                
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['value'],
                        name=f'Vehicle {vehicle_id}',
                        mode='lines',
                        line=dict(color=colors[j % len(colors)]),
                        showlegend=(i == 1)  # Only show legend for first subplot
                    ),
                    row=i,
                    col=1
                )
        
        fig.update_yaxis(title_text=telemetry_name, row=i, col=1)
    
    fig.update_xaxis(title_text="Timestamp", row=num_plots, col=1)
    fig.update_layout(
        height=300 * num_plots,
        title_text="Vehicle Telemetry Data (Averaged)",
        showlegend=True
    )
    
    fig.show()

# Example usage:
if __name__ == "__main__":
    # Load your CSV file
    filepath = "your_telemetry_data.csv"  # Replace with your file path
    
    # Process the data
    vehicle_data = load_and_process_telemetry(filepath, chunk_size=50000)
    
    # Aggregate by averaging over 5-minute intervals
    aggregated_data = aggregate_telemetry(vehicle_data, resample_freq='5min')
    
    # Plot specific vehicles and telemetry types
    # Example: plot_telemetry(aggregated_data, 
    #                         vehicle_ids=['V001', 'V002'], 
    #                         telemetry_names=['speed', 'temperature'])
    
    # Or plot all available data (limited to first 5 vehicles)
    plot_telemetry(aggregated_data)
    
    # Access the dictionary structure directly if needed:
    # vehicle_data['vehicle_id']['telemetry_name'][timestamp] = value