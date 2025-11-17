# Driver Performance Analysis using Telemetry Data

This project processes real racing telemetry data to analyze and compare driver performance.  
The dataset used is from Barber Motorsports Park (R1 session), where each row represents a vehicle signal reading such as steering angle, throttle position, braking pressure, acceleration forces, and more.

The goal of this project is to:
1. Convert long-format telemetry data into a usable table.
2. Clean and interpolate missing values.
3. Extract meaningful driver performance metrics.
4. Compare drivers based on their driving style and stability.

---

## Requirements

Make sure you have Python installed, then install dependencies:

```bash
pip install pandas numpy matplotlib
Dataset
You will need the Barber telemetry CSV file:

Copy code
R1_barber_telemetry_data.csv
Update the file path in the code if needed:

python
Copy code
file_path = r"/Users/khush/Downloads/barber-motorsports-park/barber/R1_barber_telemetry_data.csv"
What the Code Does (Step-by-Step)
1. Load and Sample Data
We randomly sample based on timestamps to reduce data size while maintaining time continuity.

2. Pivot to Wide Format
Telemetry is originally in a long format.
We convert it so each row corresponds to:

| timestamp | vehicle_id | lap | steering_angle | throttle | brake_front | … |

3. Data Cleaning & Interpolation
Convert timestamps to time-series format

Sort per driver

Fill missing sensor readings using linear interpolation

4. Create Driver Performance Metrics
Metric	Meaning
Steering Smoothness	How stable the driver turns the wheel
Throttle Variation	Smooth vs jerky acceleration
Braking Aggression	How heavily the driver brakes
G-Force	Cornering intensity
Speed Change	Consistency of speed

Formulas used:

python
Copy code
steering_smoothness = rolling std of steering angle (window 50)
throttle_variation  = rolling std of throttle input
braking_aggression  = average front brake pressure
g_force             = sqrt(accx² + accy²)
speed_change        = first difference of speed over time
5. Compare Drivers
Metrics are averaged per vehicle_id, producing a clear driver comparison table and bar charts.

Output Example
Printed performance comparison table

Bar charts for each metric showing differences between drivers

Example chart:

yaml
Copy code
Driver Comparison: Steering Smoothness
Each bar = one driver
Higher → smoother steering
Lower → more aggressive/reactive steering

How to Run
bash
Copy code
python your_script_name.py
The program will:
✔ Load and process the telemetry
✔ Compute driver performance metrics
✔ Display comparison charts

✨ Interpretation Example (Use in Your Report)
Drivers with higher steering smoothness values demonstrate more consistent and controlled handling, while drivers with lower values show more corrective and reactive steering. Variation in brake pressure and throttle stability further differentiate calm, controlled drivers from aggressive drivers.

👩‍💻 Author
Nakshatra & Team
Data Science, IU Indianapolis (2025)# Code

