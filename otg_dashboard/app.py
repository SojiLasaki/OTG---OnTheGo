import dash
from dash import Input, Output, State, page_container, dcc, html, dash_table
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.search import search
from components.line import line
import os
from dash.exceptions import PreventUpdate
import pandas as pd


# Load datasets into app
dataset_folder = "../Datasets" 
datasets = [f for f in os.listdir(dataset_folder) if not f.startswith(".")]


# initialize app
app = dash.Dash(
    __name__, 
    use_pages=True, 
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True
)
app.title = "On The GO"


# App layout
app.layout = dbc.Container([
    dcc.Store(id="session-store", storage_type="session"),
    navbar,
    search,
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


# save session
@app.callback(
    Output("session-store", "data"),
    # Output("search-output", "children"), no longer needed
    Input("search-btn", "n_clicks"),
    State("map-dropdown", "value"),
    State("race-dropdown", "value"),
    State("vehicle-dropdown", "value"),
    prevent_initial_call=True
    
)
def save_to_session(n_clicks, selected_map, selected_race, selected_vehicle):
    if not selected_map or not selected_race or not selected_vehicle:
        raise PreventUpdate
    data = {
        "map": selected_map,
        "race": selected_race,
        "vehicle": selected_vehicle
    }
    return data 
    # this was needed to read csv file properly to ensrure the right path was called
    #, f"Map: {selected_map}/ Race: {selected_race}/ Vehicle Number: {selected_vehicle}"


# access sessioin from other pages
@app.callback(
    Output("other-page-output", "children"),
    Input("session-store", "data")
)
def show_session_data(data):
    if not data:
        return "No data in session yet."
    return f"Map: {data['map']}, Race: {data['race']}, Vehicle: {data['vehicle']}"



@app.callback(
    Output("overview-summary", "children"),
    Output("overview-table", "children"),
    Input("session-store", "data"),
    prevent_initial_call=True
)
def update_overview(session_data):
    if not session_data:
        return html.P("⚠️ No session data found. Please select a race first."), None

    selected_map = session_data.get("map")
    selected_race = session_data.get("race")

    root = "../"
    file_path = f"{root}Datasets/{selected_map}/{selected_race}/03_results.CSV"

    if not os.path.exists(file_path):
        return html.P(f"File not found: {file_path}"), None

    df = pd.read_csv(file_path, sep=";")

    summary = html.Div([
        html.H5(f"Track: {selected_map} | Race: {selected_race}", className="text-center mb-2"),
        html.P(f"Total Vehickes: {len(df)}", className="text-center")
    ])

    # DataTable
    table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=100,
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "center",
            "backgroundColor": "#111",
            "color": "white",
        },
        style_header={
            "backgroundColor": "#333",
            "fontWeight": "bold",
        },
        style_data_conditional=[  # remove hover highlights
            {
                "if": {"state": "active"},
                "backgroundColor": "#111",
                "color": "white",
            },
            {
                "if": {"state": "selected"},
                "backgroundColor": "#444",
                "color": "white",
            },
        ]
        )

    return summary, table
# run app
if __name__ == "__main__":
    app.run(debug=True)
