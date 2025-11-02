import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
from dash import Dash, dcc, html, Input, Output

# Read csv files
root = "../"
weather_data = pd.read_csv(f'{root}Datasets/Road America/Race 1/26_Weather_Race 1_Anonymized.csv', sep=';')

# test to make sure the file is present in the directory.
print(os.path.exists(f'{root}Datasets/Road America/Race 1/26_Weather_Race 1_Anonymized.csv'))

print(weather_data.head())

# function to plot 
def plot_wind_speed(weather_data, x='TIME_UTC_STR', y='AIR_TEMP', compare_with=None, kind='line'):
    plt.figure(figsize=(12,6))
    sns.set_style("whitegrid")

    # plot wind speeds
    if kind == "line":
        plt.plot(weather_data[x], weather_data[y], label=y, marker='o')

    elif kind == 'scatter':
        plt.plot(weather_data[x], weather_data[y], label=y)

    # plot other variables
    if compare_with:
        for col in compare_with:
            if kind == 'line':
                plt.plot(weather_data[x], weather_data[col], label=col, linestyle='--', marker='x')
            elif kind == 'scatter':
                plt.scatter(weather_data[x], weather_data[col], label=col)


    plt.xlabel(x)
    plt.ylabel('Volume')
    plt.title('Weather Compatison')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout
    plt.show()

plot_wind_speed(weather_data)