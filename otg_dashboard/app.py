import dash
from dash import Input, Output, State, page_container, dcc
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.line import line
import os
import pandas as pd


# Load datasets into app
dataset_folder = "../Datasets" 
datasets = [f for f in os.listdir(dataset_folder) if not f.startswith(".")]


# initialize app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])
app.title = "On The GO"


# App layout
app.layout = dbc.Container([
    dcc.Store(id="selection_store", storage_type="session"),
    navbar,
    dash.page_container
], fluid=True)


# Callback to toggle collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
)
def toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


# update race
@app.callback(
    Output("race-dropdown", "options"),
    Input("map-dropdown", "value")
)
def update_races(selected_map):
    if not selected_map:
        return["No races found"]
    map_path = os.path.join(dataset_folder, selected_map)
    races = [f for f in os.listdir(map_path) if not f.startswith(".")]
    races_sorted = sorted(races, key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
    return [{"label": f.title(), "value": f} for f in races_sorted]


# dynamic vehicle selection
@app.callback(
    Output("vehicle-dropdown", "options"),
    Input("map-dropdown", "value"),
    Input("race-dropdown", "value")
)
def update_vehicle(selected_map, selected_race):
    if not selected_map or not selected_race:
        return []
    race_path = os.path.join(dataset_folder, selected_map, selected_race)
    print(race_path)
    try:
        df = pd.read_csv(f"{race_path}/03_results.CSV", sep=";")
        print(df)
        if "NUMBER" not in df.columns:
            return [{"label": "No Vehicles Found", "value": ""}]

        numbers = sorted(df["NUMBER"].unique())
        return [{"label": str(num), "value": str(num)} for num in numbers]

    except FileNotFoundError:
        return [{"label": "File not found", "value": ""}]
    except Exception as e:
        return [{"label": f"Error: {e}", "value": ""}]

# run app
if __name__ == "__main__":
    app.run(debug=True)
